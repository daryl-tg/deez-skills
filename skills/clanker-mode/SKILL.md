---
name: clanker-mode
description: "Daryl's agent style: routed playbooks, cited principles, proof on the real surface, and delivery by rebase-PR-squash. Use for /clanker-mode, $clanker-mode, or any request for rigorous work on the OM stacks."
disable-model-invocation: true
mode: true
reminder: "New task? Playbook match or rigor needed -> apply $clanker-mode. Casual turn or the operator opts out -> don't."
---

# Clanker mode

## Non-negotiables

**Start every multi-step task with a todo list whose first item is to read the
Principles index below in full.** Name each principle that shaped a decision and
the choice it changed. A citation with no decision behind it means the leaf went
unread.

- Any code change → **principle-failing-test-first**, at the fastest level that
  expresses the behavior.
- Any claim that something works → **principle-prove-on-the-real-surface**.
  Inconclusive is not a pass.
- Before promoting, reviewing, or announcing →
  **principle-visual-approval-gates-delivery**.
- Any server, port, or URL → **principle-bind-assigned-ports**.
- Any spec, plan, or handoff → **principle-planning-docs-live-outside-the-repo**.
- **Any React or Next.js code** → **vercel-react-best-practices**, grounded by
  **principle-model-the-domain** for the data shape and
  **principle-minimize-reader-load** for component boundaries. Its 70 rules are
  ordered by impact: waterfalls and bundle size first, re-render tuning much
  later. Do not start at memoisation.
- **Any motion or interaction feel** → **animate** on web, **animate-expo** on
  Expo. Reviewing existing motion is **review-animations**; auditing a whole
  codebase is **improve-animations**; naming an effect you cannot name is
  **animation-vocabulary**. The craft bar behind all of them is
  **emil-design-eng**, and **apple-design** for gesture and material work.
- Any prose surface, including your own reply → the **unslop** skill. For text
  going out in the operator's name, **humanize** after it.
- About to ask a question whose answer you could observe by running something →
  do not ask. Run it. Reserve questions for genuine preference calls, per
  **principle-never-block-on-reversible-work**.
- Frozen spec or plan → **stop and ask which execution path**. This gate is
  never auto-picked. It is the one carve-out from not blocking.
- Broken skill mid-task → fix it in its own change. Do not block, do not
  silently work around it.

## Principles

Read the leaf in full for any principle you apply. Naming one without a decision
behind it means you skipped reading it.

**Core.** How much to build, and in what order.
`laziness-protocol` · `subtract-before-you-add` · `foundational-thinking` ·
`redesign-from-first-principles` · `outcome-oriented-execution` ·
`exhaust-the-design-space` · `experience-first` · `build-the-lever` ·
`minimize-reader-load`

**Architecture.** What shape the code takes.
`model-the-domain` · `boundary-discipline` · `type-system-discipline` ·
`make-operations-idempotent` · `migrate-callers-then-delete-legacy-apis` ·
`separate-before-serializing-shared-state`

**Verification.** What counts as done.
`prove-on-the-real-surface` · `visual-approval-gates-delivery` ·
`failing-test-first` · `fix-root-causes` · `sequence-verifiable-units` ·
`finish-or-report`

**Delivery.** How work reaches main.
`rebase-pr-squash` · `one-commit-lands` · `feature-branch-isolation` ·
`promote-to-the-main-worktree` · `announce-the-linked-review` ·
`desktop-before-cloud`

**Delegation.** Working with other agents.
`delegate-implementation-review-stays-here` · `never-block-on-reversible-work` ·
`guard-the-context-window` · `todo-discipline`

**Environment and meta.**
`bind-assigned-ports` · `planning-docs-live-outside-the-repo` ·
`encode-lessons-in-structure`

## Which stack owns the work

Match on the repository, not the directory name. Every linked worktree inherits
its repo's row.

| Repository | Family | Playbook |
|---|---|---|
| `openmarket-chat`, `openmarket-chat-cloud`, `packages/rooms-client` | OM Chat | `playbooks/om-chat-feature.md` |
| `openmarket-chat-app` | OM Mobile | `playbooks/om-mobile-feature.md` |
| `kiyotaka-frontend`, `orange-v2-backend`, `tharamine-user-service`, `auth-service-backend`, `orange-shared` | Kiyotaka | Generic flow. No playbook yet |
| Anything else | none | Generic flow |

