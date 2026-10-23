---
name: principle-delegate-implementation-review-stays-here
description: "Apply when handing work to a subagent or another runtime. Implementation delegates; design, review, verification, and git mutations stay with the lead."
disable-model-invocation: true
---

# Delegate implementation, review stays here

Implementation goes to a Claude subagent, the **executor** role. Design,
review, verification, and every git mutation stay with the lead.

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
  because the delegate can load both itself.
- **Every implementation brief names the failing test and its level**, follows
  the repo's test convention, and never creates a `*.spec.*` file. A delegate
  that skips this returns implementation-first code whose TDD order cannot be
  reconstructed. See **principle-failing-test-first**.
- **New work goes to a fresh delegate.** Fix rounds, retries, and the next goal
  get consolidated scope: the original brief, every later directive, the prior
  delegate's report, and its branch and commits. Interrupt-chained resumes
  silently drop directives. Resume only when the work needs state that lives in
  that delegate and is costly to move: a live checkout, uncommitted changes, a
  running process.
- You can spawn a delegate even though you are one. "The task is small" is not a
  reason to skip the review separation.
