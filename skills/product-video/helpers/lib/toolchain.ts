// Heavy dependencies live outside the skill dir, which is symlinked into every
// runtime root. setup-scene.sh fills this dir; helpers import from it by path.
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

export function toolchainDir(): string {
  return process.env.PRODUCT_VIDEO_TOOLCHAIN || join(homedir(), ".local", "state", "product-video", "toolchain");
}

export class ToolchainMissing extends Error {}

type Playwright = typeof import("playwright");

export async function loadPlaywright(): Promise<Playwright> {
  const dir = toolchainDir();
  const entry = join(dir, "node_modules", "playwright", "index.mjs");
  if (!existsSync(entry)) {
    throw new ToolchainMissing(`playwright not installed in ${dir}; run helpers/setup-scene.sh`);
  }
  // Browsers sit beside the package so the global ms-playwright cache is never consulted.
  process.env.PLAYWRIGHT_BROWSERS_PATH = join(dir, "ms-playwright");
  return (await import(entry)) as Playwright;
}
