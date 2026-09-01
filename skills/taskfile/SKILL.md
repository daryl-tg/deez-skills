---
name: taskfile
description: >-
  Task runner automation: create, revise, or troubleshoot task
  definitions and syntax.
---
## Scope

Use this workflow for `Taskfile.yml` work and Task
automation.

Not for generic YAML editing when the file is not a
Taskfile.

## Workflow

1. Read the current Taskfile and the project's entry
   points before editing. Check existing scripts,
   Makefiles, CI jobs, and README instructions so the
   Taskfile matches the real workflow.
2. Decide which tasks are user-facing and which are
   internal before adding anything.
3. Keep shell bodies short. Move complex logic into
   scripts instead of embedding long bash programs in
   YAML.
4. Use the smallest Task feature that fits. Reach for
   includes, wildcards, prompts, watch mode, or
   fingerprinting only when the task actually needs
   them.
5. Validate with `task --list`, `task --summary`, and
   targeted dry runs or task executions.

## Rules

- Use `version: '3'`.
- Use kebab-case task names.
- Give user-facing tasks a `desc`.
- Use short syntax only for trivial one-command tasks.
- Use `deps` only for prerequisites that can run in
  parallel.
- Use `sources` and `generates` only when they model
  freshness correctly.
- Split into included Taskfiles only when the root
  file is getting hard to scan or namespaces help.
- Prefer explicit `vars` and `env` blocks over deeply
  templated shell.

## Reference map

Read [reference.md](references/reference.md) when you
need syntax or examples for:

- includes and aliases
- loops and wildcards
- preconditions, status, and fingerprinting
- watch mode, prompts, defer, or CLI flags
