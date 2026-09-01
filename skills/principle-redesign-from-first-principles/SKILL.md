---
name: principle-redesign-from-first-principles
description: "Apply when integrating a new requirement into an existing design. Redesign as if the requirement had been foundational from day one instead of bolting it on."
disable-model-invocation: true
---

# Redesign from first principles

When integrating a change, do not bolt it onto the existing design. Redesign as
if the requirement had been there from the start. The result should look like
what you would have built knowing it on day one.

- Read all affected files and understand the current design as a whole before
  changing any of it.
- Ask: if we were writing this from scratch with this requirement, what would we
  build?
- Propagate the change through every reference — types, docs, examples, and the
  rationale sections that explain the old shape.
- Think about the redesign holistically, then **deliver it incrementally**, per
  **principle-sequence-verifiable-units**.

This is the method for preserving option value when integrating change. Its
trigger in practice is **principle-exhaust-the-design-space** failing late: if
implementation keeps producing the same shape of friction, the design was wrong
and bolting on another fix compounds it.
