// Render twice, compare decoded frames on every stream, audio included. framemd5
// lines carry pts and duration as well as the hash, so a timing drift counts too.
import { ffmpeg, main, parse, requireFile } from "./lib/ffmpeg.ts";

const usage = "bun helpers/determinism.ts <a.mp4> <b.mp4> [--json]";
const description = `
Decodes both files with ffmpeg framemd5 on every stream (video and audio) and
compares them frame by frame, timestamps included.
Exit 0 if identical; 1 otherwise, naming the first differing stream and frame
and the count of differing frames; 2 on usage or decode errors.
`;

// Frame lines per stream index; framemd5 leads each line with the stream index.
function streamLines(path: string): Map<number, string[]> {
  const out = ffmpeg(["-v", "error", "-i", path, "-map", "0", "-f", "framemd5", "-"]).stdout;
  const streams = new Map<number, string[]>();
  for (const line of out.split("\n")) {
    if (!line.trim() || line.startsWith("#")) continue;
    const index = Number(line.split(",")[0]);
    if (!streams.has(index)) streams.set(index, []);
    streams.get(index)!.push(line.replace(/\s+/g, ""));
  }
  return streams;
}

main(usage, description, () => {
  const { values, positionals } = parse({ json: { type: "boolean" } });
  const a = streamLines(requireFile(positionals[0], "<a.mp4>"));
  const b = streamLines(requireFile(positionals[1], "<b.mp4>"));

  const indices = [...new Set([...a.keys(), ...b.keys()])].sort((x, y) => x - y);
  const streams = indices.map((index) => {
    const la = a.get(index) ?? [];
    const lb = b.get(index) ?? [];
    let firstDiffFrame: number | null = null;
    let diffFrames = 0;
    for (let i = 0; i < Math.max(la.length, lb.length); i++) {
      if (la[i] === lb[i]) continue;
      diffFrames++;
      firstDiffFrame ??= i;
    }
    return { index, a: la.length, b: lb.length, diffFrames, firstDiffFrame };
  });

  const first = streams.find((s) => s.diffFrames > 0);
  const diffFrames = streams.reduce((n, s) => n + s.diffFrames, 0);
  const identical = diffFrames === 0;
  const count = (m: Map<number, string[]>) => [...m.values()].reduce((n, l) => n + l.length, 0);
  return {
    code: identical ? 0 : 1,
    asJson: !!values.json,
    json: {
      identical,
      frames: { a: count(a), b: count(b) },
      diffFrames,
      firstDiffStream: first?.index ?? null,
      firstDiffFrame: first?.firstDiffFrame ?? null,
      streams,
    },
    human: identical
      ? `identical: ${count(a)} frames across ${streams.length} stream(s)`
      : `differ: stream ${first!.index} first differing frame ${first!.firstDiffFrame}, ${diffFrames} differing frames ` +
        `(${streams.filter((s) => s.diffFrames).map((s) => `stream ${s.index}: ${s.diffFrames}`).join(", ")})`,
  };
});
