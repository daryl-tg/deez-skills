# Migration status

## Done

| Source | What happened |
|---|---|
| `dev-notes/agents/om-chat` | Adopted whole |
| `dev-notes/agents/om-chat-design-system` | Adopted whole |
| `dev-notes/agents/om-super-reaction` | Adopted whole |
| `dev-notes/agents/codex-first` | Adopted whole |
| `dev-notes/agents/herdr-codex-orchestration` | Adopted whole. Arena and swarm become named modes inside it |
| `dev-notes/agents/writing-simplified-technical-english` | Adopted whole. `writing-docs` routes agent-facing work to it |
| `dev-notes/agents/om-chat-feature` | **Dissolved.** 214 lines became `clanker-mode/playbooks/om-chat-feature.md` plus `references/om-chat-boundaries.md` |
| `dev-notes/agents/om-mobile-feature` | **Dissolved.** 343 lines became `clanker-mode/playbooks/om-mobile-feature.md` plus `references/openfloor-lane.md` |
| `dev-notes/agents/om-*-completion` | **Dissolved** into `clanker-mode/playbooks/om-chat-completion.md` and `om-mobile-completion.md` |
| `dev-notes/agents/om-*-loop` | **Dissolved** into `clanker-mode/playbooks/agentic-loop.md` |
| `dev-notes/agents/om-agentic-loop`, `-stub` | **Retired.** A loop is a playbook, not a second router |
| `dev-notes/agents/clanker-agent-polish` | **Retired.** Evidence contract moved to the terminal gate and `control-<app> evidence publish`; the audit checklist belongs with `om-chat-design-system` |
| `dev-notes/agents/delivery-contract` | **Retired.** Superseded by `principle-rebase-pr-squash`, `principle-one-commit-lands`, `principle-promote-to-the-main-worktree`, and `playbooks/opening-a-review.md` |

Five descriptions arrived over the 300-character limit and were trimmed:
`om-super-reaction` was 505.

**Originals are untouched.** `bin/adopt` copies. Nothing under
`dev-notes/agents` or `skillz` was modified or deleted.

## The clean install, 2026-09-01

Both runtime skill directories were emptied and relinked to the hub alone.

**Everything was archived first**, byte-identical and verified before anything
was removed:

```
/Users/dboon/.local/state/deez-skills/pre-migration/20260901-153647/
  claude/   28 real directories + SYMLINKS.txt (42 recorded)
  codex/    49 real directories + SYMLINKS.txt (20 recorded)
```

The 77 real directories are the skills with **no upstream anywhere** — the
`cmux-*` family, the Go and shell toolchain, `gcx`, `logcli`, `kolint`,
`stackctl`, `tsdbctl`, `mailbox`, `pi-development`. They exist only in that
archive now. Adopt any of them with:

```bash
bin/adopt /Users/dboon/.local/state/deez-skills/pre-migration/20260901-153647/claude/<name> --category <cat>
```

Symlinks were recorded rather than copied, since their targets survive.

**Result:** `~/.claude/skills` 57 entries, `~/.codex/skills` 56, every one of
them pointing into the hub. `bin/doctor`: 0 failures, 0 warnings.

**Left alone deliberately:** `~/.claude/agents` still carries the five subagent
roles from `dev-notes/agents/claude-agents`. The hub does not own them, they are
not collisions, and the playbooks' role routing depends on them.

**Now absent until their owners reinstall:** the 14 vendored skills from
`~/.agents/skills` (`animate`, `agent-browser`, `write-swift` and the rest), and
`openmarket`. Their sources are untouched; re-link or re-fetch when wanted.

## The dev-notes resurrection, 2026-09-01

Hours after the clean install, 16 dev-notes symlinks reappeared and shadowed the
hub. Six hub-owned skills were being ignored, and nine retired skills were back
competing with `clanker-mode`'s playbooks. `create-verification-skill` also
wrote its output into `dev-notes/agents/verify-om-chat` and registered it in
`install-matrix.tsv`.

**Cause:** `~/.claude/CLAUDE.md` still named `dev-notes/agents` as the canonical
skill source and `tools/skills-install.sh` as the tooling. A session read that
and did exactly what it said. The pointer was the last migration item and had
not been done, so the cutover was undone by following the instructions.

**Fixed by:**

1. `verify-om-chat` adopted into the hub, with its five feature files and
   helper.
2. `install-matrix.tsv` neutralised — all 17 rows commented out, with a header
   saying why running the old installer shadows the hub.
3. All 32 dev-notes symlinks removed from both runtimes, sources untouched.
4. `bin/link --apply` re-run.
5. `~/.claude/CLAUDE.md` rewritten to name the hub as canonical, state that
   dev-notes is retired as a skill source, and say where a generated skill
   belongs. Stale references to `$om-agentic-loop` and `$delivery-contract`
   replaced with the playbook and principles that superseded them. Backup kept
   alongside.

**Lesson worth keeping:** a migration is not finished while a pointer still
names the old source. The instructions are part of the system.

## Not started

**Linking.** The hub is not installed. `~/.claude/skills` and `~/.codex/skills`
still point at the old sources. `bin/doctor` reports this as `unlinked`, which
is informational until at least one entry resolves into the hub.

**The remaining skillz skills.** `bump-rc`, `demuddy`, `graphify`, `humanize`,
`ivtg`, `llm-council`, `loop-me-in`, `om-build`, `prompt-ready`, `syncup`,
`testing-harness`, `war-diary`. Adopt with
`bin/adopt ~/github/skillz/claude/skills/<name> --category <cat>`.

`openmarket` and `om-chat` in skillz are vendored from the `om` CLI and
self-update. They belong in `vendor.toml`, not `skills/`.

**The 51 orphans** in `~/.claude/skills` and `~/.codex/skills` with no upstream.
`bin/doctor` lists every one as a warning.

**Third-party.** Twelve of the fourteen `~/.agents/skills` entries still need
recording in `vendor.toml`.

## Order of operations

1. Adopt the remaining sources. `bin/doctor` after each.
2. `bin/link` with no flags and read the plan. Expect `adopt` where the live
   directory already matches and `backup` where it differs.
3. `bin/link --apply` on one machine. Verify both runtimes still see every skill
   by name, and that `$clanker-mode` resolves.
4. Retire the old source and its installer.
5. **Only then** `bin/hook-install`, and remove the skillz `PostToolUse` hook in
   the same change. Never both: they race over edits made through the same
   symlinks and commit to different repos.
6. Update `~/.claude/CLAUDE.md`, which still names `dev-notes/agents` as
   canonical, `tools/skills-*.sh` as the tooling, and `$clanker-agent-polish` as a
   skill to load.

## Known follow-ups

- `humanize`'s voice profile is Ryan's, not Daryl's. Run `automate-me` to
  rebuild it, and empty `references/voice.md` rather than leaving a stale
  profile as a fallback.
- `bin/adopt` copies and does not rewrite the live symlink. Step 3 above does
  that.
- `~/Documents` resolves through iCloud, so `dev-notes` paths realpath to
  `~/Library/Mobile Documents/com~apple~CloudDocs/...`. Harmless, but the hub
  must not depend on it: keep skills in `~/github/deez-skills`.
