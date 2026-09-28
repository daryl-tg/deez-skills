// Seek harness: renders a real UI fixture to MP4 by owning the whole clock.
// - page.clock is installed and paused, so Date, timers and rAF advance only
//   when the harness advances them: to composition time, frame by frame.
// - Every Animation is paused and posed by hand each frame; CSS animations run
//   on the compositor, not on the faked clock, so nothing else would seek them.
// - UI changes are timed clicks by accessible role and name.
// Ported from the unit1 spike (fallback.mjs).
import { spawn } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { extname, join, resolve, sep } from "node:path";
import { parseArgs } from "node:util";
import { exitOnHelp } from "./lib/ffmpeg.ts";
import { loadPlaywright, ToolchainMissing } from "./lib/toolchain.ts";

const USAGE = "bun helpers/scene.ts <scene.json> --out <clip.mp4> [--frames-dir <dir>] [--json]";
const DESCRIPTION = `
Renders a built UI fixture to MP4 frame by frame on a virtual clock: timers,
Date and rAF advance only with composition time, and every Animation is posed
by hand each frame, so two renders decode to identical frames. Needs the Playwright
toolchain from setup-scene.sh.

scene.json (fields marked ? are optional):
{
  "root": "/abs/dir",          built fixture directory, e.g. fixture-build's "root"
  "entry": "shell-fixture.html", HTML file under root to open
  "query"?: "view=agent",      query string for the entry; a leading "?" is optional
  "viewport": {
    "width": 360,              CSS pixels
    "height": 640,             CSS pixels
    "dpr": 3                   device scale; the clip is width*dpr x height*dpr
  },
  "fps": 30,                   frames per second
  "duration": 5,               seconds; frames = round(fps * duration)
  "removeClasses"?: ["reduced-motion"],
                               classes stripped from every element before frame 0
  "routes"?: [{                stubs matched on exact pathname before static files
    "path": "/healthz",
    "status"?: 200,            default 200
    "body"?: "{}",             default ""
    "file"?: "font.woff2",     serve this file (relative to root) as the body instead
    "delayMs"?: 300,           answer after this many real milliseconds (a slow network)
    "contentType"?: "application/json"   default "text/plain"
  }],
  "triggers"?: [{              run in t order
    "t": 1.0,                  composition second of the click
    "click": {
      "role": "button",        ARIA role
      "name": "Open menu"      exact accessible name; must match exactly one element
    }
  }],
  "waitFor"?: { "selector": "#ready" }  or  { "role": "region", "name": "Inbox" }
                               awaited before frame 0, so a scene with no
                               trigger can wait for a lazy surface
}

The page is served from http://127.0.0.1:18099 through page.route (nothing
binds a port); requests to any other origin are aborted. Boot awaits waitFor and
the first trigger's target, then loads every declared @font-face (again after
each trigger). A trigger is a real mouse tap at the element's centre, then the
pointer leaves the page, so no focus ring or hover appears; a covered target is
an error. Text carets are hidden. --frames-dir also writes frame-NNNNN.png.
The report lists each trigger's animations and any finite animation that
started with no trigger (timer-driven; give it fixture control).
Exit 0 on a finished render; 2 on any usage, environment or render error.
`;
// Intercepted by page.route; nothing binds it. A loopback origin is a secure
// context, which crypto.randomUUID needs.
const ORIGIN = "http://127.0.0.1:18099";
const TYPES: Record<string, string> = {
  ".html": "text/html; charset=utf-8", ".js": "application/javascript", ".mjs": "application/javascript",
  ".css": "text/css", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
  ".webp": "image/webp", ".woff": "font/woff", ".woff2": "font/woff2", ".ttf": "font/ttf",
  ".json": "application/json", ".wasm": "application/wasm", ".glb": "model/gltf-binary",
};

class UsageError extends Error {}

interface Trigger { t: number; click: { role: string; name: string } }
interface Route { path: string; status?: number; body?: string; file?: string; contentType?: string; delayMs?: number }
interface Scene {
  root: string;
  entry: string;
  query?: string;
  viewport: { width: number; height: number; dpr: number };
  fps: number;
  duration: number;
  removeClasses?: string[];
  routes?: Route[];
  triggers?: Trigger[];
  waitFor?: { selector?: string; role?: string; name?: string };
}

