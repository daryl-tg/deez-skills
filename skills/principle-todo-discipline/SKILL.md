---
name: principle-todo-discipline
description: "Apply to any multi-step task. A step you skip stays in the list with a stated reason. Silent omission is not allowed."
disable-model-invocation: true
---

# Todo discipline

Multi-step work opens a todo list, and the list stays honest.

**Why:** the failure is not skipping a step, it is skipping it invisibly. A
plan that quietly loses its verification step looks identical to one that ran it.

**The rule.**

- Copy a playbook's steps in **verbatim** before adding task-specific items.
  Reading a playbook then writing a bespoke plan drops its named steps.
- A step you choose not to do **stays in the list** with `skip: <reason>`. A
  dimension that genuinely does not apply stays with `n/a: <reason>`.
- Mark a step in progress when starting it, complete only when it is actually
  done. Not when the code is written and the check is pending.
- Never mark complete with failing tests, partial implementation, or unresolved
  errors. Blocked stays blocked, and the blocker gets written down.
