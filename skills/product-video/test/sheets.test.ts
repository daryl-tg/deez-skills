import { afterAll, beforeAll, describe, expect, setDefaultTimeout, test } from "bun:test";
import { existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const helper = join(import.meta.dir, "..", "helpers", "sheets.ts");
const dir = mkdtempSync(join(tmpdir(), "pv-sheets-"));
afterAll(() => rmSync(dir, { recursive: true, force: true }));
setDefaultTimeout(30_000);

function ff(args: string[]): string {
  const r = Bun.spawnSync(["ffmpeg", "-v", "error", "-y", ...args]);
  if (r.exitCode !== 0) throw new Error(r.stderr.toString());
  return r.stdout.toString();
}

function dims(png: string): [number, number] {
  const r = Bun.spawnSync([
    "ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", png,
  ]);
  const [w, h] = r.stdout.toString().trim().split(",").map(Number);
  return [w, h];
}

function meanGray(input: string, vf: string): number {
  const r = Bun.spawnSync(["ffmpeg", "-v", "error", "-i", input, "-vf", `${vf},format=gray`, "-frames:v", "1", "-f", "rawvideo", "-"]);
  const px = r.stdout;
  let sum = 0;
  for (const v of px) sum += v;
  return sum / px.length;
}

// 5s at 10fps, square so every scaled height is exact. Brightness climbs 4 levels
// per frame, so each frame's index is readable from its tile.
const video = join(dir, "ramp.mp4");
beforeAll(() => {
  ff(["-f", "lavfi", "-i", "color=gray:s=96x96:r=10:d=5", "-vf", "geq=lum='16+N*4':cb=128:cr=128",
    "-c:v", "libx264", "-qp", "0", "-pix_fmt", "yuv420p", video]);
});

function run(...args: string[]) {
  const r = Bun.spawnSync(["bun", helper, ...args]);
  return { code: r.exitCode, stdout: r.stdout.toString(), stderr: r.stderr.toString() };
}

describe("sheets", () => {
  test("writes contact, phone and strip sheets at the contract's geometry", () => {
    const out = join(dir, "out");
    const r = run(video, "--out", out, "--strip", "1", "--strip", "2.5", "--json");
    expect(r.code).toBe(0);
    const paths = JSON.parse(r.stdout);
    expect(paths).toEqual({
      contact: join(out, "contact.png"),
      phone: join(out, "phone.png"),
      strips: [join(out, "strip-1.png"), join(out, "strip-2.5.png")],
    });
    // fps=2 over 5s is 10 frames: 6 across, 2 rows of 270px tiles.
    expect(dims(paths.contact)).toEqual([1620, 540]);
    // fps=1 over 5s is 5 frames: one row of 360px tiles.
    expect(dims(paths.phone)).toEqual([1800, 360]);
    expect(dims(paths.strips[0])).toEqual([3840, 320]);
    expect(dims(paths.strips[1])).toEqual([3840, 320]);
  });

  test("a strip holds 12 consecutive frames starting at the frame for t", () => {
    const out = join(dir, "strip");
    const r = run(video, "--out", out, "--strip", "2.5");
    expect(r.code).toBe(0);
    const strip = join(out, "strip-2.5.png");
    expect(r.stdout).toContain(strip);
    // Route the reference through RGB as the PNG was, so range conversion cancels out.
    const frame = (n: number) => meanGray(video, `select=eq(n\\,${n}),scale=320:-2,format=rgb24`);
    const tile = (k: number) => meanGray(strip, `crop=320:320:${k * 320}:0`);
    // t=2.5 at 10fps is frame 25; adjacent frames differ by ~4 grey levels.
    expect(Math.abs(tile(0) - frame(25))).toBeLessThan(1.5);
    expect(Math.abs(tile(11) - frame(36))).toBeLessThan(1.5);
    expect(Math.abs(tile(0) - frame(24))).toBeGreaterThan(2.5);
  });

  test("an unreadable video is an environment error and writes nothing", () => {
    const bogus = join(dir, "bogus.mp4");
    Bun.write(bogus, "not a video");
    const out = join(dir, "bogus-out");
    const r = run(bogus, "--out", out);
    expect(r.code).toBe(2);
    expect(existsSync(join(out, "contact.png"))).toBe(false);
  });

  test("--out is required", () => {
    expect(run(video).code).toBe(2);
  });
});
