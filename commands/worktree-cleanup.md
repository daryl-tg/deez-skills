---
description: After a feature branch has been merged, delete the local feature branch from the main worktree — gated on explicit user approval. Local only; never touches the remote.
argument-hint: <branch> (optional if the main worktree is currently on the feature branch)
allowed-tools: Bash(git switch:*), Bash(git rev-parse:*), Bash(git status:*), Bash(git branch:*), Bash(git symbolic-ref:*), Bash(git log:*), Bash(git -C:*), Bash(gh pr list:*), Bash(glab mr list:*)
---

Clean up a feature branch **after the user has merged it**. Repo-agnostic. Deletes the **local** branch only — remote branch deletion is left to the user on their platform.

**HARD RULE: never delete or switch anything without an explicit green light.** Run the read-only checks, present the summary, then STOP and wait for the user to confirm. Use `git branch -D` (force delete) only for a branch the forge reports as merged through a PR/MR, and only after that green light. Never touch the remote.

## Resolve targets (read-only)

1. **Default branch** `<DEF>`: `git symbolic-ref refs/remotes/origin/HEAD` stripped of `refs/remotes/origin/`; fallback `main`.
2. **Primary worktree** `<MAIN>` = first `worktree` entry in `git worktree list --porcelain`.
3. **Feature branch** = `$1`. If empty, infer from `<MAIN>`'s current branch (`git -C <MAIN> symbolic-ref --short HEAD`) if it is not the default branch; otherwise ask the user.

## Pre-flight (read-only — show to the user)

- `<MAIN>` must be clean: `git -C <MAIN> status --short`. If dirty, **STOP**.
- Classify the branch as merged by its PR/MR state first, with ancestry as the fallback. A squash-merged branch is never an ancestor of `<DEF>`, so `git log <branch> --not <DEF>` lists its commits even after it landed. Resolve the forge from `git -C <MAIN> remote get-url origin`, then:
  - GitHub: `gh pr list --head <branch> --state merged --json number,headRefOid`
  - GitLab: `glab mr list --source-branch <branch> --merged -F json` (compare its `sha`)
- **Merged by PR/MR** means a merged entry whose head commit equals `git -C <MAIN> rev-parse <branch>`. A local tip that moved past the merged head carries unmerged work, so treat it as unmerged.
- A forge error (unauthenticated, CLI not installed, no remote match) counts as no merged PR/MR. It never counts as merged.
- No merged PR/MR: fall back to `git -C <MAIN> log --oneline <branch> --not <DEF>`. Empty means merged by ancestry. If it is NOT empty, **WARN** the user the branch appears unmerged and ask them to confirm they really want it deleted — but still use the safe `-d` delete, which will refuse if git disagrees.

## Green light

Summarize: which branch will be deleted (local only), how it was classified (merged PR/MR with its number, merged by ancestry, or unmerged), which delete it gets (`-D` for a merged PR/MR, `-d` otherwise), that `<MAIN>` will first switch to `<DEF>` if it is currently on that branch, and that the remote is untouched. **STOP and ask for explicit approval.**

## Cleanup (only after approval)

1. If `<MAIN>` is currently on `<branch>`, switch it off first: `git -C <MAIN> switch <DEF>`. If that aborts, **STOP** and report.
2. Delete the branch:
   - **Merged by PR/MR:** `git -C <MAIN> branch -D <branch>`. Git's `-d` refuses a squash-merged branch, and the forge's merged state is the proof `-d` cannot see.
   - **Otherwise:** `git -C <MAIN> branch -d <branch>` — safe delete; if git refuses because the branch is not fully merged, **STOP**, show the message, and ask the user before doing anything further (never auto-escalate to `-D`).

## After cleanup

Report the branch was deleted locally, that the remote was not touched, and that `<MAIN>` is on `<DEF>` at `git -C <MAIN> rev-parse --short HEAD`.
