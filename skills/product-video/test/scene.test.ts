import { afterAll, beforeAll, describe, expect, setDefaultTimeout, test } from "bun:test";
import { mkdtempSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { loadPlaywright, toolchainDir } from "../helpers/lib/toolchain.ts";

const helpers = join(import.meta.dir, "..", "helpers");
setDefaultTimeout(120_000);

function sh(cmd: string[], env: Record<string, string> = {}) {
  const r = Bun.spawnSync(cmd, { env: { ...process.env, ...env }, stdout: "pipe", stderr: "pipe" });
  return { code: r.exitCode, stdout: r.stdout.toString(), stderr: r.stderr.toString() };
}

describe("setup-scene.sh", () => {
  // Runs against the real toolchain dir: a scratch dir would download chromium on every run.
  test(
    "installs pinned playwright and a launchable chromium, and a rerun changes nothing",
    async () => {
      const first = sh(["/bin/bash", join(helpers, "setup-scene.sh")]);
      expect(first.stderr + first.stdout).not.toContain("syntax error");
      expect(first.code).toBe(0);
      const pkg = join(toolchainDir(), "node_modules", "playwright", "package.json");
      expect(JSON.parse(readFileSync(pkg, "utf8")).version).toBe("1.61.1");
      const stamp = statSync(pkg).mtimeMs;

      const second = sh(["/bin/bash", join(helpers, "setup-scene.sh")]);
      expect(second.code).toBe(0);
      expect(statSync(pkg).mtimeMs).toBe(stamp);

      const { chromium } = await loadPlaywright();
      const browser = await chromium.launch({ args: ["--disable-gpu"] });
      try {
        const page = await browser.newPage();
        await page.setContent("<p id=x>ok</p>");
        expect(await page.textContent("#x")).toBe("ok");
      } finally {
        await browser.close();
      }
    },
    600_000,
  );
});

const FPS = 30;
const scene = {
  root: join(import.meta.dir, "fixtures"),
  entry: "scene-basic.html",
  query: "swatch=magenta",
  viewport: { width: 200, height: 200, dpr: 2 },
  fps: FPS,
  duration: 3,
  removeClasses: ["reduced-motion"],
  routes: [{ path: "/api/magenta", status: 200, body: '{"color":"#ff00ff"}', contentType: "application/json" }],
  triggers: [{ t: 1.0, click: { role: "button", name: "Fade in" } }],
};

const dir = mkdtempSync(join(tmpdir(), "pv-scene-"));
afterAll(() => rmSync(dir, { recursive: true, force: true }));
const sceneJson = join(dir, "scene.json");
writeFileSync(sceneJson, JSON.stringify(scene));

function scene_(...args: string[]) {
  return sh(["bun", join(helpers, "scene.ts"), ...args]);
}

// One RGB pixel of frame n, picked by index (never -ss).
function pixel(video: string, n: number, x: number, y: number): number[] {
  const r = Bun.spawnSync([
    "ffmpeg", "-v", "error", "-i", video,
    "-vf", `select=eq(n\\,${n}),format=rgb24,crop=1:1:${x}:${y}`, "-frames:v", "1",
    "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
  ]);
  if (r.exitCode !== 0 || r.stdout.length !== 3) throw new Error(`no pixel: ${r.stderr.toString()}`);
  return [r.stdout[0], r.stdout[1], r.stdout[2]];
}

function framemd5(video: string): string {
  const r = sh(["ffmpeg", "-v", "error", "-i", video, "-f", "framemd5", "-"]);
  if (r.code !== 0) throw new Error(r.stderr);
  return r.stdout.split("\n").filter((l) => l && !l.startsWith("#")).join("\n");
}

describe("scene.ts", () => {
  const a = join(dir, "a.mp4");
  const b = join(dir, "b.mp4");
  const frames = join(dir, "frames");
  let reportA: any;
  let reportB: any;

  beforeAll(() => {
    const ra = scene_(sceneJson, "--out", a, "--frames-dir", frames, "--json");
    if (ra.code !== 0) throw new Error(`render a exited ${ra.code}: ${ra.stderr}`);
    reportA = JSON.parse(ra.stdout);
    const rb = scene_(sceneJson, "--out", b, "--json");
    if (rb.code !== 0) throw new Error(`render b exited ${rb.code}: ${rb.stderr}`);
    reportB = JSON.parse(rb.stdout);
  }, 300_000);

  test("renders duration x fps frames at viewport x dpr", () => {
    const r = sh([
      "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
      "-show_entries", "stream=width,height,nb_read_packets,pix_fmt", "-of", "json", a,
    ]);
    expect(JSON.parse(r.stdout).streams[0]).toMatchObject({
      width: 400, height: 400, nb_read_packets: "90", pix_fmt: "yuv420p",
    });
    expect(readdirSync(frames).filter((f) => f.endsWith(".png")).length).toBe(90);
  });

  test("two renders give identical framemd5", () => {
    const ma = framemd5(a);
    expect(ma.split("\n").length).toBe(90);
    expect(framemd5(b)).toBe(ma);
  });

  test("the triggered fade is at the opacity its clock says", () => {
    // Box centre is (70,70) CSS px, (140,140) at dpr 2. Trigger at t=1.0 is frame 30.
    const [before] = pixel(a, 29, 140, 140);
    const [mid] = pixel(a, 36, 140, 140); // t=1.2: 200 of 400ms, opacity 0.5
    const [done] = pixel(a, 45, 140, 140);
    expect(before).toBeLessThanOrEqual(3);
    expect(Math.abs(mid - 128)).toBeLessThanOrEqual(3);
    expect(done).toBeGreaterThanOrEqual(252);
    // Lossless frame from --frames-dir agrees without codec error.
    const [png] = pixel(join(frames, "frame-00036.png"), 0, 140, 140);
    expect(Math.abs(png - 128)).toBeLessThanOrEqual(1);
  });

  test("removeClasses are gone before frame 0", () => {
    const [r, g] = pixel(a, 0, 20, 20);
    expect(r).toBeLessThan(40);
    expect(g).toBeGreaterThan(200);
  });

  test("query and routes reach the page", () => {
    const [r, g, bl] = pixel(a, 60, 40, 300);
    expect(r).toBeGreaterThan(220);
    expect(g).toBeLessThan(40);
    expect(bl).toBeGreaterThan(220);
  });

  test("the timer-driven animation is reported as untriggered, the click-born and infinite ones are not", () => {
    for (const rep of [reportA, reportB]) {
      const names = rep.untriggered.map((u: any) => u.animation);
      expect(names).toEqual(["toast-pop"]);
      expect(rep.untriggered[0].target).toContain("toast");
      expect(rep.triggers).toEqual([{ t: 1, name: "Fade in", born: 1 }]);
    }
    expect(reportA.untriggered[0].frame).toBe(reportB.untriggered[0].frame);
  });

  test("usage errors exit 2", () => {
    expect(scene_().code).toBe(2);
    const bad = join(dir, "bad.json");
    writeFileSync(bad, JSON.stringify({ ...scene, root: join(dir, "missing") }));
    expect(scene_(bad, "--out", join(dir, "x.mp4")).code).toBe(2);
  });
});

// Renders a scene with --frames-dir and returns the report plus the frame dir.
function renderScene(name: string, overrides: Record<string, unknown>) {
  const json = join(dir, `${name}.json`);
  writeFileSync(json, JSON.stringify({
    root: join(import.meta.dir, "fixtures"), viewport: { width: 200, height: 200, dpr: 1 }, fps: FPS, ...overrides,
  }));
  const framesDir = join(dir, `${name}-frames`);
  const r = scene_(json, "--out", join(dir, `${name}.mp4`), "--frames-dir", framesDir, "--json");
  if (r.code !== 0) throw new Error(`${name} exited ${r.code}: ${r.stderr}`);
  return { report: JSON.parse(r.stdout), framesDir };
}

// Per-frame md5 of a region of the lossless PNG frames.
function regionHashes(framesDir: string, crop: string): string[] {
  const r = sh(["ffmpeg", "-v", "error", "-i", join(framesDir, "frame-%05d.png"), "-vf", `crop=${crop}`, "-f", "framemd5", "-"]);
  if (r.code !== 0) throw new Error(r.stderr);
  return r.stdout.split("\n").filter((l) => l && !l.startsWith("#")).map((l) => l.split(",").pop()!.trim());
}

describe("scene.ts determinism on real pages", () => {
  test("an autofocused input's caret never shows, so it cannot blink between frames", () => {
    const { framesDir } = renderScene("caret", { entry: "scene-caret.html", viewport: { width: 200, height: 80, dpr: 1 }, duration: 2 });
    const hashes = regionHashes(framesDir, "180:60:10:10");
    expect(hashes.length).toBe(60);
    expect(new Set(hashes).size).toBe(1);
    // No red caret pixel anywhere in the field.
    const raw = Bun.spawnSync(["ffmpeg", "-v", "error", "-i", join(framesDir, "frame-%05d.png"),
      "-vf", "crop=180:60:10:10", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]).stdout;
    let red = 0;
    for (let i = 0; i < raw.length; i += 3) if (raw[i] > 150 && raw[i + 1] < 100 && raw[i + 2] < 100) red++;
    expect(red).toBe(0);
  });

  test("a trigger is a real tap: its effect lands, no keyboard focus ring is drawn, and no pointer is left hovering", () => {
    const { report, framesDir } = renderScene("focus", {
      entry: "scene-focus.html", duration: 1,
      triggers: [{ t: 0.3, click: { role: "button", name: "Open panel" } }],
    });
    expect(report.triggers).toEqual([{ t: 0.3, name: "Open panel", born: 0 }]);
    const raw = Bun.spawnSync(["ffmpeg", "-v", "error", "-i", join(framesDir, "frame-%05d.png"),
      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]).stdout;
    const frameBytes = 200 * 200 * 3;
    expect(raw.length).toBe(30 * frameBytes);
    let red = 0;
    for (let i = 0; i < raw.length; i += 3) if (raw[i] > 200 && raw[i + 1] < 60 && raw[i + 2] < 60) red++;
    expect(red).toBe(0);
    let magenta = 0;
    for (let i = 0; i < raw.length; i += 3) if (raw[i] > 200 && raw[i + 1] < 60 && raw[i + 2] > 200) magenta++;
    expect(magenta).toBe(0);
    // The panel opened: its green fill at (100,70) in the last frame, black before the tap.
    const at = (f: number) => raw.subarray(f * frameBytes + (70 * 200 + 100) * 3, f * frameBytes + (70 * 200 + 100) * 3 + 3);
    expect([...at(0)]).toEqual([0, 0, 0]);
    expect(at(29)[1]).toBeGreaterThan(150);
  });

  test("web fonts that load slowly are in place at frame 0 and at a trigger's first frame", () => {
    const slow = (path: string) => ({ path, file: "KaTeX_Script-Regular.woff2", contentType: "font/woff2", delayMs: 300 });
    const { framesDir } = renderScene("font", {
      entry: "scene-font.html", viewport: { width: 300, height: 200, dpr: 1 }, duration: 1.5,
      routes: [slow("/slow-a.woff2"), slow("/slow-b.woff2")],
      triggers: [{ t: 0.5, click: { role: "button", name: "Show" } }],
    });
    const a = regionHashes(framesDir, "290:50:10:0");
    const b = regionHashes(framesDir, "290:50:10:50");
    const fallback = regionHashes(framesDir, "290:50:10:100");
    expect(a.length).toBe(45);
    // The web font really rendered: "Hello" in it differs from "Hello" in the fallback.
    expect(a[44]).not.toBe(fallback[44]);
    expect(new Set(a).size).toBe(1);
    // From the tap on (frame 15), "World" is already in its web font.
    expect(new Set(b.slice(15)).size).toBe(1);
    expect(b[15]).not.toBe(b[0]);
    // JS that ran at the tap saw the face loaded, so its layout decision is the settled one.
    expect(pixel(join(framesDir, "frame-00044.png"), 0, 20, 155)).toEqual([0, 255, 0]);
  });

  test("waitFor holds frame 0 until a lazy surface mounts, by selector or by role and name", () => {
    for (const [as, waitFor] of [["div", { selector: "#late" }], ["button", { role: "button", name: "Ready" }]] as const) {
      const { framesDir } = renderScene(`late-${as}`, {
        entry: "scene-late.html", query: `as=${as}`, viewport: { width: 100, height: 100, dpr: 1 }, duration: 0.2, waitFor,
      });
      const [png] = [join(framesDir, "frame-00000.png")];
      const px = pixel(png, 0, 5, 5);
      expect({ as, px }).toEqual({ as, px: [0, 255, 0] });
    }
  });

  test("boot layout that converges over real and virtual frames is settled before frame 0", () => {
    const { report, framesDir } = renderScene("measure", {
      entry: "scene-measure.html", viewport: { width: 200, height: 60, dpr: 2 }, duration: 0.5,
    });
    const box = regionHashes(framesDir, "280:100:0:0");
    expect(box.length).toBe(15);
    expect(new Set(box).size).toBe(1);
    // Settled width 103 CSS px from x=10: device px 20..225 are white, 226 is not.
    expect(pixel(join(framesDir, "frame-00000.png"), 0, 225, 60)).toEqual([255, 255, 255]);
    expect(pixel(join(framesDir, "frame-00000.png"), 0, 226, 60)).toEqual([0, 0, 0]);
    // The spinning element never counts as unsettled layout.
    expect(report.warnings).toEqual([]);
  });

  test("boot waits for in-flight requests and re-lays out from a steady state before frame 0", () => {
    const { report, framesDir } = renderScene("pin", {
      entry: "scene-pin.html", viewport: { width: 100, height: 100, dpr: 1 }, duration: 0.3,
      routes: [{ path: "/api/rows", body: "10", contentType: "application/json", delayMs: 300 }],
    });
    const all = regionHashes(framesDir, "100:100:0:0");
    expect(all.length).toBe(9);
    expect(new Set(all).size).toBe(1);
    // Pinned after the rows arrived: the green end marker fills the bottom.
    expect(pixel(join(framesDir, "frame-00000.png"), 0, 50, 95)).toEqual([0, 255, 0]);
    expect(report.warnings).toEqual([]);
  });

  test("a transition started by boot churn is finished before frame 0; an entrance animation still plays", () => {
    const { framesDir } = renderScene("boot-transition", {
      entry: "scene-boot-transition.html", viewport: { width: 200, height: 60, dpr: 1 }, duration: 0.5,
      removeClasses: ["reduced-motion"],
    });
    const box = regionHashes(framesDir, "160:60:0:0");
    expect(box.length).toBe(15);
    expect(new Set(box).size).toBe(1);
    // Width 140 from x=10: x=149 white, x=150 black, at frame 0.
    expect(pixel(join(framesDir, "frame-00000.png"), 0, 149, 30)).toEqual([255, 255, 255]);
    expect(pixel(join(framesDir, "frame-00000.png"), 0, 150, 30)).toEqual([0, 0, 0]);
    // The entrance fade runs 0 -> 1 over 300ms: invisible at frame 0, full by frame 12.
    expect(pixel(join(framesDir, "frame-00000.png"), 0, 180, 20)[1]).toBeLessThanOrEqual(3);
    expect(pixel(join(framesDir, "frame-00012.png"), 0, 180, 20)[1]).toBeGreaterThanOrEqual(252);
  });

  const press = (name: string, trigger: Record<string, unknown>) => renderScene(name, {
    entry: "scene-press.html", viewport: { width: 200, height: 120, dpr: 1 }, duration: 1,
    triggers: [{ t: 0.5, ...trigger }],
  });

  test("a key press sends from the focused field, and the row it adds enters from birth", () => {
    const { report, framesDir } = press("press", { press: { key: "Enter" } });
    expect(report.triggers).toEqual([{ t: 0.5, key: "Enter", born: 1 }]);
    const at = (f: number, x: number) => pixel(join(framesDir, `frame-${String(f).padStart(5, "0")}.png`), 0, x, 20);
    expect(at(14, 40)).toEqual([0, 0, 0]); // before t=0.5: no row
    expect(at(15, 40)).toEqual([0, 0, 0]); // born at 0.5, opacity 0
    expect(Math.abs(at(21, 40)[0] - 170)).toBeLessThanOrEqual(3); // 200 of 300ms
    expect(at(29, 40)).toEqual([255, 255, 255]);
    expect(at(29, 150)).toEqual([0, 0, 0]); // the other field sent nothing
  });

  test("a press with a target focuses it first, by role and name or by selector", () => {
    for (const [name, target] of [["press-role", { role: "textbox", name: "Reply" }], ["press-sel", { selector: "#reply" }]] as const) {
      const { report, framesDir } = press(name, { press: { key: "Enter", ...target } });
      expect(report.triggers[0]).toMatchObject({ t: 0.5, key: "Enter", born: 1 });
      const last = join(framesDir, "frame-00029.png");
      expect({ name, reply: pixel(last, 0, 150, 20), draft: pixel(last, 0, 40, 20) })
        .toEqual({ name, reply: [0, 255, 0], draft: [0, 0, 0] });
    }
  });

  test("a trigger needs exactly one of click or press, with known fields and a real key", () => {
    const bad = (name: string, trigger: Record<string, unknown>) => {
      const json = join(dir, `${name}.json`);
      writeFileSync(json, JSON.stringify({
        root: join(import.meta.dir, "fixtures"), entry: "scene-press.html", viewport: { width: 200, height: 120, dpr: 1 },
        fps: FPS, duration: 1, triggers: [{ t: 0.5, ...trigger }],
      }));
      return scene_(json, "--out", join(dir, `${name}.mp4`));
    };
    for (const [name, trigger] of [
      ["both", { click: { role: "textbox", name: "Reply" }, press: { key: "Enter" } }],
      ["neither", {}],
      ["unknown-field", { press: { key: "Enter", repeat: 2 } }],
      ["unknown-key", { press: { key: "Entr" } }],
    ] as const) {
      const r = bad(name, trigger);
      expect({ name, code: r.code }).toEqual({ name, code: 2 });
    }
  });
});
