# deez-skills

One hub for every skill, command, and subagent I use, shared across Claude Code
and Codex on every machine. Skills live here once and are symlinked into both
runtimes, so there is no second copy to drift.

The architecture is [pstack](https://github.com/cursor/plugins/tree/main/pstack),
adapted for two runtimes instead of one. Thirty-four principles, twelve
playbooks, one router.

## install

```bash
git clone git@github.com:daryl-tg/deez-skills.git ~/github/deez-skills
cd ~/github/deez-skills
bin/link            # preview. changes nothing
bin/link --apply    # install into ~/.claude and ~/.codex
```

Restart both runtimes, then `bin/doctor` to confirm.

**That installs the hub. It does not set up verification** — that is one session
per repository and is the step everything else leans on.
[Chapter 0](./docs/guide/00-first-run.md) is the ordered checklist for both.

## get started

Two things to know.

**1. Use `$clanker-mode` when the work needs rigor.**

```
$clanker-mode the reaction picker spacing is off on mobile
```

It reads the request, picks a playbook, and copies that playbook's steps into a
todo list **verbatim** before doing anything else. A step it decides to skip
stays in the list with a reason, so you can see what it chose not to do.

**2. Three skills fire without it**, because a read-only question should not
need ceremony:

```
why is the transcript virtualized this way
teach me how the rooms cache works
unslop
```

That is it. Everything else the router reaches for when a step needs it.

## usage

`$clanker-mode` matches your task to one of twelve playbooks and runs it.

<details>
<summary>the twelve playbooks</summary>

| playbook | for |
|---|---|
| [investigation](./skills/clanker-mode/playbooks/investigation.md) | a read-only question. how does X work, why is it this way, are we sure |
| [bug fix](./skills/clanker-mode/playbooks/bug-fix.md) | reproduce a defect, root-cause it, fix it with runtime evidence |
| [feature](./skills/clanker-mode/playbooks/feature.md) | new or changed behavior, built from a named data shape |
| [refactoring](./skills/clanker-mode/playbooks/refactoring.md) | a behavior-preserving change to structure. characterize first |
| [om-chat-feature](./skills/clanker-mode/playbooks/om-chat-feature.md) | an OM Chat change. desktop proven first, then the cloud twin |
| [om-chat-completion](./skills/clanker-mode/playbooks/om-chat-completion.md) | the terminal phase for OM Chat. stops at ready_for_review |
| [om-mobile-feature](./skills/clanker-mode/playbooks/om-mobile-feature.md) | an OpenFloor mobile change. device verification once, at the end |
| [om-mobile-completion](./skills/clanker-mode/playbooks/om-mobile-completion.md) | the terminal phase for mobile. lands by squash-merge through the MR |
| [agentic-loop](./skills/clanker-mode/playbooks/agentic-loop.md) | a multi-goal plan run as one bounded loop, dispatching to Codex |
| [authoring-a-skill](./skills/clanker-mode/playbooks/authoring-a-skill.md) | writing or editing a SKILL.md |
| [opening-a-review](./skills/clanker-mode/playbooks/opening-a-review.md) | invoked at the end of every delivering playbook |
| [session-pickup](./skills/clanker-mode/playbooks/session-pickup.md) | resuming in-flight work from a prior session or branch |

</details>

### examples

```
bug fix:        $clanker-mode the composer drops the draft when you switch rooms.
                repro first, then fix and prove it on the real surface.

feature:        $clanker-mode add a pinned-message row to the transcript header.
                desktop first, cloud after it is approved.

mobile:         $clanker-mode port the reaction picker to OpenFloor. the web
                logic is the reference, the design is not.

investigation:  why do we cancel the subscription on blur rather than unmount?

understanding:  teach me how rooms-client caches messages

before shipping: review
                blast-radius

after a gap:    recall the super-reaction work

after a session: reflect that took too long. capture what we learned.
```

## skills

The router reaches for most of these when a step needs them. The table is for
when you want one directly.

<details>
<summary>all skills</summary>

| skill | use it when |
| --- | --- |
| [`automate-me`](./skills/automate-me/SKILL.md) | Draft or refresh the operator's personal mode skill from real transcript history rather than from description. Use for… |
| [`blast-radius`](./skills/blast-radius/SKILL.md) | Find what a small-looking change could break beyond its diff, proving each safety claim with running code rather than … |
| [`codex-first`](./skills/codex-first/SKILL.md) | Route implementation work to Codex; Claude specs, reviews, verifies. Use the codex plugin (/codex:rescue, /codex:revie… |
| [`create-verification-skill`](./skills/create-verification-skill/SKILL.md) | Generate a project-local verification skill and its control wrapper so an agent can drive the real app and prove behav… |
| [`design`](./skills/design/SKILL.md) | Settle the shape before writing code: ground, sketch competing designs from the caller's usage, get approval, implemen… |
| [`figure-it-out`](./skills/figure-it-out/SKILL.md) | Design an auditable playbook when no bundled one fits: a large migration, an ambitious multi-part change, or work revi… |
| [`herdr-codex-orchestration`](./skills/herdr-codex-orchestration/SKILL.md) | Run independent Codex implementation, review, and verification loops through Herdr with isolated worktrees. Covers are… |
| [`maintain-verification-skill`](./skills/maintain-verification-skill/SKILL.md) | Periodic pass keeping a project's verification skill and feature map honest: parallel source readers per feature, one … |
| [`om-chat`](./skills/om-chat/SKILL.md) | Read, search, summarize, draft, and post in OM Chat rooms, channels, and DMs as a governed guest, through the OpenMark… |
| [`om-chat-design-system`](./skills/om-chat-design-system/SKILL.md) | Design and implement OM Chat React UI against the local components, tokens, layout, and interaction patterns. Load bef… |
| [`om-super-reaction`](./skills/om-super-reaction/SKILL.md) | Design, build, and quality-gate one super reaction effect for OM Chat's premium reaction system, from constraint tuple… |
| [`recall`](./skills/recall/SKILL.md) | Rebuild your context on a topic from prior sessions and the shared record, handed back as a current-state brief. Use w… |
| [`reflect`](./skills/reflect/SKILL.md) | Mine a finished session for durable lessons and route each to a concrete skill edit, gated on approval. Use when the o… |
| [`review`](./skills/review/SKILL.md) | Review a diff from the code, with findings sorted into act-on, consider, noted, and dismissed. Use for reviewing a bra… |
| [`show-me-your-work`](./skills/show-me-your-work/SKILL.md) | Keep an auditable decision trail as a committed TSV during long or unattended runs. Use when the operator will review … |
| [`teach`](./skills/teach/SKILL.md) | Explain a change or subsystem plainly so a person actually understands it. Runs explore and why, weaves one account, b… |
| [`test-first`](./skills/test-first/SKILL.md) | Write the failing check before production code, at the fastest level that expresses the behavior, and report the faili… |
| [`unslop`](./skills/unslop/SKILL.md) | Cut AI tells from any writing. Applies to every prose surface, including your own replies. |
| [`why`](./skills/why/SKILL.md) | Recover why something was built the way it is, from git history, review threads, tickets, chat, and incident records. … |
| [`writing-docs`](./skills/writing-docs/SKILL.md) | Pick the document's audience and mode first, then apply the matching standard: STE for agent-facing docs, developer st… |
| [`writing-simplified-technical-english`](./skills/writing-simplified-technical-english/SKILL.md) | Rewrite an agent-facing document in ASD-STE100 when it is too long, gets truncated, or reads as dense prose: SKILL.md,… |

</details>

## principles

Thirty-four rules, one per skill. Playbooks **cite** them by name and never
restate them, which is what stops the same rule drifting across five files. Each
one is invisible until something routes to it, so they cost nothing at session
start.

Nine are extracted from rules my own skills already asserted. The rest are
adapted from pstack.

<details>
<summary>all thirty-four principles</summary>

**Core**

| principle | apply when |
| --- | --- |
| `laziness-protocol` | Apply when refactoring, sizing a diff, or tempted to add abstractions, layers, or signal threading. Bias to deletion a… |
| `subtract-before-you-add` | Apply when sequencing an addition, refactor, or rewrite. Remove dead weight, redundant validators, and stubs first, th… |
| `foundational-thinking` | Apply before writing logic: choosing core types and data structures, sequencing scaffold before features, asking what … |
| `redesign-from-first-principles` | Apply when integrating a new requirement into an existing design. Redesign as if the requirement had been foundational… |
| `outcome-oriented-execution` | Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture rathe… |
| `exhaust-the-design-space` | Apply to a novel interaction or architectural decision with no precedent in the codebase. Build two or three competing… |
| `experience-first` | Apply to product, UX, and feature-scope tradeoffs. Choose user delight over implementation convenience; ship fewer pol… |
| `build-the-lever` | Apply to any non-trivial work: edits, migrations, analyses, checks. Build the tool that does or proves it rather than … |
| `minimize-reader-load` | Apply when reviewing or shaping code that is hard to trace. Count the layers between question and answer, and the hidd… |

**Architecture**

| principle | apply when |
| --- | --- |
| `model-the-domain` | Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files. Encode the … |
| `boundary-discipline` | Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries; trust in… |
| `type-system-discipline` | Apply when designing types or a signature in any statically typed language. Make illegal states unrepresentable, brand… |
| `make-operations-idempotent` | Apply when designing commands, lifecycle steps, or loops that run amid crashes, restarts, and retries. Converge to the… |
| `migrate-callers-then-delete-legacy-apis` | Apply when introducing a new internal API while old callers still exist. Migrate the callers and delete the old API in… |
| `separate-before-serializing-shared-state` | Apply when concurrent workers might write the same file, branch, port, or object. Eliminate the sharing first; seriali… |

**Verification**

| principle | apply when |
| --- | --- |
| `prove-on-the-real-surface` | Apply after any change, before declaring done. Verify in the running product on the surface the change touches. Tests … |
| `visual-approval-gates-delivery` | Apply before promoting, opening a review request, or announcing. Published evidence must exist and be approved first. … |
| `failing-test-first` | Apply before writing production code. Write the failing check first, at the fastest level that expresses the behavior,… |
| `fix-root-causes` | Apply when debugging. Trace each symptom to its root cause and fix it there. Reproduce first, ask why until you reach … |
| `sequence-verifiable-units` | Apply to multi-step work and to how you stack commits. Break work into small units that each end in a check, verify ea… |
| `finish-or-report` | Apply at the end of any run. Never deliver a partial silently. Either the whole thing is done, or say precisely what i… |

**Delivery**

| principle | apply when |
| --- | --- |
| `rebase-pr-squash` | Apply to every branch delivery. Rebase onto current origin/main, push the branch only, land through the PR or MR squas… |
| `one-commit-lands` | Apply when delivering a branch. Exactly one commit reaches main, produced by squash at PR merge. Commit freely while i… |
| `feature-branch-isolation` | Apply before starting any change. Work happens on daryl/<kebab-words> in its own worktree, never on main, never in the… |
| `promote-to-the-main-worktree` | Apply after rebasing a finished feature. Check the branch out in the main worktree so the local dev stack runs it and … |
| `announce-the-linked-review` | Apply at the end of any delivered change. Announce with the PR or MR link, then read the announcement back to confirm … |
| `desktop-before-cloud` | Apply to any change spanning the desktop app and its cloud twin. The desktop change lands and is proven first; the clo… |

**Delegation**

| principle | apply when |
| --- | --- |
| `delegate-implementation-review-stays-here` | Apply when handing work to a subagent or another runtime. Implementation delegates; design, review, verification, and … |
| `never-block-on-reversible-work` | Apply when tempted to ask permission for reversible work. Proceed and present the result. Does not apply to the planni… |
| `guard-the-context-window` | Apply when context fills up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents and … |
| `todo-discipline` | Apply to any multi-step task. A step you skip stays in the list with a stated reason. Silent omission is not allowed. |

**Environment and meta**

| principle | apply when |
| --- | --- |
| `bind-assigned-ports` | Apply whenever starting a server, choosing a port, or handing back a URL. Ports are assigned, never chosen. Bind 127.0… |
| `planning-docs-live-outside-the-repo` | Apply when writing a spec, plan, design doc, research note, or handoff prompt. They live in the dev-notes folder for t… |
| `encode-lessons-in-structure` | Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the… |

</details>

## how it is put together

Four layers. The `layer` field in `registry.toml` declares which one an entry
belongs to, and `bin/doctor` enforces what follows from it.

| layer | what it is | runtimes | invisible? |
|---|---|---|---|
| **mode** | the router | Claude only | yes |
| **principle** | one rule, cited by playbooks | **both** | yes |
| **playbook-host** | owns a `playbooks/` directory | Claude only | yes |
| **workflow** | everything else | either | optional |

Two consequences worth knowing:

**The router is Claude-only** because `disable-model-invocation` is a no-op on
Codex — tested, not assumed. A mode skill there would fire on description
matches instead of waiting to be routed to. Claude can also dispatch to Codex
and there is no clean path back, so Claude plans and Codex implements.

**Principles install on both** because a handoff to Codex cites them by name,
and that citation only resolves if the leaf exists on that side.

Playbooks are plain markdown inside the router, not registry entries, so twelve
of them cost nothing at session start and can still be read by absolute path
from either runtime.

## the tooling

```bash
bin/doctor      drift, dangling citations, unknown roles, layer violations, budget
bin/link        preview the install. --apply to make it so
bin/new         scaffold and register a skill
bin/adopt       pull an existing skill in from elsewhere
bin/index       regenerate the table below
bin/sync        commit and push. rebases first, never force-pushes
bin/test        the suite
```

`bin/doctor` is the one to run before every commit. It fails on a principle
cited but never written, a routed layer that lost its flag, a skill instructing
a local merge to main, a playbook step routing to a role neither runtime
defines, and a stale index.

There is deliberately **no per-skill description limit**. A single long
description is not what makes a runtime truncate its catalogue; the total is.
`bin/doctor` reports that total per runtime instead.

## docs

[usage guide](./docs/guide/) · [architecture](./docs/architecture.md) ·
[authoring](./docs/authoring.md) · [migration status](./docs/migration.md)

---

<!-- deez:index -->

## Everything in the hub

### Always-on essentials

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `automate-me` |  | claude, codex | Draft or refresh the operator's personal mode skill from real transcript history rather than from description. Use for 'automate me', 'capture how I work', or … |
| `clanker-agent` |  | claude | — |
| `clanker-mode` | router | claude, codex | Daryl's agent style: routed playbooks, cited principles, proof on the real surface, and delivery by rebase-PR-squash. Use for /clanker-mode, $clanker-mode, or … |
| `codex-first` |  | claude, codex | Route implementation work to Codex; Claude specs, reviews, verifies. Use the codex plugin (/codex:rescue, /codex:review) as the primary path, raw codex exec as… |
| `create-verification-skill` |  | claude, codex | Generate a project-local verification skill and its control wrapper so an agent can drive the real app and prove behavior. Use for /create-verification-skill, … |
| `design` |  | claude, codex | Settle the shape before writing code: ground, sketch competing designs from the caller's usage, get approval, implement against the sketch, and scrap it when f… |
| `herdr-codex-orchestration` |  | claude, codex | Run independent Codex implementation, review, and verification loops through Herdr with isolated worktrees. Covers arena mode (N candidates, one judge) and swa… |
| `maintain-verification-skill` |  | claude, codex | Periodic pass keeping a project's verification skill and feature map honest: parallel source readers per feature, one live session driving every feature, at mo… |
| `principle-announce-the-linked-review` | principle | claude, codex | Apply at the end of any delivered change. Announce as a title line, a body in the operator's /adhd voice, and the PR or MR link — nothing else — then read the … |
| `principle-bind-assigned-ports` | principle | claude, codex | Apply whenever starting a server, choosing a port, or handing back a URL. Ports are assigned, never chosen. Bind 127.0.0.1 explicitly. Anything the operator op… |
| `principle-boundary-discipline` | principle | claude, codex | Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries; trust internal types and keep business logic pure. |
| `principle-build-the-lever` | principle | claude, codex | Apply to any non-trivial work: edits, migrations, analyses, checks. Build the tool that does or proves it rather than doing it by hand. The tool is the artifac… |
| `principle-delegate-implementation-review-stays-here` | principle | claude, codex | Apply when handing work to a subagent or another runtime. Implementation delegates; design, review, verification, and git mutations stay with the lead. |
| `principle-desktop-before-cloud` | principle | claude, codex | Apply only when the operator asks for a change in both the desktop app and its cloud twin. Cloud parity is retired, so a desktop change no longer implies a clo… |
| `principle-encode-lessons-in-structure` | principle | claude, codex | Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a check, a type, a lint, or a sc… |
| `principle-exhaust-the-design-space` | principle | claude, codex | Apply to a novel interaction or architectural decision with no precedent in the codebase. Build two or three competing sketches and compare before committing. |
| `principle-experience-first` | principle | claude, codex | Apply to product, UX, and feature-scope tradeoffs. Choose user delight over implementation convenience; ship fewer polished things over more rough ones. |
| `principle-failing-test-first` | principle | claude, codex | Apply before writing production code. Write the failing check first, at the fastest level that expresses the behavior, and watch it fail for the right reason. |
| `principle-feature-branch-isolation` | principle | claude, codex | Apply before starting any change. Work happens on daryl/<kebab-words> in its own worktree, never on main, never in the primary worktree. |
| `principle-finish-or-report` | principle | claude, codex | Apply at the end of any run. Never deliver a partial silently. Either the whole thing is done, or say precisely what is left and why. |
| `principle-fix-root-causes` | principle | claude, codex | Apply when debugging. Trace each symptom to its root cause and fix it there. Reproduce first, ask why until you reach it, resist guards that silence a crash. |
| `principle-foundational-thinking` | principle | claude, codex | Apply before writing logic: choosing core types and data structures, sequencing scaffold before features, asking what concurrent actors share. Get the shape ri… |
| `principle-guard-the-context-window` | principle | claude, codex | Apply when context fills up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents and keep summaries in the main thread. |
| `principle-laziness-protocol` | principle | claude, codex | Apply when refactoring, sizing a diff, or tempted to add abstractions, layers, or signal threading. Bias to deletion and the smallest change that solves the pr… |
| `principle-make-operations-idempotent` | principle | claude, codex | Apply when designing commands, lifecycle steps, or loops that run amid crashes, restarts, and retries. Converge to the same end state regardless of partial pri… |
| `principle-migrate-callers-then-delete-legacy-apis` | principle | claude, codex | Apply when introducing a new internal API while old callers still exist. Migrate the callers and delete the old API in the same wave rather than keeping a comp… |
| `principle-minimize-reader-load` | principle | claude, codex | Apply when reviewing or shaping code that is hard to trace. Count the layers between question and answer, and the hidden state the reader must hold. Collapse o… |
| `principle-model-the-domain` | principle | claude, codex | Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files. Encode the domain in a structure instead of scattere… |
| `principle-never-block-on-reversible-work` | principle | claude, codex | Apply when tempted to ask permission for reversible work. Proceed and present the result. Does not apply to the planning gate or to irreversible actions. |
| `principle-one-commit-lands` | principle | claude, codex | Apply when delivering a branch. Exactly one commit reaches main, produced by squash at PR merge. Commit freely while implementing; never consolidate locally. |
| `principle-outcome-oriented-execution` | principle | claude, codex | Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture rather than preserving throwaway compatibility… |
| `principle-planning-docs-live-outside-the-repo` | principle | claude, codex | Apply when writing a spec, plan, design doc, research note, or handoff prompt. They live in the dev-notes folder for the task, never in the repo and never comm… |
| `principle-promote-to-the-main-worktree` | principle | claude, codex | Apply after rebasing a finished feature. Check the branch out in the main worktree so the local dev stack runs it and the operator can test manually. Promotion… |
| `principle-prove-on-the-real-surface` | principle | claude, codex | Apply after any change, before declaring done. Verify in the running product on the surface the change touches. Tests are necessary and never sufficient; incon… |
| `principle-rebase-pr-squash` | principle | claude, codex | Apply to every branch delivery. Rebase onto current origin/main, push the branch only, land through the PR or MR squashed. Never merge locally, never push main… |
| `principle-redesign-from-first-principles` | principle | claude, codex | Apply when integrating a new requirement into an existing design. Redesign as if the requirement had been foundational from day one instead of bolting it on. |
| `principle-separate-before-serializing-shared-state` | principle | claude, codex | Apply when concurrent workers might write the same file, branch, port, or object. Eliminate the sharing first; serialize structurally only when one shared writ… |
| `principle-sequence-verifiable-units` | principle | claude, codex | Apply to multi-step work and to how you stack commits. Break work into small units that each end in a check, verify each before the next, and order delivery so… |
| `principle-subtract-before-you-add` | principle | claude, codex | Apply when sequencing an addition, refactor, or rewrite. Remove dead weight, redundant validators, and stubs first, then build on the simpler base. |
| `principle-todo-discipline` | principle | claude, codex | Apply to any multi-step task. A step you skip stays in the list with a stated reason. Silent omission is not allowed. |
| `principle-type-system-discipline` | principle | claude, codex | Apply when designing types or a signature in any statically typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data… |
| `principle-visual-approval-gates-delivery` | principle | claude, codex | Apply before promoting, opening a review request, or announcing. Published evidence must exist and be approved first. Approval is the operator's, never inferre… |
| `reflect` |  | claude, codex | Mine a finished session for durable lessons and route each to a concrete skill edit, gated on approval. Use when the operator says reflect, or after a complex … |
| `review` |  | claude, codex | Review a diff from the code, with findings sorted into act-on, consider, noted, and dismissed. Use for reviewing a branch, PR, or MR, dead-code checks, or 'wou… |
| `test-first` |  | claude, codex | Write the failing check before production code, at the fastest level that expresses the behavior, and report the failing-before evidence. Use before implementi… |

### OM Chat feature delivery

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `om-build` |  | claude, codex | Build an OM Chat GUI from source and put it in front of the operator: the daemon-embedded /rooms GUI, or the hosted /chat/ cloud fork. Covers both targets and … |
| `om-chat` |  | claude, codex | Converse in OM Chat rooms as a governed guest through the OpenMarket MCP server's rooms tools (an agent badge). Use when the user asks you to read, search, wat… |
| `om-chat-design-system` |  | claude, codex | Design and implement OM Chat React UI against the local components, tokens, layout, and interaction patterns. Load before any user-visible OM Chat UI decision:… |
| `om-super-reaction` |  | claude, codex | Design, build, and quality-gate one super reaction effect for OM Chat's premium reaction system, from constraint tuple through storyboard and implementation to… |
| `verify-om-chat` |  | claude, codex | Use when a change to the OM Chat GUI (openmarket-chat or openmarket-chat-cloud) needs to be driven and proven in the running app — launching a browser lane, ex… |

### General workflow

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `blast-radius` |  | claude, codex | Find what a small-looking change could break beyond its diff, proving each safety claim with running code rather than assertion. Use before shipping a change t… |
| `figure-it-out` |  | claude, codex | Design an auditable playbook when no bundled one fits: a large migration, an ambitious multi-part change, or work reviewed after the operator steps away. Scale… |
| `llm-council` |  | claude, codex | Run any question, idea, or decision through a council of 5 AI advisors who independently analyze it, peer-review each other anonymously, and synthesize a final… |
| `recall` |  | claude, codex | Rebuild your context on a topic from prior sessions and the shared record, handed back as a current-state brief. Use when resuming work after a gap. |
| `show-me-your-work` |  | claude, codex | Keep an auditable decision trail as a committed TSV during long or unattended runs. Use when the operator will review after stepping away, or when the reasonin… |
| `teach` |  | claude, codex | Explain a change or subsystem plainly so a person actually understands it. Runs explore and why, weaves one account, builds diagrams up one part at a time. Use… |
| `why` |  | claude, codex | Recover why something was built the way it is, from git history, review threads, tickets, chat, and incident records. Use for 'why is this like this', 'why was… |

### Writing and editing

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `unslop` |  | claude, codex | Cut AI tells from any writing. Applies to every prose surface, including your own replies. |
| `writing-docs` |  | claude, codex | Pick the document's audience and mode first, then apply the matching standard: STE for agent-facing docs, developer style for human-facing ones. Use for docs, … |
| `writing-instructions` |  | claude, codex | Agent-facing instruction edits: skills, AGENTS.md, guidelines, or prompt docs. Not prose style. |
| `writing-simplified-technical-english` |  | claude, codex | Rewrite an agent-facing document in ASD-STE100 when it is too long, gets truncated, or reads as dense prose: SKILL.md, AGENTS.md, CLAUDE.md, subagent definitio… |

