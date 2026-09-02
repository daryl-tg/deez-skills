### Feature

**You own the design. Plan, review, verify.** Delegate implementation; stay in
the lead.

1. Route to the **explore** role over the affected subsystem.
2. Run the **design** skill for anything crossing a function boundary. Skipping
   stays as `design skipped: <reason>`; never fold the decision silently into
   implementation.
3. **Name the data shape first**, and choose its organizing structure before any
   logic: a state machine over scattered booleans, a table or registry over
   For React work, apply **vercel-react-best-practices**; for motion,
   **animate** or **animate-expo**. Both are vendored and self-updating,
   so read them rather than recalling them.
   branching, a typed model over repeated shape assumptions.
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

**Before handing off: did you drive a surface the map does not cover?** If the
terminal gate exercised anything with no feature file, write one now, following
the four-H2 contract in `features/README.md`. You have the handles in front of
you and you know what proved it works. A maintenance pass can recover that later
from source, but it costs a full live sweep to learn what you already know right
now. Per **principle-encode-lessons-in-structure**: capture it where it is
cheap.


**Reply:** what you built, what you chose and why, open decisions. Tables for
design alternatives.
