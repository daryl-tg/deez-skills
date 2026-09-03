# deez-skills

One hub for every skill, command, and subagent I use, shared across Claude Code
and Codex on every machine. Skills live here once and are symlinked into both
runtimes, so there is no second copy to drift.

The architecture is [pstack](https://github.com/cursor/plugins/tree/main/pstack),
adapted for two runtimes instead of one. Thirty-four principles, twenty-four
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

`$clanker-mode` matches your task to one of twenty-four playbooks and runs it.

<details>
<summary>the twenty-four playbooks</summary>

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
| [prototype](./skills/clanker-mode/playbooks/prototype.md) | a throwaway sketch that settles a design or an empirical fork |
| [perf-issue](./skills/clanker-mode/playbooks/perf-issue.md) | a slowness with a number on it. baseline, fix, post-fix number |
| [forensics](./skills/clanker-mode/playbooks/forensics.md) | a live process or a dropped trace, read down to a cited diagnosis |
| [visual-parity](./skills/clanker-mode/playbooks/visual-parity.md) | pixel-exact equivalence, decided by image diff and never by eye |
| [multi-phase-plan](./skills/clanker-mode/playbooks/multi-phase-plan.md) | work spanning phases. the plan is the deliverable, not the code |
| [agentic-loop](./skills/clanker-mode/playbooks/agentic-loop.md) | a multi-goal plan run as one bounded loop, dispatching to Codex |
| [autonomous-run](./skills/clanker-mode/playbooks/autonomous-run.md) | one predicate, driven unattended until it holds. no delivery mid-run |
| [hillclimb](./skills/clanker-mode/playbooks/hillclimb.md) | one metric, driven to a target. one change, one measurement, keep or revert |
| [eval](./skills/clanker-mode/playbooks/eval.md) | does a change to how an agent works actually help. blind candidates, one judge |
| [authoring-a-skill](./skills/clanker-mode/playbooks/authoring-a-skill.md) | writing or editing a SKILL.md |
| [opening-a-review](./skills/clanker-mode/playbooks/opening-a-review.md) | invoked at the end of every delivering playbook |
| [review-to-green](./skills/clanker-mode/playbooks/review-to-green.md) | an open review driven to merge-ready. never past it |
| [landing](./skills/clanker-mode/playbooks/landing.md) | landing verified work, once the operator says so |
| [cleanup](./skills/clanker-mode/playbooks/cleanup.md) | pruning worktrees, simulators, and the servers a run started |
| [session-pickup](./skills/clanker-mode/playbooks/session-pickup.md) | resuming in-flight work from a prior session or branch |
| [pause-safely](./skills/clanker-mode/playbooks/pause-safely.md) | stopping cleanly, so the next session resumes from a note |

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

Playbooks are plain markdown inside the router, not registry entries, so twenty-four
of them cost nothing at session start and can still be read by absolute path
from either runtime.

## the tooling

```bash
bin/doctor      drift, dangling citations, unknown roles, layer violations, budget
bin/link        preview the install. --apply to make it so
bin/new         scaffold and register a skill
bin/adopt       pull an existing skill in from elsewhere
bin/index       regenerate the table below
bin/check-plan  check a multi-phase plan against the skeleton its playbook publishes
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

### cmux app development

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `cmux` |  | codex | End-user control of cmux topology and routing (windows, workspaces, panes/surfaces, focus, moves, reorder, identify, trigger flash). Use when automation needs … |
| `cmux-architecture` |  | codex | cmux package architecture, refactor layering, dependency inversion, file organization, DocC documentation, package design discipline, testability, and Swift 6 … |
| `cmux-backend` |  | codex | Backend TypeScript and Cloud VM development rules for cmux. Use when editing web/app/api, web/services, backend scripts, Cloud VM lifecycle, provider integrati… |
| `cmux-billing` |  | codex | Stripe checkout, pricing, subscription, Pro plan, webhook, and entitlement runbook for cmux billing work. Use when editing or debugging billing, pricing, Strip… |
| `cmux-browser` |  | codex | End-user browser automation with cmux. Use when you need to open sites, interact with pages, wait for state changes, and extract data from cmux browser surface… |
| `cmux-custom-sidebar` |  | codex | Build a custom cmux sidebar from a plain-language request. Use when the user asks for a custom sidebar, a sidebar that shows their workspaces/tabs/PRs/clock, a… |
| `cmux-customization` |  | codex | Customize cmux for an end user. Use when changing cmux.json actions, custom commands, workspace layouts, plus-button behavior, surface tab bar buttons, Command… |
| `cmux-debugging` |  | codex | Debug logging, Debug menu, runtime pitfalls, typing-latency-sensitive paths, SwiftUI list snapshot boundaries, OS-version repros, and local visual iteration fo… |
| `cmux-dev-workflow` |  | codex | Contributor workflow rules for cmux setup, Xcode project normalization, tagged sidebar ExtensionKit development, and dev builds. Use when setting up the cmux r… |
| `cmux-diagnostics` |  | codex | Run end-user cmux diagnostics. Use when cmux hooks, notifications, session restore, settings, browser automation, socket access, CLI control, or agent resume b… |
| `cmux-ghostty` |  | codex | Ghostty submodule and GhosttyKit workflow rules for cmux. Use when modifying the ghostty submodule, rebuilding GhosttyKit.xcframework, updating the parent subm… |
| `cmux-keyboard-shortcuts` |  | codex | Guide and apply cmux keyboard shortcut customization. Use when the user asks to customize, rebind, unbind, reset, audit, or create shortcut templates for cmux,… |
| `cmux-localization` |  | codex | Localization rules and audit workflow for cmux UI strings, settings rows, menus, shortcuts, schema/config text, docs, command/help text, alerts, tooltips, and … |
| `cmux-markdown` |  | codex | Open markdown files in a formatted viewer panel with live reload. Use when you need to display plans, documentation, or notes alongside the terminal with rich … |
| `cmux-release` |  | codex | cmux release workflow, version bumping, changelog updates, pretag guard, release tags, and release asset expectations. Use when preparing or troubleshooting a … |
| `cmux-settings` |  | codex | View and edit cmux settings in ~/.config/cmux/cmux.json. Use when the user wants to change cmux preferences (appearance, sidebar, notifications, automation, br… |
| `cmux-shared-behavior` |  | codex | Shared behavior and mutation-path rules for cmux. Use when a behavior is exposed through multiple entrypoints such as keyboard shortcuts, command palette, cont… |
| `cmux-socket-policy` |  | codex | Socket command threading and focus policy for cmux CLI/socket work. Use when adding or changing socket commands, CLI commands, telemetry commands, focus/select… |
| `cmux-testing` |  | codex | cmux testing rules for Swift Testing, test target compilation, test wiring, and package/refactor validation. Use when adding or changing tests, touching packag… |
| `cmux-workspace` |  | codex | Work inside the current cmux workspace and terminal. Use for cmux workspace, current workspace, caller surface, panes, surfaces, socket targeting, and non-inte… |

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

### Go language toolchain

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `ancient-go-style` |  | claude, codex | Go work where package documentation, dependency source, vendoring, or module setup matters. |
| `go-config-ko` |  | claude, codex | Go config structs with ko tags, YAML/env wiring, defaults, and ko.Load call sites. |
| `go-docopt` |  | claude, codex | Go CLI parsing conventions: usage strings, flags, subcommands, argument structs, and dispatch. |
| `go-karma-log` |  | claude, codex | Go log lines, wrapped errors, and structured context conventions. |
| `golangci-lint` |  | claude, codex | Go lint setup and configuration: rules, .golangci.yml, project wiring, or linter failures. |
| `karma-read` |  | claude, codex | Tree-formatted Go logs to structured NDJSON; field, error, and context extraction/filtering. |

### Infrastructure and observability

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `kolint` |  | claude, codex | YAML config audits against Go structs: schema, defaults, required fields, and unknowns. |
| `kubectl-logs` |  | claude, codex | Kubernetes deployment pod log capture with the bundled kubectl-logs script. |
| `logcli` |  | claude, codex | Live Loki log exports, per-pod splits, and saved Kubernetes or service log captures; not logs already on disk. |
| `stackctl` |  | claude, codex | Live Grafana/Prometheus: dashboards, panels, variables, imports, validation, or PromQL through Grafana. |
| `tsdbctl` |  | claude, codex | tsdb-gateway market data and research scripts. |

### Kiyotaka / orange stack

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `authoring-orange-shared-packages` |  | claude | Use when creating or changing a package in the orange-shared workspace (/Users/dboon/Gitlab/orange-shared, @orangecharts npm scope) — adding a shared types/sch… |
| `kiyotaka-user-docs` |  | claude, codex | Carry a kiyotaka-frontend user-facing change into its docs in the same cycle. Use when shipping a retail-visible feature or setting, when asked to "document X"… |
| `migrating-types-to-orange-shared` |  | claude | Use when centralising duplicated, hand-copied, or drift-guarded types/constants from kiyotaka-frontend (or another consumer repo) into an @orangecharts package… |
| `port-designer-ui` |  | claude, codex | Use when porting a component, dialog, page, landing-page redesign, or other visual treatment from Kiyotaka_Mar25_V9 into a Kiyotaka Vue repository, especially … |

### OM Chat feature delivery

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `om-build` |  | claude, codex | Build an OM Chat GUI from source and put it in front of the operator: the daemon-embedded /rooms GUI, or the hosted /chat/ cloud fork. Covers both targets and … |
| `om-chat` |  | claude, codex | Converse in OM Chat rooms as a governed guest through the OpenMarket MCP server's rooms tools (an agent badge). Use when the user asks you to read, search, wat… |
| `om-chat-design-system` |  | claude, codex | Design and implement OM Chat React UI against the local components, tokens, layout, and interaction patterns. Load before any user-visible OM Chat UI decision:… |
| `om-super-reaction` |  | claude, codex | Design, build, and quality-gate one super reaction effect for OM Chat's premium reaction system, from constraint tuple through storyboard and implementation to… |
| `verify-om-chat` |  | claude, codex | Use when a change to the OM Chat GUI (openmarket-chat or openmarket-chat-cloud) needs to be driven and proven in the running app — launching a browser lane, ex… |
| `verify-openfloor` |  | claude, codex | Use when a change to the OpenFloor mobile app (openmarket-chat-app, the Expo/React Native OpenMarket client) needs to be driven and proven on a real iOS simula… |

### General workflow

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `adhd` |  | claude, codex | Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state across turns, suppress tangents, give specific time estim… |
| `ancient-shell-style` |  | claude, codex | Lint, format, test, review, document, and harden maintained Bash and shell scripts with ShellCheck, shfmt, shdoc, and test-runner.bash. Use for Bash, sh, shell… |
| `blast-radius` |  | claude, codex | Find what a small-looking change could break beyond its diff, proving each safety claim with running code rather than assertion. Use before shipping a change t… |
| `bump-rc` |  | claude | Release a new @openmarket/rooms-client version — pick the bump from what actually changed, run the repo's release script, then update both GUI consumers' pins.… |
| `chrome-devtools` |  | claude, codex | Browser automation through the Chrome DevTools Protocol with the bundled chrome-devtools script. |
| `commit` |  | codex | Commit the currently staged git changes only. Use when the user invokes /commit, asks to commit staged changes, or requests a concise commit from the existing … |
| `demuddy` |  | claude | Use when a plan, spec, or design doc has accumulated edits from multiple discussion rounds and is about to be handed to an implementing agent (or human) — symp… |
| `figure-it-out` |  | claude, codex | Design an auditable playbook when no bundled one fits: a large migration, an ambitious multi-part change, or work reviewed after the operator steps away. Scale… |
| `git` |  | claude, codex | Version-control workflow: commits, staging, rebasing, branching, minimal diffs, and commit messages. |
| `glab` |  | claude, codex | GitLab MR management via glab. |
| `graphify` |  | claude, codex | Use for any question about a codebase, its architecture, file relationships, or project content — especially when graphify-out/ exists, where the question shou… |
| `hatch-pet` |  | codex | Create, repair, validate, visually QA, and package Codex-compatible v2 animated pets from character art, generated images, company or prospect brand cues, or v… |
| `ivtg` |  | claude | Use when the user wants to queue up bugs, regressions, or issues one at a time and get each one investigated across one or more repos and written up as a fix p… |
| `labiew` |  | claude, codex | GitLab MR review comments and response planning for the current branch. |
| `llm-council` |  | claude, codex | Run any question, idea, or decision through a council of 5 AI advisors who independently analyze it, peer-review each other anonymously, and synthesize a final… |
| `loop-me-in` |  | claude | Use when a fix plan, spec, or design doc needs to become a file that a fresh session can execute unattended and prove its own changes landed — "make this runna… |
| `mailbox` |  | claude, codex | Agent mail, handoffs, replies, waits, handled state, or store inspection. |
| `maintain-agents-md` |  | claude, codex | AGENTS.md maintenance and repository agent instructions. |
| `pi-development` |  | claude, codex | Pi asset development: extensions, skills, prompts, themes, packages, providers, models, TUI, or SDK integrations. |
| `prompt-ready` |  | claude | Use when the user wants to turn raw, natural-language requests into clean, self-contained, copy-paste-ready prompts for a different Claude/LLM session. Persist… |
| `recall` |  | claude, codex | Rebuild your context on a topic from prior sessions and the shared record, handed back as a current-state brief. Use when resuming work after a gap. |
| `reviewer` |  | claude, codex | Code, diff, PR, or MR review; dead-code checks, behavior drift, or REVIEW.txt notes. |
| `show-me-your-work` |  | claude, codex | Keep an auditable decision trail as a committed TSV during long or unattended runs. Use when the operator will review after stepping away, or when the reasonin… |
| `syncup` |  | claude | Use when the user wants one or more local repos brought up to date with their default branch — refresh main from origin, rebase the working branch onto it, and… |
| `taskfile` |  | claude, codex | Task runner automation: create, revise, or troubleshoot task definitions and syntax. |
| `teach` |  | claude, codex | Explain a change or subsystem plainly so a person actually understands it. Runs explore and why, weaves one account, builds diagrams up one part at a time. Use… |
| `testing-harness` |  | claude | Use when a change has to be proven in the real running product rather than in tests — visually diffing the cloud deployment against the local daemon, sweeping … |
| `war-diary` |  | claude | Use when updating the Frontend War Diaries from a GitLab activity .atom export and the day's Claude Code sessions — turning a day's GitLab work (pushes, MRs, a… |
| `why` |  | claude, codex | Recover why something was built the way it is, from git history, review threads, tickets, chat, and incident records. Use for 'why is this like this', 'why was… |

### Writing and editing

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `humanize` |  | claude | Use when Claude-authored text (design doc, MR description, README section, chat/message draft) needs to read like Ryan wrote it — before pasting into Discord o… |
| `unslop` |  | claude, codex | Cut AI tells from any writing. Applies to every prose surface, including your own replies. |
| `writing-comments` |  | claude, codex | Explicit comment, docstring, commented-out code, or public API documentation work. |
| `writing-docs` |  | claude, codex | Pick the document's audience and mode first, then apply the matching standard: STE for agent-facing docs, developer style for human-facing ones. Use for docs, … |
| `writing-instructions` |  | claude, codex | Agent-facing instruction edits: skills, AGENTS.md, guidelines, or prompt docs. Not prose style. |
| `writing-simplified-technical-english` |  | claude, codex | Rewrite an agent-facing document in ASD-STE100 when it is too long, gets truncated, or reads as dense prose: SKILL.md, AGENTS.md, CLAUDE.md, subagent definitio… |

