### Forensics

**You own the diagnosis, not the fix.** The deliverable is a cited cause with a
source location. Hand it back to `playbooks/bug-fix.md` or
`playbooks/perf-issue.md` once the mechanism is known.

Two entry points, one job.

- **Live.** "Why is X leaking, spinning, or stuttering." You capture the signal
  yourself. Instrument the running process. Do not theorize from source.
- **Dropped artifact.** A `.cpuprofile`, a `Trace-*.json.gz`, a `Spindump.txt`,
  or a `.heapsnapshot` handed to you with "why is this slow". The capture is a
  fixed dataset. Read it. Do not re-run it.

1. **Get the artifact.** Live, capture it on the matching surface through the
   repo's `verify-<app>` skill. A CPU profile for a spinning process, a heap
   snapshot for a leak, a trace for a visual glitch. Dropped, identify the format
   and open it with the tool that reads it. Either way it is a real artifact, not
   a guess.
2. **Reach a queryable shape before you read.** Dump the trace or snapshot into
   sqlite, one row per sample, frame, or node, then query it. Parsing large
   artifacts is delegate work, per **principle-guard-the-context-window**. Only
   the reduced finding comes back to the lead.
3. **Reduce it to the smoking gun.** The frames holding the most time, walked to
   the hot path. The retainer chain from the leaked object to a GC root. The
   loop firing without input. The thread stuck on-CPU with its wait reason.
4. **Prove the mechanism before believing it.** Live, inject instrumentation or
   patch the running process to confirm the hypothesis cheaply. Dropped, diff a
   paired before and after capture. With neither, say plainly that this is the
   strongest hypothesis the artifact supports, not a confirmed cause. A
   plausible cause is often wrong while the real one sits one layer over.
5. **Attribute it to source.** File, symbol, and the line that allocates or
   schedules. A frame with no source mapping is not yet a diagnosis. Resolve the
   symbols, or say the artifact does not carry them.
6. **Stop at the diagnosis.** No fix unless asked. The fix is a separate run
   under the playbook that owns it, and it starts by reproducing what you found.

**Reply:** the signal or artifact and its format, the reduced finding, how you
proved the mechanism or why it stays a hypothesis, the source location, and the
artifact paths.
