---
description: Create an isolated worktree on a fresh feature branch off the latest origin/main
argument-hint: <feature-slug>
allowed-tools: Bash(git fetch:*), Bash(git worktree:*), Bash(git branch:*), Bash(git rev-parse:*), Bash(test:*), Bash(pnpm install:*), Bash(ls:*)
---

Set up an isolated worktree for new feature work. The current worktree very likely has uncommitted, in-progress changes from an ongoing session — **do not touch it, do not stash, do not switch its branch.**

## Inputs

- Feature slug: `$1` (kebab-case, e.g. `super-search-filters`). If empty, ask the user for one before doing anything.
- Branch name: `daryl/<slug>`
- Worktree path: `../kiyotaka-frontend-<slug>` (sibling of the current repo, matching the existing convention)

## Steps

1. **Derive and validate names.** Reject a slug with spaces or characters unsafe for a path/branch. Confirm neither the target branch nor the target directory already exists:
   - `git rev-parse --verify daryl/<slug>` (should fail = branch is free)
   - `test -e ../kiyotaka-frontend-<slug>` (should fail = dir is free)
   If either exists, stop and report it rather than clobbering.

2. **Fetch the latest main without disturbing the current tree.** Run exactly:
   ```
   git fetch origin main
   ```
   Use `fetch`, never `pull` — this updates the `origin/main` ref only and leaves the current dirty working tree and current branch completely untouched.

3. **Create the isolated worktree + branch off the freshly-fetched main:**
   ```
   git worktree add ../kiyotaka-frontend-<slug> -b daryl/<slug> origin/main
   ```
   This gives the new feature its own working directory and its own branch based on the latest `origin/main`, so file changes there cannot collide with the ongoing session here.

4. **Install deps in the new worktree** (node_modules is not shared across worktrees):
   ```
   pnpm --dir ../kiyotaka-frontend-<slug> install
   ```
   This can take a while — run it, but tell the user they can skip/interrupt if they only need the branch set up.

5. **Report** the worktree path, branch name, and base commit (`git -C ../kiyotaka-frontend-<slug> rev-parse --short HEAD`). Then tell the user to start the new feature there by opening a new Claude Code session in that directory:
   ```
   cd ../kiyotaka-frontend-<slug>
   ```
   Keep this session focused on whatever it was already doing.
