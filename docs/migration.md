# Migration — not yet started

The framework is deliberately inert. `registry.toml` has no entries, nothing is
linked, and no file outside this repo has been touched. `bin/link --apply` and
`bin/hook-install` have never been run.

## Sources to bring in

| Source | Count | Action |
| --- | --- | --- |
| `~/github/skillz/{claude,codex}/skills` | 15 | `bin/adopt` each, then retire the repo |
| `~/Documents/dev-notes/agents/*` | 14 skills + 5 subagents | `bin/adopt`, then retire `install-matrix.tsv` and `skills-install.sh` |
| `~/.agents/skills` | 14 | Record in `vendor.toml`; never vendor the files |
| Orphans in `~/.claude/skills`, `~/.codex/skills` | 51 | Decide per skill; `bin/doctor` lists every one |

## Third-party still to record in vendor.toml

`animate` and `agent-browser` are in place. Remaining 12: `animate-expo`,
`animation-vocabulary`, `review-animations`, `improve-animations`,
`find-animation-opportunities`, `apple-design`, `emil-design-eng`,
`ask-sonner`, `pick-ui-library`, `prototype`, `write-swift`, `find-skills`.

## Known follow-ups

- `bin/adopt` copies and leaves the original in place. Migration adds the step
  that runs `bin/link --apply` and retires the superseded source.
- The `vendor-drift` doctor warning is not implemented yet — it needs a fully
  populated `vendor.toml` to check against `~/.agents/.skill-lock.json`.
- `openmarket` and `om-chat` in skillz are vendored from the `om` CLI, not
  hand-authored. They belong in `vendor.toml`, not `skills/`.
- `prompt-ready` exists twice today: the skillz Claude copy and an orphan Codex
  copy. Pick one before adopting.
- `~/.claude/CLAUDE.md` still names `dev-notes/agents` as canonical and
  `tools/skills-*.sh` as the tooling. Update it in the same change that retires
  those.
- `bin/hook-install` has never been run. Run it once, on one machine, after the
  first successful `bin/link --apply`.

## Order of operations

1. `bin/adopt` every skill from one source; `bin/doctor` after each source.
2. `bin/link` (no `--apply`) and read the plan. Expect `adopt` verbs where the
   live directory already matches, `backup` where it differs.
3. `bin/link --apply` on one machine. Verify both runtimes still see every
   skill by name.
4. Retire the old source and its installer.
5. Only then, `bin/hook-install`.
