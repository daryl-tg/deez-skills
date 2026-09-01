---
name: principle-boundary-discipline
description: "Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries; trust internal types and keep business logic pure."
disable-model-invocation: true
---

# Boundary discipline

Put validation, type narrowing, and error handling at system boundaries. Trust
internal code. Business logic lives in pure functions; the shell is thin.

**Why:** scattered validation is noisy, redundant, and gives false confidence.
Validate once at the boundary. Keep logic out of framework wiring so it can be
tested without the framework.

- **At boundaries** — CLI args, config files, external APIs, network protocols,
  database rows: validate, return errors, handle defensively.
- **Inside** — typed data, error propagation, no re-validation. Trust the types.
- **Across the boundary** — expose domain concepts, not the boundary's private
  representation. Keep general mechanism inside, special-purpose policy at the
  edge. Do not re-export transport, storage, or wire types through a public
  surface.

**Two tests:**

- "Is this data crossing a system boundary right now?" If not, the validation is
  redundant.
- "Can this be a pure function the shell just calls?" If yes, extract it.

Where the parsed types come from is **principle-type-system-discipline**.
