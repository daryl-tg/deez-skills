// Two-pass loudnorm. The first pass measures; the second applies one linear gain
// from those measurements, so the mix keeps its dynamics instead of being pumped.
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { ffmpeg, main, mustRun, parse, requireFile, UsageError } from "./lib/ffmpeg.ts";

const usage = "bun helpers/loudness.ts <in> <out> [--i -14] [--tp -1.5] [--lra 11] [--no-limit] [--json]";
const description = `
Two-pass ffmpeg loudnorm: measures <in>, then writes <out> with one linear
gain from those measurements, at the input's sample rate.
When that gain would push true peak past --tp (an already-mastered bed with
AAC overshoot, say), a true-peak limiter runs first: the bed is gained toward
--i and limited 4x oversampled to 0.5 dB under --tp, with no makeup gain,
until one linear gain fits. --no-limit skips it. The report says whether the
limiter ran and how much it pulled the peaks down. The LRA target is
widened to the measured range if needed so loudnorm stays linear.
Defaults: --i -14 LUFS, --tp -1.5 dBTP, --lra 11 LU.
Prints measured input and output integrated loudness and true peak.
Exit 0 if loudnorm applied one linear gain and the output lands within 0.5 LU
of --i with true peak at most --tp +0.1. Exit 1 if it missed target, or if
loudnorm fell back to dynamic mode (it reshaped the dynamics, which a mastered
bed must not have), even when the output is on target. Exit 2 on usage or
decode errors.
`;

type Stats = Record<string, string>;

// loudnorm prints one JSON block on stderr, followed by ffmpeg's own stats lines.
function loudnormJson(stderr: string): Stats {
  const m = stderr.match(/\{[^{}]*"input_i"[^{}]*\}/g);
  if (!m) throw new UsageError("loudnorm printed no measurement");
  return JSON.parse(m[m.length - 1]);
}

function num(flag: string, raw: string | undefined, fallback: number): number {
  const v = raw === undefined ? fallback : Number(raw);
  if (!Number.isFinite(v)) throw new UsageError(`bad --${flag}: ${raw}`);
  return v;
}

main(usage, description, () => {
  const { values, positionals } = parse({
    i: { type: "string" }, tp: { type: "string" }, lra: { type: "string" },
    "no-limit": { type: "boolean" }, json: { type: "boolean" },
  });
  const input = requireFile(positionals[0], "<in>");
  const output = positionals[1];
  if (!output) throw new UsageError("missing <out>");
  const target = { i: num("i", values.i, -14), tp: num("tp", values.tp, -1.5), lra: num("lra", values.lra, 11) };

  const rate = mustRun([
    "ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate", "-of", "csv=p=0", input,
  ]).stdout.trim();
  if (!rate) throw new UsageError(`no audio stream in ${input}`);

  const measure = (path: string) => loudnormJson(ffmpeg([
    "-i", path, "-af", `loudnorm=I=${target.i}:TP=${target.tp}:LRA=${target.lra}:print_format=json`, "-f", "null", "-",
  ]).stderr);
  // loudnorm stays linear only if the gain to target leaves true peak under --tp.
  const fits = (m: Stats) => Number(m.input_tp) + target.i - Number(m.input_i) <= target.tp;

  const first = measure(input);
  let measured = first;
  let source = input;
  let limiter: { preGainDb: number; ceilingDbtp: number; peakReductionDb: number } | null = null;
  const scratch = mkdtempSync(join(tmpdir(), "pv-loudness-"));
  try {
    if (!values["no-limit"] && !fits(first)) {
      // Same stage as music.py finish: gain toward target, then limit oversampled 4x to approximate true peak.
      const ceilingDbtp = target.tp - 0.5;
      const limit = (10 ** (ceilingDbtp / 20)).toFixed(5);
      let gain = 0;
      source = join(scratch, "limited.wav");
      for (let k = 0; k < 4 && !fits(measured); k++) {
        gain += target.i - Number(measured.input_i);
        ffmpeg([
          "-y", "-i", input, "-af",
          `aresample=${4 * Number(rate)},volume=${gain.toFixed(3)}dB,` +
            `alimiter=level_in=1:level_out=1:limit=${limit}:attack=1:release=60:level=false:latency=true,aresample=${rate}`,
          "-c:a", "pcm_f32le", source,
        ]);
        measured = measure(source);
      }
      const r2 = (x: number) => Math.round(x * 100) / 100;
      limiter = { preGainDb: r2(gain), ceilingDbtp, peakReductionDb: r2(Number(first.input_tp) + gain - Number(measured.input_tp)) };
    }

    // A range wider than the target LRA forces dynamic mode, so widen it rather than compress the bed.
    const lra = Math.max(target.lra, Number(measured.input_lra));
    const applied = loudnormJson(ffmpeg([
      "-y", "-i", source, "-af",
      `loudnorm=I=${target.i}:TP=${target.tp}:LRA=${lra}:measured_I=${measured.input_i}:measured_TP=${measured.input_tp}` +
        `:measured_LRA=${measured.input_lra}:measured_thresh=${measured.input_thresh}:offset=${measured.target_offset}` +
        `:linear=true:print_format=json`,
      // loudnorm resamples to 192kHz internally; hand back the input's rate.
      "-ar", rate, output,
    ]).stderr);

    const inStats = { i: Number(first.input_i), tp: Number(first.input_tp), lra: Number(first.input_lra) };
    const outStats = { i: Number(applied.output_i), tp: Number(applied.output_tp), lra: Number(applied.output_lra) };
    const normalization = applied.normalization_type;
    const misses = [
      // Dynamic mode rides the gain over time; a mastered bed must come out with its dynamics intact.
      normalization !== "linear" && `loudnorm fell back to ${normalization} normalization, not one linear gain`,
      Math.abs(outStats.i - target.i) > 0.5 && `output ${outStats.i} LUFS is more than 0.5 LU from ${target.i}`,
      outStats.tp > target.tp + 0.1 && `output true peak ${outStats.tp} dBTP exceeds ${target.tp}`,
    ].filter((m): m is string => !!m);
    const pass = misses.length === 0;
    const reason = pass ? null : misses.join("; ");
    const row = (label: string, s: { i: number; tp: number }) => `${label}  ${s.i.toFixed(2)} LUFS  ${s.tp.toFixed(2)} dBTP`;
    return {
      code: pass ? 0 : 1,
      asJson: !!values.json,
      json: { pass, reason, target, lra, normalization, limited: !!limiter, limiter, input: inStats, output: outStats, path: output },
      human: [
        pass ? `on target (${target.i} LUFS, ${target.tp} dBTP, linear)` : `failed: ${reason}`,
        row("input ", inStats),
        ...(limiter ? [`limited: +${limiter.preGainDb} dB into a ${limiter.ceilingDbtp} dBTP ceiling, peaks down ${limiter.peakReductionDb} dB`] : []),
        row("output", outStats),
        output,
      ].join("\n"),
    };
  } finally {
    rmSync(scratch, { recursive: true, force: true });
  }
});
