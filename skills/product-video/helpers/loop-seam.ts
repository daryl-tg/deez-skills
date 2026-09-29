// A looping clip jumps visibly at the seam unless its last frame matches its first.
import { ffmpeg, main, parse, probeVideo, requireFile, UsageError } from "./lib/ffmpeg.ts";

const usage = "bun helpers/loop-seam.ts <video> [--min 0.98] [--json]";
const description = `
Scores the loop seam: ffmpeg SSIM (all planes, YUV) between the first and
last frames, both selected by index.
--min  pass bar (default 0.98).
Exit 0 at or above --min; 1 below; 2 on usage or decode errors.
`;

main(usage, description, () => {
  const { values, positionals } = parse({ min: { type: "string" }, json: { type: "boolean" } });
  const video = requireFile(positionals[0], "<video>");
  const min = values.min === undefined ? 0.98 : Number(values.min);
  if (!Number.isFinite(min)) throw new UsageError(`bad --min: ${values.min}`);

  const lastFrame = probeVideo(video).frames - 1;
  if (lastFrame < 1) throw new UsageError(`${video} has fewer than two frames`);
  // Zero both timestamps so ssim pairs the two frames instead of waiting on pts.
  const { stderr } = ffmpeg([
    "-v", "info", "-i", video, "-i", video,
    "-filter_complex", `[0:v]select=eq(n\\,0),setpts=0[a];[1:v]select=eq(n\\,${lastFrame}),setpts=0[b];[a][b]ssim`,
    "-f", "null", "-",
  ]);
  const m = stderr.match(/SSIM .*All:([\d.]+)/);
  if (!m) throw new UsageError("ffmpeg ssim printed no score");
  const ssim = Number(m[1]);
  const pass = ssim >= min;
  return {
    code: pass ? 0 : 1,
    asJson: !!values.json,
    json: { pass, ssim, min, lastFrame },
    human: `${pass ? "seam ok" : "seam jumps"}: frame 0 vs ${lastFrame} SSIM ${ssim.toFixed(4)} ${pass ? ">=" : "<"} ${min}`,
  };
});
