### OM Chat completion

The terminal phase for the OM Chat family. **Stops at `ready_for_review`.**
Never merges. Never closes the loop by landing.

Preconditions, all of them: implementation complete, evidence published, the
operator has approved. Missing any one, stop and say which.

1. **Verify the candidate** is what was approved. Re-read the diff; confirm the
   evidence revision matches the current head. Any change that can affect
   rendering invalidates the revision, so publish a new one rather than pointing
   at a stale URL.
2. Run `playbooks/opening-a-review.md`, which rebases, promotes, pushes the
   branch, and opens the review request.
3. **Announce** the linked review request and read it back.
4. **Clean up** run-owned worktrees and state. Only what this run created.

Terminal state is `ready_for_review`, not merged. The operator lands it.

**Reply:** the review URL, the evidence URL, the announcement confirmation, and
what was cleaned up.
