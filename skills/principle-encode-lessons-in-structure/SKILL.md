---
name: principle-encode-lessons-in-structure
description: "Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a check, a type, a lint, or a script instead of more text."
disable-model-invocation: true
---

# Encode lessons in structure

Encode recurring fixes in mechanisms, not in more instruction text. Every error,
correction, and unexpected outcome is a signal. Capture it, route it, close the
loop.

**Why:** text is easy to miss. It requires the reader to notice, remember, and
comply. A lint rule, a type, a runtime check, or a script enforces the rule
without cooperation.

When you catch yourself writing the same instruction twice:

1. Ask whether it can be a type, a lint rule, a runtime check, or a script.
2. If yes, **encode it and delete the instruction.**
3. If it genuinely requires judgement, make the instruction more prominent and
   add an example of the failure mode.

**Pick the strongest rung.** When several mechanisms would work, choose the
strongest the situation allows: a state that cannot compile, then a lint that
fails the build, then a canonical helper, then a runtime check. Agents copy
whatever the surrounding code already does, so a weak guard becomes the next
template.

**Do not paper over symptoms.** If the fix is structural, use only the
structural fix. The instruction is the symptom.

**Anti-patterns:** acknowledging without recording; recording without routing;
fixing one instance while leaving the pattern intact.

This is why `bin/doctor` exists, and why **reflect** moves anything better
served by a check out of the accepted list and into a build request.
