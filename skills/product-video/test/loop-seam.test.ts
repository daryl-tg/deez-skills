import { afterAll, describe, expect, setDefaultTimeout, test } from "bun:test";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const helper = join(import.meta.dir, "..", "helpers", "loop-seam.ts");
const dir = mkdtempSync(join(tmpdir(), "pv-loop-seam-"));
afterAll(() => rmSync(dir, { recursive: true, force: true }));
setDefaultTimeout(30_000);

// 2s at 15fps, frames 0..29. A card slides over static bars; x decides the seam.
// Positions use t, since overlay counts n from 1.
function clip(name: string, x: string): string {
  const out = join(dir, name);
  const r = Bun.spawnSync([
    "ffmpeg", "-v", "error", "-y",
    "-f", "lavfi", "-i", "smptebars=s=180x320:r=15:d=2", "-f", "lavfi", "-i", "color=white:s=60x60:r=15:d=2",
    "-filter_complex", `[0][1]overlay=x='${x}':y=130:shortest=1`,
    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", out,
  ]);
  if (r.exitCode !== 0) throw new Error(r.stderr.toString());
  return out;
}

function run(...args: string[]) {
  const r = Bun.spawnSync(["bun", helper, ...args]);
  return { code: r.exitCode, stdout: r.stdout.toString(), stderr: r.stderr.toString() };
}

describe("loop-seam", () => {
  // Out and back: the last frame puts the card where the first did.
  const loops = () => clip("loops.mp4", "10+80*sin(PI*t*15/29)");
  // Drifts right and never returns.
  const drifts = () => clip("drifts.mp4", "10+80*t*15/29");

  test("a clip whose last frame matches its first passes", () => {
    const r = run(loops(), "--json");
    expect(r.code).toBe(0);
    const out = JSON.parse(r.stdout);
    expect(out).toMatchObject({ pass: true, min: 0.98, lastFrame: 29 });
    expect(out.ssim).toBeGreaterThanOrEqual(0.98);
  });

  test("a clip that drifts fails", () => {
    const r = run(drifts(), "--json");
    expect(r.code).toBe(1);
    const out = JSON.parse(r.stdout);
    expect(out).toMatchObject({ pass: false, min: 0.98, lastFrame: 29 });
    expect(out.ssim).toBeLessThan(0.98);
  });

  test("--min sets the bar", () => {
    const drift = drifts();
    const ssim = JSON.parse(run(drift, "--json").stdout).ssim;
    expect(run(drift, "--min", String(ssim - 0.01)).code).toBe(0);
    expect(run(drift, "--min", "0.999").code).toBe(1);
  });

  test("human report shows the score", () => {
    const r = run(drifts());
    expect(r.code).toBe(1);
    expect(r.stdout).toMatch(/SSIM 0\.\d+ < 0\.98/);
  });

  test("a missing video is a usage error", () => {
    expect(run(join(dir, "nope.mp4")).code).toBe(2);
  });
});
