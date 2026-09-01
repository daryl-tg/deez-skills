---
name: figure-it-out
description: "Design an auditable playbook when no bundled one fits: a large migration, an ambitious multi-part change, or work reviewed after the operator steps away. Scales rigor to the task."
disable-model-invocation: true
---

# Figure it out

When the task matches no playbook, design one. The deliverable before any code
is the workflow itself. Bias toward more rigor: building the wrong thing costs
far more than being careful.

Do not reinvent a playbook you have. A focused single-unit task routes to Bug
fix, Feature, or Refactoring. A large or cross-cutting version of one, or work
the operator reviews after stepping away, belongs here.

## A. Frame

Do not start until you can state:

- **Done as a falsifiable predicate.** "Done well" has to be checkable, per
  **principle-prove-on-the-real-surface**.
- **Scope, quantified.** Rough units and effort, plus the blockers grounding
  surfaced. Raise them before spending hours, not after.
- **The rigor level, biased high.** One-way doors get more. Rigor means gates
  and artifacts, not trying harder.

Present the framing before committing to a long run. Reversible work proceeds,
but a multi-hour run earns one checkpoint.

## B. Design the workflow

Decompose into atomic, independently landable units. Sequence
riskiest-unknown-first so option value stays high.

- **Build the verification harness before the work**, with the baseline captured
  from the pre-change state, so the check reads as old value versus new.
- **Decide what fans out.** Parallelize only across genuine seams, and give each
  worker its own worktree, per
  **principle-separate-before-serializing-shared-state**.
- **Write the phase list down.** That list is what the operator reviews.

## C. Run the loop

Each unit is an experiment: state the hypothesis, make the smallest change,
measure against the predicate on the real artifact, keep it if it advanced,
revert it if it did not. Verify each unit before starting the next.

Pair delegated work with a check and audit the artifacts yourself. If a worker
games the gate, harden the contract. If the gate itself is wrong, fix the gate
in its own change rather than routing around it.

## D. Keep the trail

Log via **show-me-your-work**, a row per decision and per unit, evidence as
links. Commit it when confidence has to be shown later.

## E. Verify and hand back

Check the whole against the Phase A predicate on the real product, not just the
harness. Encode any recurring correction as a gate or a check so the win cannot
silently regress.

**Reply:** the playbook you designed, the rigor level and why, the trail's path,
what is verified, what is open.
