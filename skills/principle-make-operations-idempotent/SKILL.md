---
name: principle-make-operations-idempotent
description: "Apply when designing commands, lifecycle steps, or loops that run amid crashes, restarts, and retries. Converge to the same end state regardless of partial prior runs."
disable-model-invocation: true
---

# Make operations idempotent

Design operations to converge to the correct state regardless of how many times
they run or where they start. Every state-mutating operation must answer: what
happens if this runs twice, and what happens if the previous run died halfway?

**Why:** commands, lifecycle steps, and processing loops run where crashes and
retries are normal. If partial state changes the next run's outcome, every
restart becomes a debugging session.

- **Convergent startup.** Scan for existing state, clean stale artifacts, adopt
  live sessions rather than assuming a clean slate.
- **Content-based cleanup.** Compare by content equivalence, not creation order.
- **Self-healing locks.** Detect a stale lock by whether its owner is alive, not
  by its age.
- **Idempotent scheduling.** Failed work respawns cleanly; fresh input is
  regenerated each cycle.

**Three tests:**

1. What happens if this runs twice in a row?
2. What happens if the previous run crashed at each possible point?
3. Does re-execution converge to the same end state?

If any answer is "it depends what was left behind", the operation needs a
reconciliation step.

`bin/link` is the worked example here: rerunning it is safe, a conflicting
destination is moved aside rather than assumed absent, and nothing is deleted.
