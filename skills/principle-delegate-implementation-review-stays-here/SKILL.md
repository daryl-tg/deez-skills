---
name: principle-delegate-implementation-review-stays-here
description: "Apply when handing work to a subagent or another runtime. Implementation delegates; design, review, verification, and git mutations stay with the lead."
disable-model-invocation: true
---

# Delegate implementation, review stays here

Implementation can go to a subagent or to Codex. Design, review, verification,
and every git mutation stay with the lead.

**Why:** delegation buys throughput and a second perspective. It does not buy
judgement. The lead owns the diff regardless of who typed it.

**Non-dispatchable, whatever the routing config says:** planning, review,
verification, git mutations.

**The rule.**

- Delegate with a **specific scope**: file paths, the named data shape, success
  criteria. Vague scope produces vague work.
- **Review the diff yourself** and write your own summary. Never pass through
  what the delegate said. Inspect the artifact, not the self-report.
- **The delegate does not inherit your context.** Every handoff is
  self-contained: cite the playbook by absolute path and the principles by name,
  because those exist on the delegate's runtime too.
- **Fire a fresh delegate rather than chaining an interrupt.** Interrupt-chained
  resumes silently drop directives. Resume within one feature's lifecycle; go
  fresh at a phase boundary with consolidated scope.
- You can spawn a delegate even though you are one. "The task is small" is not a
  reason to skip the review separation.
