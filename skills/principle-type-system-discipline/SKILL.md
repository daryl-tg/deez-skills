---
name: principle-type-system-discipline
description: "Apply when designing types or a signature in any statically typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants."
disable-model-invocation: true
---

# Type system discipline

Make the compiler reject impossible states, mismatched primitives, and unhandled
variants. A case the types let you ignore becomes a runtime failure.

- **Make illegal states unrepresentable.** Model variants as sum types, not a
  bag of optional fields. `{ completed: boolean; completedAt?: Date }` compiles
  `completed: true` with no date. Derive the boolean or model the variants.
- **Build types up, never carve them out.** A non-empty list is a head plus a
  rest. A valid range is a start plus a duration, not two timestamps you must
  keep ordered.
- **Brand semantic primitives.** If two arguments share a primitive but mean
  different things, give each its own type. Validate once at creation through a
  verifying type guard (`input is AgentId`), never `as`.
- **External data is untyped until parsed.** JSON, RPC payloads, CLI args,
  config, environment variables, and database rows go through a parse function
  at the boundary, per **principle-boundary-discipline**. Annotate a schema with
  the type it proves (`const userSchema: z.ZodType<User>`) so the compiler
  rejects a validator that proves less.
- **Do not lie to the compiler.** A cast it cannot verify is a runtime crash
  waiting. Prove the fact or treat the cast as a hazard.
- **Exhaust variants.** Adding a variant must fail the build everywhere it is
  unhandled.
- **Derive types from authoritative schemas.** When a protobuf, OpenAPI spec, or
  migration owns a shape, derive from it instead of hand-rolling a parallel type.
- **Strengthen a type only where partiality appears.** A "should never happen"
  throw marks a type that is too weak. Push that check into the type, then stop.

The test. If you can write a comment explaining when a field combination is
valid, the type is too loose. If a new variant would not break the build, the
match is not exhaustive.
