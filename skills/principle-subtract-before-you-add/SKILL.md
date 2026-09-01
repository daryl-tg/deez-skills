---
name: principle-subtract-before-you-add
description: "Apply when sequencing an addition, refactor, or rewrite. Remove dead weight, redundant validators, and stubs first, then build on the simpler base."
disable-model-invocation: true
---

# Subtract before you add

When evolving a system, remove complexity first, then build. Deletion gives a
simpler base, which makes the next addition smaller and less brittle.

**Why:** adding to a complex system compounds complexity. Removing first cuts
surface area, reveals the essential structure, and usually makes the next design
obvious.

- Sequence removal before construction.
- Cut before you polish. Reach the minimum before investing in quality.
- Design for observed usage, not speculative edge cases.
- No speculative validators, parsers, or guards beyond what the spec demands.
  Out-of-spec features drag validators behind them: persistence, retry, and
  schema migration each need guards to defend their inputs.
- When a reference has no novel content, delete it rather than leaving a stub.

Make simplification a continual investment. Leave the design slightly simpler
and more capable behind the same or a smaller surface than you found it.
