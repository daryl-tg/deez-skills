---
name: principle-build-the-lever
description: "Apply to any non-trivial work: edits, migrations, analyses, checks. Build the tool that does or proves it rather than doing it by hand. The tool is the artifact a reviewer reruns."
disable-model-invocation: true
---

# Build the lever

When the work is not trivial, build the tool that does it instead of doing it by
hand.

**Why:** two payoffs. Throughput, because a script does the work the same way
every time and reruns for free. Confidence, because the tool is one artifact a
reviewer can read and rerun. Hand-done work can only be re-verified by redoing
it. A deterministic script turns "trust me" into "run this".

**Pattern.** Default to building the lever. Skip it only when the task is
genuinely trivial.

- Do the first unit by hand to learn the recipe, then build the tool. Prove it
  by rerunning it on that unit and diffing against the hand-done version.
- Make the lever safe to rerun, because a reviewer will.
- A deterministic lever beats fan-out. If one pass can process every unit, run
  it; do not spawn delegates to hand-apply what a script can do.
- **When you do fan out, write the lever as a skill every delegate reads** —
  the recipe, the verification contract, the do-not-touch fences in one
  artifact. This is how a handoff to another runtime stays consistent instead of
  drifting per prompt. Keep it outside the delegates' write scope.
- **Applying this principle produces a file.** If you cited it and there is no
  script, codemod, generator, or delegate skill in the diff, you did not apply
  it.
- Commit the lever when the work outlives the session.

The bar is triviality, not repetition. A one-off earns a lever when the lever is
what makes the work checkable. Build the smallest thing that does or proves the
job, never a framework.
