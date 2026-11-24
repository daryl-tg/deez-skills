---
name: clanker-mode
description: "Daryl's agent style: routed playbooks, cited principles, proof on the real surface, and delivery by rebase-PR-squash. Use for /clanker-mode, $clanker-mode, or any request for rigorous work on the OM stacks."
disable-model-invocation: true
mode: true
---

# Clanker mode

## Session continuity

Explicit `$clanker-mode`, `/clanker-mode`, or "use clanker mode" activates this
mode for the session until the user opts out or clears the conversation.
Follow-ups continue the current task. A new task selects a new playbook. A
casual question or a finished task does not deactivate it. Never infer
activation from merely discussing the skill.

The hub's session hooks save activation outside the transcript and remind on
user turns, after compaction or resume, and every 20 tool calls. They grant no
permission and enforce no playbook. Install them with
`bin/deez clanker-hooks --apply` at the hub root. Without running hooks this is
a prose convention. [Session persistence](references/session-persistence.md)
owns setup, scope and limits.

On task selection, write `resume.md` in the task's dev-notes folder and register
its absolute path and the playbook with `bin/deez clanker-checkpoint`. The note
holds what session persistence lists, from the goal to the next action. Update
it after each meaningful step, before a handoff and before a planned compaction.
A checkpoint records progress and authorizes nothing. It is not a phase
boundary. Keep going after it.

After compaction or resume, reread this skill, the playbook and the note.
Restore the checklist, verify current state where needed, and continue at the
first unproven step. Never restart finished work, drop gates, stop delegates or
commit WIP for compaction. An explicit pause uses `playbooks/pause-safely.md`.

## Non-negotiables

**Start every multi-step task with a todo list whose first item is to read the
Principles index below in full.** Name each principle that shaped a decision and
the choice it changed. A citation with no decision behind it means the leaf went
unread.

- A non-trivial task → open with a one-line playback of the operator's goal, the
  problem, and, when it ships a change, the smallest change that meets it. Then
  the todo list. It is a statement, not a question. If the evidence rules out
  the change asked for, show it and stop. Restate the goal in every delegate
  brief, each review's `## Why`, and the top of the final report.
- Starting any agent → the first line of its brief is
  `Read ~/.claude/skills/clanker-mode/worker.md before anything else.` The
  operator's rules live in skills that load only from a slash command, so they
  reach a delegate no other way.
- Any code change → **principle-failing-test-first**, at the fastest level that
  expresses the behavior. A test you write, change, or keep →
  **principle-test-behavior-not-implementation**. A check that passes with
  every import returning `undefined` is not a check. Code you write or edit →
  **principle-code-speaks-for-itself**.
- Any typecheck, test run, lint, or build →
  **principle-scope-checks-to-the-change**. Whole-repo gates run only when the
  operator asks.
- A claim that something works → **principle-prove-on-the-real-surface**.
  Inconclusive is not a pass.
- Measuring, or reporting or acting on a measured number →
  **principle-explain-the-number**, and **benchmark-checklist** for a
  performance number.
- Before promoting, reviewing, or announcing →
  **principle-visual-approval-gates-delivery**.
- Any server, port, or URL → **principle-bind-assigned-ports**.
- Any spec, plan, or handoff → **principle-planning-docs-live-outside-the-repo**.
- **Any React or Next.js code** → **vercel-react-best-practices**, grounded by
  **principle-model-the-domain** for the data shape and
  **principle-minimize-reader-load** for component boundaries. Its rules run by
  impact, so start at waterfalls and bundle size, never at memoisation.
- **Product motion films, feature demos, UI launch films and product reels** →
  **product-video**, through `playbooks/product-video.md`. Read the project's
  verification map first. The playbook and the skill own the storyboard gate,
  the motion rules, the runtime, the preset records and the review cadence.
- **Motion in shipped components and interaction feel** → **animate** on web,
  **animate-expo** on Expo, held to **emil-design-eng**, and **apple-design**
  for gesture and material work. Auditing motion is **improve-animations**, and
  **find-animation-opportunities** for what should move and does not. Both
  return a roadmap, which is `playbooks/feature-plan.md` work, not something to
  start applying. Naming an effect you cannot name is **animation-vocabulary**.
- **review-animations** is operator-invoked, so ask for `/review-animations` on
  the diff. Never claim a motion review you did not run.
- The operator wants to understand something → **teach** for one plain account
  at their pace, **show-me** for the picture, **tutor** when they ask to be
  quizzed or drilled to mastery. When the gap is the words for what they are
  building → **reframe**, which the operator runs as `/reframe`. A one-off
  question just gets answered.
- Any prose surface, your reply included → **unslop**. Text going out in the
  operator's name → **humanize** after it.
