# Video preferences and continuity

Read this file and the matching brand preset when starting a film. Reuse the
established identity so each video belongs to the same family. Adapt the story
and pacing to its feature; a consistent motif does not require identical shots.

## Shared operator preferences

Confirmed by the operator on 2026-10-05:

- Prioritize overall film quality and storytelling.
- Feature launches communicate the feature's core value and distinctive proof.
  Use a walkthrough when the brief asks to teach the steps.
- The agent determines runtime from what the audience must understand. There is
  no predefined duration or blanket cap; explicit user or placement limits apply.
- Carry approved motifs and reusable creative preferences into later videos.
- Use the creation, iteration and finalization cadence in
  [review.md](review.md). The operator decides when a preview is ready for final
  verification; feedback iterations skip verification.

## Where a preference belongs

| Scope | Canonical record |
|---|---|
| Across brands | This file, for explicitly shared preferences |
| One brand | `references/brands/<brand>.md`, including its approved assets |
| One recurring series | `references/series/<brand>-<series>.md`, created when that series has distinct reusable choices |
| One film or shot | That run's brief in dev-notes |

Use the current user instruction first, then the applicable series preset,
brand preset, shared operator preferences and generic skill defaults. A scoped
instruction does not replace defaults outside its scope. If the brand is not
identified by the brief or product evidence, resolve it before using its assets.

The [OpenMarket preset](brands/openmarket.md) owns that brand's mascot, palette,
type treatment, closing signature and double-blink asset. Load it for OpenMarket
films. Reuse the referenced assets and measured cue timing instead of generating
a similar motif. Other brands use their own records and assets.

At creation, record the selected preset paths, applied values and film-specific
overrides in the run brief. Bundle its assets with the composition. Keep that
snapshot through revisions, so a later preset edit cannot silently alter an
in-progress or archived film. New films load the latest confirmed preferences.

## Learn from feedback

Maintain these records locally as the operator uses the skill. This upkeep is
already requested; it does not need a separate permission round.

- Persist an explicit future default immediately in its narrowest stated scope.
  Capture reusable style corrections in the relevant brand or series preset.
  Keep content, entity choices and shot-specific timing in the run brief.
- A request scoped to “this video” or “this shot” stays in that run. When the
  scope is genuinely unclear, apply it to the current preview and keep it as a
  candidate preference. Resolve it with the final-readiness question rather
  than blocking an edit.
- Record the chosen value, scope, confirmation date and a short source note
  or existing approved artifact path. Save measured timing when available;
  do not invent numbers for “a little faster”. Update the existing entry rather
  than accumulating contradictory rules or a transcript.
- Briefly state any saved default alongside the preview. Reuse it next time
  without asking the same preference again. A film's approval alone does not
  make all of its content and timings universal defaults.

For example, “Use this faster cursor in future OpenMarket videos; dark background
for this one only” updates the brand's cursor preference and the run's background
override. It leaves the brand palette and approved blink motif intact.

Keep asset paths, motif timing, colors, type, framing, cursor/camera feel and
ending choices together in the applicable preset when they are established.
Retain the reusable treatment, not the previous film's feature sequence.
