---
name: om-super-reaction
description: "Design, build, and quality-gate one super reaction effect for OM Chat's premium reaction system, from constraint tuple through storyboard and implementation to a graded pass and operator sign-off."
---

# OM Super Reaction

Run the authoring pipeline for exactly one super reaction effect, from
constraint tuple to a rubric-passing, operator-approved implementation.
Effects live in `openmarket-chat`'s
`src/lib/super-reactions/catalog/<effect-id>.ts`; this skill owns the design
and quality gate around writing that file. It does not own the harness, wire
plumbing, pill, or picker machinery those files run on — that is
`$om-chat-feature` scope, already built once per the feature's own plan.

**No rarity tiers.** Every super reaction ships at the same premium bar; there
is no lighter curation lane for a "common" effect.

## Before starting

- Read `references/motion-bible.md`, `references/vocabularies.md`,
  `references/rubric.md`, and `references/stack-idioms.md` in full. Every
  generation in stages 2–3 must carry the bible's rules and the anti-pattern
  blacklist plus the chosen tuple — there is no unconstrained "make
  something cool" path.
- List every shipped effect's `tuple` from
  `src/lib/super-reactions/catalog/*.ts` in the target repo before stage 1.
- Check `~/Documents/dev-notes/om-chat-super-reactions/inspiration-inbox.md`
  for unprocessed entries and mine it per `references/vocabularies.md`
  before picking a tuple. New vocabulary entries come from a deliberate
  mining session, never invented ad hoc mid-pipeline.

## The six-stage pipeline

### 1. Tuple

Pick material × motion character × shape verb from
`references/vocabularies.md`. Check tuple distance: the candidate must
differ from every shipped effect's tuple on at least 2 of the 3 axes
(procedure in `references/rubric.md`). Reject and re-pick on failure — this
is a free check, do it before any generation.

### 2. Color script

Generate 3–5 static key-moment frames per candidate direction as cards into
the Claude Design project ("OM Super Reactions"; create it via DesignSync if
absent, per `references/stack-idioms.md`). Grade every candidate on palette
rules alone (`references/motion-bible.md`, Color rules) — no animation
exists yet; this is the cheapest kill point in the pipeline.

**STOP — operator gate.** Present the candidates. The operator culls to one
direction on palette rules. Do not pick the surviving direction yourself and
proceed to storyboards.

### 3. Storyboard

For the surviving direction, generate 3 storyboard candidates as cards: a
one-sentence silhouette, primary element, secondary action, envelope ms marks
(anticipation/peak/settle, summing to ≤3s), backend (`"dom"` unless a
genuine case for `"webgl"` escalation exists), sound yes/no.

**STOP — operator gate.** Present the 3 storyboards. The operator culls to
one. Do not implement a storyboard you selected yourself.

### 4. Implement

Bake any sprite assets (`bun tools/super-reactions/bake.ts`) and write the
catalog file against the harness contract — the full `SuperReactionEffect`
field list is in `references/stack-idioms.md`. Stay inside the DOM-backend
rules: `plus-lighter` additive layering, ≤120 garnish DOM nodes,
compositor-only motion (`transform`/`opacity` only), named easing (never
linear). Add the metadata entry to the identity leaf's catalog and register
the effect file. Manifest every new or changed file in the same change
(`tools/parity-manifest.json`, then `bun tools/sync-shared.ts --refresh`) —
every new `src/` file in this repo is shared by default.

Test-first applies to the deterministic parts: seeded randomness, timing/phase
math, catalog registration, and manifest wiring get a failing
`test/<name>.test.ts` first, run with `bun test`, and never a `*.spec.*` file.
The look itself is not unit-testable — the rubric and the self-grade loop below
remain its only gate, so do not fake a test that asserts an appearance.

### 5. Self-grade loop

Capture the effect deterministically
(`bun tools/visual/super-reaction-capture.ts <effect-id> [--seed 1]`), score
every capture against `references/rubric.md`, fix the single lowest-scoring
axis, recapture, repeat. Record every iteration's scores in
`~/Documents/dev-notes/om-chat-super-reactions/run-artifacts/<effect-id>/rubric.md`
— keep prior iterations rather than overwriting them; the improvement trace
is part of the evidence. Do not advance until total ≥ 22/30, no axis below
3, and neither Concept Originality nor Palette Discipline is ≤ 1 (that
combination hard-fails regardless of total).

### 6. Curation

**STOP — operator gate.** Publish the passing captures (envelope frames +
calm variant + pill idle/hover, both viewports) and the final rubric sheet to
the operator for sign-off. Passing the self-grade loop in stage 5 is
necessary but not sufficient — the operator's sign-off here is the actual
ship gate. Do not commit, promote, or announce past this point; hand the
approved effect back to `$om-chat-feature` / `$om-chat-feature-completion`
for that.

## The two operator gates are non-skippable

Stage 2's palette cull and stage 3's storyboard cull are hard stops: generate
candidates and present them, but never choose the surviving direction or
storyboard yourself and proceed on your own authority. Stage 6's sign-off is
a third, terminal gate that always follows a passing self-grade loop —
passing the rubric moves an effect INTO curation, never past it.

## Guardrails that apply throughout

- Never paste `openmarket-chat` repo source into the Claude Design project;
  it is proprietary. Build cards from specs (palettes, frames, storyboard
  text) only, never from source files.
- The design project is disposable working state. The repo registry entry
  and `~/Documents/dev-notes/om-chat-super-reactions/super-reactions-spec.md`
  are the source of truth; delete rejected candidates' cards rather than
  archiving them.
- Frame-by-frame motion tuning happens in the repo fixture, never in the
  design project.
- The bake tool and the fixture/capture tool
  (`tools/super-reactions/bake.ts`, `tools/visual/super-reaction-capture.ts`)
  may land in the same implementation effort as this skill and not exist yet
  the first time this skill runs. `references/stack-idioms.md` documents
  their contract at spec time — verify the real CLI flags and output shape
  against the landed tool before trusting this doc's description of it.
