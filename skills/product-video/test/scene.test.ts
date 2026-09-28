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
