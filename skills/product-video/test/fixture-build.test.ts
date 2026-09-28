import { afterAll, describe, expect, setDefaultTimeout, test } from "bun:test";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const helper = join(import.meta.dir, "..", "helpers", "fixture-build.ts");
const REPO = join(process.env.HOME ?? "", "gitlab", "openmarket-chat");
const dir = mkdtempSync(join(tmpdir(), "pv-fixture-build-"));
afterAll(() => rmSync(dir, { recursive: true, force: true }));
setDefaultTimeout(180_000);

function run(...args: string[]) {
  const r = Bun.spawnSync(["bun", helper, ...args], { stdout: "pipe", stderr: "pipe" });
  return { code: r.exitCode, stdout: r.stdout.toString(), stderr: r.stderr.toString() };
}

function porcelain(): string {
  return Bun.spawnSync(["git", "-C", REPO, "status", "--porcelain"]).stdout.toString();
}

const haveRepo = existsSync(join(REPO, "tools", "visual", "shell-fixture.html"));
const cleanBefore = haveRepo && porcelain() === "";
if (!haveRepo) console.warn(`fixture-build: skipping the OM Chat build, ${REPO} is absent`);
else if (!cleanBefore) console.warn(`fixture-build: skipping the OM Chat build, ${REPO} is dirty before the test`);

describe("fixture-build.ts", () => {
  test.skipIf(!cleanBefore)("builds the unchanged shell fixture outside the repo and leaves it clean", () => {
    const out = join(dir, "shell");
    const r = run("--repo", REPO, "--fixture", "shell", "--out", out, "--json");
    expect(r.stderr).not.toContain("error");
    expect(r.code).toBe(0);
    const { root, entry } = JSON.parse(r.stdout);
    expect(entry).toBe("shell-fixture.html");
    expect(root.startsWith(out)).toBe(true);

    // base "/" : the entry loads its module from /assets, and that file was built.
    const html = readFileSync(join(root, entry), "utf8");
    const src = html.match(/<script[^>]*type="module"[^>]*src="([^"]+)"/)?.[1] ?? "";
    expect(src.startsWith("/assets/")).toBe(true);
    expect(existsSync(join(root, src))).toBe(true);

    expect(porcelain()).toBe("");
  });

  test("usage and environment errors exit 2", () => {
    expect(run().code).toBe(2);
    const notARepo = join(dir, "not-a-repo");
    mkdirSync(notARepo, { recursive: true });
    writeFileSync(join(notARepo, "README"), "");
    expect(run("--repo", notARepo, "--fixture", "shell", "--out", join(dir, "x")).code).toBe(2);
  });

  test.skipIf(!haveRepo)("an unknown fixture name and an --out inside the repo exit 2", () => {
    expect(run("--repo", REPO, "--fixture", "no-such", "--out", join(dir, "y")).code).toBe(2);
    expect(run("--repo", REPO, "--fixture", "shell", "--out", join(REPO, "dist-pv")).code).toBe(2);
    expect(existsSync(join(REPO, "dist-pv"))).toBe(false);
  });
});
