---
name: principle-foundational-thinking
description: "Apply before writing logic: choosing core types and data structures, sequencing scaffold before features, asking what concurrent actors share. Get the shape right and the rest becomes obvious."
disable-model-invocation: true
---

# Foundational thinking

Structural decisions protect option value. Code-level decisions protect
simplicity. Over-engineering is usually a premature decision that closes a door;
the right foundational data structure keeps doors open.

**Data structures first.** Get the shape right before writing logic. Define the
core types early, trace every access pattern, and choose structures matching the
dominant paths. A data-structure change late is a rewrite. Early, it is often a
one-line diff.

At code level, DRY the structure, not every line. Three similar statements still
beat a premature abstraction. Prefer explicit over clever.

**Concurrency corollary.** Before sharing state between actors, ask what happens
if another modifies it concurrently. If the answer is not "nothing", isolate —
see **principle-separate-before-serializing-shared-state**.

**Scaffold first.** If something helps every later phase, do it first. Ask
whether every subsequent phase benefits from this existing. CI, linting, test
infrastructure, and shared types are scaffold. Setup before features, tests
before fixes.

Each increment should land a coherent abstraction or deepen one that exists. Do
not spread a new capability across callers as special-case coordination.

Subtraction comes before scaffolding: remove dead weight first, then lay
foundations.
