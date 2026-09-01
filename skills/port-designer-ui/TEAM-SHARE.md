# port-designer-ui — team install

A Claude Code skill that ports UI from the designer repo (`Kiyotaka_Mar25_V9`, React + Tailwind) into kiyotaka-frontend (Vue 3 + Quasar) as **styling/layout-only changes** — it live-previews the exact source component for your sign-off before any code changes, hands implementation to Codex, verifies side-by-side, and cleans up after itself (no orphaned dev servers, no screenshots anywhere near git).

## Prerequisites

- Claude Code with Playwright MCP browser tools enabled
- Codex CLI installed (implementation is delegated to `codex --full-auto`)
- A local clone of the designer repo `Kiyotaka-v4-revamp/Kiyotaka_Mar25_V9`

## Install (copy-paste the whole block)

This installs to `~/.claude/skills/` in your **home directory** — deliberately NOT the repo's `.claude/skills/`, which is git-tracked. Installed this way, the skill can never show up in `git status` or a commit.

```bash
mkdir -p ~/.claude/skills/port-designer-ui
cat > ~/.claude/skills/port-designer-ui/SKILL.md <<'SKILL_EOF'
---
name: port-designer-ui
description: Use when porting a component, dialog, page, or visual redesign from the designer repo (Kiyotaka-v4-revamp / Kiyotaka_Mar25_V9) into kiyotaka-frontend — e.g. "port the symbol search dialog", "match the new design", "bring over the designer version of X".
---

# Port Designer UI → kiyotaka-frontend

## Setup (per developer — edit these two paths)

- `DESIGNER_REPO` = your clone of the designer repo `Kiyotaka_Mar25_V9` (e.g. `~/Github/Kiyotaka-v4-revamp/Kiyotaka_Mar25_V9`).
- `NOTES_DIR` = a personal notes folder OUTSIDE any git repo (e.g. `~/Documents/dev-notes`). Port artifacts go to `NOTES_DIR/port-<component>/`.

Prerequisites: Playwright MCP browser tools; Codex CLI. This skill file lives ONLY in `~/.claude/skills/port-designer-ui/` (your home dir) — never copy it into a repo's `.claude/skills/`, which is git-tracked.

## Overview

Ports a component from the designer repo (`DESIGNER_REPO`, React 19 + Tailwind) into kiyotaka-frontend (Vue 3 + Quasar + SCSS tokens). A port is a **restyle of the existing Vue component, never a rebuild**.

**Iron rule — UI only.** Styling, layout, colors, fonts, spacing, icons. Props, emits, store wiring, handlers, data sources, and triggers stay byte-identical. Any behavior difference in the design (new tab, removed button, changed sequence) is a **flow change**: list it, get the user's explicit keep/drop decision, and drop it by default. Do NOT wire real data, add entry points, or create new components "while you're here".

**Executor is hard-wired: Codex implements** (`codex --full-auto`, never `--yolo`). Skip the usual subagent-vs-Codex question. Claude owns locate, capture, validation, review, verify.

## Pipeline — no phase may be skipped or reordered

### 1. Locate
- Designer repo `git log --oneline -30` FIRST — commit subjects name what changed ("Symbol search v4: desktop polish").
- Grep `src/components/` (~168 flat .tsx). Variants (`V2/V25/V3/V4/V5`): pick the one recent commits touched AND that `src/App.tsx` / `src/main.tsx` actually renders — not the highest suffix. Ignore `* 2.tsx` duplicates and `.zip`s. Find the mount route (hash routes like `#perceptmodular`).
- Locate the existing target `.vue` component(s) in kiyotaka-frontend.
- Still ambiguous → show top candidates with commit evidence; never guess silently.

