---
description: Create an isolated worktree on a fresh feature branch off the latest default branch, in any repo
argument-hint: <feature-slug>
allowed-tools: Bash(git fetch:*), Bash(git worktree:*), Bash(git branch:*), Bash(git rev-parse:*), Bash(git symbolic-ref:*), Bash(test:*), Bash(ls:*), Bash(bun install:*), Bash(pnpm install:*), Bash(pnpm --dir:*), Bash(yarn install:*), Bash(yarn --cwd:*), Bash(npm ci:*), Bash(npm --prefix:*), Bash(uv sync:*)
---

Set up an isolated worktree for new feature work, in whatever repository this session is in. The current worktree very likely has uncommitted, in-progress changes from an ongoing session — **do not touch it, do not stash, do not switch its branch.**

If the repo has an owner in the global `## Project routing` table (OM Chat, OM Mobile), stop and use its skill instead; this command is the generic flow.

## Inputs

- Feature slug: `$1` (kebab-case, e.g. `super-search-filters`). If empty, ask the user for one before doing anything.
- Branch name: `daryl/<slug>`

## Resolve the repo (read-only)

Read these from git; never assume a repo name, a default branch or a package manager.

- **Primary worktree** `<PRIMARY>`: the first `worktree` line of `git worktree list --porcelain`. This is the repo's main working directory even when the session stands in a linked worktree.
- **Repo name** `<REPO>`: the basename of `<PRIMARY>`.
- **Default branch** `<DEF>`: `git symbolic-ref --short refs/remotes/origin/HEAD` with the `origin/` prefix removed. If that ref is unset, fall back to `main`, and say so in the report.
- **Worktree path** `<WT>`: `<parent of PRIMARY>/<REPO>-<slug>`, a sibling of the primary worktree.

## Steps

1. **Validate names.** Reject a slug with spaces or characters unsafe for a path or branch. Confirm neither target exists, and stop and report if either does:
   - `git rev-parse --verify daryl/<slug>` should fail (the branch is free).
   - `test -e <WT>` should fail (the directory is free).

2. **Fetch the latest default branch without disturbing the current tree:**
   ```
   git fetch origin <DEF>
   ```
   Use `fetch`, never `pull`. It updates `origin/<DEF>` only and leaves the current working tree and branch untouched.

3. **Create the worktree and branch off it:**
   ```
   git worktree add <WT> -b daryl/<slug> origin/<DEF>
   git -C <WT> branch --unset-upstream
   ```
   `worktree add` sets the new branch to track `origin/<DEF>`. Unsetting that upstream means a bare `git push` from the feature branch can never land on the default branch.

4. **Install dependencies if the repo has any.** Dependency folders are not shared across worktrees. Pick the installer from the lockfile at `<WT>`'s root, first match wins:

   | Lockfile | Command |
   |---|---|
   | `bun.lock` or `bun.lockb` | `bun install --cwd <WT>` |
   | `pnpm-lock.yaml` | `pnpm --dir <WT> install` |
   | `yarn.lock` | `yarn --cwd <WT> install` |
   | `package-lock.json` | `npm --prefix <WT> ci` |
   | `uv.lock` | `uv sync --directory <WT>` |
   | none of these | skip, and say "no dependencies to install" |

   Installs can take a while. Run it, and tell the user they can interrupt if they only need the branch.

5. **Report** `<WT>`, the branch, `<DEF>` and the base commit (`git -C <WT> rev-parse --short HEAD`). Then tell the user to start the feature in a new Claude Code session in that directory:
   ```
   cd <WT>
   ```
   Keep this session focused on whatever it was already doing.
