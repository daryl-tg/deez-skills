### Agentic loop

A plan of several approved goals, run as one bounded loop that dispatches
implementation to Codex. Claude orchestrates; it never hands the loop away.

**Entering this playbook pre-answers the execution gate for the whole run.** Do
not re-ask per goal.

**Stays with Claude by rule**, whatever the goal says: tiny edits, anything
needing session-only tools, all git mutations and pushes, and every review or
validation step.

1. **Read the approved plan** from its dev-notes folder by absolute path. If the
   plan is not frozen, stop: that is the planning gate, and it is not this
   playbook's to skip.
2. **One branch per repository** for the whole run, not per goal.
3. **Per goal:** dispatch implementation to Codex with a self-contained handoff
   citing the playbook path and the principles by name. Resume the thread within
   the run; go fresh at a phase boundary. Review the diff yourself. Run the
   inner-loop verification.
4. **Never deliver a goal.** No incremental push, review request, announcement,
   or promotion mid-loop. A partial candidate is not a deliverable.
5. **When every goal is verified**, run the terminal gate once for the whole
   candidate, then the family's completion playbook once.

**Reply:** goals completed, evidence URL, the single review request, what is
open.
