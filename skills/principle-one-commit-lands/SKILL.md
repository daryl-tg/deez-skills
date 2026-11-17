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
- Main's commit is the PR title plus the squash body, which the forge builds
  from the PR body or from the branch commits' messages (`openmarket-internal`
  uses the commit messages). Every one of them is a receipt agents read back:
  what changed and why, in the repo's commit convention, and nothing else. No
  sign-off or co-author trailers, no tool attribution, no verification notes.
  Verification belongs in the PR body.
