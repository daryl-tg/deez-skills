---
name: principle-prove-on-the-real-surface
description: "Apply after any change, before declaring done. Verify in the running product on the surface the change touches. Tests are necessary and never sufficient; inconclusive is not a pass."
disable-model-invocation: true
---

# Prove on the real surface

Verify every output by checking the real thing in the running product, on the
surface the change touches. Proxies such as file timestamps, a passing build,
cached output, a delegate's summary, or "it compiles" do not count. A green suite
says the code does what the test says, not that the feature works.

Match the proof to the change. Drive the UI for a UI change. Run the command and
read the exit code for a CLI change. Replay real input for a migration. Prove a
change to code shared by several hosts on each host's own surface, per
**principle-prove-every-host**.

There are three verdicts, VERIFIED, NOT VERIFIED, and INCONCLUSIVE, and only the
first passes. Inconclusive and wrong-surface are not passes. Say so rather than
rounding up.

For delegated work, inspect the diff, the file, and the runtime behavior. Agents
report what they intended, not always what happened. When a check fails or
passes too easily, suspect the observation before the system. A blank
screenshot satisfies a lazy gate.

Script the check. The scripted lane is `control-<app>` and reruns constantly
during implementation. The agentic lane runs once at the end and produces the
evidence pair. Both are required, and neither substitutes for the other. Keep
the output where the human can see it, and commit the trail only when it must
be auditable later, per **show-me-your-work**.
