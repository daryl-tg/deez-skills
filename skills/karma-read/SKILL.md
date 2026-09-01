---
name: karma-read
description: >-
  Tree-formatted Go logs to structured NDJSON; field, error,
  and context extraction/filtering.
---
## Scope

Use this workflow for karma-go tree-formatted logs
that need to become structured JSON before analysis.

Not for plain single-line logs or already structured
JSON logs.

## Workflow

1. Confirm the input really uses karma tree markers.
2. Prefer `--flat` unless the tree hierarchy itself is
   the thing you need to study.
3. Parse complete entries first, then filter with
   `jq`, `sort`, or other NDJSON-aware tools.
4. Extract fields and counts from parsed JSON, not
   from the raw multi-line text.
5. Switch to nested mode only when parent-child
   relationships in the context tree matter.

## Rules

- Use `--flat` by default.
- Treat raw `grep` on the tree text as a last resort.
- Keep files in order when parsing multiple logs.
- Filter after parsing when the context fields matter.
- Expect auto-typed values in flat mode.

## Reference map

Read [reference.md](references/reference.md) for:

- example karma-go log shape
- flat vs nested output
- common `jq` patterns
- stdin and multi-file usage
