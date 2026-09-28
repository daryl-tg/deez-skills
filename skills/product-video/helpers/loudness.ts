// Two-pass loudnorm. The first pass measures; the second applies one linear gain
// from those measurements, so the mix keeps its dynamics instead of being pumped.
import { ffmpeg, main, mustRun, parse, requireFile, UsageError } from "./lib/ffmpeg.ts";

const usage = "bun helpers/loudness.ts <in> <out> [--i -14] [--tp -1.5] [--lra 11] [--json]";
const description = `
Two-pass ffmpeg loudnorm: measures <in>, then writes <out> with one linear
gain from those measurements, at the input's sample rate. The LRA target is
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
    i: { type: "string" }, tp: { type: "string" }, lra: { type: "string" }, json: { type: "boolean" },
  });
  const input = requireFile(positionals[0], "<in>");
  const output = positionals[1];
  if (!output) throw new UsageError("missing <out>");
  const target = { i: num("i", values.i, -14), tp: num("tp", values.tp, -1.5), lra: num("lra", values.lra, 11) };

  const rate = mustRun([
    "ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate", "-of", "csv=p=0", input,
  ]).stdout.trim();
  if (!rate) throw new UsageError(`no audio stream in ${input}`);

  const measured = loudnormJson(ffmpeg([
    "-i", input, "-af", `loudnorm=I=${target.i}:TP=${target.tp}:LRA=${target.lra}:print_format=json`, "-f", "null", "-",
  ]).stderr);

  // A range wider than the target LRA forces dynamic mode, so widen it rather than compress the bed.
  const lra = Math.max(target.lra, Number(measured.input_lra));
  const applied = loudnormJson(ffmpeg([
    "-y", "-i", input, "-af",
    `loudnorm=I=${target.i}:TP=${target.tp}:LRA=${lra}:measured_I=${measured.input_i}:measured_TP=${measured.input_tp}` +
      `:measured_LRA=${measured.input_lra}:measured_thresh=${measured.input_thresh}:offset=${measured.target_offset}` +
      `:linear=true:print_format=json`,
    // loudnorm resamples to 192kHz internally; hand back the input's rate.
    "-ar", rate, output,
  ]).stderr);

  const inStats = { i: Number(measured.input_i), tp: Number(measured.input_tp), lra: Number(measured.input_lra) };
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
    json: { pass, reason, target, lra, normalization, input: inStats, output: outStats, path: output },
    human: [
      pass ? `on target (${target.i} LUFS, ${target.tp} dBTP, linear)` : `failed: ${reason}`,
      row("input ", inStats),
      row("output", outStats),
      output,
    ].join("\n"),
  };
});
