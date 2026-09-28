// Shared ffmpeg plumbing for the check helpers. Exit codes follow the contract:
// 0 pass, 1 a real finding, 2 usage or environment error.
import { existsSync } from "node:fs";
import { parseArgs, type ParseArgsConfig } from "node:util";

export class UsageError extends Error {}

export interface Run {
  code: number;
  stdout: string;
  stderr: string;
}

export function run(cmd: string[]): Run {
  let r;
  try {
    r = Bun.spawnSync(cmd, { stdout: "pipe", stderr: "pipe" });
  } catch {
    throw new UsageError(`${cmd[0]} not found on PATH`);
  }
  return { code: r.exitCode ?? 1, stdout: r.stdout.toString(), stderr: r.stderr.toString() };
}

// A decode failure is an environment problem, never a finding.
export function mustRun(cmd: string[]): Run {
  const r = run(cmd);
  if (r.code !== 0) {
    const tail = r.stderr.trim().split("\n").slice(-3).join("\n");
    throw new UsageError(`${cmd[0]} failed (${r.code}): ${tail}`);
  }
  return r;
}

export function ffmpeg(args: string[]): Run {
  return mustRun(["ffmpeg", "-hide_banner", "-nostdin", ...args]);
}

export function requireFile(path: string | undefined, what: string): string {
  if (!path) throw new UsageError(`missing ${what}`);
  if (!existsSync(path)) throw new UsageError(`${what} not found: ${path}`);
  return path;
}

export interface VideoInfo {
  width: number;
  height: number;
  fps: number;
  frames: number;
  duration: number;
}

// Counting packets reads the container without decoding, so it stays cheap on long renders.
export function probeVideo(path: string): VideoInfo {
  const r = mustRun([
    "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
    "-show_entries", "stream=width,height,r_frame_rate,nb_read_packets,duration:format=duration", "-of", "json", path,
  ]);
  const parsed = JSON.parse(r.stdout);
  const s = parsed.streams?.[0];
  if (!s) throw new UsageError(`no video stream in ${path}`);
  const [num, den] = String(s.r_frame_rate).split("/").map(Number);
  const fps = num / (den || 1);
  const frames = Number(s.nb_read_packets);
  // Some containers omit stream duration; the format's is the next best.
  const duration = Number(s.duration ?? parsed.format?.duration ?? frames / fps);
  return { width: s.width, height: s.height, fps, frames, duration };
}

export function parse<T extends NonNullable<ParseArgsConfig["options"]>>(options: T) {
  // parseArgs reads "-14" as a flag, but the interfaces take `--i -14`; bind negative numbers to their option.
  const args: string[] = [];
  const argv = Bun.argv.slice(2);
  for (let k = 0; k < argv.length; k++) {
    const name = argv[k].startsWith("--") && !argv[k].includes("=") ? argv[k].slice(2) : "";
    if (options[name]?.type === "string" && /^-\.?\d/.test(argv[k + 1] ?? "")) args.push(`${argv[k]}=${argv[++k]}`);
    else args.push(argv[k]);
  }
  try {
    return parseArgs({ args, options, allowPositionals: true, strict: true });
  } catch (e) {
    throw new UsageError((e as Error).message);
  }
}

// Help wins over every other argument, so a half-typed command can still ask for it.
export function exitOnHelp(usage: string, description: string): void {
  const args = Bun.argv.slice(2);
  if (!args.includes("--help") && !args.includes("-h")) return;
  console.log(`usage: ${usage}\n\n${description.trim()}`);
  process.exit(0);
}

// One JSON object on stdout with --json, a short human report otherwise.
export function main(
  usage: string,
  description: string,
  body: () => { code: 0 | 1; json: unknown; human: string; asJson: boolean },
): never {
  exitOnHelp(usage, description);
  try {
    const { code, json, human, asJson } = body();
    console.log(asJson ? JSON.stringify(json) : human);
    process.exit(code);
  } catch (e) {
    if (e instanceof UsageError) {
      console.error(`${e.message}\nusage: ${usage}`);
      process.exit(2);
    }
    throw e;
  }
}
