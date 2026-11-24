---
name: principle-sequence-verifiable-units
description: "Apply to multi-step work and to how you stack commits. Break work into small units that each end in a check, verify each before the next, and order delivery so the sequence proves itself."
disable-model-invocation: true
---

# Sequence work into verifiable units

Order work as small units that each end in a state you can check, and do not
advance until the current one is green. A break caught at the unit that caused
it is cheap to localise. Caught after a batch, it is buried under work built on
top of it.

In a sweep, migration, or run of similar edits, each unit is a bracket of
known-good state, one change, the check, then the next unit. Rebase onto clean
trunk first so every check measures the real baseline. Run the per-unit check
even when a tool does the edits, per **principle-build-the-lever**.

**Units are not phases.** A unit is a check inside one continuous pass by one
owner. It is never a phase handed to a later session, a separate delegate, or a
separate review. Build every unit of a feature in the same run. Stopping
between units drops the context the next unit needs, the parts drift from the
plan, and the work left over gets done carelessly or not at all.

Deliver in the order that proves the work. The failing check first, then the
fix. The subtraction before the reshape. The baseline before the treatment. The
scaffold before the feature. Each commit lands on its own, and the sequence
reads as an argument.
