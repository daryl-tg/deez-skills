---
name: product-video
description: Use when asked for a launch video, product reel or marketing clip that must show a product's real UI, rendered from its own components rather than screenshots or generated footage.
---

# Product Video

A marketing video where every UI shot is the product itself. The project's real
components are mounted from its visual fixtures and rendered frame by frame on a
virtual clock. Titles, music and transitions are composed around those clips.
The video reaches the operator only after objective checks and an independent
judge pass.

## Before starting

1. Read `references/pipeline.md` in full, then `references/projects/<project>.md`.
   If the project has no file, write one first from the template in
   `pipeline.md` and stop for the operator to confirm it.
2. Run `bash helpers/setup-scene.sh` and `bash helpers/setup-audio.sh --music`.
   Both are idempotent.
3. Create the run workspace `~/.local/state/product-video/runs/<run-id>/`.
   Renders, clips, music and builds live there. The brief, storyboard and style
   guide are text and live in the task's dev-notes folder, per
   **principle-planning-docs-live-outside-the-repo**.
4. HyperFrames skills come from the `hyperframes@hyperframes` Claude plugin, or
   `npx hyperframes skills update` on Codex. Load `/hyperframes-core` before
   writing composition HTML.

## Stages

Copy these eight stages into your todo list, verbatim and in order, before any
other work. A stage you skip stays in the list as `skip: <reason>`. Each stage's
detail is in `references/pipeline.md`.

1. **References.** Study 3 to 5 launch films and write `style_guide.md`.
2. **Brief and storyboard.** One beat per 2 to 4 seconds, each beat naming the
   fixture state it shows. Render one still per beat with `scene.ts` and ask the
   operator to approve the storyboard. This is the run's only mid-course
   question.
3. **Music.** `music.py generate`, then `beats.py`, then `music.py finish`. The
   finished WAV is an asset. Never regenerate it at render time.
4. **Scenes.** One `scene.json` per beat, rendered to a clip by `scene.ts`.
5. **Compose and master.** A HyperFrames composition takes the clips as
   `<video>`, plus titles and the finished music. Render with the deterministic
   flags, then master the audio to the loudness target and remux, copying the
   video untouched.
6. **Checks.** Run every check in `references/review.md`. A failing check goes
   back to stage 4 or 5.
7. **Judge.** A fresh-context subagent compares this revision against the last
   one, per `references/review.md`. Fix and repeat, at least three rounds.
8. **Approval.** Publish through the project's evidence renderer and stop for
   sign-off, per **principle-visual-approval-gates-delivery**.

## Hard rules

- **UI shots come only from `scene.ts`.** Never use Playwright `recordVideo` or
  `video: 'on'`, a screen recorder, `hyperframes capture <url>`, redrawn UI, or
  a video model. They capture on the wall clock, or show UI that is not the
  product.
- **Remove every class the project file lists under `removeClasses`.** Visual
  fixtures often force `reduced-motion`, which turns every animation off and
  renders a still video. `dead-beats.ts` catches a video that stopped moving.
- **9:16 is 360×640 CSS pixels at DPR 3. 16:9 is 960×540 at DPR 2.** A wide CSS
  viewport renders the desktop layout squeezed. DPR 1 renders a small video.
- **Published music comes from ACE-Step 1.5 only.** HyperFrames' local music
  fallback is MusicGen, whose weights are CC-BY-NC. Never let HyperFrames
  resolve background music. Pass it the finished asset. `references/music.md`
  has the license record.
- **Evidence is files, never a claim of having watched the video.** The
  evidence is check output, contact sheets, frame strips and the judge's
  verdict.
- **Scenes are `scene.json`.** Never create `*.spec.*` or `*.test.*` files in
  the product repository, and never edit its source.
- **No servers.** `scene.ts` serves pages through `page.route`. Run a HyperFrames
  preview only if the operator asks for one. Before binding it on `127.0.0.1`,
  preflight the forwarded slot `4178`. If `4178` is busy, ask which forwarded
  slot to use, per **principle-bind-assigned-ports**.
- **Set `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1` on every `hyperframes` command.**

## Helpers

Paths are relative to this skill's directory, which is `~/.claude/skills/product-video`
on Claude and `~/.codex/skills/product-video` on Codex. Every helper takes
`--help`. The TypeScript helpers run with `bun`, the Python helpers with the
toolchain venv from `setup-audio.sh`.

| Helper | Job |
|---|---|
| `fixture-build.ts` | Build a project fixture outside the repo |
| `scene.ts` | Render a `scene.json` to a clip on a virtual clock |
| `music.py` | Generate takes with ACE-Step, then trim, loop and normalize one |
| `beats.py` | Beat grid at the requested BPM, phase-fitted to detected downbeats |
| `determinism.ts` | Two renders, identical frames or the first difference |
| `sheets.ts` | Contact sheet, phone-width grid, frame strips |
| `dead-beats.ts` | Beat windows where nothing moves |
| `loop-seam.ts` | First-to-last frame similarity for loops |
| `loudness.ts` | Two-pass loudnorm to -14 LUFS / -1.5 dBTP |
