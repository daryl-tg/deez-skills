---
name: principle-minimize-reader-load
description: "Apply when reviewing or shaping code that is hard to trace. Count the layers between question and answer, and the hidden state the reader must hold. Collapse one-caller wrappers, shrink mutable scope."
disable-model-invocation: true
---

# Minimise reader load

Maintainability is the work a reader must do. Track two axes:

1. **Layers to trace.** How many indirections sit between the question and the
   answer.
2. **State to hold.** How much hidden or mutable context the reader must keep in
   their head.

They are independent. A flat file with fifty globals is as hard as a six-layer
adapter stack. Guard both. This is the human analogue of
**principle-guard-the-context-window**: working memory is finite for readers too.

- **Collapse layers that do not earn their keep.** Wrappers with one caller,
  adapters with no second implementation, indirection for a future that never
  came. Inline them.
- **Make adjacent layers change the abstraction.** A layer repeating the same
  methods and arguments adds load without compression.
- **Demand interface compression.** A broad interface hiding little complexity
  makes readers learn both the surface and the implementation.
- **Shrink state scope.** Pure functions over mutations, locals over fields,
  fields over module state, module state over globals. Derive instead of sync.
- **Name the invariant at the boundary**, not in every consumer, so the reader
  learns it once.

Before adding a layer or a piece of state, ask whether it reduces reader load
somewhere else by at least as much.

**The test:** can a new reader answer "where does X come from?" and "what can
change X?" in under thirty seconds? If not, cut layers or cut state.
