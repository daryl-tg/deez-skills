### Pause safely

**You own a clean stop.** Leave a checkpoint a cold-start session can resume
from without you.

Explicit only. "Pause safely", "I am going offline", "restarting the CLI", and
the moment before context compacts. "Keep going" and "going to bed, keep going"
mean continue, not pause. `playbooks/agentic-loop.md` already checkpoints per
goal.

1. **Stop at a safe boundary.** Finish the current atomic step or back out of
   it. Never stop mid-edit in a known-broken state. Start nothing new. Cancel
   every delegate still running. A delegate that finishes into a dead session
   writes work nobody reads.
2. **Do not cross an irreversible line to pause.** No push, no review request,
   no announcement you did not already owe. Pausing is not delivering.
3. **Make the work durable.** Commit the tree as one `wip:` commit on the
   current branch so nothing lives only in your context. If it does not build,
   say so in the commit body in one line. The rebase before delivery squashes it
   away, per **principle-one-commit-lands**.
4. **Stop what the run started.** Release the ports this run allocated from the
   `18097`-`18197` band and leave every reserved port alone, per
   **principle-bind-assigned-ports**. A server that outlives its session serves a
   tree nobody is editing.
5. **Write the resume note off-context**, as `resume.md` in the task's dev-notes
   folder, per **principle-planning-docs-live-outside-the-repo**. An in-context
   plan does not survive summarization, and that folder is what the next session
   reads. Capture the intent, where you stopped, what is verified against what is
   only claimed, the branch and head SHA, the next action, and the gotchas. Point
   at a **show-me-your-work** trail rather than copying it.

**Reply:** where you stopped, what is on disk against what is still in your head
with paths and no diff dumps, the commits you made and whether the tree is
clean, the resume note path, and the first action on resume. This is a pause,
not a final report. `playbooks/session-pickup.md` reads the note back.