- About to ask the operator → classify the fork per
  **principle-never-block-on-reversible-work**. A fact you could observe by
  running something is an experiment, through `playbooks/prototype.md`. A
  read-only question answers from the evidence, through
  `playbooks/investigation.md`. Under a full-autonomy grant
  (`playbooks/autonomous-run.md`, `playbooks/agentic-loop.md`), decide what the
  grant covers, act, and report it with the alternative in plain words, never a
  shorthand token to type back. Product and preference calls still get asked,
  two or more in one round through `playbooks/grill-me.md`.
- A feature or any multi-step change → **one pass, no phases.** One owner holds
  the whole context, plans the whole scope and builds it in the same run. Never
  a phase 1 and a phase 2, never a deferred follow-up, never a stop between
  units to hand back, because each handoff drops context and the build drifts.
  Split only when the work cannot ship as one review, and name the reason, an
  ordered landing across repositories or a staged production rollout. Each unit
  still ends in a check, per **principle-sequence-verifiable-units**.
- Frozen spec or plan → **build it through Claude subagents, without asking**,
  through `playbooks/agentic-loop.md`. There is no execution-path question. The
  lead stays inline only for tiny edits, session-only tools, or when the
  operator asks for inline.
- Broken skill mid-task → fix it in its own change. Do not block, and do not
  silently work around it.

## Principles

Read the leaf in full for any principle you apply. Naming one without a decision
behind it means you skipped reading it.

**Core.** How much to build, and in what order.
`laziness-protocol` · `subtract-before-you-add` · `foundational-thinking` ·
`redesign-from-first-principles` · `attack-the-premise` ·
`outcome-oriented-execution` · `exhaust-the-design-space` · `experience-first` ·
`build-the-lever` · `minimize-reader-load`

**Architecture.** What shape the code takes.
`model-the-domain` · `boundary-discipline` · `type-system-discipline` ·
`make-operations-idempotent` · `migrate-callers-then-delete-legacy-apis` ·
`separate-before-serializing-shared-state` · `code-speaks-for-itself`

**Verification.** What counts as done.
`prove-on-the-real-surface` · `explain-the-number` · `visual-approval-gates-delivery` ·
`failing-test-first` · `test-behavior-not-implementation` · `fix-root-causes` ·
`sequence-verifiable-units` · `scope-checks-to-the-change` · `finish-or-report`

**Delivery.** How work reaches main.
`rebase-pr-squash` · `one-commit-lands` · `feature-branch-isolation` ·
`promote-to-the-main-worktree` · `announce-the-linked-review` ·
`prove-every-host`

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
| `openmarket-chat` (both hosts: `/rooms` root, `apps/cloud`), `packages/rooms-client` | OM Chat | `playbooks/om-chat-feature.md` |
| `openmarket-chat-app` | OM Mobile | `playbooks/om-mobile-feature.md` |
| `kiyotaka-frontend`, `orange-v2-backend`, `tharamine-user-service`, `auth-service-backend`, `orange-shared` | Kiyotaka | Generic flow. No playbook yet |
| Anything else | none | Generic flow |

OM Chat stops at `ready_for_review`. OM Mobile carries through to a squash-merge
through the MR. Neither ever merges locally.

## Project verification maps

Read [the project verification contract](../../docs/project-verification.md)
before choosing a verification skill. It owns where the map lives and how its
repository is resolved. A project with no verification skill gets one through
**create-verification-skill**. **maintain-verification-skill** updates the same
map.

During exploration, reconcile the touched user outcomes with the README's
source-supported surface inventory. Record unmapped discoveries and
prerequisites even when live verification is blocked, marked pending. A feature
already in a guide still needs its new paths captured.

After live verification, add missing entries, update recipes, provenance, the
inventory and `features/README.md`. Map persistence is a visible checklist step
with the changed paths and the publication receipt, or a no-change or pending
reason. Before handing off, commit and push only the changed map Markdown
through `bin/deez sync-feature-maps`. That authorizes no product push and no
publication of skill or config changes.

## Delegation

**The operator runs Claude Code only.** Every delegate is a Claude subagent.
The Codex column below is dormant install support for a resubscribe, never a
routing target. Never hand a task to Codex, and never offer it.

Playbook steps name a **role**. Never a model, never a runtime.

| Role | On Claude | On Codex (dormant) |
|---|---|---|
| **explore** | `Agent(subagent_type: "explore")` | `agent_type: explore` |
| **executor** | `Agent(subagent_type: "executor")` | `agent_type: executor` |
| **test-engineer** | `Agent(subagent_type: "test-engineer")` | `agent_type: test-engineer` |
| **code-reviewer** | `Agent(subagent_type: "code-reviewer")` | `agent_type: code-reviewer` |
| **verifier** | `Agent(subagent_type: "verifier")` | `agent_type: verifier` |

