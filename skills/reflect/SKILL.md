---
name: reflect
description: "Mine a finished session for durable lessons and route each to a concrete skill edit, gated on approval. Use when the operator says reflect, or after a complex task where the recipe is worth keeping."
disable-model-invocation: true
---

# Reflect

Turn what a session taught into skill edits. Nothing is applied without
approval.

## When

The operator said reflect. A complex task just landed and the recipe generalizes.
You hit dead ends, found the path, and the path would help next time. The
operator corrected your approach mid-task.

Skip when the session was trivial, or when an existing skill already covered it
and was followed correctly. **One-offs are not learnings.**

## Process

**1. Locate the transcript.** `~/.claude/projects/<slug>/` on Claude,
`~/.codex/sessions` on Codex. If no path resolves, write a tight digest of the
session and use that instead.

**2. Three reviewers in parallel**, on the **explore** role, read-only, each
with a different lens. They return findings; they never edit.

| Lens | Looks for |
|---|---|
| Judgement | Decisions that were wrong or slow, and what would have changed them |
| Tooling | Steps a script, check, or gate would have made unnecessary |
| Divergent | What nobody asked about — the risk that went unexamined |

**3. Synthesize** into **Accepted / Rejected / Backlog**. A finding is accepted
only if it would change a future decision. Require the pattern, not the
instance: something seen once is an anecdote.

**4. Structural enforcement check.** Any accepted item better served by a lint
rule, script, or check moves to Backlog as a build request rather than becoming
more instruction text. More prose is the weakest rung.

**5. Present and wait.** Show the full Accepted / Rejected / Backlog list and
**stop**. Skill edits affect every future session. The operator picks the subset
and may redirect where each lands.

**6. Apply what was approved**, following each item's routing: a one-line
tightening directly; a new section through **superpowers:writing-skills**; a
genuinely new rule as a principle leaf. Run `bin/doctor` on every touched skill.

**Reply:** edits applied with one line each, backlog filed, and what was dropped
with the reason.
