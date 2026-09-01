---
name: go-config-ko
description: >-
  Go config structs with ko tags, YAML/env wiring, defaults,
  and ko.Load call sites.
---
## Scope

Use this workflow for Go code that defines
configuration structs, uses ko struct tags, or loads
config files with `ko.Load`.

Not for CLI argument parsing. Use `go-docopt` when
the task is about command-line args.

Pair it with `go-karma-log` when the same change also
touches error wrapping or logging in a codebase that
uses karma.

## Workflow

1. Read the config struct and its file format first.
   Confirm whether the file is YAML, TOML, or JSON.
2. Put defaults, required checks, and env fallbacks in
   struct tags instead of helper methods.
3. Call `ko.Load` with the explicit unmarshaller for
   the real file format.
4. Validate nested sections by checking parent tags,
   pointer usage, and map element types.
5. Test the precedence you rely on: file, then env,
   then default.

## Rules

- Put defaults in `default:"..."` tags, not in code.
- Use `required:"true"` on the parent field when the
  nested section must be validated.
- Use pointer map values when ko must populate nested
  fields.
- Use pointer fields when unset and zero mean
  different things.
- Pass `yaml.Unmarshal` explicitly for YAML files.
- Keep config loading helpers thin. Let ko do the
  defaulting and validation work.

## Reference map

Read [reference.md](references/reference.md) when you
need details or examples for:

- tag semantics and precedence
- nested structs, slices, maps, and pointers
- optional files and `ko.RequireFile(false)`
- full config examples and common mistakes
