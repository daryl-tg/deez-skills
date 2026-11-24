---
name: principle-boundary-discipline
description: "Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries; trust internal types and keep business logic pure."
disable-model-invocation: true
---

# Boundary discipline

Validate, narrow types, and handle errors where data crosses a system boundary
(CLI args, config files, external APIs, network, database rows). Inside, trust
the types. Do not re-validate, and do not add nil checks the boundary already
made.

Parse raw data into domain types at the boundary, and keep transport, storage,
and wire types out of the public surface. Keep general mechanism inside and
special-purpose policy at the edge. Business logic lives in pure functions with
no framework dependencies, so it tests without the framework. The shell that
calls them is thin.

Two tests. Is this data crossing a boundary right now? If not, the validation
is redundant. Can this be a pure function the shell just calls? If yes, extract
it.

Where the parsed types come from is **principle-type-system-discipline**.
