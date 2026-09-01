---
name: codex-first
description: "Route implementation work to Codex; Claude specs, reviews, verifies. Use the codex plugin (/codex:rescue, /codex:review) as the primary path, raw codex exec as fallback."
---

# Codex First

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a task, ignore this skill. Do the work yourself; a subagent must never re-delegate to Codex.
</SUBAGENT-STOP>

Claude Code main sessions only. Codex/other harnesses: skip; never self-delegate.

This is the L2 dispatch contract: exactly how a piece of work Claude has
already decided to hand off becomes a Codex run. `$clanker-agentic-loop` calls
this skill for phase 2 (Dispatch) of every goal cycle; it applies just the
same for ordinary, non-loop delegations.

Rationale: Claude (Fable/Opus) tokens metered + expensive; Codex flat-rate. GPT-5.5+ is usually the better and faster model at writing/implementing code; Claude wins at ergonomics — judgment, design, spec-writing, review, orchestration. So Codex types, Claude thinks and verifies.

Inside `$clanker-agentic-loop`, the handoff decision is already made: invoking
the loop is the Codex-handoff decision, and the loop dispatches straight
into the route below for every goal. For ordinary, non-loop work, the
plan→execution gate in the user's CLAUDE.md still applies — ask before
routing here.

## Route

Delegate to Codex (default for hands-on work):

- implementation from a frozen spec; refactors; mechanical migrations
- bug fixes with known repro; test writing; coverage fills
- CI fixes, dependency bumps, scripts/tooling
- bulk codebase exploration where raw reading ≫ the answer

Keep in Claude — design judgment, plus the exact exceptions
`$clanker-agentic-loop`'s validation-ownership table states, so the two files
cannot disagree:

- design, API design, architecture, naming, UX judgment
- tasks where writing the spec IS the work (ambiguity = design)
- a tiny edit (~<20 lines, single obvious change)
- dependent on session-only tools (MCP browser/computer-use, secrets)
- a git mutation, release, push, or other destructive operation
- review and validation of any kind

## The spec lives in dev-notes — point Codex at it (REQUIRED)

Plans/specs live in the shared control center `~/Documents/dev-notes/<task-slug>/` (per global CLAUDE.md), NOT in the repo. Codex starts with zero context, so **every handoff prompt MUST open by telling Codex the exact docs folder and which files to read first.** Never hand off without this — a prompt that omits the doc paths is incomplete.

- Name the **absolute folder**, not just one file: `~/Documents/dev-notes/<task-slug>/` — so Codex can read the design, spec, and plan together for context.
- Call out the specific files to read in order, e.g. "Read `~/Documents/dev-notes/<task>/<...>-design.md` and `<...>-plan.md` first, then implement the plan. Do not start coding before reading them."
- Cross-layer work: point Codex at the same folder from each repo run; the plan is the shared source of truth across FE/BFF/backend.
- Keep the handoff prompt itself as `codex-handoff-prompt.md` in that folder for reuse and audit.

Template opening line for any Codex prompt (plugin or CLI):

```
Read the docs in ~/Documents/dev-notes/<task-slug>/ first — start with <design>.md and <plan>.md. Do not write any code until you have read them. Then implement the plan in <repo path>.
```

## Goal-contract handoff (dispatch from `$clanker-agentic-loop`)

When `$clanker-agentic-loop` dispatches a goal here, the prompt carries the
dev-notes pointer above plus these goal-specific fields, unchanged from the
loop's dispatch contract:

- Goal ID
- Ordinal/total
- Success criteria (deterministic)
- Current attempt and attempt limit
- Path to `<taskFolder>/goals/G<n>-contract.md` — the goal's contract
  (outcome, in-scope, non-goals, exact validation commands, allowed writes,
  worktree path, commit policy, required report shape); Codex must read it
  before writing any code.

This is additive to the dev-notes pointer requirement above, never a
replacement for it.

## Kiyotaka stack

Codex starts with zero session context — always give it the exact repo path
and layer. For the Kiyotaka stack, do not re-derive the repo list here: read
`$clanker-agentic-loop`'s profile at
`/Users/dboon/Documents/dev-notes/agents/clanker-agentic-loop/profiles/kiyotaka.md`,
which carries the four repo paths and the order they must land in. For any
other stack, name the repo's absolute path and its layer explicitly in the
prompt.

## Invoke — plugin path (default, current repo)

The `codex@openai-codex` plugin owns delegation for the repo the session is in: background job tracking, resume, result storage. Prefer it over hand-rolled CLI calls.

**Delegate work** — invoke the `codex:rescue` command with the full spec as args:

- `/codex:rescue <spec>` — write-capable by default; Codex may run commands/tests. House mode is full-auto (workspace-write sandbox): pass the sandbox flags if the plugin exposes them; never sandbox-off unless the user names it
- `--background` for anything non-trivial (most delegations); `--wait` only for quick jobs
- `--model gpt-5.6-sol --effort high` — house defaults; pin them, don't rely on Codex defaults
- `--resume <follow-up>` — continue the last rescue thread; cheaper than fresh runs, keeps context. After two failed resume rounds within the same attempt, stop resuming and have Claude complete the work directly.
- `--fresh` — force a new thread when the last one is a dead end

