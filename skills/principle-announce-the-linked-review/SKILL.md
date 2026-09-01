---
name: principle-announce-the-linked-review
description: "Apply at the end of any delivered change. Announce with the PR or MR link, then read the announcement back to confirm it posted."
disable-model-invocation: true
---

# Announce the linked review

Work ends with an announcement carrying the review link, and the announcement is
read back to confirm it landed.

**Why:** an unannounced change is invisible to everyone who did not watch it
happen. A post that silently failed is worse than none, because the sender
believes it went out.

**The rule.**

- The announcement carries the PR or MR URL, not a branch name and not a
  summary alone.
- Post, then **read it back** from the room. A send that returned no error is
  not proof of a message that exists.
- Announce once, at the end. Never per goal inside a loop: a loop announces when
  the whole candidate is delivered, not per milestone.
- No announcement before approval. See
  **principle-visual-approval-gates-delivery**.
