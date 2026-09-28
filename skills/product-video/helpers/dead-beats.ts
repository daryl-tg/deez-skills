// A beat where nothing on screen changes reads as a stall, however good the
// music. Energy is the mean absolute luma difference between consecutive frames.
import { readFileSync } from "node:fs";
import { ffmpeg, main, parse, probeVideo, requireFile, UsageError } from "./lib/ffmpeg.ts";

const usage = "bun helpers/dead-beats.ts <video> <beats.json> [--threshold <x>] [--json]";
const description = `
Flags beat windows where the picture barely changes. For each window
[beat_i, beat_i+1), plus a tail window from the last beat to the video's end,
computes the mean absolute frame-to-frame luma difference.
beats.json: a bare array of seconds, or beats.py's object (its "grid" is used,
else its "beats").
--threshold  flag windows below this energy (default 0.01).
Exit 1 if any window is flagged; 0 if none; 2 on usage or decode errors.
`;

// Frozen stretches measured ≤0.005 (crf 23 refinement noise); a 40px card crawling 1px/frame measured ~0.019. 0.01 splits them.
const DEFAULT_THRESHOLD = 0.01;

function readBeats(path: string): number[] {
  let raw: unknown;
  try {
    raw = JSON.parse(readFileSync(path, "utf8"));
  } catch (e) {
    throw new UsageError(`cannot read beats: ${(e as Error).message}`);
  }
  // beats.py's object carries a grid at the requested BPM; cuts snap to it, so it wins over detected beats.
  const obj = raw as { grid?: unknown; beats?: unknown };
  const beats = Array.isArray(raw) ? raw : (obj?.grid ?? obj?.beats);
  if (!Array.isArray(beats) || beats.length < 1 || !beats.every((b) => typeof b === "number" && Number.isFinite(b))) {
    throw new UsageError("beats.json must be an array of beat times in seconds, or an object with one under \"grid\" or \"beats\"");
  }
  return [...beats].sort((a, b) => a - b);
}

// tblend stamps each difference with the later frame's time.
function frameDiffs(video: string): { t: number; energy: number }[] {
  const out = ffmpeg([
    "-v", "error", "-i", video, "-map", "0:v:0",
    "-vf", "tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-",
    "-f", "null", "-",
  ]).stdout;
  const diffs: { t: number; energy: number }[] = [];
  let t = NaN;
  for (const line of out.split("\n")) {
    const time = line.match(/pts_time:(\S+)/);
    if (time) t = Number(time[1]);
    const avg = line.match(/YAVG=(\S+)/);
    if (avg) diffs.push({ t, energy: Number(avg[1]) });
  }
  return diffs;
}

main(usage, description, () => {
  const { values, positionals } = parse({ threshold: { type: "string" }, json: { type: "boolean" } });
  const video = requireFile(positionals[0], "<video>");
  const beats = readBeats(requireFile(positionals[1], "<beats.json>"));
  const threshold = values.threshold === undefined ? DEFAULT_THRESHOLD : Number(values.threshold);
  if (!Number.isFinite(threshold)) throw new UsageError(`bad --threshold: ${values.threshold}`);

  const { duration } = probeVideo(video);
  const diffs = frameDiffs(video);
  const eps = 1e-6;
  // The last beat opens a tail window that runs to the end of the video.
  const bounds = duration > beats[beats.length - 1] + eps ? [...beats, duration] : beats;
  const windows = bounds.slice(0, -1).map((start, index) => {
    const end = bounds[index + 1];
    const inside = diffs.filter((d) => d.t >= start - eps && d.t < end - eps);
    // A window shorter than a frame has no evidence either way.
    const energy = inside.length ? inside.reduce((s, d) => s + d.energy, 0) / inside.length : null;
    return { index, start, end, energy, flagged: energy !== null && energy < threshold };
  });
  const dead = windows.filter((w) => w.flagged);
  const fmt = (w: (typeof windows)[number]) => `${w.start.toFixed(2)}-${w.end.toFixed(2)}s energy ${w.energy!.toFixed(4)}`;
  return {
    code: dead.length ? 1 : 0,
    asJson: !!values.json,
    json: { threshold, windows, flagged: dead.map((w) => w.index) },
    human: dead.length
      ? `${dead.length} dead beat(s) below ${threshold}:\n${dead.map(fmt).join("\n")}`
      : `no dead beats across ${windows.length} windows (threshold ${threshold})`,
  };
});
