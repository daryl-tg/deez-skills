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

- **Derive each step from the state that exists**, not from what the previous
  run meant to do. Intent died with the run.
- **Apply only the difference** between the state found and the state wanted.
  Never assume a clean slate.
- **Judge staleness by evidence that stays true wherever the previous run could
  have stopped.** Whether a lock owner is alive holds at every crash point. A
  lock's age does not.
- **Write to a temp path and rename into place**, so a crash leaves the old
  file or the new one, never half of either.

**Three tests:**

1. What happens if this runs twice in a row?
2. What happens if the previous run crashed at each possible point?
3. Does re-execution converge to the same end state?

If any answer is "it depends what was left behind", the operation needs a
reconciliation step.

`bin/link` is the worked example here: rerunning it is safe, a conflicting
destination is moved aside rather than assumed absent, and nothing is deleted.
