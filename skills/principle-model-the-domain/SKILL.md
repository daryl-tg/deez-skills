---
name: principle-model-the-domain
description: "Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files. Encode the domain in a structure instead of scattered conditionals."
disable-model-invocation: true
---

# Model the domain

Encode the domain in a data structure instead of scattering it across
conditionals. The right structure makes invalid states unrepresentable and
deletes branches. Choosing it at write time is cheap. Recovering it later reads
as a refactor and gets deferred.

Reach for a state machine instead of scattered booleans or phase checks, a typed
model instead of loose parameters, a map, registry, or discriminated union
instead of branching spread across files, a reducer instead of ad hoc mutations,
and an index, queue, or normalised collection where the access pattern calls for
it. Organise a module around one body of domain knowledge, not one step of a
load, validate, save sequence. Execution order is not ownership.

Do not force it. Keep boring code when the shape is clear, local, and unlikely
to grow, and distrust an abstraction that adds indirection without removing
branches or invalid states.

The sign that you skipped this is a feature that grows an if/else chain by one
more branch, or a second boolean that must stay in sync with the first.
