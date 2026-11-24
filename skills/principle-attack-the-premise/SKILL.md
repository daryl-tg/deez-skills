---
name: principle-attack-the-premise
description: "Apply when two or more fixes that share one premise have failed the same gate. Write the premise down, find an observation that would differ if it were false and make it, then remove the condition instead of writing a third fix that assumes it."
disable-model-invocation: true
---

# Attack the premise

When two or more fixes that share one premise have failed the same gate,
suspect the premise, not the fixes.

- **Write the premise down.** It is the one sentence every failed fix assumed.
- **Test it before the next fix.** Find an observation that would come out
  differently if the premise were false, and make it. Look at how the failures
  are distributed, not only at how large they are. Make the check rerunnable,
  per **principle-build-the-lever**.
- **If the evidence contradicts the premise**, look for what the failures share
  that it did not predict. Keep the observation as evidence.
- **Remove the condition instead of compensating for it**, per
  **principle-laziness-protocol**. If the same few actors land on the losing
  side every run, find what assigns them that role, per
  **principle-fix-root-causes**, and change it. A return path, a shared pool, or
  a periodic rebalance leaves the condition in place and adds work on every run.

Do not start the next fix before the premise is written down and tested.
