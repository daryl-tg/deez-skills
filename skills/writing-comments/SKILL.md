---
name: writing-comments
description: >-
  Removing explanatory comments, docstrings, or commented-out
  code, and reviewing a diff for comments that explain code
  or the agent's own work.
---
## Scope

Applies **principle-code-speaks-for-itself**: no comment may
explain code or the work done on it. Use this skill when a
diff or a file carries such comments, or when you are about
to reach for one.

Not for prose outside code. Use `writing-instructions` for
agent-facing instructions.

## Workflow

1. Find the comments the change adds or touches. Notes about
   the work ("added", "fixed", "now uses", "moved from") go
   first.
2. For each, ask what the reader would miss without it, then
   put that into the code: a name, a type, a smaller function,
   or a test that shows the behavior.
3. Delete the comment. Move any reason for the change into the
   commit message.
4. Leave tool directives, required license headers, and shdoc
   tags in maintained shell scripts alone.
5. Leave comments in code the change does not touch. Mass
   deletion outside the diff is scope creep.

## Reference map

Read [reference.md](references/reference.md) for:

- the catalog of comments to delete, work narration first
- ways to make a comment unnecessary
- LLM commenting habits to suppress
