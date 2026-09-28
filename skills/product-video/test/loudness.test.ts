import { afterAll, describe, expect, setDefaultTimeout, test } from "bun:test";
import { existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const helper = join(import.meta.dir, "..", "helpers", "loudness.ts");
const dir = mkdtempSync(join(tmpdir(), "pv-loudness-"));
afterAll(() => rmSync(dir, { recursive: true, force: true }));
setDefaultTimeout(30_000);

// 6s at 48kHz. A chord with a slow tremolo: loudnorm refuses linear gain on a
// signal whose loudness range is exactly zero, which real music never has.
function tone(name: string, amplitude: number): string {
  const out = join(dir, name);
  const expr = `${amplitude}*(0.7+0.3*sin(2*PI*0.5*t))*(sin(2*PI*220*t)+0.6*sin(2*PI*330*t)+0.3*sin(2*PI*440*t))/1.9`;
  ff(["-f", "lavfi", "-i", `aevalsrc='${expr}':s=48000:d=6`, out]);
  return out;
}

function ff(args: string[]) {
  const r = Bun.spawnSync(["ffmpeg", "-v", "error", "-y", ...args]);
  if (r.exitCode !== 0) throw new Error(r.stderr.toString());
}

// Measured with ebur128, independent of the loudnorm the helper uses.
function measure(file: string): { i: number; tp: number; rate: number } {
  const r = Bun.spawnSync(["ffmpeg", "-hide_banner", "-nostdin", "-i", file, "-af", "ebur128=peak=true", "-f", "null", "-"]);
  const summary = r.stderr.toString().split("Summary:")[1] ?? "";
  const probe = Bun.spawnSync(["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate", "-of", "csv=p=0", file]);
  return {
    i: Number(summary.match(/I:\s+(-?[\d.]+) LUFS/)?.[1]),
    tp: Number(summary.match(/Peak:\s+(-?[\d.]+) dBFS/)?.[1]),
    rate: Number(probe.stdout.toString().trim()),
  };
}

function run(...args: string[]) {
  const r = Bun.spawnSync(["bun", helper, ...args]);
  return { code: r.exitCode, stdout: r.stdout.toString(), stderr: r.stderr.toString() };
}

describe("loudness", () => {
  test("a quiet bed is raised to -14 LUFS under -1.5 dBTP", () => {
    const input = tone("quiet.wav", 0.05);
    const out = join(dir, "quiet-out.wav");
    const r = run(input, out, "--json");
    expect(r.code).toBe(0);
    const m = measure(out);
    expect(Math.abs(m.i - -14)).toBeLessThanOrEqual(0.5);
    expect(m.tp).toBeLessThanOrEqual(-1.5 + 0.1);
    expect(m.rate).toBe(48000);
    const report = JSON.parse(r.stdout);
    expect(report.normalization).toBe("linear");
    expect(Math.abs(report.input.i - measure(input).i)).toBeLessThanOrEqual(0.5);
    expect(Math.abs(report.output.i - m.i)).toBeLessThanOrEqual(0.5);
    expect(Math.abs(report.output.tp - m.tp)).toBeLessThanOrEqual(0.5);
  });

  test("custom targets are honoured on a loud bed", () => {
    const input = tone("loud.wav", 0.7);
    const out = join(dir, "loud-out.wav");
    const r = run(input, out, "--i", "-23", "--tp", "-3", "--json");
    expect(r.code).toBe(0);
    const m = measure(out);
    expect(Math.abs(m.i - -23)).toBeLessThanOrEqual(0.5);
    expect(m.tp).toBeLessThanOrEqual(-3 + 0.1);
    expect(r.stdout).toContain('"i":-23');
  });

  test("human report prints measured input and output loudness and peak", () => {
    const r = run(tone("human.wav", 0.05), join(dir, "human-out.wav"));
    expect(r.code).toBe(0);
    expect(r.stdout).toMatch(/input\s+-\d+\.\d+ LUFS\s+-\d+\.\d+ dBTP/);
    expect(r.stdout).toMatch(/output\s+-1[34]\.\d+ LUFS\s+-\d+\.\d+ dBTP/);
  });

// An already-mastered bed with a few sharp transients, as AAC overshoot leaves
// it: about -14.2 LUFS, -1.2 dBTP. The 0.2 dB it needs would push peaks past
// -1.5, so no single linear gain fits until the transients are limited.
function mastered(name: string): string {
  const out = join(dir, name);
  const bed = "0.65*(0.7+0.3*sin(2*PI*0.5*t))*(sin(2*PI*220*t)+0.6*sin(2*PI*330*t)+0.3*sin(2*PI*440*t))/1.9";
  ff(["-f", "lavfi", "-i", `aevalsrc='if(lt(mod(t\\,2)\\,0.003)\\,0.87*sin(2*PI*2000*t)\\,${bed})':s=48000:d=6`, out]);
  return out;
}

  test("transients over the peak target are limited so one linear gain fits", () => {
    const input = mastered("mastered.wav");
    const before = measure(input);
    expect(Math.abs(before.i - -14.2)).toBeLessThanOrEqual(0.2);
    expect(Math.abs(before.tp - -1.2)).toBeLessThanOrEqual(0.2);
    const out = join(dir, "mastered-out.wav");
    const r = run(input, out, "--json");
    expect(r.code).toBe(0);
    const report = JSON.parse(r.stdout);
    expect(report).toMatchObject({ pass: true, normalization: "linear", limited: true });
    expect(report.limiter.peakReductionDb).toBeGreaterThan(0);
    const m = measure(out);
    expect(Math.abs(m.i - -14)).toBeLessThanOrEqual(0.5);
    expect(m.tp).toBeLessThanOrEqual(-1.5 + 0.1);
    expect(m.rate).toBe(48000);
  });

  test("--no-limit skips the limiter, so the same bed falls back to dynamic", () => {
    const r = run(mastered("mastered-nl.wav"), join(dir, "mastered-nl-out.wav"), "--no-limit", "--json");
    expect(r.code).toBe(1);
    expect(JSON.parse(r.stdout)).toMatchObject({ pass: false, normalization: "dynamic", limited: false });
  });

  test("a bed with headroom is not limited", () => {
    const r = run(tone("headroom.wav", 0.05), join(dir, "headroom-out.wav"), "--json");
    expect(r.code).toBe(0);
    expect(JSON.parse(r.stdout)).toMatchObject({ limited: false, normalization: "linear" });
  });

  test("dynamic normalization is a finding even when the output lands on target", () => {
    // A steady tone has a loudness range of exactly 0, which makes loudnorm
    // refuse linear gain and reshape the dynamics instead.
    const steady = join(dir, "steady.wav");
    ff(["-f", "lavfi", "-i", "aevalsrc='0.03*sin(2*PI*440*t)+0.02*sin(2*PI*660*t)':s=48000:d=6", steady]);
    const out = join(dir, "steady-out.wav");
    const r = run(steady, out, "--json");
    expect(r.code).toBe(1);
    const report = JSON.parse(r.stdout);
    expect(report).toMatchObject({ pass: false, normalization: "dynamic" });
    expect(report.reason).toContain("dynamic");
    expect(Math.abs(measure(out).i - -14)).toBeLessThanOrEqual(0.5);
    const human = run(steady, join(dir, "steady-human.wav"));
    expect(human.code).toBe(1);
    expect(human.stdout).toContain("dynamic");
    expect(human.stdout).toContain("not one linear gain");
  });

  test("a signal that cannot reach target is a finding", () => {
    // Full-scale 5ms clicks over near silence: any gain that reaches -14 LUFS
    // would clip, so loudnorm limits and lands well short.
    const clicks = join(dir, "clicks.wav");
    ff(["-f", "lavfi", "-i", "aevalsrc='if(lt(mod(t\\,1)\\,0.005)\\,0.99*sin(2*PI*1000*t)\\,0.0005*(random(0)-0.5))':s=48000:d=6", clicks]);
    const out = join(dir, "clicks-out.wav");
    const r = run(clicks, out, "--json");
    expect(r.code).toBe(1);
    const report = JSON.parse(r.stdout);
    expect(report.pass).toBe(false);
    expect(report.output.i).toBeLessThan(-14.5);
    expect(measure(out).rate).toBe(48000);
  });

  test("a missing input is a usage error and writes nothing", () => {
    const out = join(dir, "none.wav");
    expect(run(join(dir, "nope.wav"), out).code).toBe(2);
    expect(existsSync(out)).toBe(false);
  });
});
