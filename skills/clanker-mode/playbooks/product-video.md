### Product video

**You own the film and its two approval gates.** For a launch video, product
reel, demo or marketing clip that shows a product's real UI. The **product-video**
skill holds the method. This playbook holds the order and who does what.

1. **Load product-video** and read its `references/pipeline.md` and the
   project file under `references/projects/`. If the repo has no project file,
   write one from the pipeline's template and stop for the operator to confirm
   it. Its eight stages go into your todo list verbatim, below these steps.
2. **Plan outside the repo.** The brief, style guide and judge log are text in
   the task's dev-notes folder, per **principle-planning-docs-live-outside-the-repo**.
   Renders, clips and music live in the run workspace the skill names.
3. **Storyboard gate.** Render one still per beat, publish them through the
   project's evidence renderer, and ask the operator to approve the beats. This
   is the only mid-run question, so bundle every open choice into it: formats
   (9:16, 16:9, 1:1), CTA, title wording, beats to swap.
4. **Delegate production to the executor role:** music, scenes, compose and
   master. Every handoff cites the skill by absolute path and names the scene,
   check and file limits. Review each clip and render yourself, per
   **principle-delegate-implementation-review-stays-here**. Inspect frames, never
   the self-report.
5. **Run the checks and measure the cuts yourself.** Determinism,
   dead-beats, loudness of the muxed file, and every cut frame. A failing check
   goes back to production, never to the judge.
6. **Judge with a fresh-context subagent,** pairwise from round two, order
   randomized and recorded, at least three rounds. Log a disposition for every
   problem it names: accepted, declined with the reason, or left for the
   operator. Judges misread timing and swing on pacing. Once the skill's stop
   rule holds, stop.
7. **Fix the skill, not just the video.** A harness or pipeline bug found while
   filming is fixed in the skill, test-first, in its own commit, per
   **principle-failing-test-first** and **principle-encode-lessons-in-structure**.
   A product defect the camera exposes is reported to the operator, never
   papered over in the scene.
8. **Approval gate.** Publish the passing revision with its sheets and MP4, and
   stop for sign-off, per **principle-visual-approval-gates-delivery**. Deliver
   the files where the operator asks.
9. **Other formats** re-render the same beats at the new viewport, and each gets
   its own checks and the operator's look. Never crop one format into another.

**Reply:** the film paths, the checks with numbers, the judge's final verdict
and open suggestions, product defects the filming exposed, and skill changes
made.
