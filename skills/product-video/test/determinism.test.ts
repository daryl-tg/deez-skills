import { afterAll, describe, expect, setDefaultTimeout, test } from "bun:test";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const helper = join(import.meta.dir, "..", "helpers", "determinism.ts");
const dir = mkdtempSync(join(tmpdir(), "pv-determinism-"));
afterAll(() => rmSync(dir, { recursive: true, force: true }));
setDefaultTimeout(30_000);

// Lossless intra-only encode so a one-frame edit cannot bleed into neighbours.
function clip(name: string, vf: string, seconds = 2): string {
  const out = join(dir, name);
  const r = Bun.spawnSync([
    "ffmpeg", "-v", "error", "-y",
    "-f", "lavfi", "-i", `testsrc2=s=64x64:r=10:d=${seconds}`,
    "-vf", vf, "-c:v", "libx264", "-qp", "0", "-g", "1", "-pix_fmt", "yuv420p", out,
  ]);
  if (r.exitCode !== 0) throw new Error(r.stderr.toString());
  return out;
}

// Identical lossless video with a sine track, so only the audio can differ.
function withAudio(name: string, hz: number): string {
  const out = join(dir, name);
  const r = Bun.spawnSync([
    "ffmpeg", "-v", "error", "-y",
    "-f", "lavfi", "-i", "testsrc2=s=64x64:r=10:d=2", "-f", "lavfi", "-i", `sine=frequency=${hz}:sample_rate=48000:d=2`,
    "-c:v", "libx264", "-qp", "0", "-g", "1", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", out,
  ]);
  if (r.exitCode !== 0) throw new Error(r.stderr.toString());
  return out;
}

function run(...args: string[]) {
  const r = Bun.spawnSync(["bun", helper, ...args]);
  return { code: r.exitCode, stdout: r.stdout.toString(), stderr: r.stderr.toString() };
}

const same = "null";
const frame7 = "drawbox=x=10:y=10:w=20:h=20:color=red:t=fill:enable='eq(n,7)'";

describe("determinism", () => {
  test("two identical renders pass", () => {
    const r = run(clip("a.mp4", same), clip("b.mp4", same), "--json");
    expect(r.code).toBe(0);
    expect(JSON.parse(r.stdout)).toMatchObject({
      identical: true, frames: { a: 20, b: 20 }, diffFrames: 0, firstDiffFrame: null,
    });
  });

  test("one differing frame is reported by index and count", () => {
    const r = run(clip("a2.mp4", same), clip("c.mp4", frame7), "--json");
    expect(r.code).toBe(1);
    expect(JSON.parse(r.stdout)).toMatchObject({
      identical: false, frames: { a: 20, b: 20 }, diffFrames: 1, firstDiffFrame: 7,
    });
  });

  test("a shorter render counts its missing frames as differing", () => {
    const r = run(clip("a3.mp4", same), clip("short.mp4", same, 1.5), "--json");
    expect(r.code).toBe(1);
    expect(JSON.parse(r.stdout)).toMatchObject({
      identical: false, frames: { a: 20, b: 15 }, diffFrames: 5, firstDiffFrame: 15,
    });
  });

  test("human report names the first differing frame", () => {
    const r = run(clip("a4.mp4", same), clip("c2.mp4", frame7));
    expect(r.code).toBe(1);
    expect(r.stdout).toContain("first differing frame 7");
  });

  test("identical video and audio pass", () => {
    const r = run(withAudio("av1.mp4", 440), withAudio("av2.mp4", 440), "--json");
    expect(r.code).toBe(0);
    expect(JSON.parse(r.stdout)).toMatchObject({ identical: true, diffFrames: 0, firstDiffStream: null });
  });

  test("a differing audio track fails and names its stream", () => {
    const r = run(withAudio("av3.mp4", 440), withAudio("av4.mp4", 880), "--json");
    expect(r.code).toBe(1);
    const out = JSON.parse(r.stdout);
    expect(out).toMatchObject({ identical: false, firstDiffStream: 1, firstDiffFrame: 0 });
    expect(out.streams[0]).toMatchObject({ index: 0, diffFrames: 0, firstDiffFrame: null });
    expect(out.streams[1].diffFrames).toBeGreaterThan(80);
    const human = run(withAudio("av5.mp4", 440), withAudio("av6.mp4", 880));
    expect(human.stdout).toContain("stream 1");
  });

  test("a video difference names stream 0", () => {
    const r = run(clip("a5.mp4", same), clip("c3.mp4", frame7), "--json");
    expect(JSON.parse(r.stdout)).toMatchObject({ firstDiffStream: 0, firstDiffFrame: 7 });
  });

  test("a missing input is a usage error", () => {
    const r = run(join(dir, "nope.mp4"), join(dir, "nope2.mp4"));
    expect(r.code).toBe(2);
  });
});
