---
name: principle-fix-root-causes
description: "Apply when debugging. Trace each symptom to its root cause and fix it there. Reproduce first, ask why until you reach it, a guard is a fix only for a state that is legitimate."
disable-model-invocation: true
---

# Fix root causes

Fix the fault, not the place where it surfaced. The root cause is the first
place the system did something it should not do, or failed to handle a state it
should handle.

- Reproduce first. The repro is what proves the fix, per
  **principle-prove-on-the-real-surface**, so it exists before the fix does.
- Ask "why" until the answer is a wrong decision in the code. When stuck,
  instrument and read the actual state. Do not guess.
- Ask whether the state that triggered the symptom is legitimate. If it is,
  handle it where the code broke. If it should never exist, a check there hides
  the bug, so find what produced it. Guards, retries, swallowed errors, clamped
  values, and discarded state are the usual ways to hide a bug.
- After a restart, suspect persisted state before code (config, caches, lock
  files, serialized state). If clearing a state file restores behavior, state
  validation is the fix.
- Fix the pattern, not the instance. Find every place with the same fault.
- If a workaround needs a paragraph to justify it, fix the code, not the
  comment.
- If the deciding fact took a deep dig, propose the cheap, always-on signal (a
  log line, a metric, a doctor check) that would have shown it at first look.
