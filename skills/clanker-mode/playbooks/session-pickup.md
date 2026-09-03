### Session pickup

Resuming or taking over in-flight work from a prior session, a branch, or
another agent's thread.

1. **Establish what actually exists** before believing any summary. Read the
   branch, the diff against `origin/main`, the worktree state, and whether
   anything is running on an owned port. A handoff note describes intent; the
   repository describes reality.
2. **Run the doctor** for the affected repo. An instance left over from the
   prior session may be serving a tree nobody is editing any more.
3. **Reconstruct the goal** from the dev-notes folder for the task, by absolute
   path, not from the transcript alone. A session that stopped under
   `playbooks/pause-safely.md` left `resume.md` there. Read it for the intent and
   the next action, then hold it to step 1 anyway. It states what the prior
   session believed.
4. **Re-verify the last claimed-complete step** rather than trusting it. This is
   the step most likely to be wrong, because it is the one that was interrupted.
5. **Re-enter the matching playbook** at the first unproven step, copying its
   remaining steps in verbatim.

Never resume by chaining an interrupt onto a stale delegate thread. Start a
fresh one with consolidated scope, per
**principle-delegate-implementation-review-stays-here**.

**Reply:** what state you found, what you re-verified, where you re-entered, and
what remains.
