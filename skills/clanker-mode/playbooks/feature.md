### Feature

**You own the design. Plan, review, verify.** Delegate implementation; stay in
the lead.

1. Route to the **explore** role over the affected subsystem.
2. Run the **design** skill for anything crossing a function boundary. Skipping
   stays as `design skipped: <reason>`; never fold the decision silently into
   implementation.
3. **Name the data shape first**, and choose its organizing structure before any
   logic: a state machine over scattered booleans, a table or registry over
   branching, a typed model over repeated shape assumptions.
   For React work, apply **vercel-react-best-practices**. A product motion film
   or feature demo follows `playbooks/product-video.md`. For component motion,
   **animate** or **animate-expo**. Both are vendored and self-updating, so read
   them rather than recalling them.
4. **Throughput checkpoint**, four todo items. One that does not apply keeps its
   item with `n/a: <reason>`:
   - Blocking first steps, run before any fan-out.
   - Independent workstreams. Disjoint files parallelize; shared writes
     serialize.
   - Shared mutable state. Default to splitting the target, per
     **principle-separate-before-serializing-shared-state**.
   - Smallest safe decomposition. If one worker is best, name why.
5. **Failing check first**, then delegate implementation to the **executor**
   role with a specific scope: file paths, the named data shape, success
   criteria. Review the diff yourself.
6. **Verify on the matching surface** with `control-<app>`.
7. Rebase into ordered commits, verifying each before the next.
8. Run `playbooks/opening-a-review.md`.

**Before handing off:** follow the project verification contract in
`docs/project-verification.md` at the hub root. Add any live-driven unmapped
surface to its project skill's `features/`, update the README and verification
provenance, and automatically commit and push only the changed map Markdown
with `bin/deez sync-feature-maps`. Per **principle-encode-lessons-in-structure**,
capture the recipe while its handles and proof are still in front of you.


**Reply:** what you built, what you chose and why, open decisions. Tables for
design alternatives.
