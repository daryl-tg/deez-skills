---
name: principle-attack-the-premise
description: "Apply when two or more fixes that share one premise have failed the same gate. Write the premise down, take a census of which actors hold the imbalance, then question the premise instead of writing a third fix that assumes it."
disable-model-invocation: true
---

# Attack the premise

When two or more fixes that share one premise have failed the same gate,
suspect the premise, not the fixes.

**Why:** each failure under a shared premise is evidence about the premise. A
third fix that assumes it is the most expensive way to collect a fourth piece of
the same evidence.

- **Write the premise down.** It is the one sentence every failed fix assumed.
  Until it is written, you cannot tell whether the next fix assumes it too.
- **Take a census before the next fix.** Count the imbalance per actor. The
  census answers which actors hold it, not how large it is. Write it as a
  rerunnable script, per **principle-build-the-lever**, so the next run compares
  against this one.
- **Read the skew.** If the same few actors hold most of the imbalance on every
  run, something assigns them that role. Find what assigns it. That assignment
  is the next why, per **principle-fix-root-causes**.
- **Remove the asymmetry rather than compensate for it**, per
  **principle-laziness-protocol**. Rotate the role, randomize the assignment, or
  move it, so no actor holds it on every run. A return path, a shared pool, a
  batched handoff, or a periodic rebalance all leave the assignment in place and
  add work on every run.

**Stop:**

- Do not start the next fix before the premise is written and the census exists.
- If the census is even across actors, the premise is not the cause. Look
  elsewhere and keep the census as evidence.

Distinct from **principle-redesign-from-first-principles**, which rebuilds a
design around a new requirement. This one questions a fact the current design
already assumes.
