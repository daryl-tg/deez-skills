# 5. Delivery

One sequence, every repository, no exceptions.

1. **Work in the feature worktree** on `daryl/<kebab-words>`. Commit freely.
2. **Rebase onto current `origin/main`** when implementation is complete.
   Resolve conflicts in the worktree.
3. **Promote**: check the branch out in the main worktree.
4. **Push the feature branch only.** Never main.
5. **Open the PR or MR.**
6. **Land through it, squashed.** Never a local merge.
7. **Clean up** the worktree.

## Step 3 is not ceremony

The main worktree drives the local dev stack. Promotion is how a finished
feature becomes something you can actually use on the machine in front of you.
Skip it and you have removed the manual-test surface entirely.

Promotion is **not a merge**. Nothing lands on main; the primary worktree simply
has the branch checked out.

## Step 6 and why not locally

The review request is the record. Squash puts exactly one commit on main.
Nothing reaches main that review did not see, and no local operation can put it
there.

This applies to **every** family. The mobile workflow previously landed by local
fast-forward; it now squash-merges through the MR. The linear-history guarantee
is unchanged — squash produces one commit — but the proof changes from
"fast-forward succeeded locally" to "main's head is the squashed commit".

`bin/doctor` fails any skill whose body instructs a local merge. It knows the
difference between instructing one and forbidding one.

## Commit freely, squash at the end

Incremental commits during implementation are wanted. Do **not** consolidate
locally: no interactive squash, no amend-until-there-is-one. The PR squash
produces the single commit, and the branch keeps the honest history a reviewer
can step through.

One consequence worth internalising: **the PR title and body become main's
commit message.** Write them for someone reading `git log` a year out.

## Approval comes first

Nothing is promoted, reviewed, or announced before evidence is published and
approved. Silence is not approval. A passing check is not approval. And any
change that can affect rendering invalidates the current evidence revision, so
publish a new one rather than pointing at a stale URL.

Next: [Two runtimes](./06-two-runtimes.md).
