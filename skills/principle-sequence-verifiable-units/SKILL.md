---
name: principle-sequence-verifiable-units
description: "Apply to multi-step work and to how you stack commits. Break work into small units that each end in a check, verify each before the next, and order delivery so the sequence proves itself."
disable-model-invocation: true
---

# Sequence work into verifiable units

Order work as small units, each ending in a state you can check, and do not
advance until the current one is green. The same discipline runs at two
altitudes: how you execute, and how you deliver.

**Why:** a break caught at the unit that caused it is cheap to localise. Caught
after a batch it is buried, and you have already built on a broken base.

**Execution.** In a sweep, migration, or run of similar edits, verify each
change before starting the next. Never batch the edits and verify once at the
end. Each unit is a bracket: known-good state, one change, run the check,
proceed. Rebase onto clean trunk first so every check measures against the real
baseline. When a lever does the edits the per-unit check is nearly free — run it
anyway.

**Delivery.** Stack commits in the order that proves the work. The canonical
shape is the failing check first, then the fix on top: the first unit shows the
bug is real, the next shows it resolved, so a reviewer sees both the problem and
the proof. Other orders that work: a subtraction before the reshape, a baseline
capture before the treatment, the scaffold before the feature.

Each commit should stand on its own, and the sequence should read as an
argument.

The sequencing complement to **principle-prove-on-the-real-surface**, which
keeps each check real, and **principle-build-the-lever**, which makes the
per-unit check cheap.
