### Opening a review

Invoked at the end of every delivering playbook. Applies
**principle-rebase-pr-squash** and **principle-one-commit-lands**.

1. **Rebase** onto current `origin/main`. Resolve every conflict in the
   worktree. Never consolidate commits locally.
2. **Promote**: check the branch out in the main worktree, per
   **principle-promote-to-the-main-worktree**, so the local dev stack runs it
   and the operator can test manually.
3. **Evidence must already exist and be approved**, per
   **principle-visual-approval-gates-delivery**. If it does not, stop here.
4. **Push the feature branch only.** Never main. Never push unless the operator
   asked.
5. **Open the PR or MR** with the standard body: what changed, why, how it was
   verified, and the evidence URL.
6. **Announce** with the link and read the announcement back, per
   **principle-announce-the-linked-review**.
7. **Clean up** the worktree.

Landing, where the family lands, is squash-merge **through the review request**.
Never a local merge, in any repository.

**Reply:** the review URL, what it contains, what was verified, what is open.
