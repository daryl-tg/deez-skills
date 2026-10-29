### Agentic loop

A plan of several approved goals, run as one bounded loop. The lead
orchestrates and never hands the loop away.

Goals go to the **executor** role as Claude subagents. There is no other
execution path.

**Entering this playbook pre-answers the execution gate for the whole run.** Do
not re-ask per goal.

**Stays with the lead by rule**, whatever the goal says: tiny edits, anything
needing session-only tools, all git mutations and pushes, and every review or
validation step.

1. **Read the approved plan** from its dev-notes folder by absolute path. If the
   plan is not frozen, stop: that is the planning gate, and it is not this
   playbook's to skip.
2. **One branch per repository** for the whole run, not per goal.
3. **Per goal:** delegate implementation to the **executor** role with a
   self-contained handoff citing the playbook path and the principles by name.
   Each goal and each fix round gets a fresh delegate with consolidated scope,
   per **principle-delegate-implementation-review-stays-here**. Resume only
   where that principle allows. Review the diff yourself. Run the inner-loop
   verification.
   - **Start with one goal end to end** before running goals in parallel, so a
     flaw in the handoff costs one delegate, not every one.
   - **The handoff carries everything the goal depends on**, including each
     earlier delegate's report pasted in full. Delegates cannot see each other.
     It names the evidence that proves the goal done, the paths it may and may
     not write, and the actions it must not take. If you cannot name the
     evidence, the goal is not scoped yet.
   - **Never message a delegate to check on it.** Judge a stalled one by its
     diff and output, not its status text. Retry by cause: a smaller scope after
     a context limit, the same handoff after a dropped connection, a different
     approach after a tool error. After two retries, drop the goal and replan
     around it.
4. **Never deliver a goal.** No incremental push, review request, announcement,
   or promotion mid-loop. A partial candidate is not a deliverable.
5. **When every goal is verified**, run the terminal gate once for the whole
   candidate, then the family's completion playbook once.

**When the operator returns mid-loop, or a wake has something new**, reply in
the shape of **ketchup**: decisions first, every waiting call decidable from the
reply alone. A wake with nothing new stays silent, as in
`playbooks/autonomous-run.md` step 2.

**Reply:** goals completed, evidence URL, the single review request, what is
open.
