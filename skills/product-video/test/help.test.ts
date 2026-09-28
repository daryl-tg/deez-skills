import { describe, expect, setDefaultTimeout, test } from "bun:test";
import { readdirSync } from "node:fs";
import { join } from "node:path";

const helpers = join(import.meta.dir, "..", "helpers");
setDefaultTimeout(30_000);

function run(file: string, flag: string) {
  const r = Bun.spawnSync(["bun", join(helpers, file), flag]);
  return { code: r.exitCode, stdout: r.stdout.toString() };
}

describe("--help", () => {
  // Discovered, not listed, so a new helper cannot ship without help.
  const files = readdirSync(helpers).filter((f) => f.endsWith(".ts")).sort();

  test("every TypeScript helper prints usage and a description, then exits 0", () => {
    expect(files).toContain("scene.ts");
    expect(files).toContain("fixture-build.ts");
    for (const file of files) {
      for (const flag of ["--help", "-h"]) {
        const r = run(file, flag);
        expect({ file, flag, code: r.code }).toEqual({ file, flag, code: 0 });
        expect(r.stdout).toContain(`usage: bun helpers/${file}`);
        // A description after the usage line, not the usage alone.
        expect(r.stdout.trim().split("\n").length).toBeGreaterThan(2);
      }
    }
  });

  test("scene.ts documents every scene.json field", () => {
    const { stdout } = run("scene.ts", "--help");
    for (const field of ["root", "entry", "query", "viewport", "width", "height", "dpr", "fps", "duration",
      "removeClasses", "routes", "path", "status", "body", "contentType", "triggers", "click", "role", "name"]) {
      expect(stdout).toMatch(new RegExp(`"${field}"`));
    }
  });
});
