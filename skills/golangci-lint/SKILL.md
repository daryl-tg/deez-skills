---
name: golangci-lint
description: >-
  Go lint setup and configuration: rules, .golangci.yml,
  project wiring, or linter failures.
---
## Scope

Use this workflow to install, configure, or tune
`golangci-lint` for a Go project.

Not for general style advice outside the
`golangci-lint` toolchain.

## Workflow

1. Check the installed version first. Config syntax
   differs between major versions.
2. Read the raw upstream reference before editing the
   config.
3. Start from a small, explainable config that matches
   the project's tolerance for noise.
4. Run the linter, then disable or tune only the
   linters that are not earning their keep.
5. If using `--fix`, re-run `go build` and tests after
   the fix pass.

## Rules

- Make config syntax match the installed version.
- Prefer explicit comments for disabled linters.
- Do not cargo-cult a huge config without checking
  what each setting buys you.
- Keep formatter and linter choices intentional.
- Re-verify imports and buildability after automated
  fixes.

## Reference map

Read [reference.md](references/reference.md) for:

- raw upstream reference URLs
- install command and version notes
- v2 config structure and example settings
- run and fix commands