**Manage jobs:** `/codex:status` (progress), `/codex:result` (final output + session id), `/codex:cancel` (kill a runaway).

**Codex as reviewer** (supplements, never replaces, Claude's own review). The
om families — `$om-chat-feature`, `$clanker-agentic-loop`, `$om-mobile-feature` —
have cross-model review switched **off**: they run Claude's review only, and a
Codex pass happens there just when the operator asks for it by name. Outside
those families the commands below are ordinary tools:

- `/codex:review [--base <ref>] [--background]` — read-only review of uncommitted changes or branch vs base
- `/codex:adversarial-review [--base <ref>] <focus>` — steerable challenge review; use before shipping risky work to pressure-test design, races, rollback, data loss

**Session handoff:** `/codex:transfer` — convert the current Claude session into a persistent Codex thread when the user wants to continue in Codex directly.

## Invoke — raw CLI (fallback)

Use when the plugin can't: a different directory than the session's (`-C` — this includes every feature worktree, so it is the normal case for loop dispatch), or parallel runs across repos. Prompt via temp file, never inline quoting:

```bash
P=$(mktemp); cat >"$P" <<'EOF'
Read the docs in ~/Documents/dev-notes/<task-slug>/ first — start with <design>.md and <plan>.md; do not write code until you have.
<goal, repo + key paths, constraints ("don't touch X"), non-goals, proof expected, output shape>
EOF
command codex exec -C <worktree> -o /tmp/codex-last.md - <"$P" 2>/tmp/codex-last.err
```

**Do not pin sandbox, approval, model, or effort flags.** The operator's
`~/.codex/config.toml` already sets `approval_policy = "never"`,
`sandbox_mode = "danger-full-access"`, `model = "gpt-5.6-sol"`, and
`model_reasoning_effort = "xhigh"` (verified 2026-08-12; re-read that file rather
than trusting this line if behaviour surprises you). Their default is
deliberately permissive, so overriding it only narrows what Codex can do — the
usual symptom being a worker that cannot write artifacts outside the repo.
Because the sandbox is full-access, Codex writes evidence straight to the run's
external evidence root; there is no need for an in-repo `.artifacts/` staging
directory.

Deviate only to be *more* restrictive for a specific reason, and say why in the
prompt. `-s/--sandbox <read-only|workspace-write|danger-full-access>` is the flag
for that.

- **`--full-auto` does not exist on `codex exec`.** codex-cli 0.147.0 rejects it
  outright (`error: unexpected argument '--full-auto' found`). Older notes and
  habits still reach for it; they are wrong. `--yolo` is likewise not an
  `exec` flag — full access comes from the config default above.
- **Capture stderr to a file, never `/dev/null`.** Codex prints its startup
  banner, session id, and every fatal argument error on stderr. Discarding it
  turns a flag error into a silent no-op that looks like a hung worker: the
  process exits instantly, `-o` is never written, and nothing says why. Keep
  `2>/tmp/codex-last.err` and read it when a run produces no result.
- The session id appears in that stderr banner — record it as the goal's
  `codexThread` so a follow-up can `resume` the same thread.
- read the `-o` file for the result; don't parse the JSONL stream
- long runs: Bash run_in_background, read `-o` file on exit; don't kill quiet runs <30 min
- **`nohup … &` inside a background Bash call returns immediately.** The harness
  reports that wrapper as exited while Codex keeps running, so never read
  "completed" as "Codex finished" — confirm with `pgrep -f 'codex exec'` and by
  the `-o` file existing.
- parallel independent tasks OK: separate worktrees, separate `-o` files
- outside a git repo add `--skip-git-repo-check`

Follow-up fixes: `resume` has no `-C`, so run it from the target directory. It
inherits the same config defaults, so it needs no mode flags either:

```bash
(cd <worktree> && command codex exec resume --last \
  -o /tmp/codex-last.md - <"$P2" 2>/tmp/codex-last.err)
```

## Prompt contract

**Every implementation prompt must state the test-first rule.** Codex writes the
failing test first, shows it failing, then implements. Name the contract's
failing test and its level, tell Codex to follow the repository's existing test
convention, and tell it never to create a `*.spec.*` file. A dispatch that omits
this gets implementation-first code back, and the TDD order cannot be
reconstructed afterwards.

Codex starts with zero session context. Every prompt: **the dev-notes docs folder + which files to read first** (required — see above), goal, exact repo/paths (see Kiyotaka stack above), constraints, non-goals, proof expected (exact test command), output shape ("report files changed + test output"). Spec quality decides success. Applies identically to `/codex:rescue` args and raw CLI prompts.

## Verify

Validation and review ownership belong to `$clanker-agentic-loop`'s
validation-ownership table, not to this skill — see
`/Users/dboon/Documents/dev-notes/agents/clanker-agentic-loop/SKILL.md` for what
Claude runs directly versus what Codex output only advises. This skill
governs dispatch, not verification.

## Economics

Win = generation + exploration tokens moved to Codex; Claude spends only on spec + diff review. Don't ping-pong trivia through delegation; don't re-read what Codex already summarized.
