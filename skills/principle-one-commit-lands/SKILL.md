---
name: principle-one-commit-lands
description: "Apply when delivering a branch. Exactly one commit reaches main, produced by squash at PR merge. Commit freely while implementing; never consolidate locally."
disable-model-invocation: true
---

# One commit lands

Exactly one commit reaches main per change, and it is produced by **squash at PR
merge**.

**Why:** main stays readable and revertable at the granularity of a change,
while the branch keeps the honest step-by-step history a reviewer can follow.
Squashing at the PR gets both. Consolidating locally throws the second away and
adds an interactive rebase that can go wrong.

**The rule.**

- **Commit freely while implementing.** Incremental commits are wanted, not
  something to clean up later.
- **Never consolidate locally.** No interactive squash, no
  amend-until-there-is-one.
- The PR squash produces main's single commit. See
  **principle-rebase-pr-squash**.
- The commit message on main is the PR title and body, so those carry the
  weight. Write them for someone reading `git log` a year from now.
