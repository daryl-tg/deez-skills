---
name: principle-announce-the-linked-review
description: "Apply at the end of any delivered change. Announce as a title line, a body in the operator's /adhd voice, and the PR or MR link — nothing else — then read the announcement back to confirm it posted."
disable-model-invocation: true
---

# Announce the linked review

Work ends with an announcement carrying the review link, and the announcement is
read back to confirm it landed.

**Why:** an unannounced change is invisible to everyone who did not watch it
happen. A post that silently failed is worse than none, because the sender
believes it went out.

**The shape.** Three parts, in this order, and nothing else:

1. **A title line.** What changed, in one line, in the reader's terms.
2. **A body.** What is different for someone using the product now. A short
   paragraph or a few bullets, not a changelog of files.
3. **The PR or MR link.** On its own line, last.

Leave out the evidence or preview URL, the gate results, the test counts, the
branch name, and what is still open. Whoever cares opens the link for all of
that. A room announcement is a notification, not a report, and the operator
reads these rooms on a phone: anything past the link is scrolling.

**Write it in the operator's `/adhd` voice.** Read
`~/.claude/commands/adhd.md` and apply it to the announcement text, whether or
not the mode is on for the session. The rules that bite here:

- Lead with what now works. Not context, not what the work was.
- Number anything multi-part, five items or fewer, one bounded item each.
- Cut preambles, recaps, tangents, and closing pleasantries.
- State a change as its outcome, not its process.

The fuller version of that style is the operator's `i-have-adhd` plugin skill,
which only they invoke (`/i-have-adhd`). The `/adhd` command file is the part
an agent may read and apply on its own.

**The rule.**

- The announcement carries the PR or MR URL, not a branch name and not a
  summary alone.
- Post, then **read it back** from the room. A send that returned no error is
  not proof of a message that exists.
- Announce once, at the end. Never per goal inside a loop: a loop announces when
  the whole candidate is delivered, not per milestone.
- No announcement before approval. See
  **principle-visual-approval-gates-delivery**.
