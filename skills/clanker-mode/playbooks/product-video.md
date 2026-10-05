### Product motion film

**You own the journey, storyboard and evidence.** For a product reel, feature
demo or UI launch film, load **product-video**. It defines the continuous shell,
human cursor, purposeful zooms and transitions, musical timing and deterministic
rendering. Launches lead with the feature's core value and visible proof;
walkthroughs teach the steps. Determine runtime from the feature's communication
needs and propose it with the storyboard. There is no predefined duration.
Use the skill's preference records for continuity across films. Its
`references/review.md` owns the operator-requested verification cadence:
creation checks, unverified feedback previews, then final checks after the
operator confirms readiness. Apply that cadence to video revisions here.

1. **Understand the product first.** Resolve its project verification skill
   using `docs/project-verification.md` at the hub root. Read the feature index,
   matching guides, documentation and implementation. Trace entry → action →
   response → next action → outcome for research, then select the feature's core
   and proof moments for the film. Separate documented behavior, live proof
   and cinematic treatment. Check any existing fixture notes against source.
2. **Define the feature core, budget its story, then align audio.** Read the skill's
   `references/music.md` for supplied or selected music; check the license,
   measure BPM and onsets, and validate downbeat phase before storyboard timing.
   A provisional 120 BPM grid is only for audio still unselected.
   Follow the skill's story-before-choreography guidance. Derive the necessary
   real UI states and the complete beat grid, grouped by story phrase. Include
   the launch or walkthrough purpose, feature core, proof moments, focal subjects,
   settled payoff time, omitted preparation, prerequisites,
   persistent choices, cursor actions, camera moves, visible consequences and
   ending mode (`loop` or `brand-card`). Load
   the skill's shared preferences and the applicable brand preset. Use OpenMarket
   when that is the requested brand; do not infer branding from a historical
   repository name. Determine seconds per story phrase from what the viewer
   needs to understand; fit music to that budget using measured tempo. Plan
   outside the repo, per **principle-planning-docs-live-outside-the-repo**.
3. **Storyboard gate.** Show the plan before animation code. Bundle missing
   creative preferences, the recommended runtime with its reasoning and approval
   in one request. Resolve factual gaps from the map and source; report missing fixture
   support before substituting a recreation. A material journey or duration
   change returns to this gate. Carry existing approvals into follow-up revisions.
4. **Delegate the approved build to the executor role.** Name the composition,
   asset and output paths and cite the skill by absolute path. Require a single
   1440×1440 HTML composition with every visible value reconstructed by
   `seek(t)`, locally bundled assets, licensed audio and a measured beat grid.
   The cursor, drags and camera must follow the same coordinate transforms.
   Review the build yourself, per
   **principle-delegate-implementation-review-stays-here**.
5. **Inspect the creation preview before the full render.** Include settled
   frames for dense states and strips for fast actions. Fix readability, spacing,
   pointer alignment and continuity first. Preview the sequence at normal speed, muted
   and at delivery size to check the story and payoff. Render through Playwright
   seek calls at four temporal subframes per 60 fps output frame, blended with
   ffmpeg `tmix`.
6. **Verify creation, then iterate with previews.** Follow the skill's
   `references/review.md` for the first complete film. For subsequent feedback,
   edit and show quick previews with verification deferred. Persist reusable
   preferences in their proper scope. Do not repeat steps 1–5 for each tweak.
   Fixture footage does not qualify as live backend verification.
7. **Fix discovered defects at their source.** A harness bug belongs in the
   skill, per **principle-encode-lessons-in-structure**; report product defects
   instead of disguising them in the film. Keep fixes scoped to the task.
8. **Readiness, final verification and delivery.** Ask whether the operator is
   ready for final verification and export. An explicit request to finalize
   already answers this question. Run the full applicable checks on that final
   candidate, then deliver its passing film and evidence through the project's
   renderer or supported local review surface. Follow `references/review.md` in
   product-video for failed checks or changes after readiness. This implements
   **principle-visual-approval-gates-delivery** with the operator's requested
   sign-off before final verification. Unchanged verified cuts need no second
   sign-off.

**Reply:** film and composition paths, duration and measured BPM, checks and
verification gaps, audio license, product defects and any skill fixes.