The Claude column is authoritative. The hub versions the Claude halves in
`agents/` and links them into `~/.claude/agents/`. The dormant Codex halves are
oh-my-codex agents under `~/.codex/agents/`, recorded in `vendor.toml` rather
than copied.

**Non-delegable.** Design, review, verification, and every git mutation stay
with the lead, you, whatever the roles table offers. `[routing]` in
`registry.toml` records that, and the registry rejects any other value for them.

**Every brief opens with the worker line**, then the goal and the task. A
delegate inherits none of your context, so the brief cites the playbook by
absolute path and the principles by name.

**Own every delegate's work.** Review the diff yourself and write your own
summary. Inspect the artifact, never the self-report.

**Match effort to the job.** More reasoning effort for the hardest or subtlest
work, less for routine mechanical work. Verifier and code-reviewer effort never
drops, because a cheap review passes what it missed.

**Read-only roles still hold Bash.** Note `git status` before dispatching an
explore, verifier, or code-reviewer delegate and compare it after. A change is
the delegate's mutation to inspect and revert, not yours to keep.

**Fan-out reads in parallel.** Several slices to review or verify get one
delegate each, in its own worktree, per
**principle-separate-before-serializing-shared-state**, and one report. Each
brief names the exact SHAs and the method for any measurement, and asks for
every defect the delegate can prove, not only the first. A result without SHAs
or method is dropped and that slice respawned once. A gap in coverage is not a
pass.

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
| `playbooks/om-chat-feature.md` | An OM Chat change, in the one workspace both hosts share |
| `playbooks/om-chat-completion.md` | The terminal phase for OM Chat. Stops at ready_for_review |
| `playbooks/om-mobile-feature.md` | An OpenFloor mobile change |
| `playbooks/om-mobile-completion.md` | The terminal phase for mobile. Lands by squash-merge through the MR |
| `playbooks/prototype.md` | A throwaway sketch that settles a design or empirical fork |
| `playbooks/grill-me.md` | Open decisions settled with the operator, one round of questions at a time |
| `playbooks/perf-issue.md` | A slowness with a number on it, fixed against a baseline |
| `playbooks/forensics.md` | A live process or a dropped trace, read to a cited diagnosis |
| `playbooks/visual-parity.md` | Pixel-exact equivalence, decided by image diff |
| `playbooks/product-video.md` | A continuous product motion film or feature demo derived from the project's verification map |
| `playbooks/feature-plan.md` | A feature too large to build without a written plan. Planned whole, built in the same run |
| `playbooks/agentic-loop.md` | A multi-goal plan run as one bounded loop |
| `playbooks/autonomous-run.md` | One predicate, driven unattended until it holds |
| `playbooks/hillclimb.md` | One metric, driven to a target over many attempts |
| `playbooks/eval.md` | Does a change to how an agent works actually help |
| `playbooks/authoring-a-skill.md` | Writing or editing a SKILL.md |
| `playbooks/opening-a-review.md` | Invoked at the end of every delivering playbook |
| `playbooks/review-to-green.md` | An open review driven to merge-ready. Never past it |
| `playbooks/landing.md` | Landing verified work, once the operator says so |
| `playbooks/cleanup.md` | Pruning worktrees, simulators, and the run's servers |
| `playbooks/session-pickup.md` | Resuming in-flight work from a prior session |
| `playbooks/pause-safely.md` | Stopping cleanly, so the next session can resume |

No playbook fits → **figure-it-out**, which designs one with a falsifiable
definition of done, independently verifiable units run as experiments, and a
decision trail. Bias toward more rigor.

## Writing the reply

Write it clean as you draft. A cleanup pass afterwards has been measured to
fail, so do not generate the bad sentence.

Short declarative sentences, one thought each. No long dash, in either of its
disguises, a filename joined to its description or a bold header joined to its
text, so write the header as its own sentence. No colon as a mid-sentence
connector. A colon before a list is fine. Terse never drops content, so every
section the playbook names stays, details, tradeoffs, choices and open
decisions. Name who the work is for and what changes for them before any
implementation detail, then what the next engineer inherits. Never fabricate a
link, a citation, or a transcript reference. Every claim carries its evidence
or its label, measured, inferred, or guess, in the same sentence. A prediction
or a cause you have not observed is a guess. Never hand the operator a check you
could run yourself, per **principle-never-block-on-reversible-work**.

A command you do hand the operator gets a leading `!`, as in
`!bun test test/foo.test.ts`, and a line telling them they can run it directly
in the input. A `!` command has no terminal to type into, so one that stops for
a prompt or a typed yes refuses there. Give that one bare, for a real terminal,
and say why.
