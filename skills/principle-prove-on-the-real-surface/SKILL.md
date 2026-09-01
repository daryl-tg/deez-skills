---
name: principle-prove-on-the-real-surface
description: "Apply after any change, before declaring done. Verify in the running product on the surface the change touches. Tests are necessary and never sufficient; inconclusive is not a pass."
disable-model-invocation: true
---

# Prove on the real surface

Verification happens in the running product, on the surface the change touches.
A green test suite says the code does what the test says. It does not say the
feature works.

**Why:** unverified work has unknown correctness. Indirect verification — file
timestamps, a passing build, a delegate's summary — feels cheaper than looking,
and acting on a wrong inference costs far more than checking.

**The rule.** Match the proof to the change. A UI change is proven by driving
the UI. A CLI change is proven by running the command and reading the exit code.
A migration is proven by replaying real input. A desktop change is proven on
desktop, and separately on cloud, per **principle-desktop-before-cloud**.

**Three verdicts, and only one passes.** VERIFIED, NOT VERIFIED, INCONCLUSIVE.
Inconclusive is not a pass. Wrong-surface is not a pass. Say so rather than
rounding up.

**Trust artifacts, not self-reports.** When verifying delegated work, inspect
the diff, the file, the runtime behavior. Agents report what they intended, not
always what happened.

**When something passes too easily, suspect the observation before the system.**
A blank screenshot satisfies a lazy gate.

The scripted lane is `control-<app>` and runs constantly during implementation.
The agentic lane runs once at the end and produces the evidence pair. Both are
required; neither substitutes for the other.
