### Bug fix

**You own this. Plan, review, verify.** Delegate investigation and the fix, and
stay in the lead.

Every shipped line traces to runtime evidence. A change that "might help" is a
hypothesis, not a fix, and does not ship. When evidence refutes a hypothesis,
revert what it motivated.

1. **Reproduce it yourself** on the matching surface, via `control-<app>` and
   the repo's `verify-<app>` skill. Never hand the repro to the operator. If it
   will not reproduce, force it. Synthesize the trigger, tighten conditions, or
   instrument until it fires.
2. **Binary-search the cause.** Seed the candidate hypotheses with the
   **explore** role over the subsystem and the **why** skill for regression
   history, then eliminate until one survives. Each pass takes the split that
   cuts the most remaining space and produces runtime evidence. When state is
   unclear, instrument and read it rather than guess. Confirm the surviving
   mechanism with runtime evidence before designing the fix.
3. **Write the failing check first**, per **principle-failing-test-first**, at
   the level that expresses the bug. Watch it fail for the right reason.
4. **Fix it.** Delegate to the **executor** role with a specific scope and
   review the diff yourself. Smallest change the evidence justifies.
5. **Verify on the same surface as the repro.** The original repro now passes.
   Wrong-surface or inconclusive is not a pass. Say so.
6. Stage so the failing check lands before the fix. The diff tells the story.
7. Run `playbooks/opening-a-review.md`.

**Before handing off,** add any live-driven unmapped surface to its project
skill's `features/` and update the README and provenance, per
`docs/project-verification.md` at the hub root. Publish only the changed map
Markdown with `bin/deez sync-feature-maps`. Capture the recipe while its handles
and proof are in front of you, per **principle-encode-lessons-in-structure**.

**Reply:** what was broken, the root cause, the fix, how you verified. Paste the
failing-then-passing output verbatim.
