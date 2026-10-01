# Continuous film pipeline

Use after the storyboard gate in `SKILL.md`. Keep the brief and storyboard in
the task's dev-notes folder. Builds, audio, previews and final films live in
`~/.local/state/product-video/runs/<run-id>/`.

## One composition

Create a single HTML entry at 1440×1440 with the persistent shell, product
content, cursor and camera. Bundle fonts, icons and other assets locally; wait
for fonts and assets before capture and eliminate render-time network requests.

Prefer the actual product components with deterministic fixture data. First
inventory missing fixture states and unsupported actions. Identify any faithful
recreation to the user before using it. A fixture cannot invent product behavior
or stand in for successful live backend verification.

Project files under `references/projects/` are source and fixture pointers,
not overrides of this film contract. Recheck their dated findings. Where a
product's styling conflicts with the requested monochrome treatment, preserve
semantic color distinctions and state the visual adaptation in the storyboard.
Do not add an unrelated project-configuration approval gate.

## Seek contract

Expose `seek(t)`, with time in seconds, and the agreed duration. Compute every
visible value from the normalized time and immutable fixtures. Calling
`seek(9), seek(2), seek(9)` must yield identical frames at the two visits to 9.

Evaluate components' selected data, expanded panels, focus, hover, pressed state,
typed text and any animated data directly from the authored event schedule.
Do not replay clicks from frame zero, depend on a prior seek, or leave mounted
component timers or CSS transitions running. Product components that cannot
expose the required deterministic states are a fixture-support gap to resolve.

Use closed-form springs, including their derivatives when velocity matters.
For repeated targets, sum the response to each target delta over the initial
value, instead of restarting the last animation and losing momentum. At drag
release, evaluate the response from the exact release position and velocity.
During pointer contact, derive the value directly from pointer coordinates.
Clamp semantic values to the product's real bounds.

Author cursor paths with gently curved segments and analytic easing. Precompute
any seeded variation once. Define button-down/up and keystrokes on the same
timeline as their visible consequences. Transform cursor and hit targets through
the same camera mapping. Coordinate scene-state envelopes so outgoing text is
gone before incoming text becomes readable.

Measure the visible target after applying scroll, layout and camera state. Map
its coordinates once, and check the cursor's actual tip, not its graphic's
bounding-box center, at press and release. A point measured before an accordion
collapses may be outside the component when the click appears.

Animate actual scroll position, with enough fixture rows to demonstrate the
requested range. For a bottom-of-list beat, reach the real maximum and expose
the last row. When opening another accordion closes the first, derive outgoing
height, incoming height and scroll compensation from one continuous progress
value. Keep the clicked header at its pre-click position on the first transition
frame, then carry it upward as the old section closes. A brief cursor follow can
clarify that relationship before it parks. Reconstruct any temporary outgoing
DOM from immutable fixtures on every seek; never accumulate clones.

The camera and shell are cinematic; preserve the product's controls and labels.
Use focus zooms and relationship-preserving morphs where they clarify the next
action or result. Keep readable inspection intervals around dense content.

## Audio and duration

Read `music.md`. Analyze the selected asset, verify its license, listen to check
downbeat phase, and use measured BPM and onsets. Record the final beat grid.
For seven bars the duration is `28 × 60 / measured_BPM`; other approved phrases
use `beats × 60 / measured_BPM`. Begin the excerpt on a verified downbeat.

Prefer under 20 seconds. If the measured track makes the phrase 20 seconds or
longer, report that duration and the reason, offer a shorter scope or phrase, and
include the longer proposal in storyboard approval. If that approval already
covers the measured duration, continue. Do not speed up the track to fit.

Use numpy to measure UI sound transients. If an effect's peak is `p` seconds
after its file begins and the target action is at `a`, place the sound at
`a - p`. Leading silence is part of this offset. Verify the mixed peak against
the action, rather than aligning file starts by eye. For loops, wrap effects and
the music excerpt at the video's periodic boundary. For closing cards, follow
`music.md` for a resolved cadence and completed tails. Keep the original audio
and finished mix as fixed assets; do not regenerate music while rendering.

