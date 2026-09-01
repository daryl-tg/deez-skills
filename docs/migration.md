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

> **Correction, 2026-09-01 (later).** That archive path was **absent** when the
> sole-source cutover below re-checked it — `~/.local/state/deez-skills` did not
> exist at all. So "they exist only in that archive now" was not true of any
> directory, and this section read as a licence to delete originals that had no
> backup. A fresh archive was taken and verified byte-identical before anything
> was removed:
>
> ```
> /Users/dboon/.local/state/deez-skills/pre-migration/20260901-154913
>   claude/   5 real directories + SYMLINKS.txt (55 recorded)
>   codex/   27 real directories + SYMLINKS.txt (31 recorded)
> ```
>
> Nothing in this doc should be trusted as a statement about the filesystem
> without checking the filesystem.

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

## The sole-source cutover, 2026-09-01

The hub is now the only source of skills. `bin/doctor`: 0 failures.

**Adopted: 59 skills**, taking every remaining source tree with it.

| Was | Count | Now |
|---|---|---|
| `~/repos/llm/skills` | 23 | hub-owned |
| `~/Github/skillz` | 12 | hub-owned |
| No upstream anywhere | 22 | hub-owned (20 `cmux-*`, `hatch-pet`, `adhd`) |
| `~/Documents/dev-notes/skills` | 3 | hub-owned |

Two categories were added for the intake: `go` (the Go toolchain, 6) and `cmux`
(20, Codex-only). Both sit outside the `lean` profile, which is the point of
having them.

**Recorded, not adopted.** `gcx` is a Claude *plugin* — four nested skills and a
`.claude-plugin` manifest, vendored from `gcx agent skills` — so adopting it
would fork a generated tree. It went to `vendor.toml`, which now has 17 entries.

**Deleted: the 5 dissolved skills.** `om-chat-feature`, `om-chat-feature-completion`,
`om-mobile-feature`, `-completion`, `-loop` were still live and shadowing the
`clanker-mode` playbooks that replaced them. Removed from both runtimes, each
real directory checked against the archive first. Worth a spot-check: 218 lines
of playbook now carry what was 1050+ lines of skill.

**`graphify` forks per runtime.** Claude dispatches with the Agent tool, Codex
with `spawn_agent`/`wait_agent`. Rather than pick one, the Codex copy lives at
`skills/graphify.codex` and the entry carries
`variant = { codex = "skills/graphify.codex" }`.

**`port-designer-ui` had diverged.** The Codex copy was newer and richer (118
lines, plus an `agents/` directory) than the dev-notes one (67 lines). Adopted
the Codex copy and carried `TEAM-SHARE.md` over from the other.

**Result**

| | claude | codex |
|---|---|---|
| Resolving into the hub | 97 | 107 |
| Vendored (recorded in `vendor.toml`) | 13 | 2 |
| Unmanaged | **0** | **0** |
| Broken links | 0 | 0 |

**What the check learned.** Adoption surfaced six `local-merge` failures that
were all regex artifacts, so the check was tightened rather than the skills
bent around it. The rule is now the *ref being merged*, not the flag:
`git merge-base`/`-tree`/`-file` is plumbing; a merge naming `origin/*` or
`upstream/*` is a branch catching up to its own remote or a vendored fork
syncing from what it forked. A merge naming no such ref is a landing whatever
flags it carries, so `git merge --ff-only` onto main still fails. The existing
118 tests pin both directions.

**Cost of carrying everything.** `bin/doctor` reports the aggregate, and the
`full` profile is not free:

```
claude: 49 visible ~2672 tok every session, 49 routed ~2504 tok not paid
codex: 107 visible ~5583 tok every session
```

Codex has no `disable-model-invocation`, so every hub skill is visible there and
the 20 `cmux-*` are ~1k of that. The `lean` profile, or a `cmux`-less profile,
is the lever if that gets uncomfortable.

## Still open

**`bin/hook-install` has not been run.** When it is, remove the skillz
`PostToolUse` hook in the same change. Never both: they race over edits made
through the same symlinks and commit to different repos.

**`~/.claude/agents`** still carries the five subagent roles from
`dev-notes/agents/claude-agents`. The hub does not own them, they are not
collisions, and the playbooks' role routing depends on them.

## Known follow-ups

- `humanize`'s voice profile is Ryan's, not Daryl's. Run `automate-me` to
  rebuild it, and empty `references/voice.md` rather than leaving a stale
  profile as a fallback.
- `bin/adopt` copies and does not rewrite the live symlink; `bin/link --apply`
  does that. `bin/link` never prunes, either — an entry it does not own is left
  alone, so removing a stale one is a separate deliberate step.
- `~/Documents` resolves through iCloud, so `dev-notes` paths realpath to
  `~/Library/Mobile Documents/com~apple~CloudDocs/...`. Harmless, but the hub
  must not depend on it: keep skills in `~/github/deez-skills`.
