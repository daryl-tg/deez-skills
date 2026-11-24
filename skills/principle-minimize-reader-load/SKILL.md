---
name: principle-minimize-reader-load
description: "Apply when reviewing or shaping code that is hard to trace. Count the layers between question and answer, and the hidden state the reader must hold. Collapse one-caller wrappers, shrink mutable scope."
disable-model-invocation: true
---

# Minimise reader load

Reader load is the work a reader must do to understand code. It has two
independent axes, the layers to trace between the question and the answer and
the hidden or mutable state to hold in their head. Guard both. Working memory is
finite for readers too, per **principle-guard-the-context-window**.

- Collapse layers that only forward. Inline wrappers with one caller, adapters
  with no second implementation, and pass-through methods.
- Shrink state scope. Returns over mutations, locals over fields, fields over
  module state, module state over globals. Derive instead of sync.
- Name an invariant once at the boundary, not in every consumer.

The test. Can a new reader answer "where does X come from?" and "what can change
X?" in under thirty seconds? If not, cut layers or cut state.
