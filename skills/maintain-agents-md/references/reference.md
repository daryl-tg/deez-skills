Create or update AGENTS.md — the document you wish you
had before reading the first line of code.

Your job is to orient someone (human or agent) who is
about to dive into this codebase. Give them the terrain,
not the coordinates. Anything `grep` or `find` can
answer does not belong here.

## How to Build It

1. Study the codebase. Read code, build it, run it,
   trace the important paths.
2. Identify what was hard to figure out — the things
   that aren't obvious from the directory structure,
   file names, or reading any single file in isolation.
3. Write that down.

## What Belongs in AGENTS.md

Focus on **architecture**: subsystems, how they relate,
data flow, key abstractions, layering, non-obvious
contracts, and conventions that would be silently
violated by someone who didn't know about them.

The litmus test: **would this sentence survive a
500-line refactor?** If a single commit could make it
wrong, it's too specific. Don't document flag names,
file lists, option enumerations, or current behavior
that may shift — document the *structure* and the *why*.

## Use `docs/` for Depth

AGENTS.md is the map, not the encyclopedia. When a
subsystem or topic needs more than a couple of
paragraphs, create a `docs/<topic>.md` and reference
it from AGENTS.md.

Each reference must include a one-liner describing what
the doc covers and **when you'd need it**, so a reader
can decide whether to load it without opening it.

Example:

```
- `docs/storage.md` — Persistence layer: write-ahead
  log, compaction, crash-recovery invariants. Read this
  before touching anything under `src/storage/`.
```

## What Does NOT Belong

- Lists of files or directories (an agent will find
  them)
- Anything that restates what the code already says
  plainly
- Detailed API surfaces, CLI flags, config knobs —
  these change constantly
- Version-specific behavior or temporary workarounds

## Writing Style

Write plain, direct prose. Avoid filler transitions, inflated
stakes, repeated metaphors, and bullets that all start with a
bold keyword.

Wrap lines at 80 columns. Code can exceed 80 when
breaking the line would hurt readability, but prose
should not.
