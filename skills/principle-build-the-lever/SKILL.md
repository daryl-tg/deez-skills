---
name: principle-build-the-lever
description: "Apply to any non-trivial work: edits, migrations, analyses, checks. Build the tool that does or proves it rather than doing it by hand. The tool is the artifact a reviewer reruns."
disable-model-invocation: true
---

# Build the lever

When the work is not trivial, build the tool that does it (a codemod, script,
generator, or rerunnable check) instead of doing it by hand. A reviewer can
rerun the tool. Hand-done work can only be re-verified by redoing it. The bar is
triviality, not repetition. Skip the tool only for a couple of obvious edits.

- Do the first unit by hand, then build the tool and prove it by rerunning it on
  that unit and diffing against the hand-done version. Make it safe to rerun.
- A deterministic tool beats fan-out. When you do fan out, write the recipe, the
  verification contract, and the do-not-touch fences as one skill every
  delegate reads, kept outside their write scope. That keeps many delegates
  consistent instead of drifting per prompt.
- Applying this produces a file. No script, codemod, generator, or delegate
  skill in the diff means you did not apply it. Commit it when the work outlives
  the session.
- Build the smallest thing that does or proves the job, never a framework.
