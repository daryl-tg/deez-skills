---
description: After a feature branch has been merged, delete the local feature branch from the main worktree — gated on explicit user approval. Local only; never touches the remote.
argument-hint: <branch> (optional if the main worktree is currently on the feature branch)
allowed-tools: Bash(git switch:*), Bash(git rev-parse:*), Bash(git status:*), Bash(git branch:*), Bash(git symbolic-ref:*), Bash(git log:*), Bash(git -C:*)
---

Clean up a feature branch **after the user has merged it**. Repo-agnostic. Deletes the **local** branch only — remote branch deletion is left to the user on their platform.

**HARD RULE: never delete or switch anything without an explicit green light.** Run the read-only checks, present the summary, then STOP and wait for the user to confirm. Never use `git branch -D` (force delete) and never touch the remote.

## Resolve targets (read-only)

1. **Default branch** `<DEF>`: `git symbolic-ref refs/remotes/origin/HEAD` stripped of `refs/remotes/origin/`; fallback `main`.
2. **Primary worktree** `<MAIN>` = first `worktree` entry in `git worktree list --porcelain`.
3. **Feature branch** = `$1`. If empty, infer from `<MAIN>`'s current branch (`git -C <MAIN> symbolic-ref --short HEAD`) if it is not the default branch; otherwise ask the user.

## Pre-flight (read-only — show to the user)

- `<MAIN>` must be clean: `git -C <MAIN> status --short`. If dirty, **STOP**.
- Confirm the branch looks merged: `git -C <MAIN> log --oneline <branch> --not <DEF>` should be empty (no commits unique to the feature branch). If it is NOT empty, **WARN** the user the branch appears unmerged and ask them to confirm they really want it deleted — but still use the safe `-d` delete, which will refuse if git disagrees.

## Green light

Summarize: which branch will be deleted (local only), that `<MAIN>` will first switch to `<DEF>` if it is currently on that branch, and that the remote is untouched. **STOP and ask for explicit approval.**

## Cleanup (only after approval)

1. If `<MAIN>` is currently on `<branch>`, switch it off first: `git -C <MAIN> switch <DEF>`. If that aborts, **STOP** and report.
2. `git -C <MAIN> branch -d <branch>` — safe delete; if git refuses because the branch is not fully merged, **STOP**, show the message, and ask the user before doing anything further (never auto-escalate to `-D`).

## After cleanup

Report the branch was deleted locally, that the remote was not touched, and that `<MAIN>` is on `<DEF>` at `git -C <MAIN> rev-parse --short HEAD`.
