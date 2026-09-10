---
description: Promote a finished feature worktree by checking out its branch in the main worktree and removing the feature worktree — gated on explicit user approval. Does NOT merge into the main branch.
argument-hint: <feature-slug> (optional if run from the feature worktree)
allowed-tools: Bash(git worktree:*), Bash(git switch:*), Bash(git checkout:*), Bash(git rev-parse:*), Bash(git log:*), Bash(git status:*), Bash(git branch:*), Bash(git symbolic-ref:*), Bash(git -C:*), Bash(test:*)
---

Bring a finished feature branch into the **main worktree** by checking it out there, then remove the now-redundant feature worktree.

**This does NOT merge the feature branch into the `main` branch.** The `main` branch ref is left exactly where it is. Integrating into `main` (push + PR/merge on the remote) is a separate, later step that the user drives. The point of this command is purely to consolidate the work back into the primary working directory and free up the sibling worktree.

**HARD RULE: never switch or remove anything without an explicit green light from the user.** Run the read-only pre-flight, present the summary, then STOP and wait for the user to confirm in their own words. Do not stash, do not push, do not commit, do not delete the feature branch, do not touch the `main` branch, and never use `--force`.

## Resolve targets (read-only)

1. **Feature slug** = `$1`. If empty, infer from the current branch (`git rev-parse --abbrev-ref HEAD`) only if it matches `daryl/<slug>`; otherwise ask the user which feature to finish. Feature branch = `daryl/<slug>`, feature worktree = `../kiyotaka-frontend-<slug>`.
2. **Main worktree** `<MAIN>` = the **primary** worktree: the first entry in `git worktree list`, whose path is the repo root `…/kiyotaka-frontend` (NOT a `kiyotaka-frontend-<slug>` sibling, and NOT anything under `.claude/worktrees`). Do not assume it is the entry currently on `[main]` — after a previous promote the primary worktree may itself be sitting on a `daryl/*` branch. Capture its absolute path as `<MAIN>`.
3. Confirm the feature branch and feature worktree both exist; if not, stop and report.

## Pre-flight inspection (read-only — show all of this to the user)

- **Work the branch carries:** `git -C <MAIN> log --oneline main..daryl/<slug>` — the commits that will come into the main worktree when it switches to this branch.
- **Feature worktree must be clean:** `git -C ../kiyotaka-frontend-<slug> status --short`. If it has uncommitted changes, **STOP** — removing the worktree would lose them. Tell the user to commit first (or that you can, only with their explicit go-ahead). Never commit on their behalf without approval.
- **Main worktree must be clean:** `git -C <MAIN> status --short`, and note its current branch (`git -C <MAIN> symbolic-ref --short HEAD`). Switching the main worktree onto the feature branch will fail or drag uncommitted changes across branches if `<MAIN>` is dirty — if there are uncommitted changes, **STOP** and hand back control. Do not stash.

## Green light

Present a one-screen summary:

- feature branch + the commits it carries,
- that the **main worktree** (`<MAIN>`) will be switched onto `daryl/<slug>`,
- that the feature worktree `../kiyotaka-frontend-<slug>` will be **removed**,
- that the **`main` branch is left untouched**,
- any warnings (dirty feature worktree, dirty main worktree, branch diverged from `origin/main`).

Then **stop and ask the user to explicitly approve.** Proceed only on a clear yes.

## Promote (only after approval)

Order matters — the feature worktree must be released before its branch can be checked out elsewhere:

```
git -C <MAIN> worktree remove ../kiyotaka-frontend-<slug>
git -C <MAIN> switch daryl/<slug>
```

- `git worktree remove` refuses on a dirty worktree (no `--force`) — that is the safety net. If it aborts, **stop** and report.
- If `git switch` aborts (e.g. "local changes would be overwritten"), **stop immediately**, show the exact error, and leave everything as-is. Do not stash or resolve on the user's behalf — report and hand back control.

## After a successful promote

Report:

- The main worktree is now on `daryl/<slug>` at `git -C <MAIN> rev-parse --short HEAD`.
- The `main` branch is unchanged — state this explicitly.
- If the branch has diverged from `origin/main` (it was branched off an older `main`), note it and **offer** — do not perform — a rebase onto the latest `main` before the user pushes.

The feature worktree is already gone, so there is no further cleanup. Do **not** delete the feature branch (it is now the active checkout in `<MAIN>`), and leave pushing / opening a PR to the user.
