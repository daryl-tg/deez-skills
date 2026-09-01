# Motion Quality Bible

The codified taste every super reaction is designed and graded against.
Sources: Disney's 12 principles as applied to UI motion, Riot's League VFX
Style Guide, Material 3 / IBM Carbon / Apple HIG motion specs, "Juice it or
Lose it" (Jonasson & Purho).

**No rarity tiers.** Every super reaction ships at the same premium bar —
there is no lighter rule set for a "common" effect. Where the source research
described rules that scaled with a rarity tier, this file states the flat
rule that supersedes them; see "Superseded by the no-tiers decision" at the
bottom.

## Structural rules (every effect MUST have)

1. **A three-phase timing envelope: anticipation → peak → settle.** A wind-up
   beat before the burst; an overshoot at peak (hit ~110%, ease back to
   100%); a staggered decay. An effect that appears at full intensity and
   vanishes instantly is auto-rejected.
2. **Follow-through staggering.** Layers settle 80–150ms apart from each
   other, never all at once.
3. **One primary element.** Instantly identifiable as "the point"; every
   other layer is subordinate to it. If you cannot describe the silhouette
   in one clause, it's noise, not a primary element.
4. **Exactly one secondary action.** A glint, a shimmer, a temperature
   shift — supporting the primary element, never competing with it.
5. **Squash & stretch on the trigger glyph**, not on particles or garnish.

## Color rules

6. **One dominant hue per effect; supporting elements desaturated.** Reserve
   maximum saturation for the single focal element. Rainbow-random
   per-particle hue is banned, full stop — no exception. (The source
   research allowed a "top-rarity prismatic" exception; it does not survive
   the no-rarity-tiers decision. See "Superseded" below.)
7. **Value discipline.** No pure-black/pure-white extremes; mid-range
   brightness with real tonal spread. Build palettes in OKLCH so
   lightness/saturation ladders are perceptually computed, not eyeballed.
8. **Color script before code.** Grade 3–5 static key-moment thumbnails on
   color/value alone before any animation is written (Pixar's practice).
   This is the cheapest point to catch rainbow-noise or a muddy palette —
   do it before storyboarding, not after.

## Timing and easing tokens

9. **Named easing only.** Standard `cubic-bezier(0.4,0,0.2,1)`, decelerate
   `(0,0,0.2,1)` for arrivals, accelerate `(0.4,0,1,1)` for exits;
   expressive/bounce curves are allowed (Carbon "Expressive" mode, not
   "Productive"). **Linear easing is banned everywhere.**
10. **Duration: ≤3s total (anticipation + peak + settle), for every effect.**
    "If it feels long, it's way too long" (Riot). The source research scaled
    this cap by rarity tier (common ≤1.2s, rare ≤2s, legendary ≤3s); with no
    tiers, every effect uses the flat ≤3s ceiling — treat it as a hard
    budget, not a target to spend in full.

## Craft texture

11. **No perfect geometric primitives.** Irregular, authored edges over
    perfect circles and perfect radial gradients — programmatic-looking
    reads as cheap-looking.
12. **Juice is layered.** A good effect stacks 3–4 coordinated channels
    (motion + scale-bounce + particles/trails + optional sound); a cheap one
    uses one channel and calls it done.

## Anti-pattern blacklist (auto-fail)

Any one of these on its own fails the effect regardless of how the rest
scores. Check every capture against this list before scoring the rubric.

- Linear easing anywhere.
- Uniform start/stop timing across all elements (no stagger).
- No hierarchy — everything reads as co-equal, no describable primary
  element.
- Rainbow-random hues (no exception — see rule 6 above).
- Untuned library defaults (stock particle-library parameters, untuned bloom
  presets) — slop by definition, regardless of the library.
- No anticipation and/or no settle phase.
- A reduced-motion "fallback" that is animation deleted, instead of a
  designed calm variant.

## Superseded by the no-tiers decision

The source research (`2026-08-19-super-reactions-research.md` §4) wrote two
rules against a rarity-tier model that the spec later rejected (decisions
log, round 2: "no rarity tiers — every super reaction must be premium. Flat
catalog, full rubric on every effect, no lighter curation lanes"). Both are
resolved above and listed here so a reader of the original research doesn't
apply the stale version:

- "Duration scales with rarity tier" → flat ≤3s cap for every effect (rule
  10 above).
- "Rainbow-random hues banned except as a deliberate top-rarity prismatic
  treatment" → banned with no exception (rule 6 above). The original
  blacklist also listed "duration flat across rarity tiers" as an anti-fail
  pattern — that item is retired outright, since there is only one tier now
  and flat duration across effects is expected, not a defect.