### 2. Capture (live app, not code reading)
- Start the designer server in background: `pnpm dev` in `DESIGNER_REPO` (port 5173; kiyotaka uses 8080). Track PID.
- Drive Playwright through EVERY interaction — clicks, hovers, drags, keyboard/focus, open/close transitions, empty/loading states. Code reading misses hover/drag/transient states; the live walk is mandatory.
- Write a **flow inventory** to `NOTES_DIR/port-<component>/`: every element+state, then two lists — *pure styling changes* vs *flow changes needing keep/drop*.

### 3. Validation gate (HARD STOP before any implementation)
- Screenshot the exact component state (dialog open, tab selected — never the app root) to the **scratchpad**, show the user via `open <file>` (Quick Look), delete after their verdict. Offer the live 5173 URL only if a screenshot isn't enough.
- Present the flow inventory + both change lists. User comments → loop back to 1/2. Only an explicit "correct" advances. Each flow change gets an explicit user decision here.

### 4. Codex handoff
- Write `codex-handoff-prompt.md` in `NOTES_DIR/port-<component>/`: absolute source/target paths, approved inventory, reference screenshots (NOTES_DIR only), and the translation contract:
  - JSX+Tailwind → Vue SFC template + scoped SCSS.
  - Every color → `var(--token)` declared in BOTH `src/styles/colors.scss` and `src/styles/dark-colors.scss`. Never raw hex/rgb/hsl.
  - Dark selectors in scoped CSS: wrap whole selector `:global(body.body--dark .scope)`.
  - Every user-facing string → i18n keys in all six locales (`en cn ja ko ru hi`).
  - Template/style edits only; approved flow changes only.
- Feature worktree per standard workflow. No commits unless the user asks.

### 5. Verify + cleanup
- Review the diff: any change outside template/style/i18n/color-token files is a finding.
- Side-by-side screenshots (designer 5173 vs kiyotaka 8080) of every inventoried state → scratchpad → `open` for user → discard after sign-off. Check both light and dark mode.
- Kill the designer server; `lsof -ti:5173` must return nothing. Delete all scratchpad shots.
- `git status --porcelain` in BOTH repos: no stray screenshots/artifacts. Worktree promotion stays the user's call.

## Screenshot hygiene (hard rule)
Screenshots go ONLY to the session scratchpad (disposable) or `NOTES_DIR/port-<component>/` (inventory-cited reference shots). NEVER under any repo path — nothing can then leak into a commit.

## Red flags — stop, you're off the pipeline
| Thought | Reality |
|---|---|
| "I can see the interactions from the .tsx" | Hover/drag/transient states only show in the live app. Run phase 2. |
| "I'll wire the real data while I'm here" | Logic change. UI only; flag it as a flow change instead. |
| "This needs a new component + trigger" | Rebuild, not a port. Restyle the existing target. |
| "Should I ask: subagents or Codex?" | Hard-wired Codex. Don't ask. |
| "User can validate at the end" | The gate is BEFORE implementation. Hard stop at phase 3. |
| "Server can stay up for later" | Kill it in phase 5; verify with lsof. No dead ports. |
| "Quick screenshot into the repo dir" | Never. Scratchpad or dev-notes only. |
SKILL_EOF
echo "Installed: ~/.claude/skills/port-designer-ui/SKILL.md — now edit the two paths in the Setup section"
```

## After installing

1. Open `~/.claude/skills/port-designer-ui/SKILL.md` and set the two paths in **Setup**: `DESIGNER_REPO` (your clone location) and `NOTES_DIR` (any folder outside a git repo).
2. Restart Claude Code (skills load at session start).
3. Use it: just ask, e.g. *"port the alert dialog from the designer repo"*. Claude will show you a screenshot of the component it found for your confirmation before anything is implemented.

## Why this can't end up in git

- The skill lives in `~/.claude/skills/` (home dir), not in any repository.
- The skill itself forbids writing screenshots or artifacts under any repo path — everything goes to the Claude session scratchpad (auto-cleaned) or your personal notes folder.
- Its final phase runs `git status --porcelain` in both repos to prove nothing leaked.