function readScene(path: string): Scene {
  if (!existsSync(path)) throw new UsageError(`scene not found: ${path}`);
  let s: Scene;
  try {
    s = JSON.parse(readFileSync(path, "utf8"));
  } catch (e) {
    throw new UsageError(`scene is not JSON: ${(e as Error).message}`);
  }
  const num = (v: unknown) => typeof v === "number" && Number.isFinite(v) && v > 0;
  if (!s.root || !existsSync(s.root) || !statSync(s.root).isDirectory()) throw new UsageError(`root is not a directory: ${s.root}`);
  if (!s.entry || !existsSync(join(s.root, s.entry))) throw new UsageError(`entry not found under root: ${s.entry}`);
  const v = s.viewport;
  if (!v || !num(v.width) || !num(v.height) || !num(v.dpr)) throw new UsageError("viewport needs positive width, height, dpr");
  if (!num(s.fps) || !num(s.duration)) throw new UsageError("fps and duration must be positive numbers");
  const w = s.waitFor;
  if (w && !(typeof w.selector === "string" && w.selector) && !(w.role && w.name)) {
    throw new UsageError(`waitFor needs "selector", or "role" and "name": ${JSON.stringify(w)}`);
  }
  s.triggers = [...(s.triggers ?? [])].sort((a, b) => a.t - b.t);
  for (const t of s.triggers) {
    if (typeof t.t !== "number" || t.t < 0 || !t.click?.role || !t.click?.name) {
      throw new UsageError(`bad trigger: ${JSON.stringify(t)}`);
    }
  }
  return s;
}

// Runs in the page. birth maps each Animation to the composition second its
// local time counts from: 0 for the baseline and for infinite loops (phase
// locked to t, so a remount never shifts them), T for a trigger's spawn, and
// first-seen t for anything a timer started.
function installPageLib() {
  const w = window as any;
  const infinite = (a: Animation) => !Number.isFinite(Number(a.effect?.getComputedTiming().endTime));
  const describe = (a: any) => {
    const el = a.effect?.target as Element | undefined;
    const cls = el ? Array.from(el.classList).slice(0, 2).map((c) => "." + c).join("") : "";
    return {
      animation: a.animationName || a.transitionProperty || a.id || a.constructor.name,
      target: el ? `${el.tagName.toLowerCase()}${el.id ? "#" + el.id : ""}${cls}`.slice(0, 80) : "?",
    };
  };
  const birth = new Map<Animation, number>();
  const untriggered: unknown[] = [];
  // Claim every unseen animation. Finite ones freeze at their start so no wall
  // clock progress (or animationend side effect) leaks in before the next pose.
  function adopt(mode: "baseline" | "trigger" | "timer", T: number, frame: number): number {
    let born = 0;
    for (const a of document.getAnimations()) {
      if (birth.has(a) || !a.effect) continue;
      a.pause();
      if (mode === "baseline" || infinite(a)) {
        birth.set(a, 0);
        continue;
      }
      a.currentTime = 0;
      birth.set(a, T);
      born++;
      if (mode === "timer") untriggered.push({ ...describe(a), t: T, frame });
    }
    return born;
  }
  function pose(t: number, frame: number) {
    adopt("timer", t, frame);
    for (const a of document.getAnimations()) {
      const b = birth.get(a);
      if (b === undefined) continue;
      a.pause();
      a.currentTime = Math.max(0, t - b) * 1000;
    }
  }
  w.__pv = { adopt, pose, untriggered };
}

