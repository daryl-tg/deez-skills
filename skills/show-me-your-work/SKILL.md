---
name: show-me-your-work
description: "Keep an auditable decision trail as a committed TSV during long or unattended runs. Use when the operator will review after stepping away, or when the reasoning has to survive the session."
disable-model-invocation: true
---

# Show me your work

A decision trail the operator can read after the fact, when they were not
watching it happen.

## The file

One TSV, appended as you go, never rewritten. Columns:

```
time	phase	decision	reason	evidence	result
```

- **time** absolute, never "recently".
- **phase** which playbook step this belongs to.
- **decision** what you chose, in one line.
- **reason** why, including the alternative you rejected.
- **evidence** a path, a command, or a URL. Never a summary.
- **result** what happened, filled in when known. An empty result is an open
  item, which is the point.

## Rules

- **A row as each unit lands**, not the whole trail written at the end. A trail
  reconstructed afterwards is a story, not a record.
- **Evidence is a pointer, not prose.** Prefer something a reviewer can rerun,
  per **build-the-lever**.
- **Log the reversals too.** A hypothesis that failed and what it cost is the
  most useful row in the file.
- **Commit it** when the run is large enough that the reasoning has to be
  auditable later, such as a migration or an overnight run. Keep it local
  otherwise. Never commit it into a product repo as a planning doc, per
  **principle-planning-docs-live-outside-the-repo** — it goes to the task's
  dev-notes folder unless it is genuinely part of the change.

**Reply:** the trail's path, the decisions that mattered, and the open rows.
