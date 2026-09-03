### Landing

**You own what lands.** Verify each review independently, then land only the
verified one, then keep your hands off the rest. For "land it", "ship it", "merge
when ready", and the half that follows `playbooks/review-to-green.md`.

Green is not the same as safe. Green says the checks ran. Verified says someone
drove the change and watched it work.

1. **The operator's explicit word is the only authorization.** "Land it", "ship
   it", "merge it". A clean verdict never authorizes itself, and neither does an
   approval. Without that word, stop and say the queue is ready.
2. **Know where the family lands.** OM Chat stops at `ready_for_review` and the
   operator lands it. OM Mobile lands by squash-merge through the MR. Everything
   else follows **principle-rebase-pr-squash**. No repository ever merges
   locally, and nothing merges from a feature worktree.
3. **Verify each unit at its own head**, one at a time, through the **verifier**
   role, against the evidence the review claims rather than the review body. A
   unit whose evidence has gone stale goes back to its owner and blocks nothing
   else.
4. **Hold the approval gate.** The published evidence is approved before
   anything lands, per **principle-visual-approval-gates-delivery**. Landing an
   unapproved change is the one failure this playbook exists to prevent.
5. **Rebase last, then confirm nothing changed.** Rebase onto current
   `origin/main`, then check the patch-id is unchanged before landing, per
   **principle-one-commit-lands**. A rebase that altered the change invalidates
   the verdict, so verify again.
6. **Land one at a time and re-verify the next.** Each landing moves trunk under
   everything behind it. Never arm a queue to drain itself.
7. **Announce with the link** and read the announcement back, per
   **principle-announce-the-linked-review**. Then run the family's completion
   playbook once, and `playbooks/cleanup.md` for what the run created.

**Reply:** what landed with its SHA, what is still queued and why, what you
sent back, and what needs the operator.
