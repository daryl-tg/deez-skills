---
name: principle-attack-the-premise
description: "Apply when two or more fixes that share one premise have failed the same gate. Write the premise down, find an observation that would differ if it were false and make it, then remove the condition instead of writing a third fix that assumes it."
disable-model-invocation: true
---

# Attack the premise

When two or more fixes that share one premise have failed the same gate,
suspect the premise, not the fixes.

**Why:** each failure under a shared premise is evidence about the premise. A
third fix that assumes it is the most expensive way to collect a fourth piece of
the same evidence.

- **Find an observation that would come out differently if the premise were
  false, and make it.** Write the premise down first: the one sentence every
  failed fix assumed. Without it you cannot tell whether the next fix assumes it
  too. Make the observation a rerunnable script, per **principle-build-the-lever**.
- **Remove the condition instead of compensating for it**, per
  **principle-laziness-protocol**. A return path, a shared pool, a batched
  handoff, or a periodic rebalance all leave the condition in place and add work
  on every run.
- **Worked example: a census per actor.** Count the imbalance per actor. If the
  same few hold most of it on every run, something assigns them that role. Find
  what assigns it, per **principle-fix-root-causes**, then rotate, randomize, or
  move the role.

**Stop:**

- Do not start the next fix before the premise is written and the observation
  is made.
- If the observation comes out the same either way, the premise is not the
  cause. Look elsewhere and keep the observation as evidence.

Distinct from **principle-redesign-from-first-principles**, which rebuilds a
design around a new requirement. This one questions a fact the current design
already assumes.
