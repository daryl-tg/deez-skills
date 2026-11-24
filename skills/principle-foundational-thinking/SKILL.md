---
name: principle-foundational-thinking
description: "Apply before writing logic: choosing core types and data structures, sequencing scaffold before features, asking what concurrent actors share. Get the shape right and the rest becomes obvious."
disable-model-invocation: true
---

# Foundational thinking

Get the data shape right before writing logic. Define core types early, trace
every access pattern, and choose structures that match the dominant paths. A
data-structure change late is a rewrite. Early, it is often a one-line diff.
DRY the structure, not every line. Three similar statements still beat a
premature abstraction.

Before sharing state between actors, ask what happens if another actor modifies
it concurrently. If the answer is not "nothing", isolate, per
**principle-separate-before-serializing-shared-state**.

Scaffold first. Remove dead code, then build whatever helps every later unit
(CI, linting, test infrastructure, shared types). Setup before features, tests
before fixes. Each increment lands a coherent abstraction or deepens one that
exists, never a capability spread across callers as special-case coordination.
Keep commits small and single-purpose.
