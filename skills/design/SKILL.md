---
name: design
description: "Settle the shape before writing code: ground, sketch competing designs from the caller's usage, get approval, implement against the sketch, and scrap it when friction repeats. Use for /design, 'design this', or work crossing a function boundary."
disable-model-invocation: true
---

# Design

Merges the classification and approval gate of brainstorming, the technical
artifact of architect, and the decomposition of writing-plans.

## 0. Classify, and say which

- **Spike** — a feasibility question whose output is an answer, not code you
  keep. Present the question and the probe in two sentences, get a nod, find out
  cheaply, report a recommendation. Anything built is labelled throwaway.
- **Bounded** — a well-scoped change to a flow that already exists in this repo.
  Ask the questions that matter, present a short design in chat, stop.
- **Architectural** — new subsystems, or changes that restructure how components
  fit. Full process below.

Bounded measures the repo, not your familiarity. If there is no existing flow to
change, it is architectural. When torn, take the heavier path. Hidden complexity
upgrades the path mid-task; nothing downgrades.

## A. Ground *(architectural)*

Build a real model of every system the new code touches. Route to the **explore**
role. When the design redefines ownership or layering, also run **why**, so the
existing rationale is a constraint rather than a guess. Naming a file is not
grounding.

## B. Sketch *(architectural, bounded)*

**Write the caller's usage first**, then derive the types, signatures, and module
map from it. Bodies stay `not implemented`.

**Design it twice.** Produce at least two *structurally distinct* candidates
before choosing. A second flavour of the first shape does not count. When the
fork is genuinely open, run one **executor** per candidate in its own worktree
and judge them in one judge pass. `playbooks/eval.md` has the judge rules, not
the whole protocol.

Assume the next contributor is an agent that sees only the files it opened,
copies the nearest example, and takes the shortest path that compiles. Prefer
the design where a change that looks right from one file is right for the whole
repo.

Screen every candidate before comparing: shallow modules, information leakage,
temporal decomposition, pass-through layers, and the four that agents trip on:

- **Split ownership.** Two modules write the same state. Give it one owner.
- **Two ways to do one task.** The agent copies whichever it finds first. Keep
  one and delete the rest in the same change.
- **Importable internals.** The shortest path that compiles becomes the
  interface. Make an outside import fail the build.
- **Hand-synced list.** Adding an item means editing every list. Derive them
  from one, or fail the build when they disagree.

Then compare on **interface depth** — prefer the design hiding more complexity
behind a smaller surface.

## C. Agree — **mandatory**

Present the design and **stop**. This gate is not opt-in and is not skipped
because the design looks obvious. Presenting and starting in the same breath is
skipping it.

When the spec is frozen, ask which execution path takes it forward. That choice
is made every time and never auto-picked. This is the standing carve-out from
**principle-never-block-on-reversible-work**.

For architectural work, write the design to the task's dev-notes folder, per
**principle-planning-docs-live-outside-the-repo**, and have it reviewed before
planning.

## D. Plan *(architectural)*

Decompose into units that each end in a check, ordered so the sequence proves
itself. Every step names its files and its verification. No placeholders: a step
saying "add error handling" is a plan failure.

## E. Implement against the sketch

The sketch is the contract. **Surface deviations rather than absorbing them.** If
a function needs a parameter the sketch did not anticipate, say whether the
sketch was wrong, the requirement was missed, or the implementation is
overreaching.

## F. Scrap when the architecture is wrong

If implementation keeps producing friction the sketch cannot absorb, throw the
sketch out. The signal is a **repeated pattern**, not one hard case:

- The same shape of workaround in unrelated places.
- Several unrelated edge cases all needing special-case branches.
- Types needing escape hatches to compile.
- A lock needed where the sketch said nothing was shared.
- Callers having to know the abstraction's internals.

When you scrap: re-ground on what was built, redesign as if the new constraints
were day-one assumptions, subtract before adding, and return to B.

**Reply:** the design, the alternatives and why this one, the open decisions.