## Preview gate

After the approved storyboard is implemented, capture one frame per measured
beat plus settled frames for dense states. Add short strips around content swaps,
clicks, drags and the selected ending. Inspect at delivery size for readable labels,
spacing, overlap, pointer targeting, correct consequences, persistent data and
camera continuity. Fix the preview frames before starting the full render.

A meaningful inspection beat can be steady. Do not add a meaningless push or
cursor motion merely to make a pixel-change detector pass.

## Frame production

Render through Playwright by calling `seek(t)` and capturing still frames.
Never use `recordVideo`, a screen recorder or sequential wall-clock playback.

Use four temporal samples per output frame at 60 fps. Choose and record a shutter
interval and distribute samples within it. For output time `t`, evaluate four
independent samples at `t + offset[j]`. In loop mode, wrap times modulo duration.
In brand-card mode, clamp them to `[0, duration]` so the closing frame cannot
pick up the opening. Every sample evaluates the full composition independently.

Blend each group of four with ffmpeg `tmix=frames=4:weights='1 1 1 1'`. Because
`tmix` uses a sliding history, align the retained frame with the last sample in
each four-sample group, discard startup history, and select one blend per group.
Do not emit every sliding blend. If filter history needs padding, use periodic
padding for loops and held endpoints for closing cards. Trim padding and reset
timestamps. Encode the resulting sequence at 60 fps.

For loops, keep the endpoint out of the encoded sequence. Make `seek(duration)`
identical to `seek(0)`, and sample frame centers only on `[0, duration)`. If the
musical duration is not an integer number of 60 fps frames, record the frame
count and subframe rounding policy; keep the muxed audio and video seam aligned
within one frame. Never append an extra copy of the opening frame.

For loop mode, verify position and velocity analytically and with seam frames.
A completed action remains completed: use composition or camera reframing to
return to the opening view instead of resetting the product's persistent choices.
The opening should support that return; avoid returning to an old value that
contradicts the completed journey.

For brand-card mode, `seek(duration)` is the settled closing composition. Inspect
the final encoded frame, complete motif and audio tail; no seam equality check
applies. For either mode, record frame rounding and keep audio/video duration
within one output frame.

For revisions, rebuild only affected frames or audio. An audio-only revision can
remux with video stream copy; compare video stream hashes to prove the visuals
were preserved. Recheck final encoded loudness and transient timing after muxing.

## Existing helpers

Paths are relative to this skill. Use a helper only where its output satisfies
the current contract; inspect `--help` before running it.

- `fixture-build.ts` can build supported product fixtures outside the repo.
- `beats.py` detects tempo and downbeats; its `--bpm` argument gates estimates
  near the requested tempo. Its `bpm_detected` and `grid` describe the measured
  track. Still validate phase by listening and analyze onsets with numpy.
- `determinism.ts` compares complete decoded renders; additionally test repeated
  and random-order seeks before encoding.
- `sheets.ts` extracts contact sheets and strips; include the exact beat and
  settled frames required above.
- `loudness.ts` can master a mix; measure the final encoded audio.
- `loop-seam.ts` measures first/last frame similarity only. It does not prove
  matching endpoint values or velocity.
- `dead-beats.ts` measures pixel changes, not whether a beat is meaningful.
- `scene.ts` renders sequential fixture clips on a virtual clock. It does not
  provide this composition's random-order `seek(t)` or four-subframe blending.
  Do not use it as the final renderer.
- `music.py` is optional generation/finishing tooling. Its `finish` changes
  tempo to the requested BPM; for this workflow preserve the chosen track's
  measured tempo and perform the approved trim, ending-specific mix and mastering.

There is no required HyperFrames workflow, generated-music provider, multi-clip
composition or fixed number of judging rounds. The entry skill and approved
storyboard define the film.
