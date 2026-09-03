### Cleanup

**You own the disk and the safety gate.** Prune finished worktrees, stray
simulators, and the servers a run started. Deletion is irreversible, so every
step proves the target is idle before it goes.

**Not for OM Chat or OM Mobile.** Their completion playbooks own their own
teardown. Layering this on top of one removes a worktree the completion step is
still standing in.

1. **List before you delete.** `git worktree list` and `git branch -vv` in the
   main worktree. Name each worktree, its branch, and whether that branch is
   merged, promoted, or unfinished. A branch you cannot classify is not a
   deletion candidate.
2. **Promote before pruning.** A branch that only exists in a feature worktree
   is lost when that worktree goes. Check it out in the main worktree first, per
   **principle-promote-to-the-main-worktree**.
3. **Refuse to delete work.** Uncommitted changes, untracked files that are not
   build output, or unpushed commits on an unmerged branch all stop the
   deletion. Say what is there and ask. **git** covers reading the state
   correctly.
4. **Refuse to delete what is in use.** A worktree with a running server, a
   process holding its path, or a session attached to it stays. Check the ports
   the run allocated from the `18097`-`18197` band, per
   **principle-bind-assigned-ports**.
5. **Release the run's servers.** Stop what this run started and nothing else.
   The reserved ports belong to their owners, and `8098` and `31337` are never
   yours to restart.
6. **Then prune.** `/worktree-cleanup` for a branch the operator has approved
   deleting, and `git worktree prune` for administrative leftovers. Local only.
   Never delete a remote branch.
7. **Stale simulators last.** `xcrun simctl list` then `xcrun simctl delete
   unavailable` for the unbootable ones. Never delete a booted device or one a
   run is driving.

**Reply:** what you pruned, what you refused to prune and why, the space
reclaimed, and what still needs the operator's approval.
