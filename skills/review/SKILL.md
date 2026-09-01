---
name: review
description: "Review a diff from the code, with findings sorted into act-on, consider, noted, and dismissed. Use for reviewing a branch, PR, or MR, dead-code checks, or 'would this pass review'."
disable-model-invocation: true
---

# Review

Merges the local review stance with adversarial multi-model fan-out and a
forced verdict per finding.

## Stance

Start from the diff. **Statements of fact over coaching, compliments, or
rhetorical questions.** Short and emotionally detached. If an issue is real, say
it plainly — never "possibly" for something the code shows. If something is
unclear, say exactly what is unclear rather than implying it is wrong.

## Scope

The caller's files, or the current diff against the base branch including the
working tree. Read the whole changed file, not only the hunk: the bug is often
in what the diff leaves in place.

## Fan out

Send the diff to reviewers with **distinct lenses**, not identical ones.
Redundancy finds the same thing twice; diversity finds what one lens cannot see.

| Lens | Asks |
|---|---|
| Correctness | Concrete inputs producing wrong output. Name them |
| Contract | Does this break a caller, a persisted shape, or a message in flight |
| Simplification | What is here that does not need to be |
| Test integrity | Does the test prove the behavior, or restate the implementation |

Dispatch cross-model through **codex-first** or
**herdr-codex-orchestration**. For a decision rather than a diff, **llm-council**
is the right tool and this one is not.

## Categorize — every finding gets a verdict

- **Act on.** Real, in scope, must change before this lands.
- **Consider.** Real, defensible either way. State your recommendation.
- **Noted.** True but out of scope. Record it; do not widen the diff.
- **Dismissed.** Not a real problem. **Say why.** A dismissal without a reason
  is indistinguishable from missing it.

A list of concerns with no verdicts is not a review.

## Skepticism about automated findings

Bots catch real bugs and also file non-issues. Assess each on merit and dismiss
noise with a concrete reason rather than churning code to satisfy it.

**Reply:** the four buckets, most severe first. For each act-on item, the
failure it produces, not just its name.