OM Chat stops at `ready_for_review`. OM Mobile carries through to a squash-merge
through the MR. Neither ever merges locally.

## Delegation

**This skill runs the same on Claude Code and on Codex.** Same playbooks, same
principles, same roles. Only the resolution differs, and the runtime you are in
resolves its own.

Playbook steps name a **role**. Never a model, never a runtime.

| Role | On Claude | On Codex |
|---|---|---|
| **explore** | `Agent(subagent_type: "explore")` | `agent_type: explore` |
| **executor** | `Agent(subagent_type: "executor")` | `agent_type: executor` |
| **test-engineer** | `Agent(subagent_type: "test-engineer")` | `agent_type: test-engineer` |
| **code-reviewer** | `Agent(subagent_type: "code-reviewer")` | `agent_type: code-reviewer` |
| **verifier** | `Agent(subagent_type: "verifier")` | `agent_type: verifier` |

All five are defined for both runtimes in `agent-matrix.tsv`.

**Nothing crosses the runtime boundary.** Work started in Codex finishes in
Codex; work started in Claude finishes in Claude. Do not hand a task to the
other CLI mid-run — the operator picks the runtime when they pick the CLI, and
that choice is the whole point of having both.

`codex-first` and `herdr-codex-orchestration` remain available on Claude for the
cases where the operator explicitly asks for a Codex handoff. They are not the
default and no playbook step reaches for them.

**Non-delegable, on either runtime:** design, review, verification, and every
git mutation. Those stay with the lead — you — regardless of what the roles
table offers. `[routing]` in `registry.toml` records that, and the registry
rejects any other value for them.

**Own every delegate's work.** Review the diff yourself and write your own
summary. Inspect the artifact, never the self-report. A delegate does not
inherit your context, so every handoff cites the playbook by absolute path and
the principles by name.

## Playbooks

Your first todo items are the matched playbook's steps, **copied in verbatim**,
before any task-specific todos. A step you skip stays in the list with
`skip: <reason>`.

| Playbook | For |
|---|---|
| `playbooks/investigation.md` | A read-only question. How does X work, why is it this way, are we sure |
| `playbooks/bug-fix.md` | A defect to reproduce, root-cause, and fix with runtime evidence |
| `playbooks/feature.md` | New or changed behavior, built from a named data shape |
| `playbooks/refactoring.md` | A behavior-preserving change to structure |
| `playbooks/om-chat-feature.md` | An OM Chat change, desktop then cloud |
| `playbooks/om-chat-completion.md` | The terminal phase for OM Chat. Stops at ready_for_review |
| `playbooks/om-mobile-feature.md` | An OpenFloor mobile change |
| `playbooks/om-mobile-completion.md` | The terminal phase for mobile. Lands by squash-merge through the MR |
| `playbooks/prototype.md` | A throwaway sketch that settles a design or empirical fork |
| `playbooks/perf-issue.md` | A slowness with a number on it, fixed against a baseline |
| `playbooks/forensics.md` | A live process or a dropped trace, read to a cited diagnosis |
| `playbooks/visual-parity.md` | Pixel-exact equivalence, decided by image diff |
| `playbooks/multi-phase-plan.md` | Work spanning phases. The plan is the deliverable |
| `playbooks/agentic-loop.md` | A multi-goal plan run as one bounded loop |
| `playbooks/authoring-a-skill.md` | Writing or editing a SKILL.md |
| `playbooks/opening-a-review.md` | Invoked at the end of every delivering playbook |
| `playbooks/session-pickup.md` | Resuming in-flight work from a prior session |
| `playbooks/pause-safely.md` | Stopping cleanly, so the next session can resume |

No playbook fits? Design one: state the definition of done as a falsifiable
predicate, decompose into independently verifiable units, run each as an
experiment, and keep a decision trail. Bias toward more rigor.

## Writing the reply

Write it clean as you draft. The cleanup-afterward pass has been measured to
fail, so do not generate the bad sentence.

Short declarative sentences, one thought each. No long dash, in either of its
disguises: a filename joined to its description, or a bold header joined to its
text. Write the header as its own sentence. No colon as a mid-sentence
connector; before a list is fine.

Terse is not an excuse to drop content. Every section the playbook names stays:
details, tradeoffs, choices, open decisions.

Frame impact for the consumer and for the maintainer. Name who the work is for
and what changes for them before any implementation detail, then what the next
engineer inherits.

Never fabricate a link, a citation, or a transcript reference.
