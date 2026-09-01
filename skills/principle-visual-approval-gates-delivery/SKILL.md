---
name: principle-visual-approval-gates-delivery
description: "Apply before promoting, opening a review request, or announcing. Published evidence must exist and be approved first. Approval is the operator's, never inferred."
disable-model-invocation: true
---

# Visual approval gates delivery

Nothing is promoted, reviewed, or announced until evidence has been published
and the operator has approved it.

**Why:** approval is the one gate an agent cannot self-issue. Everything else in
the pipeline can be checked mechanically; whether the result is *right* is a
judgement the operator makes by looking.

**The rule.**

- Capture the pair: an accessibility snapshot and a screenshot. The snapshot is
  diffable and survives a restyle; the screenshot is what a person reads.
- Publish a revision through the device-owned renderer at
  `/<run-id>/<revision>/`. Never author a revision `index.html` by hand.
- Hand back the review URL and stop. Silence is not approval, and a passing
  check is not approval.
- Any change that can affect rendering invalidates the current revision. Publish
  a new one rather than pointing at a stale URL.

**Never hand over an untunnelled URL.** Agent test servers on `18097`–`18197`
are unreachable from the operator's machine, so one offered as a review link is
a dead end that reads as a working one. See **principle-bind-assigned-ports**.
