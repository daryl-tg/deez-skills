---
name: principle-model-the-domain
description: "Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files. Encode the domain in a structure instead of scattered conditionals."
disable-model-invocation: true
---

# Model the domain

Encode the real domain in a data structure instead of scattering it across
conditionals.

**Why:** scattered booleans, repeated shape assumptions, and branching spread
across files are accidental complexity. A structure matching the domain makes
invalid states unrepresentable and deletes branches. Choosing it at write time
is cheap; recovering it later reads as a refactor and gets deferred.

Reach for a structure that fits:

- A **state machine** instead of scattered booleans, phases, or lifecycle checks.
- A **typed model** instead of loose parameters or repeated shape assumptions.
- A **map, registry, lookup table, or discriminated union** instead of branching
  spread across files.
- A **reducer or command/event model** instead of ad hoc mutations.
- A module organised around **one body of domain knowledge** rather than a
  sequence such as load, validate, transform, save. Execution order is not
  ownership.
- A **queue, cache, index, tree, or normalised collection** where the access
  pattern calls for it.

When none fits, work out what the code must never allow and how the data is
read, then find the structure encoding exactly that.

Do not force an abstraction. Prefer boring code when the current shape is clear,
local, and unlikely to grow. Be skeptical of indirection that removes no
branches, no duplicated rules, and no invalid states.

**The tells that you skipped this:** a new feature that grows an if/else chain
by one more branch, a second boolean that must stay in sync with the first, or
phase-named modules repeating the same domain rules across steps.
