// Review sheets: the whole clip at a glance, at phone width, and frame-by-frame
// strips around moments that need a closer look.
import { mkdirSync } from "node:fs";
import { join } from "node:path";
import { ffmpeg, main, parse, probeVideo, requireFile, UsageError } from "./lib/ffmpeg.ts";

const usage = "bun helpers/sheets.ts <video> --out <dir> [--strip <t> [<t>...]]... [--json]";
const description = `
Writes review sheets into --out and prints their paths:
  contact.png      fps=2, 270px wide tiles, 6 across, as many rows as needed
  phone.png        fps=1, 360px wide tiles, 5 across
  strip-<t>.png    per strip time: 12 consecutive frames from the frame at t seconds, 320px, 12x1
--strip takes one or more times in seconds, and may repeat: "--strip 2 5.9" and
"--strip 2 --strip 5.9" are the same. Any other extra argument is a usage error.
Exit 0 on success; 2 on usage or decode errors.
`;

// The tile filter pads to a full grid, so rows must be sized to the real frame count.
function sampledFrames(video: string, fps: number): number {
  const out = ffmpeg(["-v", "error", "-i", video, "-map", "0:v:0", "-vf", `fps=${fps},scale=16:-2`, "-f", "framemd5", "-"]).stdout;
  return out.split("\n").filter((l) => l.trim() && !l.startsWith("#")).length;
}

function sheet(video: string, vf: string, out: string): string {
  ffmpeg(["-v", "error", "-y", "-i", video, "-map", "0:v:0", "-vf", vf, "-frames:v", "1", "-update", "1", out]);
  return out;
}

main(usage, description, () => {
  const { values, positionals } = parse({
    out: { type: "string" },
    strip: { type: "string", multiple: true },
    json: { type: "boolean" },
  });
  if (positionals.length > 1) throw new UsageError(`unexpected argument(s): ${positionals.slice(1).join(" ")}`);
  const video = requireFile(positionals[0], "<video>");
  if (!values.out) throw new UsageError("missing --out <dir>");
  const strips = (values.strip ?? []).map((t) => {
    const s = Number(t);
    if (!Number.isFinite(s) || s < 0) throw new UsageError(`bad --strip time: ${t}`);
    return { label: t, seconds: s };
  });
  const info = probeVideo(video);
  mkdirSync(values.out, { recursive: true });

  const grid = (fps: number, across: number) => `${across}x${Math.max(1, Math.ceil(sampledFrames(video, fps) / across))}`;
  const contact = sheet(video, `fps=2,scale=270:-2,tile=${grid(2, 6)}`, join(values.out, "contact.png"));
  const phone = sheet(video, `fps=1,scale=360:-2,tile=${grid(1, 5)}`, join(values.out, "phone.png"));
  const stripPaths = strips.map(({ label, seconds }) => {
    const start = Math.round(seconds * info.fps);
    return sheet(video, `select='between(n\\,${start}\\,${start + 11})',scale=320:-2,tile=12x1`, join(values.out!, `strip-${label}.png`));
  });

  const paths = { contact, phone, strips: stripPaths };
  return { code: 0, asJson: !!values.json, json: paths, human: [contact, phone, ...stripPaths].join("\n") };
});
