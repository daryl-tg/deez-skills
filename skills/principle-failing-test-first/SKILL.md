---
name: principle-failing-test-first
description: "Apply before writing production code. Write the failing check first, at the fastest level that expresses the behavior, and watch it fail for the right reason."
disable-model-invocation: true
---

# Failing test first

No production code without a failing check first.

**Why:** if you did not watch it fail, you do not know it tests the right thing.
A test written after the code tends to assert what the code does rather than
what it should do.

**The law.** Write the check. Run it. Watch it fail *for the intended reason*.
Write the minimum that passes. If implementation came first, delete it and start
from the check. Not "adapt it", not "keep it as reference".

**The check need not be a unit test.** Put it at the fastest level that
expresses the behavior: a unit or integration test for a function, hook,
reducer, or controller; a real-surface check when the behavior is only
observable there. A scripted repro, a driven simulator journey, or a log
assertion is a first-class failing check. One level is enough — do not mirror
the same assertion at three.

**Prefer no new test over a bad test.** A bad test mostly exercises mocks,
encodes implementation details, depends on timing or global state, or would be
deleted the moment it goes green.

**Never skip silently.** If a failing check is genuinely impractical, say why
before fixing, then name the closest executable check you used instead.

**Report the evidence.** Name the failing-before run and what it produced, then
the passing-after run. Update assertions your change breaks and commit them with
the feature; leaving a maintained test out of the commit ships a red suite.
