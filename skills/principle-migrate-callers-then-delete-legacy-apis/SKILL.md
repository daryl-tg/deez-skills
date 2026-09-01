---
name: principle-migrate-callers-then-delete-legacy-apis
description: "Apply when introducing a new internal API while old callers still exist. Migrate the callers and delete the old API in the same wave rather than keeping a compatibility layer."
disable-model-invocation: true
---

# Migrate callers, then delete legacy APIs

When a new API is the right design, migrate callers and remove the old one in
the same wave. Do not preserve a compatibility layer by default.

- Do not keep a legacy path alive only because internal callers still exist.
- Inventory the callers, migrate them, delete the old API.
- Treat a temporary adapter as exceptional and time-boxed, not as default
  architecture.
- Update tests to assert the new contract, and delete tests that only protected
  pre-refactor implementation details.

**When this applies:** no external consumer depends on the old surface, the
project can absorb a coordinated breaking change, and the new API is part of a
simplification.

Keeping both creates dual-path complexity, slows cleanup, and makes the codebase
feel append-only. Use the **blast-radius** skill to enumerate callers so the
migration wave is complete rather than partial.
