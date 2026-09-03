### Opening a review

Invoked at the end of every delivering playbook. Applies
**principle-rebase-pr-squash** and **principle-one-commit-lands**.

1. **Rebase** onto current `origin/main`. Resolve every conflict in the
   worktree. Never consolidate commits locally.
2. **Promote**: check the branch out in the main worktree, per
   **principle-promote-to-the-main-worktree**, so the local dev stack runs it
   and the operator can test manually.
3. **Hold motion to the bar** when the diff moves anything. Read
   **emil-design-eng**, and **apple-design** for gesture or material work, then
   fix what they flag before you ask for approval. `review-animations` is the
   deeper pass and only the operator can invoke it, so name it in the request as
   `/review-animations` rather than reporting a review you did not run. A diff
   with no motion in it keeps this step as `n/a: no motion`.
4. **Evidence must already exist and be approved**, per
   **principle-visual-approval-gates-delivery**. If it does not, stop here.
   Motion is judged in the recording, not in the code, so the evidence shows it
   running.
5. **Push the feature branch only.** Never main. Never push unless the operator
   asked.
6. **Open the PR or MR** with the standard body: what changed, why, how it was
   verified, and the evidence URL.
7. **Announce** with the link and read the announcement back, per
   **principle-announce-the-linked-review**.
8. **Clean up** the worktree.

Landing, where the family lands, is squash-merge **through the review request**.
Never a local merge, in any repository.

**Reply:** the review URL, what it contains, what was verified, what is open.
