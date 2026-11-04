### Grill me

**You own the questions. The operator owns the answers.** For "grill me",
"interview me", "make sure we agree before you start", and for any point where
two or more genuine product or preference calls are open at once. Testing a
decision against outside opinions is **llm-council**, not this.

1. **Map the decisions as a tree.** Each decision branches into the decisions
   that depend on it. Write the tree to the task's dev-notes folder, so a later
   round or a later session starts from it rather than from memory.
2. **Find the facts yourself.** A question that a file, a tool, or a run could
   answer is not the operator's, per
   **principle-never-block-on-reversible-work**. Route it to the **explore**
   role, or to `playbooks/prototype.md` when only a run settles it. A lookup in
   flight blocks only the questions downstream of it. Ask the rest now.
3. **Ask the whole frontier in one round.** The frontier is every decision
   whose prerequisites are settled. A question that depends on another still
   open in this round waits for the next round. Number each question, and put
   your recommendation under it, worded so that "yes" accepts it.
4. **Wait for the answers, then recompute.** Record each answer in the tree.
   Settled decisions unblock the questions that hung off them, and those form
   the next frontier.
5. **Stop when the frontier is empty.** Every branch visited, nothing assumed
   silently. Play the settled tree back and act only after the operator
   confirms it. If the result is a frozen spec, the execution-path question
   still follows.

**Not under a full-autonomy grant.** Inside `playbooks/autonomous-run.md` or
`playbooks/agentic-loop.md`, decide the calls the grant covers and report each
with its alternative. This playbook needs an operator who is present.

A round looks like this:

```
**Q1. <title>.** <the question, with its options>

Recommended: <answer>. "Yes" accepts it.

**Q2. <title>.** <the question, with its options>

Recommended: <answer>. "Yes" accepts it.
```

**Reply:** one round per turn, in that shape. At the end, the settled tree and
what you will do with it.

Adapted from `grilling` in mattpocock/skills (MIT).
