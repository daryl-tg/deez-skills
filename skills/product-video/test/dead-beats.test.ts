import { afterAll, beforeAll, describe, expect, setDefaultTimeout, test } from "bun:test";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const helper = join(import.meta.dir, "..", "helpers", "dead-beats.ts");
const dir = mkdtempSync(join(tmpdir(), "pv-dead-beats-"));
afterAll(() => rmSync(dir, { recursive: true, force: true }));
setDefaultTimeout(30_000);

function ff(args: string[]) {
  const r = Bun.spawnSync(["ffmpeg", "-v", "error", "-y", ...args]);
  if (r.exitCode !== 0) throw new Error(r.stderr.toString());
}

function run(...args: string[]) {
  const r = Bun.spawnSync(["bun", helper, ...args]);
  return { code: r.exitCode, stdout: r.stdout.toString(), stderr: r.stderr.toString() };
}

// 4s at 30fps on the harness's 360x640 viewport, frozen from 1s to 3s.
// Beats every 0.5s (120 BPM), so windows 2..5 (1.0s to 3.0s) are dead.
const beats = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4];
const deadStarts = [1, 1.5, 2, 2.5];
const textured = join(dir, "textured.mp4");
const subtle = join(dir, "subtle.mp4");
const beatsFile = join(dir, "beats.json");

beforeAll(() => {
  writeFileSync(beatsFile, JSON.stringify(beats));
  // Busy texture, frame 29 held through frame 89. crf 23 leaves encoder
  // refinement noise in the held stretch, the floor a real freeze sits on.
  ff(["-f", "lavfi", "-i", "testsrc2=s=360x640:r=30:d=4",
    "-vf", "select='lt(n,30)+gte(n,90)',setpts=N/30/TB,loop=loop=61:size=1:start=29",
    "-frames:v", "120", "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", textured]);
  // The quietest motion that should still count: a 40px card crawling 1px per
  // frame on a dark background, like a slow UI drift.
  const x = "if(lt(t,1),t*30,if(lt(t,3),30,30+(t-3)*30))";
  ff(["-f", "lavfi", "-i", "color=0x1a1a1a:s=360x640:r=30:d=4", "-f", "lavfi", "-i", "color=0x5a5a5a:s=40x40:r=30:d=4",
    "-filter_complex", `[0][1]overlay=x='${x}':y=300`, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", subtle]);
});

const flaggedStarts = (stdout: string) =>
  JSON.parse(stdout).windows.filter((w: { flagged: boolean }) => w.flagged).map((w: { start: number }) => w.start);

describe("dead-beats", () => {
  test("a frozen stretch is flagged at its beats over encoder noise", () => {
    const r = run(textured, beatsFile, "--json");
    expect(r.code).toBe(1);
    expect(flaggedStarts(r.stdout)).toEqual(deadStarts);
    expect(JSON.parse(r.stdout).windows).toHaveLength(8);
  });

  test("the default threshold keeps a slow crawl alive and still flags its freeze", () => {
    const r = run(subtle, beatsFile, "--json");
    expect(r.code).toBe(1);
    expect(flaggedStarts(r.stdout)).toEqual(deadStarts);
  });

  test("a clip moving on every beat passes", () => {
    const moving = join(dir, "moving.mp4");
    ff(["-f", "lavfi", "-i", "testsrc2=s=180x320:r=30:d=4", "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", moving]);
    const r = run(moving, beatsFile, "--json");
    expect(r.code).toBe(0);
    expect(flaggedStarts(r.stdout)).toEqual([]);
    expect(JSON.parse(r.stdout).windows).toHaveLength(8);
  });

  test("--threshold overrides the default", () => {
    const r = run(subtle, beatsFile, "--threshold", "0.05", "--json");
    expect(r.code).toBe(1);
    expect(flaggedStarts(r.stdout)).toEqual([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]);
  });

  test("reads the grid from beats.py's object, since cuts snap to it", () => {
    // Detected beats only at 0 and 4 average the freeze away; the grid exposes it.
    const obj = join(dir, "beats-obj.json");
    writeFileSync(obj, JSON.stringify({ bpm_requested: 120, bpm_detected: 120, beats: [0, 4], downbeats: [0], grid: beats }));
    const r = run(textured, obj, "--json");
    expect(r.code).toBe(1);
    expect(flaggedStarts(r.stdout)).toEqual(deadStarts);
  });

  test("falls back to beats when the object has no grid", () => {
    const obj = join(dir, "beats-only.json");
    writeFileSync(obj, JSON.stringify({ bpm_requested: 120, beats }));
    const r = run(textured, obj, "--json");
    expect(r.code).toBe(1);
    expect(flaggedStarts(r.stdout)).toEqual(deadStarts);
  });

  test("a freeze after the last beat is caught in the tail window", () => {
    // Moves for 3s, then holds to 5s; the last beat is at 3.
    const tail = join(dir, "tail.mp4");
    ff(["-f", "lavfi", "-i", "testsrc2=s=180x320:r=30:d=3", "-vf", "loop=loop=-1:size=1:start=89",
      "-frames:v", "150", "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", tail]);
    const early = join(dir, "early-beats.json");
    writeFileSync(early, JSON.stringify([0, 1, 2, 3]));
    const r = run(tail, early, "--json");
    expect(r.code).toBe(1);
    const windows = JSON.parse(r.stdout).windows;
    expect(windows).toHaveLength(4);
    expect(windows[3]).toMatchObject({ start: 3, end: 5, flagged: true });
    expect(flaggedStarts(r.stdout)).toEqual([3]);
  });

  test("human report names the dead windows", () => {
    const r = run(textured, beatsFile);
    expect(r.code).toBe(1);
    expect(r.stdout).toContain("1.00-1.50s");
    expect(r.stdout).toContain("2.50-3.00s");
    expect(r.stdout).not.toContain("0.50-1.00s");
  });

  test("malformed beats are a usage error", () => {
    const bad = join(dir, "bad.json");
    writeFileSync(bad, JSON.stringify({ tempo: 120 }));
    expect(run(textured, bad).code).toBe(2);
  });
});
