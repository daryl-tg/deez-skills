---
name: principle-fix-root-causes
description: "Apply when debugging. Trace each symptom to its root cause and fix it there. Reproduce first, ask why until you reach it, a guard is a fix only for a state that is legitimate."
disable-model-invocation: true
---

# Fix root causes

Do not paper over symptoms. Trace every problem to its root cause and fix it
there.

**Why:** symptom fixes accumulate. Each workaround makes the system harder to
reason about, and the real bug remains. Root-cause fixes are slower up front and
reduce total debugging time.

- **Reproduce first.** If you cannot reproduce it, you cannot verify the fix.
- **Ask why until you hit the cause.** The first plausible explanation is rarely
  the last one.
- **Test the guard for legitimacy.** A guard is a fix only when the state it
  handles is legitimate. If the system may be in that state, the code that broke
  on it is the root cause, and handling the state there is the fix. Otherwise
  the guard hides the bug, like a retry, a swallowed error, or a clamped value.
- **If a workaround needs a paragraph to justify it, the code is wrong.** Fix
  the code, not the comment.
- **Check for the pattern, not the instance.** Grep for the same shape and fix
  all of them.
- **When stuck, instrument.** Add logging and read what the code actually does.
  Do not guess. If the deciding fact took a deep dig to find, propose the
  cheap, always-on signal (a log line, metric, or doctor check) that would have
  shown it at first look.

**Restart bugs: suspect state before code.** Code does not change between runs;
state does. When something fails after a restart, suspect stale persistent
state first — config, caches, lock files, serialized state. If clearing a state
file restores behavior, state validation is the fix.

Pairs with **principle-prove-on-the-real-surface**: the repro is what proves the
fix, so it has to exist before the fix does.
