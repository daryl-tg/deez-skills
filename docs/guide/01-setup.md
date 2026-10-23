# 1. Setup

The [README](../../README.md#install) has the commands. This
chapter is what they mean and what to check.

## What "installed" means

Nothing is copied. `bin/link --apply` creates symlinks from the runtimes' skill
directories into this repo:

```
~/.claude/skills/clanker-mode        -> ~/github/deez-skills/skills/clanker-mode
~/.codex/skills/principle-*     -> ~/github/deez-skills/skills/principle-*
```

So editing a skill through either path edits the repo, and `git status` sees it.
That is the whole point: one copy, two runtimes, no drift.

## Why the interpreter probe exists

`registry.toml` needs a real TOML parser. Hand-rolling one in shell on the file
that decides what gets symlinked into two runtimes is a correctness risk not
worth taking, so the tooling is Python and needs `tomllib`, which means 3.11+.

macOS ships 3.9. `bin/deez` therefore probes for a capable interpreter rather
than assuming `python3` is one, and fails loudly with the remedy if none exists.
This matters because device parity is the point of the repo: a hub that works on
one machine and mysteriously does not on another is worse than no hub.

## Read the plan before applying

`bin/link` with no flags never touches disk. The verb on each line tells you
what happens to whatever is at the destination now. The two worth pausing on:

- **`backup`** — something real is there and it **differs**. It gets moved to
  `~/.local/state/deez-skills/<stamp>/`, not deleted. If you see many of these
  on a machine you thought was clean, stop and look at one first.
- **`missing-source`** — a registry entry with no folder. This blocks the entire
  apply rather than skipping the entry, because a partial install is harder to
  reason about than none.

## Verify against the runtime, not the filesystem

`bin/doctor` proves the symlinks are right. It cannot prove a runtime *loaded*
them, because Claude Code reads its skill directory at session start.

So: restart, then check. `$clanker-mode` should resolve in Claude Code. Codex
support is dormant, so there is no routine Codex check.

If a skill is missing, check the frontmatter `name` matches the install name.
The runtimes resolve their catalogues by that field, so a mismatch makes a skill
invisible even when the symlink is perfect. `bin/doctor`
checks this, which is why it exists as a check at all.

Next: [The router](./02-the-router.md).
