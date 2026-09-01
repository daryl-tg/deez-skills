---
name: principle-type-system-discipline
description: "Apply when designing types or a signature in any statically typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants."
disable-model-invocation: true
---

# Type system discipline

The type checker is a proof assistant. Use it to eliminate impossible states and
unhandled variants at compile time. A case the types let you ignore becomes a
runtime failure the compiler could have stopped.

- **Make illegal states unrepresentable.** Model variants as sum types, not a bag
  of optional fields where contradictory combinations compile.
  `{ completed: boolean; completedAt?: Date }` admits `completed: true` with no
  date, which is meaningless. Derive the boolean, or model the variants.
- **Types are constructions, not restrictions.** Build the type up from the
  values you want rather than carving them out of a looser type with checks. A
  non-empty list is a head plus a rest. A valid range is a start plus a
  duration, not two timestamps you must keep ordered.
- **Brand semantic primitives.** `UserId` and `OrderId` are both strings and must
  not be interchangeable. Validate once at creation, trust the type after.
- **External data is untyped until parsed.** Payloads, JSON, CLI args, config,
  env vars, database rows. A parse function at every boundary — see
  **principle-boundary-discipline**.
- **Do not lie to the compiler.** A cast it cannot verify is a runtime crash
  waiting. Prove the fact or accept that the cast is a hazard.
- **Exhaustive matching is the compiler's job.** Adding a variant must fail the
  build everywhere it is unhandled.
- **Derive from authoritative schemas.** Where a protobuf, OpenAPI spec, or
  migration defines a shape, derive from it. Manual duplication drifts.
- **Strengthen a type only where partiality appears.** A "should never happen"
  throw marks a type that is too weak. Push that check into the type, then stop.
  Extra precision costs reuse and buys no safety.

**The tests:** if you can write a comment explaining when a field combination is
valid, the type is too loose. If two arguments share a primitive and mean
different things, brand them. If a new variant would not break the build, the
match is not exhaustive.
