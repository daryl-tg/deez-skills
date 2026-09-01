# Curation Rubric

Six axes, scored 0–5 each, 30 points total. Score every axis from the fixture
captures (deterministic, seeded — see `stack-idioms.md`) plus a live pass on
the daemon rig for Performance.

**Pass: total ≥ 22/30 AND no axis below 3.**

**Hard fail, regardless of total:** Concept Originality ≤ 1, or Palette
Discipline ≤ 1. These are the anti-slop axes; a low score on either means the
effect is default-prompt output no amount of polish elsewhere fixes.

A blacklist violation from `motion-bible.md` (linear easing, no anticipation
or settle, rainbow-random hue, uniform timing, untuned defaults, deleted
reduced motion) forces the axis it violates to 0–1, independent of how the
rest of that axis reads.

## Axes and anchors

### 1. Concept Originality

- **4–5 (ship bar):** Traceable to a deliberate constraint tuple; not
  reachable by default-prompting.
- **2–3:** A tuple exists, but the combination is predictable, or one axis of
  the tuple (material, motion character, or shape verb) reads as a generic
  default rather than a deliberate choice. Pretty, not surprising.
- **0–1:** No discernible tuple, or the output matches an obvious
  default-prompt cliché (rainbow burst, stock confetti look, generic
  "celebration" burst). **Hard fail.**

### 2. Silhouette & Readability

- **4–5 (ship bar):** One-sentence-describable; hierarchy holds at small
  size (pill scale, not just full ceremony scale).
- **2–3:** Describable, but takes more than one clause, or the hierarchy that
  holds at ceremony scale degrades to an indistinct blob at pill scale.
- **0–1:** No single describable silhouette; multiple co-equal elements
  compete for attention (the blacklist's "no hierarchy" violation).

### 3. Timing Craft

- **4–5 (ship bar):** Full anticipation → peak → settle envelope; staggered
  layers (80–150ms apart); duration matches the flat ≤3s budget.
- **2–3:** Envelope present but one phase is underweighted — a peak with no
  real overshoot, or a settle that is rushed/abrupt — or stagger exists but
  reads mechanical/uniform rather than authored.
- **0–1:** Missing anticipation, missing settle, or all layers move in
  lockstep. These are blacklist violations; the axis is forced into this
  band regardless of anything else.

### 4. Palette Discipline

- **4–5 (ship bar):** One dominant hue; clear saturation hierarchy reserved
  for the focal element; OKLCH-built value ladder; matches its color script.
- **2–3:** A dominant hue exists, but the value ladder is uneven (a harsh
  pure-black/white extreme, or a ladder that reads eyeballed rather than
  OKLCH-consistent), or a secondary element steals saturation from the
  primary.
- **0–1:** Rainbow-random or per-particle hue, or no discernible dominant
  hue. **Hard fail.**

### 5. Performance

- **4–5 (ship bar):** Profiled; bounded element/particle counts (≤120 DOM
  garnish nodes per ceremony for the DOM backend); no jank; respects harness
  caps (exclusivity, one active ceremony).
- **2–3:** Within budget but unprofiled, or occasional dropped frames appear
  under a throttled-CPU pass.
- **0–1:** Exceeds the node/particle budget, causes long tasks >50ms
  attributable to the ceremony, or does not tear down cleanly (stage/DOM
  leaks after teardown).

### 6. Reduced-Motion Grace

- **4–5 (ship bar):** A designed calm variant that still reads celebratory
  (minimum bar: a dignified pill pulse + sheen); a live mid-flight
  reduced-motion toggle jumps the timeline to its end and settles cleanly.
- **2–3:** A calm variant exists but reads flat/lifeless, or only the
  pre-mount reduced-motion path is honored (a live mid-flight toggle is not
  handled).
- **0–1:** Reduced motion is animation deleted instead of a designed
  variant. Blacklist violation; forced into this band.

## Tuple-distance rule

Every new effect's tuple must differ from every shipped effect's tuple on **at
least 2 of the 3 axes** (material, motion character, shape verb). Check this
before stage 2 (Color script), not after implementation — it's a free
rejection point.

Procedure: list `tuple` from every file in
`src/lib/super-reactions/catalog/*.ts` in the target repo. For the candidate
tuple, count how many of the three fields differ from each shipped tuple. If
any shipped tuple shares 2 or all 3 fields with the candidate, the candidate
fails distance — re-pick before generating anything. The first effect in the
catalog trivially satisfies this (nothing to compare against).

## Evidence format

Record every self-grade iteration — never overwrite a prior one — in:

```
~/Documents/dev-notes/om-chat-super-reactions/run-artifacts/<effect-id>/rubric.md
```

Each iteration is a dated entry with:

- Iteration number and date.
- What changed since the previous iteration (one sentence; "initial
  implementation" for the first).
- A score + one-line justification for each of the six axes.
- Total, pass/fail against the ≥22/30-and-no-axis-below-3 bar, and whether
  either hard-fail condition (Concept Originality ≤ 1 or Palette Discipline
  ≤ 1) is triggered.
- Which single axis was identified as lowest-impact to fix next (omit on the
  final passing iteration).

Mark the iteration that passes the bar and is presented at the curation gate
as `FINAL — passing, pending operator sign-off`. After the operator signs off
(the pipeline's stage 6 in `SKILL.md`), append one line noting the sign-off
date; do not delete or rewrite the iteration history above it — the trace of
what improved is part of the evidence.
