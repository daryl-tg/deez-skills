### Opening a review

Invoked at the end of every delivering playbook. Applies
**principle-rebase-pr-squash** and **principle-one-commit-lands**.

**Resolve the forge first, once.** Read `git remote get-url origin` before the
first review operation and hold that answer for create, edit, view, watch, and
land. GitHub takes `gh`. GitLab takes `glab`, with the **glab** skill for writes
and **labiew** for review threads. Never infer the forge from the directory name
or the last repository you worked in. OM Chat, OM Mobile and the Kiyotaka stack
are GitLab. `openmarket-internal`, home of the daemon and
`packages/rooms-client`, is GitHub.

1. **Rebase** onto current `origin/main` and resolve every conflict in the
   worktree. Never consolidate commits locally.
2. **Promote.** Check the branch out in the main worktree, per
   **principle-promote-to-the-main-worktree**, so the local dev stack runs it
   and the operator can test it by hand.
3. **Hold motion to the bar** when the diff moves anything. Read
   **emil-design-eng**, and **apple-design** for gesture or material work, and
   fix what they flag before you ask for approval. Only the operator can invoke
   `review-animations`, so name `/review-animations` in the request rather than
   reporting a review you did not run. A diff with no motion keeps this step as
   `n/a: no motion`.
4. **Evidence must already exist and be approved**, per
   **principle-visual-approval-gates-delivery**. If it does not, stop here.
   Motion is judged in a recording of it running, not in the code.
5. **Check the title and the branch commits.** The title becomes main's commit
   subject, so write it in the repo's commit convention. When the repo ships a
   message checker, run it on the title and the branch and fix what it flags,
   because CI may never run it. In `openmarket-internal` that is
   `bun scripts/check-commit-message.ts --title "<title>"` and
   `bun scripts/check-commit-message.ts --range origin/main..HEAD`. No Claude
   attribution in a commit or the body.
6. **Push the feature branch only**, from the main worktree, under the
   operator's standing grant once the gates pass. Never main, and never
   force-push a branch someone else pushed.
7. **Open the PR or MR ready for review**, never as a draft (`gh pr create` or
   `glab mr create`, without `--draft`). The body is a one-minute briefing under
   about 40 lines, with these `##` headings in order: Why, What changed, Scope,
   Tradeoffs, Blast Radius, Verification. Scope is always present. Tradeoffs
   appears only when there are some. On Claude, `/mr-markdown` drafts the same
   set. **Never put the evidence URL in it.** That renderer lives on the
   operator's loopback, so the link is dead for every other reader. Describe
   what was driven and what it showed, and put the URL in the reply.
8. **Announce** with the link and read the announcement back, per
   **principle-announce-the-linked-review**.
9. **Clean up** the worktree.

Opening a review does not start `playbooks/review-to-green.md`. Landing, where
the family lands, is squash-merge **through the review request**. Never a local
merge, in any repository.

**Reply:** the resolved forge, the review URL, what it contains, what was
verified, what is open.
