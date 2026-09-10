---
description: Move a finished feature worktree's branch into the main worktree so it can be checked out and tested — gated on explicit user approval. Does NOT merge into the default branch.
argument-hint: <branch-or-name> (optional if run from inside the feature worktree)
allowed-tools: Bash(git worktree:*), Bash(git switch:*), Bash(git rev-parse:*), Bash(git log:*), Bash(git status:*), Bash(git branch:*), Bash(git symbolic-ref:*), Bash(git -C:*), Bash(test:*), ExitWorktree
---

Bring a finished feature branch into the **primary worktree** by checking it out there, then remove the now-redundant linked worktree under `.claude/worktrees/`. Repo-agnostic — works in any git repo.

**This does NOT merge the feature branch into the default branch** (`main`/`master`). That ref is left exactly where it is. Integrating (push + PR/merge on the remote) is a separate later step the user drives. This command only consolidates the work back into the primary working directory so the user can checkout and test it, and frees the linked worktree.

**HARD RULE: never switch or remove anything without an explicit green light from the user.** Run the read-only pre-flight, present the summary, then STOP and wait for the user to confirm in their own words. Do not stash, push, commit, delete the feature branch, touch the default branch, or ever use `--force`.

## Resolve targets (read-only)

1. **Default branch** `<DEF>`: `git symbolic-ref refs/remotes/origin/HEAD` stripped of `refs/remotes/origin/` (e.g. `main` or `master`). Fallback to `main` if unset.
2. **Feature branch / worktree** = `$1`.
   - If `$1` is empty, infer from the current location: if this session is inside a linked worktree (`git rev-parse --absolute-git-dir` contains `/worktrees/`), use its checked-out branch (`git rev-parse --abbrev-ref HEAD`) and its worktree path.
   - Otherwise ask the user which feature to promote.
   - Resolve the actual linked worktree path for the branch from `git worktree list --porcelain` (do not assume a naming convention — read it).
3. **Primary worktree** `<MAIN>` = the first entry in `git worktree list --porcelain` (the `worktree` line), i.e. the repo's primary working directory — NOT a path under `.claude/worktrees/`. Capture its absolute path. Do not assume it is currently on the default branch.
4. Confirm both the feature branch and its linked worktree exist; if not, STOP and report.

## Pre-flight inspection (read-only — show all of this to the user)

- **Work the branch carries:** `git -C <MAIN> log --oneline <DEF>..<branch>` — the commits that will come into the primary worktree.
- **Linked worktree must be clean:** `git -C <linked-worktree> status --short`. If dirty, **STOP** — removing it would lose work. Tell the user to commit first (or offer to, only with explicit go-ahead).
- **Primary worktree must be clean:** `git -C <MAIN> status --short`, and note its current branch (`git -C <MAIN> symbolic-ref --short HEAD`). If dirty, **STOP** — switching it would fail or drag changes across branches. Do not stash.

## Green light

Present a one-screen summary:
- feature branch + the commits it carries,
- that `<MAIN>` will be switched onto `<branch>`,
- that the linked worktree will be **removed**,
- that the default branch is left **untouched**,
- any warnings (dirty trees, branch diverged from `origin/<DEF>`).

Then **STOP and ask the user to explicitly approve.** Proceed only on a clear yes.

## Promote (only after approval)

Order matters — release the linked worktree before checking its branch out elsewhere:

1. If this session is currently inside the linked worktree, leave it first: call `ExitWorktree` with `action: "keep"` (preserves the worktree + branch on disk and returns the session to its original directory). **Never use `remove` here** — that would delete the branch you are trying to promote.
2. `git -C <MAIN> worktree remove <linked-worktree>` — refuses on a dirty worktree (no `--force`); if it aborts, **STOP** and report.
3. `git -C <MAIN> switch <branch>` — if it aborts (e.g. "local changes would be overwritten"), **STOP immediately**, show the exact error, leave everything as-is. Do not stash or resolve on the user's behalf.

## After a successful promote

Report:
- `<MAIN>` is now on `<branch>` at `git -C <MAIN> rev-parse --short HEAD`.
- The default branch is unchanged — state this explicitly.
- If the branch has diverged from `origin/<DEF>`, note it and **offer** (do not perform) a rebase onto the latest default before the user pushes.
- The feature branch is now the active checkout in `<MAIN>`; do **not** delete it. Run `/worktree-cleanup` after the user has merged. Pushing / opening a PR is left to the user.
