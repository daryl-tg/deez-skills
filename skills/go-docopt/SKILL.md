---
name: go-docopt
description: >-
  Go CLI parsing conventions: usage strings, flags, subcommands,
  argument structs, and dispatch.
---
## Scope

Use this workflow for Go CLIs that parse arguments
with `github.com/docopt/docopt-go`.

Not for `flag`, Cobra, or other CLI parsing stacks.

## Workflow

1. Keep `usage` and `version` together at package
   scope.
2. Bind everything into one exported `Arguments`
   struct with `docopt:"..."` tags.
3. Follow the naming convention consistently:
   `Mode*`, `Value*`, and `Flag*`.
4. Choose `ParseArgs` when the binary has a real
   version string; otherwise use `ParseDoc`.
5. Dispatch on parsed mode booleans with a `switch`
   after binding.

## Rules

- Keep one source of truth in the usage string.
- Keep docopt tags aligned with usage tokens exactly.
- Prefer one argument struct over scattered locals.
- Treat subcommands as explicit `Mode*` fields.
- Pair with `go-karma-log` when the same change also
  touches logging or error wrapping in that stack.

## Reference map

Read [reference.md](references/reference.md) for:

- usage-string pattern and version embedding
- `Arguments` struct conventions
- `ParseArgs` vs `ParseDoc`
- subcommand dispatch examples
