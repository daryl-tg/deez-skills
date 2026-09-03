### Autonomous run

**You own the exit condition.** Define done as a predicate, then drive to it
without stopping. For "run until done", "going to bed, keep going", and any
unattended stretch. A plan of approved goals is `playbooks/agentic-loop.md`
instead. This is one predicate, driven.

1. **State the predicate before the first iteration.** Tests green, the repro
   fixed, the diff at zero, the metric past its target. Checkable by a command,
   not by opinion. A vague goal stalls. A predicate lets you stop.
2. **Pick the wake mechanism.** An event worth watching, a run finishing, a ref
   advancing, gets watched with a long fallback heartbeat behind it. Nothing to
   watch gets a fixed interval sized to when the answer could have changed. Use
   `/loop` in dynamic mode and let each wake report what moved.
3. **One change per iteration**, the smallest the evidence justifies. Verify it
   against the predicate, keep it if it advanced, discard it if it did not, per
   **principle-sequence-verifiable-units**. Anything that "might help" gets
   reverted, never left to ride.
4. **Mid-run discoveries are yours.** Broken skills, flaky checks, related bugs,
   tooling failures, drift. Fix them yourself and keep the predicate as the main
   drive, per **principle-never-block-on-reversible-work**. Out-of-band fixes go
   in their own commit. Surface only an irreversible action, a genuine
   preference call no experiment settles, or a real dead end.
5. **Checkpoint every iteration** with a **show-me-your-work** row for what
   changed and whether the predicate moved. A run with no trail cannot be
   audited or resumed. Before context compacts, run `playbooks/pause-safely.md`.
6. **Deliver nothing mid-run.** No push, no review request, no announcement.
   Those need the operator, and the point of the run is that they are asleep.
7. **Stop when the predicate is met.** A plateau is not a stop. Pivot the
   approach and push past it. Surface a real dead end rather than spinning, and
   never relax the predicate to declare victory.

**Reply:** the predicate, iterations run, what landed, what was discarded, the
trail path, and the predicate's final state.
