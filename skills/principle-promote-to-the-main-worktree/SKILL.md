---
name: principle-promote-to-the-main-worktree
description: "Apply after rebasing a finished feature. Check the branch out in the main worktree so the local dev stack runs it and the operator can test manually. Promotion is not a merge."
disable-model-invocation: true
---

# Promote to the main worktree

Once implementation is complete and rebased, check the feature branch out in the
main worktree.

**Why:** the main worktree drives the local dev stack. Promotion is how a
finished feature becomes something the operator can actually use and test on the
machine in front of them. Skipping it removes the manual-test surface entirely,
which is the step most often dropped.

**Promotion is not a merge.** Nothing lands on main. The branch is simply what
the primary worktree has checked out.

**Order.** Rebase onto current `origin/main` and resolve conflicts first, then
promote, then push the branch, then open the review request. Promoting an
unrebased branch puts a stale stack in front of the operator.

Never use a generic promote command in a repo whose own workflow owns
promotion. The owning skill's version runs the gates the generic one skips.
