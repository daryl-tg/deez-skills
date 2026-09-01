---
name: go-karma-log
description: >-
  Go log lines, wrapped errors, and structured context conventions.
---
## Scope

Use this workflow for Go code that imports the
project log package or `karma-go`, or when a change
should use those libraries for logging and error
wrapping.

Not for generic `slog`, `zap`, or stdlib logging
advice outside this stack.

## Workflow

1. Inspect nearby code first. Match the package's
   existing logging style unless it is already wrong.
2. Pick the correct log call form before writing the
   message.
3. Wrap errors where context becomes known. Add
   `karma.Describe(...)` fields close to the source of
   the failure.
4. If several log calls share the same fields, create
   a child logger instead of repeating them.
5. Run the log linter or project lint/test commands
   after editing.

## Rules

- Use `*f` for plain formatted messages.
- Use `Errorx`, `Warningx`, or `Fatalx` with a real
  `error` value.
- Use `Infox`, `Debugx`, or `Tracex` with a
  `*karma.Context` when you need structured fields.
- Write messages in lowercase infinitive form.
- Do not format an error into the message text.
- Do not use `fmt.Errorf("...: %w", err)` for wrapped
  errors here. Use `karma.Format`.
- Keep static context in child loggers, not in every
  call site.

## Reference map

Read [reference.md](references/reference.md) when you
need details or examples for:

- `*f`, `*x`, and `*ln` call families
- message style and linter expectations
- `karma.Format` and `karma.Describe`
- child loggers, hooks, encodings, and levels
