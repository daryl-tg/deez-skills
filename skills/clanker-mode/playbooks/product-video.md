### Product motion film

**You own the journey, storyboard and evidence.** For a product reel, feature
demo or UI launch film, load **product-video**. It defines the continuous shell,
human cursor, purposeful zooms and transitions, musical timing and deterministic
rendering. Prefer edits under 20 seconds; raise a longer cut at storyboard
approval with its reason and a shorter option. This is a guideline, not a cap.

1. **Understand the product first.** Resolve its project verification skill
   using `docs/project-verification.md` at the hub root. Read the feature index,
   matching guides, documentation and implementation. Trace entry → action →
   response → next action → outcome. Separate documented behavior, live proof
   and cinematic treatment. Check any existing fixture notes against source.
2. **Measure chosen audio, then propose one coherent journey.** Read the skill's
   `references/music.md` for supplied or selected music; check the license,
   measure BPM and onsets, and validate downbeat phase before storyboard timing.
   A provisional 120 BPM grid is only for audio still unselected.
   Derive 8–12 real UI states and the complete
   beat grid. Include prerequisites, persistent choices, cursor actions, camera
   moves, visible consequences and ending mode (`loop` or `brand-card`). Load
   the product-video OpenMarket preset when that is the requested brand; do not
   infer branding from a historical repository name. The default is seven bars
   at about 120 BPM; use measured tempo for final timing. Plan outside the repo,
   per **principle-planning-docs-live-outside-the-repo**.
3. **Storyboard gate.** Show the plan before animation code. Bundle missing
   creative preferences, any longer-duration proposal and approval in one
   request. Resolve factual gaps from the map and source; report missing fixture
   support before substituting a recreation. A material journey or duration
   change returns to this gate. Carry existing approvals into follow-up revisions.
4. **Delegate the approved build to the executor role.** Name the composition,
   asset and output paths and cite the skill by absolute path. Require a single
   1440×1440 HTML composition with every visible value reconstructed by
   `seek(t)`, locally bundled assets, licensed audio and a measured beat grid.
   The cursor, drags and camera must follow the same coordinate transforms.
   Review the build yourself, per
   **principle-delegate-implementation-review-stays-here**.
5. **Inspect beat frames before the full render.** Include settled frames for
   dense states and strips for fast actions. Fix readability, spacing, pointer
   alignment and continuity first. Render through Playwright seek calls at
   four temporal subframes per 60 fps output frame, blended with ffmpeg `tmix`.
6. **Verify and review.** Follow the skill's `references/review.md`. Check
   random-order seeks, real interaction consequences, audio peaks, delivery-size
   readability and the chosen ending contract. Fixture renders show supported
   UI states; they do not establish live backend success. New live verification
   recipes follow the project map contract; cinematic fixtures alone do not
   qualify a feature as live verified.
7. **Fix discovered defects at their source.** A harness bug belongs in the
   skill, per **principle-encode-lessons-in-structure**; report product defects
   instead of disguising them in the film. Keep fixes scoped to the task.
8. **Visual approval gate.** Publish the passing film and evidence through the
   project's renderer, or provide local artifacts on the supported review
   surface if no renderer is configured. Then stop for sign-off, per
   **principle-visual-approval-gates-delivery**. Deliver the approved files where
   the user asks. Other requested formats get their own layout and checks.

**Reply:** film and composition paths, duration and measured BPM, checks and
verification gaps, audio license, product defects and any skill fixes.
