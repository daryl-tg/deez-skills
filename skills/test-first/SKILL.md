---
name: test-first
description: "Write the failing check before production code, at the fastest level that expresses the behavior, and report the failing-before evidence. Use before implementing any feature or fix."
disable-model-invocation: true
---

# Test first

The execution loop for **principle-failing-test-first**. The principle states
the rule; this is how you run it.

## The loop

1. **Understand the behavior.** Intended versus current, the affected path, and
   the smallest observable reproduction.
2. **Choose the narrowest executable check.** Prefer the level already used for
   that code path. A unit or integration test for a function, hook, reducer, or
   controller. A real-surface check when the behavior is only observable there —
   a scripted repro through `control-<app>`, a driven simulator journey, a log
   assertion. **One level is enough.** Do not mirror the same assertion at three.
3. **Write it first.** The smallest focused check that would have caught this.
   Encode the intended behavior, not the current implementation.
4. **Run it and watch it fail for the intended reason.** If it passes, or fails
   for an unrelated reason, fix the check before touching the implementation.
   This step is the whole point: a check you did not watch fail proves nothing.
5. **Write the minimum that passes.** If implementation came first, delete it
   and start from the check. Not "adapt it", not "keep it for reference".
6. **Rerun.** Then run the adjacent checks the change puts at risk.

## When a check is genuinely impractical

**Never skip silently.** Before fixing, say why a failing check is impossible or
not worth its cost, then name the closest executable alternative and use that.

**Prefer no new test to a bad one.** A bad test mostly exercises mocks, encodes
implementation details, depends on timing or global state, needs heavy
infrastructure for a small fix, or would be deleted the moment it goes green.

## Guardrails

- Never change a test to match a wrong implementation.
- Never weaken an assertion unless the expected behavior genuinely changed, and
  say why.
- Keep the check focused on this behavior. No fixture churn.
- Update assertions the change breaks and **commit them with the feature**.
  Leaving a maintained test out of the commit ships a red suite.
- `*.spec.*` naming is banned. Follow the repo's existing convention.

**Reply:** name the failing-before run and what it produced, then the
passing-after run and the adjacent checks. If failing-before could not be
demonstrated, say so and name what you used instead.