async function render(scene: Scene, out: string, framesDir?: string) {
  const started = Date.now();
  const { chromium } = await loadPlaywright();
  const { width, height, dpr } = scene.viewport;
  const frames = Math.round(scene.fps * scene.duration);
  const misses: string[] = [];
  const root = resolve(scene.root);
  const routes = new Map((scene.routes ?? []).map((r) => [r.path, r]));

  // Software raster: hardware GPU anti-aliasing differs run to run.
  const browser = await chromium.launch({ args: ["--disable-gpu"] });
  try {
    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: dpr });
    await page.clock.install({ time: 0 });
    await page.clock.pauseAt(0);
    await page.route("**/*", async (route) => {
      const url = new URL(route.request().url());
      if (url.origin !== ORIGIN) return route.abort();
      const stub = routes.get(url.pathname);
      if (stub) {
        // Real time, not virtual: it models a slow network, which the paused clock must not stall.
        if (stub.delayMs) await Bun.sleep(stub.delayMs);
        const body = stub.file ? await readFile(resolve(root, stub.file)) : stub.body ?? "";
        const type = stub.contentType ?? (stub.file ? TYPES[extname(stub.file)] : undefined) ?? "text/plain";
        return route.fulfill({ status: stub.status ?? 200, body, contentType: type });
      }
      let p = decodeURIComponent(url.pathname);
      if (p.endsWith("/")) p += "index.html";
      const file = resolve(join(root, p));
      try {
        if (!file.startsWith(root + sep)) throw new Error("outside root");
        await route.fulfill({ body: await readFile(file), contentType: TYPES[extname(p)] ?? "application/octet-stream" });
      } catch {
        misses.push(p);
        await route.fulfill({ status: 404, body: "" });
      }
    });

    const query = scene.query ? `?${scene.query.replace(/^\?/, "")}` : "";
    await page.goto(`${ORIGIN}/${scene.entry.replace(/^\//, "")}${query}`, { waitUntil: "load" });
    const target = (t: Trigger) => page.getByRole(t.click.role as any, { name: t.click.name, exact: true });
    // A caret blinks on the wall clock, which the virtual clock does not own.
    await page.addStyleTag({ content: "*, *::before, *::after { caret-color: transparent !important; }" });

    // Boot. Wait in real time first, so the virtual time spent booting stays
    // fixed; step virtual time only for surfaces that need timers to mount.
    const w = scene.waitFor;
    const awaited = [
      ...(w ? [{ loc: w.selector ? page.locator(w.selector) : page.getByRole(w.role as any, { name: w.name, exact: true }), what: `waitFor ${JSON.stringify(w)}` }] : []),
      ...(scene.triggers![0] ? [{ loc: target(scene.triggers![0]), what: `first trigger target ${JSON.stringify(scene.triggers![0].click)}` }] : []),
    ];
    for (const { loc, what } of awaited) {
      await loc.first().waitFor({ state: "attached", timeout: 5_000 }).catch(() => {});
      for (let i = 0; i < 400 && !(await loc.count()); i++) await page.clock.runFor(25);
      if (!(await loc.count())) throw new UsageError(`${what} never appeared`);
    }

    // Load every declared face, not just those in use: a surface a trigger
    // mounts later would otherwise measure text before its font arrives, and
    // lay out one of two ways. Real-time wait; fonts never depend on timers.
    const warnings: string[] = [];
    const settleFonts = async (when: string) => {
      const done = page.evaluate(async () => {
        await Promise.all(
          Array.from(document.fonts).filter((f) => f.status !== "loaded").map((f) => f.load().catch(() => {})),
        );
        await document.fonts.ready;
        return true;
      });
      if (!(await Promise.race([done, Bun.sleep(15_000).then(() => false)]))) warnings.push(`fonts still loading 15s ${when}`);
    };
    const strip = (classes: string[]) =>
      page.evaluate((classes) => {
        for (const c of classes) for (const el of Array.from(document.querySelectorAll("." + CSS.escape(c)))) el.classList.remove(c);
      }, classes);
    await strip(scene.removeClasses ?? []);
    await settleFonts("at boot");
    await page.clock.runFor(250);
    await strip(scene.removeClasses ?? []);
    await settleFonts("before frame 0");
    await page.evaluate(installPageLib);
    await page.evaluate(() => (window as any).__pv.adopt("baseline", 0, 0));

    if (framesDir) mkdirSync(framesDir, { recursive: true });
    const ff = spawn("ffmpeg", [
      "-v", "error", "-y", "-f", "image2pipe", "-framerate", String(scene.fps), "-c:v", "png", "-i", "-",
      "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
      "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
      "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
      "-threads", "1", "-movflags", "+faststart", out,
    ], { stdio: ["pipe", "ignore", "pipe"] });
    let ffErr = "";
    ff.stderr.on("data", (d) => (ffErr += d));
    const ffDone = new Promise<number>((r) => ff.on("close", (code) => r(code ?? 1)));
    ff.on("error", () => {});

    const fired: { t: number; name: string; born: number }[] = [];
    let next = 0;
    let clockMs = 0; // virtual ms since composition t=0
    for (let n = 0; n < frames; n++) {
      const t = n / scene.fps;
      const want = Math.round((n * 1000) / scene.fps);
      if (want > clockMs) {
        await page.clock.runFor(want - clockMs);
        clockMs = want;
      }
      // Anything a timer started up to now is attributed to no trigger.
      await page.evaluate(([t, n]) => (window as any).__pv.adopt("timer", t, n), [t, n]);
      while (next < scene.triggers!.length && t + 1e-9 >= scene.triggers![next].t) {
        const trig = scene.triggers![next++];
        const T = trig.t;
        await page.evaluate(([T, n]) => (window as any).__pv.pose(T, n), [T, n]);
        const loc = target(trig);
        if ((await loc.count()) !== 1) {
          throw new UsageError(`trigger at t=${T}: ${await loc.count()} elements match ${trig.click.role} "${trig.click.name}"`);
        }
        // A real tap through CDP input, not el.click(): a synthetic click
        // leaves the page in keyboard modality, so any focus the app moves
        // draws a focus-visible ring no finger ever would. CDP input does
        // not wait on actionability, so it works under the paused clock.
        const hit = await loc.evaluate((el: HTMLElement) => {
          el.scrollIntoView({ block: "center", inline: "center", behavior: "instant" });
          const r = el.getBoundingClientRect();
          const x = r.left + r.width / 2;
          const y = r.top + r.height / 2;
          const top = document.elementFromPoint(x, y);
          return { x, y, covered: !top || !(el === top || el.contains(top)) };
        });
        if (hit.covered) throw new UsageError(`trigger at t=${T}: ${trig.click.role} "${trig.click.name}" is covered at its centre`);
        await page.mouse.move(hit.x, hit.y);
        await page.mouse.down();
        await page.mouse.up();
        // Lift the finger. A resting pointer hovers whatever layout slides under
        // it, and Chrome applies that on a wall-clock timer.
        await page.mouse.move(-1, -1);
        let born = await page.evaluate((T: number) => {
          const pv = (window as any).__pv;
          const now = pv.adopt("trigger", T, -1);
          // React commits discrete clicks in a microtask; claim what that spawns too.
          return Promise.resolve().then(() => now + pv.adopt("trigger", T, -1));
        }, T);
        // Timer and rAF chained follow-ups run in virtual time and belong to this trigger.
        for (let k = 0; k < 4; k++) {
          await page.clock.runFor(16);
          clockMs += 16;
          born += await page.evaluate((T) => (window as any).__pv.adopt("trigger", T, -1), T);
        }
        await settleFonts(`after the trigger at t=${T}`);
        fired.push({ t: T, name: trig.click.name, born });
      }
      await page.evaluate(([t, n]) => (window as any).__pv.pose(t, n), [t, n]);
      const png = await page.screenshot({ type: "png", caret: "hide" });
      if (framesDir) writeFileSync(join(framesDir, `frame-${String(n).padStart(5, "0")}.png`), png);
      if (!ff.stdin!.write(png)) await new Promise((r) => ff.stdin!.once("drain", r));
    }
    ff.stdin!.end();
    const code = await ffDone;
    if (code !== 0) throw new UsageError(`ffmpeg failed (${code}): ${ffErr.trim().split("\n").slice(-3).join("\n")}`);
    const untriggered = await page.evaluate(() => (window as any).__pv.untriggered);
    return {
      out, frames, fps: scene.fps, width: width * dpr, height: height * dpr,
      wallSeconds: (Date.now() - started) / 1000, triggers: fired, untriggered, misses, warnings,
    };
  } finally {
    await browser.close();
  }
}

