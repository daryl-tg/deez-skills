---
name: principle-fix-root-causes
description: "Apply when debugging. Trace each symptom to its root cause and fix it there. Reproduce first, ask why until you reach it, resist guards that silence a crash."
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
- **Resist the guard.** Adding a null check to silence a crash is a symptom fix.
- **If a workaround needs a paragraph to justify it, the code is wrong.** Fix
  the code, not the comment.
- **Check for the pattern, not the instance.** Grep for the same shape and fix
  all of them.
- **When stuck, instrument.** Add logging and read what the code actually does.
  Do not guess.

**Restart bugs: suspect state before code.** Code does not change between runs;
state does. When something fails after a restart, suspect stale persistent
state first — config, caches, lock files, serialized state. If clearing a state
file restores behavior, state validation is the fix.

Pairs with **principle-prove-on-the-real-surface**: the repro is what proves the
fix, so it has to exist before the fix does.
