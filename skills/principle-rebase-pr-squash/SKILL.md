---
name: principle-rebase-pr-squash
description: "Apply to every branch delivery. Rebase onto current origin/main, push the branch only, land through the PR or MR squashed. Never merge locally, never push main. No exceptions."
disable-model-invocation: true
---

# Rebase, PR, squash

The delivery sequence, no exceptions, every repository.

1. **Work in the feature worktree.** Commit freely as you go.
2. **Rebase onto current `origin/main`** when implementation is complete.
   Resolve every conflict in the worktree.
3. **Promote** the branch into the main worktree, per
   **principle-promote-to-the-main-worktree**.
4. **Push the feature branch only.** Never main.
5. **Open the PR or MR.**
6. **Land through it, squashed.** Never a local merge.
7. **Clean up** the worktree.

**Why the PR and not a local merge:** the review request is the record. Squash
keeps main linear. Nothing reaches main that review did not see, and no local
operation can put a commit there.

**Never:**

- `git merge` onto main from a worktree, fast-forward or otherwise.
- `git push` to main.
- Mutating local main at all. It tracks the remote and nothing else.

**Every family, including mobile.** There is no repository whose completion
merges locally. Where a workflow previously landed by local fast-forward, it now
squash-merges through the MR: the linear-history guarantee is unchanged, and the
proof becomes "main's head is the squashed commit" rather than "fast-forward
succeeded".

Never push at all unless the operator asked.
