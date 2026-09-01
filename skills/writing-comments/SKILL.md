---
name: writing-comments
description: >-
  Explicit comment, docstring, commented-out code,
  or public API documentation work.
---
## Scope

Use this workflow for code comments, doc comments, and
comment review.

Not for prose outside code. Use `writing-instructions` for
agent-facing instructions.

## Workflow

1. Try to remove the need for a comment with better
   names, types, tests, or smaller functions.
2. Delete comments that narrate the obvious or restate
   the code.
3. Keep comments that explain why, warn about
   non-obvious constraints, or document real API
   behavior.
4. Require stronger standards for public API comments
   than for internal helpers.
5. Treat TODOs without a ticket and commented-out code
   as cleanup targets.

## Rules

- Comment the why, not the what.
- If a comment only compensates for unclear code, fix
  the code first.
- Public APIs get doc comments that add real
  information.
- Internal helpers do not need ceremonial doc
  comments.
- Delete changelog comments, brace labels, section
  banners, and reassurance comments.

## Reference map

Read [reference.md](references/reference.md) for:

- anti-pattern catalog and examples
- comments worth keeping
- public API doc-comment guidance
- LLM-specific commenting habits to suppress
