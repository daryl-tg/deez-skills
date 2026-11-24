### Perf issue

**You own the measurement story.** Plan, review, verify the numbers. Every fix
ties to a measurement. Reading source is not measuring.

1. **Capture a baseline.** Drive the surface through the repo's `verify-<app>`
   skill and save the trace or the timing. A repo with no way to drive it gets
   one first, via **create-verification-skill**. No baseline, no perf claim.
   Vet the baseline with **benchmark-checklist** before you plan from it, and
   explain it per **principle-explain-the-number**.
2. **Ground the hypotheses in the code** with the **explore** role over the hot
   subsystem, and the **why** skill when the cost arrived in a regression. Never
   claim a ceiling you have not run.

   Most fixes come from eight families. They generate hypotheses and are not a
   checklist. A family earns an attempt only when the trace shows its signal,
   and a focused fix for the dominant cost beats applying all eight.

   - **Elimination.** Work that does not run is cheapest. A computation nobody
     consumes, a gate always off for this user, a sync that mirrors state
     redundantly, a legacy path kept just in case. A trace shows what is slow,
     never that it is deletable, so this family needs a reading pass. When it
     applies it beats every other family.
   - **Divide and conquer.** The dominant cost scales with input size. Split the
     work so each piece touches less, or so independent pieces run at once.
   - **Caching.** The same computation or fetch repeats on identical inputs.
     Store and reuse it, and name what invalidates it before claiming the win.
   - **Indirection.** The hot path does work a cheaper intermediate could
     absorb. An index instead of a scan, a queue off the interactive thread, a
     handle that lets a cheaper implementation swap in. Add the hop only when it
     removes more from the critical path than it adds.
   - **Batching.** Many small operations each pay a fixed overhead per request,
     query, syscall, or draw call. Coalesce them and pay it once.
   - **Redundancy.** The wait hangs on one slow attempt. Duplicate the work and
     take the fastest result. This trades load for tail latency, so the trace
     has to show the wait dominates and the system has headroom.
   - **Lazy evaluation.** Cost lands on results never used or not needed yet,
     such as eager init on the boot path or offscreen rows. Defer to first use.
   - **Scheduling.** The work must happen, but not during the interactive
     moment. Move it where nobody waits, to idle callbacks, a warmup after boot,
     precompute before the user arrives, cleanup after the frame commits. Often
     that is earlier, not later, which separates it from lazy evaluation. The
     win is perceived latency, so measure the interactive path.
3. **Write the check that fails at the baseline** before the fix, per
   **principle-failing-test-first**. Where a unit-level assertion expresses the
   cost, that is the check. Where only the trace expresses it, the baseline
   number and the failing threshold are the check, both written down before you
   change a line.
4. **Plan the fix from the trace.** Cross a function boundary and the **design**
   skill settles the shape first. Delegate the change to the **executor** role
   with a scope the trace justifies, then review the diff yourself. One attempt
   at a time, each verified before the next, per
   **principle-sequence-verifiable-units**.
5. **Capture the post-fix trace on the same surface** and compare the artifacts,
   not your memory of them. Vet it with **benchmark-checklist** the same way,
   since a delta is only as good as both its numbers. Inconclusive is not a
   pass. Wrong surface is not a pass. Say so and go again.
6. **Cite the measurement in the review.** Baseline, post-fix, delta, artifact
   path, in the body itself.
7. Run `playbooks/opening-a-review.md`.

Sustained improvement of one metric against a target, rather than one fix, is
`playbooks/hillclimb.md`.

**Reply:** the baseline number, the post-fix number, the delta, the artifact
paths, and which family the fix came from.
