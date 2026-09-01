---
name: maintain-agents-md
description: >-
  AGENTS.md maintenance and repository agent instructions.
---
## Scope

Use this workflow to create or revise `AGENTS.md` as a
high-level orientation document for a codebase.

Not for deep subsystem reference docs, API manuals, or
file inventories. Put deeper material in `docs/`.

## Workflow

1. Study the codebase until you understand what is
   hard to infer from filenames, directory layout, or
   a single-file read.
2. Capture architecture, subsystem relationships,
   invariants, non-obvious contracts, and conventions
   that future work depends on.
3. Keep `AGENTS.md` lean. Move deep topics into
   `docs/<topic>.md` and link them with a one-line
   why-and-when description.
4. Omit file lists, flag inventories, and other facts
   a tool can rediscover cheaply.
5. Before drafting, load `writing-instructions`.

## Rules

- `AGENTS.md` is the map, not the encyclopedia.
- Prefer structure and why over current coordinates.
- If a sentence would not survive a large refactor, it
  is probably too specific.
- Every `docs/` reference must say what it covers and
  when to read it.
- Wrap prose at 80 columns.

## Reference map

Read [reference.md](references/reference.md) for the
full rationale, examples, and exclusions.
