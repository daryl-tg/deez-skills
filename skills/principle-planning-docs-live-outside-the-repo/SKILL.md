---
name: principle-planning-docs-live-outside-the-repo
description: "Apply when writing a spec, plan, design doc, research note, or handoff prompt. They live in the dev-notes folder for the task, never in the repo and never committed."
disable-model-invocation: true
---

# Planning docs live outside the repo

Every planning artifact — spec, plan, design doc, research note, task tracking,
handoff prompt — lives in `~/Documents/dev-notes/<task-slug>/`. One folder per
task. Never in a repo, never committed, nothing to gitignore.

**Why:** the folder is a shared control centre. Subagents read it, every worktree
reads it, and it survives the branch it was written for. A plan committed into a
repo is invisible from a sibling worktree and dies with the branch.

**The rule.**

- Dated files: `YYYY-MM-DD-<topic>-design.md`, `YYYY-MM-DD-<topic>-plan.md`.
- Delegation briefs and handoff prompts as `<role>-handoff-prompt.md`, for
  example `executor-handoff-prompt.md`.
- Every brief opens by naming the task's dev-notes folder and the files to read
  first.
- Reference the plan **by absolute path** in every handoff. A delegate does not
  inherit context, and its working directory may be another worktree, so a
  relative path does not resolve.
- Skills that default to writing plans inside the repo get overridden. This
  outranks their defaults.

Commits carry source and config. They do not carry tests-in-progress notes, QA
artifacts, planning files, or agent handoff notes unless explicitly requested.
