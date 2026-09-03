### Hillclimb

**You own the metric and the experiment's integrity.** Supervise and review.
Delegate the attempts. For sustained improvement of one measurable thing against
a target. A single fix is `playbooks/perf-issue.md`. This is the loop.

One change, one measurement, keep or revert. Never stack untested changes, and
never claim a win from reading code. The data decides, per
**principle-prove-on-the-real-surface**.

1. **Ground the workload before choosing the ruler.** Run the **explore** role
   over the target and **teach** for the mental model. Name the dimensions that
   can move the result, data size, history, state, concurrency, and pick a case
   that reproduces the operator's complaint. Nothing reproduces it means fix the
   repro first. Then fix one metric, the direction that counts as better, and a
   stop predicate that pairs a target with a floor on attempts, so a lucky first
   win cannot end the run.
2. **Build the harness, prove it discriminates, then freeze it**, per
   **principle-build-the-lever**. One repeatable command emits the metric,
   sampled past the noise, a median of several runs and not a single one.
   Changing it later invalidates every earlier number. Record the baseline and a
   green regression gate before any change.
3. **Open the decision log** with **show-me-your-work**. One row per attempt.
   Id, hypothesis, change, before, after, delta, gate, verdict, note. Read it
   before each attempt so the search accumulates instead of circling. Keep it
   outside the tree so it survives every revert.
4. **Each hypothesis names a mechanism**, grounded in step 1. "Defer X off the
   boot path because it blocks first paint", never "try memoising something".
5. **Loop, one hypothesis at a time.** Delegate the change to the **executor**
   role with a tight scope and review the diff, per
   **principle-guard-the-context-window**. Independent hypotheses fan out, each
   in its own worktree so they cannot collide, per
   **principle-separate-before-serializing-shared-state**. Measure before and
   after on the frozen harness and run the gate. Accept only when the metric
   clears the noise and the gate stays green. Otherwise revert in full. One
   commit per accepted change, staging only its files. Log the row either way.
6. **Push past the first plateau.** Several rejects in a row means pivot
   category, combine near misses, or try something more radical. Correctness and
   simplicity outrank the number, per **principle-laziness-protocol**. Revert a
   win that breaks behavior. Keep a simplification that holds the number.
7. **Stop on the predicate**, or when the remaining ideas are genuinely
   marginal. Never relax the predicate to declare victory, and never quit while
   cheap untried hypotheses remain. Unattended, borrow only the wake mechanism
   from `playbooks/autonomous-run.md`, not its stop rule.
8. Run `playbooks/opening-a-review.md` with the accepted commits in the order
   they landed, so the climb reads top to bottom.

**Reply:** the metric and target, baseline to final with the delta, iterations
kept against reverted, each accepted change on one line, the log path, and the
best idea you would try next.
