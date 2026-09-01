# deez-skills

One hub for every skill, command, and subagent, shared across Claude Code and
Codex on every machine. Skills live here once and are symlinked into both
runtimes, so there is no second copy to drift.

Architecture is borrowed from [pstack](https://github.com/cursor/plugins/tree/main/pstack)
and adapted for two runtimes instead of one. Four layers, strictly separated:

| Layer | What it is | Runtimes |
|---|---|---|
| **mode** | The router. Classifies a request and copies a playbook's steps in verbatim | Claude only |
| **principle** | One rule. Cited by playbooks, never restated in them | Both |
| **playbook-host** | A skill owning a `playbooks/` directory | Claude only |
| **workflow** | Everything else | Either |

Playbooks are plain markdown inside the router, not registry entries, so twelve
of them cost nothing at session start.

---

## Set it up on a new machine

### 1. Prerequisites

```bash
python3 --version        # need 3.11+ somewhere, for tomllib
git --version
```

Python 3.11 or newer must exist **somewhere**; it need not be `python3`. macOS
ships 3.9, which has no `tomllib`. If nothing newer is installed:

```bash
brew install python@3.14
```

`bin/deez` probes `$DEEZ_PYTHON`, then `python3`, then `python3.14` down to
`python3.11`, and exits 3 with the fix if none works.

Optional, needed only by the skills that use them: `agent-browser` for
verification, the `codex` CLI for dispatch, `jq` for `bin/hook-install`.

### 2. Clone

```bash
git clone git@github.com:daryl-tg/deez-skills.git ~/github/deez-skills
cd ~/github/deez-skills
```

Clone to a real local path. Do not put it in a cloud-synced folder: two machines
writing the same working tree through iCloud or Dropbox corrupts git.

### 3. Check the toolchain

```bash
bin/deez version         # deez 0.1.0
bin/deez python-path     # the interpreter it resolved
bin/test                 # the full suite
```

### 4. Preview the install

```bash
bin/link
```

Prints what it *would* do and changes nothing. Read it. Every line is one
symlink, and the verb says what happens to whatever is there now:

| Verb | Meaning |
|---|---|
| `link` | Nothing at the destination. Creates the symlink |
| `ok` | Already correct |
| `relink` | A symlink pointing elsewhere. Repointed |
| `adopt` | A real directory whose contents already match. Replaced |
| `backup` | A real directory that **differs**. Moved to `~/.local/state/deez-skills/<stamp>/` first |
| `missing-source` | Registry entry with no folder. **Blocks the whole apply** |

Nothing is ever deleted. A conflict is moved aside, never removed.

### 5. Install

```bash
bin/link --apply
```

Restart Claude Code and Codex. Both read their skill directories at session
start, so a skill installed mid-session stays invisible until then.

### 6. Verify

```bash
bin/doctor               # exits non-zero on drift
```

Then confirm the runtimes actually see it. In Claude Code, `$clanker-mode` should
resolve. In Codex, ask it to list skills whose name starts with `principle-`:
all seventeen should appear, because principles install on both runtimes so a
handoff citing one resolves on either side.

### Installing a subset

A machine that does not need a stack should not carry it. Skill descriptions
load into every session before you type.

```bash
bin/link --profile lean            # preview
bin/link --profile lean --apply
bin/link --runtime codex --apply   # one runtime only
```

Profiles live in `registry.toml`. `full` is everything; `lean` is core,
workflow, and writing.

### Keeping machines in sync

```bash
bin/sync                 # commit and push. Rebases first, never force-pushes
touch .sync-hold         # pause it
bin/hook-install         # fire bin/sync automatically on edits
```

`bin/hook-install` writes to `~/.claude/settings.json` and keeps a backup. If
another skills repo already installs its own sync hook, remove that one in the
same change: two hooks race over edits made through the same symlinks and commit
to different repos.

---

## Using it

**`$clanker-mode`** is the entry point for anything needing rigor. It classifies the
request, opens the matching playbook, and copies its steps into a todo list
before doing anything else.

```
$clanker-mode the reaction picker spacing is off on mobile
```

Three skills fire without it, for read-only asks that should not need ceremony:
`why` (why is it built this way), `teach` (explain it properly), and `unslop`
(cut AI tells from any prose).

The [usage guide](./docs/guide/) walks a first real task end to end.

## Working on the hub itself

```bash
bin/new my-skill --category workflow --runtimes claude,codex
bin/adopt ~/some/path/existing-skill --category workflow
bin/index                # regenerate the table below
bin/doctor               # before every commit
```

Docs: [architecture](./docs/architecture.md) ·
[authoring](./docs/authoring.md) · [migration status](./docs/migration.md) ·
[usage guide](./docs/guide/)

---

<!-- deez:index -->

## Everything in the hub

### Always-on essentials

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `automate-me` |  | claude, codex | Draft or refresh the operator's personal mode skill from real transcript history rather than from description. Use for 'automate me', 'capture how I work', or … |
| `clanker-agent` |  | claude | — |
| `clanker-mode` | router | claude | Daryl's agent style: routed playbooks, cited principles, proof on the real surface, and delivery by rebase-PR-squash. Use for /clanker-mode, $clanker-mode, or … |
| `codex-first` |  | claude, codex | Route implementation work to Codex; Claude specs, reviews, verifies. Use the codex plugin (/codex:rescue, /codex:review) as the primary path, raw codex exec as… |
| `create-verification-skill` |  | claude, codex | Generate a project-local verification skill and its control wrapper so an agent can drive the real app and prove behavior. Use for /create-verification-skill, … |
| `design` |  | claude, codex | Settle the shape before writing code: ground, sketch competing designs from the caller's usage, get approval, implement against the sketch, and scrap it when f… |
| `herdr-codex-orchestration` |  | claude, codex | Run independent Codex implementation, review, and verification loops through Herdr with isolated worktrees. Covers arena mode (N candidates, one judge) and swa… |
| `maintain-verification-skill` |  | claude, codex | Periodic pass keeping a project's verification skill and feature map honest: parallel source readers per feature, one live session driving every feature, at mo… |
| `principle-announce-the-linked-review` | principle | claude, codex | Apply at the end of any delivered change. Announce with the PR or MR link, then read the announcement back to confirm it posted. |
| `principle-bind-assigned-ports` | principle | claude, codex | Apply whenever starting a server, choosing a port, or handing back a URL. Ports are assigned, never chosen. Bind 127.0.0.1 explicitly. Anything the operator op… |
| `principle-build-the-lever` | principle | claude, codex | Apply to any non-trivial work: edits, migrations, analyses, checks. Build the tool that does or proves it rather than doing it by hand. The tool is the artifac… |
| `principle-delegate-implementation-review-stays-here` | principle | claude, codex | Apply when handing work to a subagent or another runtime. Implementation delegates; design, review, verification, and git mutations stay with the lead. |
| `principle-desktop-before-cloud` | principle | claude, codex | Apply to any change spanning the desktop app and its cloud twin. The desktop change lands and is proven first; the cloud fork follows. |
| `principle-failing-test-first` | principle | claude, codex | Apply before writing production code. Write the failing check first, at the fastest level that expresses the behavior, and watch it fail for the right reason. |
| `principle-feature-branch-isolation` | principle | claude, codex | Apply before starting any change. Work happens on daryl/<kebab-words> in its own worktree, never on main, never in the primary worktree. |
| `principle-finish-or-report` | principle | claude, codex | Apply at the end of any run. Never deliver a partial silently. Either the whole thing is done, or say precisely what is left and why. |
| `principle-never-block-on-reversible-work` | principle | claude, codex | Apply when tempted to ask permission for reversible work. Proceed and present the result. Does not apply to the planning gate or to irreversible actions. |
| `principle-one-commit-lands` | principle | claude, codex | Apply when delivering a branch. Exactly one commit reaches main, produced by squash at PR merge. Commit freely while implementing; never consolidate locally. |
| `principle-planning-docs-live-outside-the-repo` | principle | claude, codex | Apply when writing a spec, plan, design doc, research note, or handoff prompt. They live in the dev-notes folder for the task, never in the repo and never comm… |
| `principle-promote-to-the-main-worktree` | principle | claude, codex | Apply after rebasing a finished feature. Check the branch out in the main worktree so the local dev stack runs it and the operator can test manually. Promotion… |
| `principle-prove-on-the-real-surface` | principle | claude, codex | Apply after any change, before declaring done. Verify in the running product on the surface the change touches. Tests are necessary and never sufficient; incon… |
| `principle-rebase-pr-squash` | principle | claude, codex | Apply to every branch delivery. Rebase onto current origin/main, push the branch only, land through the PR or MR squashed. Never merge locally, never push main… |
| `principle-separate-before-serializing-shared-state` | principle | claude, codex | Apply when concurrent workers might write the same file, branch, port, or object. Eliminate the sharing first; serialize structurally only when one shared writ… |
| `principle-todo-discipline` | principle | claude, codex | Apply to any multi-step task. A step you skip stays in the list with a stated reason. Silent omission is not allowed. |
| `principle-visual-approval-gates-delivery` | principle | claude, codex | Apply before promoting, opening a review request, or announcing. Published evidence must exist and be approved first. Approval is the operator's, never inferre… |
| `reflect` |  | claude, codex | Mine a finished session for durable lessons and route each to a concrete skill edit, gated on approval. Use when the operator says reflect, or after a complex … |
| `review` |  | claude, codex | Review a diff from the code, with findings sorted into act-on, consider, noted, and dismissed. Use for reviewing a branch, PR, or MR, dead-code checks, or 'wou… |
| `test-first` |  | claude, codex | Write the failing check before production code, at the fastest level that expresses the behavior, and report the failing-before evidence. Use before implementi… |

### OM Chat feature delivery

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `om-chat` |  | claude, codex | Read, search, summarize, draft, and post in OM Chat rooms, channels, and DMs as a governed guest, through the OpenMarket MCP rooms tools. Use when the task con… |
| `om-chat-design-system` |  | claude, codex | Design and implement OM Chat React UI against the local components, tokens, layout, and interaction patterns. Load before any user-visible OM Chat UI decision:… |
| `om-super-reaction` |  | claude, codex | Design, build, and quality-gate one super reaction effect for OM Chat's premium reaction system, from constraint tuple through storyboard and implementation to… |

### General workflow

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `blast-radius` |  | claude, codex | Find what a small-looking change could break beyond its diff, proving each safety claim with running code rather than assertion. Use before shipping a change t… |
| `figure-it-out` |  | claude, codex | Design an auditable playbook when no bundled one fits: a large migration, an ambitious multi-part change, or work reviewed after the operator steps away. Scale… |
| `recall` |  | claude, codex | Rebuild your context on a topic from prior sessions and the shared record, handed back as a current-state brief. Use when resuming work after a gap. |
| `show-me-your-work` |  | claude, codex | Keep an auditable decision trail as a committed TSV during long or unattended runs. Use when the operator will review after stepping away, or when the reasonin… |
| `teach` |  | claude, codex | Explain a change or subsystem plainly so a person actually understands it. Runs explore and why, weaves one account, builds diagrams up one part at a time. Use… |
| `why` |  | claude, codex | Recover why something was built the way it is, from git history, review threads, tickets, chat, and incident records. Use for 'why is this like this', 'why was… |

### Writing and editing

| Name | Layer | Runtimes | Description |
| --- | --- | --- | --- |
| `unslop` |  | claude, codex | Cut AI tells from any writing. Applies to every prose surface, including your own replies. |
| `writing-docs` |  | claude, codex | Pick the document's audience and mode first, then apply the matching standard: STE for agent-facing docs, developer style for human-facing ones. Use for docs, … |
| `writing-simplified-technical-english` |  | claude, codex | Rewrite an agent-facing document in ASD-STE100 when it is too long, gets truncated, or reads as dense prose: SKILL.md, AGENTS.md, CLAUDE.md, subagent definitio… |

