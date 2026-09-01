---
name: principle-feature-branch-isolation
description: "Apply before starting any change. Work happens on daryl/<kebab-words> in its own worktree, never on main, never in the primary worktree."
disable-model-invocation: true
---

# Feature branch isolation

Every change gets its own branch, `daryl/<one-to-five-kebab-words>`, in its own
worktree.

**Why:** the primary worktree drives the local dev stack. Editing it directly
means the running stack and the change under construction are the same thing,
so nothing can be compared against a known-good baseline.

**The rule.**

- Branch off current `origin/main`, never off a stale local main.
- One feature, one worktree, one branch.
- Never commit on main. Never push main. See **principle-rebase-pr-squash**.
- Parallel workers get a worktree each, per
  **principle-separate-before-serializing-shared-state**.
- Clean up the worktree once the branch is promoted. No dangling worktrees.

Promotion is a separate step and does not mean merging. See
**principle-promote-to-the-main-worktree**.
