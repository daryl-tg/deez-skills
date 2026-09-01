### OM Mobile completion

The terminal phase for the mobile family. Unlike OM Chat, this family **lands**.
`local_complete` is not terminal: success is a merged MR, a verified
announcement, and cleanup.

**Landing is squash-merge through the MR.** Never a local merge, never a local
fast-forward. The linear-history guarantee comes from the squash producing one
commit on main.

1. **Verify the candidate** matches what was approved.
2. Run `playbooks/opening-a-review.md` to rebase, promote, push the branch, and
   open the MR.
3. **Land it: squash-merge through the MR.** Then prove it: main's head is the
   squashed commit, and history is linear. Read that back from the remote rather
   than assuming the merge did what was asked.
4. **Announce** the merged change and read the announcement back.
5. **Fast-forward the primary worktree** to the new main.
6. **Clean up** owned worktrees and branches. Only what this run created.

Every step must pass. A run that stops after step 2 is unfinished, per
**principle-finish-or-report**.

**Reply:** the MR URL, the linear-history proof, the announcement confirmation,
and what was cleaned up.
