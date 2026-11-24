### Feature

**You own the design. Plan, review, verify.** Delegate implementation and stay
in the lead. Plan and build the whole feature in one pass. No phases and no
deferred follow-ups.

1. Route to the **explore** role over the affected subsystem.
2. Run the **design** skill for the shape of anything crossing a function
   boundary. A skip stays as `design skipped: <reason>`. Never fold the decision
   silently into implementation.
3. **Name the data shape first**, and choose its organizing structure before any
   logic. A state machine over scattered booleans, a table or registry over
   branching, a typed model over repeated shape assumptions. React work applies
   **vercel-react-best-practices**. A product motion film follows
   `playbooks/product-video.md`. Component motion is **animate** or
   **animate-expo**. Both are vendored and self-updating, so read them rather
   than recalling them.
4. **Throughput checkpoint**, four todo items. One that does not apply keeps its
   item with `n/a: <reason>`.
   - Blocking first steps, run before any fan-out.
   - Independent workstreams. Disjoint files parallelize. Shared writes
     serialize.
   - Shared mutable state. Default to splitting the target, per
     **principle-separate-before-serializing-shared-state**.
   - One owner by default. The whole feature goes to one worker with the whole
     plan, never phase by phase. Split off a workstream only when its files are
     disjoint and it needs none of the shared context, and name why.
5. **Failing check first**, then delegate implementation to the **executor**
   role with a specific scope. File paths, the named data shape, success
   criteria. Review the diff yourself.
6. **Verify on the matching surface** with `control-<app>`.
7. Rebase into ordered commits, verifying each before the next.
8. Run `playbooks/opening-a-review.md`.

**Before handing off,** add any live-driven unmapped surface to its project
skill's `features/` and update the README and provenance, per
`docs/project-verification.md` at the hub root. Publish only the changed map
Markdown with `bin/deez sync-feature-maps`. Capture the recipe while its handles
and proof are in front of you, per **principle-encode-lessons-in-structure**.

**Reply:** what you built, what you chose and why, open decisions. Tables for
design alternatives.