async function main() {
  exitOnHelp(USAGE, DESCRIPTION);
  let values, positionals;
  try {
    ({ values, positionals } = parseArgs({
      args: Bun.argv.slice(2),
      options: { out: { type: "string" }, "frames-dir": { type: "string" }, json: { type: "boolean" } },
      allowPositionals: true,
      strict: true,
    }));
    if (positionals.length !== 1 || !values.out) throw new UsageError("need one <scene.json> and --out");
    const scene = readScene(positionals[0]);
    const report = await render(scene, resolve(values.out), values["frames-dir"] && resolve(values["frames-dir"]));
    if (values.json) {
      console.log(JSON.stringify(report));
    } else {
      const lines = [
        `${report.out}: ${report.frames} frames, ${report.width}x${report.height} @ ${report.fps}fps in ${report.wallSeconds}s`,
        ...report.triggers.map((t) => `  trigger t=${t.t} "${t.name}": ${t.born} animations`),
        ...report.untriggered.map((u: any) => `  UNTRIGGERED ${u.animation} on ${u.target} first seen t=${u.t.toFixed(3)} (frame ${u.frame}); timer-driven, give it fixture control`),
        ...(report.misses.length ? [`  404s: ${[...new Set(report.misses)].join(", ")}`] : []),
        ...report.warnings.map((w) => `  WARNING ${w}`),
      ];
      console.log(lines.join("\n"));
    }
    process.exit(0);
  } catch (e) {
    const known = e instanceof UsageError || e instanceof ToolchainMissing || (e as Error)?.name === "TypeError";
    console.error(known ? (e as Error).message : (e as Error)?.stack ?? String(e));
    console.error(`usage: ${USAGE}`);
    // No finding is possible here, so any failure is usage or environment.
    process.exit(2);
  }
}

await main();
