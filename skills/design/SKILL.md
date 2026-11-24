---
name: design
description: "Settle the shape before writing code: ground, sketch competing designs from the caller's usage, get approval, implement against the sketch, and scrap it when friction repeats. Use for /design, 'design this', or work crossing a function boundary."
disable-model-invocation: true
---

# Design

## 0. Classify, and say which

- **Spike.** A feasibility question whose output is an answer, not code you
  keep. Present the question and the probe in two sentences, get a nod, find out
  cheaply, report a recommendation. Anything built is labelled throwaway.
- **Bounded.** A well-scoped change to a flow that already exists in this repo.
  Ask the questions that matter in one round, per `playbooks/grill-me.md`,
  present a short design in chat, stop.
- **Architectural.** New subsystems, or changes that restructure how components
  fit. Full process below.

Bounded measures the repo, not your familiarity. With no existing flow to
change, it is architectural. When torn, take the heavier path. Hidden
complexity upgrades the path mid-task, and nothing downgrades.

## A. Ground *(architectural)*

Trace every system the change touches, through the **explore** role. When the
design redefines ownership or layering, also run **why**, so the existing
rationale is a constraint rather than a guess. Naming a file is not grounding.

## B. Sketch *(architectural, bounded)*

**Write the caller's usage first**, then derive the types, signatures, and
module map from it. Bodies stay `not implemented`.

**Sketch two structurally distinct shapes** before choosing. A second flavour of
the first does not count. Pick the one where each piece of state has one owner,
each task has one way to do it, internals cannot be imported from outside, no
list is kept in sync by hand, and callers need to know least. The next
contributor is an agent that copies the nearest example, so prefer the design
where a change that looks right from one file is right for the whole repo.

When the fork is open or contested, run one **executor** per candidate in its
own worktree and judge them in one pass by one judge, with the judge rules from
`playbooks/eval.md`.

## C. Agree, **mandatory**

Present the design and **stop**. This gate is not opt-in and is not skipped
because the design looks obvious. Presenting and starting in the same breath is
skipping it.

When the spec is frozen, build it through Claude subagents without asking which
execution path. The design agreement above is the gate. There is no second one.

For architectural work, write the design to the task's dev-notes folder, per
**principle-planning-docs-live-outside-the-repo**, and have it reviewed before
planning.

## D. Plan *(architectural)*

Decompose into units that each end in a check, ordered so the sequence proves
itself. Every step names its files and its verification. No placeholders. A
step saying "add error handling" is a plan failure.

## E. Implement against the sketch

The sketch is the contract. **Surface deviations rather than absorbing them.** If
a function needs a parameter the sketch did not anticipate, say whether the
sketch was wrong, the requirement was missed, or the implementation is
overreaching.

## F. Redesign when workarounds repeat

If implementation keeps producing friction the sketch cannot absorb, throw the
sketch out. The signal is a **repeated pattern**, not one hard case. It shows as
the same workaround in unrelated places, special-case branches for unrelated
edge cases, type escape hatches, a lock where the sketch said nothing was
shared, or callers needing the abstraction's internals.

Re-ground on what was built, redesign as if the new constraints were day-one
assumptions, subtract before adding, and return to B.

**Reply:** the design, the alternatives and why this one, the open decisions.
