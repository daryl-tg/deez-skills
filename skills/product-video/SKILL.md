---
name: product-video
description: Turn a product journey or feature into a continuous UI motion film with faithful product states, a human cursor, musical timing and deterministic rendering. Use for product reels, feature demos and UI launch films.
---

# Product Motion Film

Act as a product motion designer and creative engineer. Turn a supplied product
journey or feature into a polished, continuous UI motion film. For a launch,
capture what the feature makes possible and why the viewer should care.
Understand the product before designing the choreography.

## Inputs

Accept a product repository or reference, the journey or outcome to demonstrate,
a feature map or verification skill if available, and any required states or
interactions. Creative inputs are pure black and white or one accent color, and
royalty-free music around 120 BPM with its commercial-use license.

Read supplied context before asking questions. Infer product facts from maps,
documentation and source; ask only for missing preferences. Choose the states
needed to tell the supplied journey. State count follows the story, not a quota.
Do not ask the user to design the sequence.
Load [preferences and continuity](references/preferences.md) and the applicable
brand or series preset. For OpenMarket, use [its preset](references/brands/openmarket.md)
for the approved mascot, closing card and double-blink sound. Carry reusable
feedback into those records; keep one-film overrides in the run brief. Existing
storyboard approval and later corrections carry forward. The final-readiness
question is separate from storyboard approval.

## Understand the product

When Clanker is available, resolve the project's verification skill and read its
`features/README.md` and matching guides. The hub's
`docs/project-verification.md` defines their canonical project folders. Otherwise
use the supplied map, product documentation and implementation. Existing
`references/projects/<project>.md` files are fixture leads; check them against
the current source and map.

Trace the real workflow for understanding and evidence:
entry point → user action → system response → next action → final outcome.
This research path is not automatically the film's sequence. Select what to
show according to the film's purpose below.

For each proposed state, identify:

- The real component or screen and how the user reaches it.
- The click, drag, hover or keyboard action and its visible consequence.
- Required data, permissions, account state and feature flags.
- The choices that persist into subsequent states.
- Supporting source or guide, and whether the behavior is documented, freshly
  verified or a proposed cinematic treatment.

Read the implementation when guides are incomplete or contradictory. Preserve
actual labels, control types and interaction semantics. Do not invent a slider,
toggle, toast, loading state or confirmation for an attractive transition.
Every state must advance the chosen outcome or explain an important feature.
Report factual gaps and missing fixture support before substituting a recreation.

## Story before choreography

Set `purpose: launch | walkthrough` from the request. Feature announcements,
release reels and product launches use `launch`. An explicit tutorial or request
to teach the steps uses `walkthrough`. Do not turn an announcement into onboarding.

For a launch, write the feature's core in one sentence: who it is for, what new
capability it gives them, and why that change matters. Name the distinguishing
mechanism and the visible evidence supporting the claim. Avoid benefits or
comparisons the product evidence does not establish.

Build the film around the strongest reveal of that capability. Open on the
feature's value, a meaningful contrast or the problem it resolves. Show the
decisive proof and let the result register before the brand signature. Supporting
moments earn their time by making the core claim understandable or credible.
Feature lists and menu tours are not substitutes for this reveal.

A launch can begin in a real prepared state with the relevant feature already
open. Keep its product context recognizable. Leave unrelated setup, navigation,
saving and housekeeping out of the film. Record omitted preparation in the
storyboard; do not imply those steps never exist or that the shown click performs
them. Any prerequisite or confirmation needed for an action actually shown
remains truthful. Compression must preserve cause and effect.

A walkthrough follows the required interaction sequence so the viewer can repeat
it. A launch's primary question is what becomes possible; a walkthrough's is how
to do it. For example, a launch for pinned chart values can start with a tooltip
open, reveal that its reference survives a new hover, and hold the comparison.
It need not teach symbol selection or toolbar navigation.

For each story phrase, name the focal subject and what the viewer learns.
Cursor, camera, UI response and copy direct attention to that subject; competing
motion waits. Reserve a settled view of the payoff. Keep the same entity
recognizable so viewers can see what changed. Editorial copy stays outside
product controls and explains the benefit. Use step-by-step captions for a
walkthrough. A camera pose or cursor approach does not require another scene.

## Visual direction

Dribbble-level UI motion: one shape, never cut. A persistent outer shell morphs
in size, radius and color while its content swaps with a short blur. The shell
is cinematic framing; its controls remain faithful to the product. Preserve
recognizable screen context: demonstrate a feature inside its real dialog or
page. Include navigation when it contributes to the story or is needed to teach
the workflow. Keep controls in their product context rather than unrelated cards.

Use a light warm-gray canvas, black and white components, optionally one accent.
Use the product font when recognizable, otherwise Geist, and consistent icon
strokes. Styling must preserve legibility and meaningful product distinctions.

Use restrained springs with at most a tiny overshoot. Direct manipulation
follows the pointer without spring lag. Keep essential values sharp while the
viewer inspects them; outgoing text clears before incoming text becomes readable.

Use purposeful zooms, continuous camera moves and transitions when they improve
engagement or explain cause and effect. Zoom toward the active control before a
precise action, reveal the result, then pull back when context matters. Anchor
the reframe to the selected entity or control so viewers can follow it. Each
active state should fill the frame without losing necessary context. Keep text
readable during moves; a settled inspection beat is useful. Avoid repetitive
zoom pumping, disorienting pans and motion added just to fill time.

Use real visual relationships for transitions: a row expands into its detail;
a compact control widens into its associated panel; an existing selection marker
stretches between actual tabs; a result contracts toward its originating entry.
A progress track may carry into another genuine linear control. These are
options, not required components. Engagement never requires a hard cut.

Banned: bouncy easing, particle bursts, glows, gradients on UI chrome, mismatched
icons, unreadable dashboards, overlapping text, dead time, generic template
styling and fabricated product behavior.

## Human cursor and input

The cursor is an intentional user, with visible targets and credible input:

- Move along gentle curved paths with acceleration and deceleration. Vary travel
  time with distance and precision; roughly 180–500 ms is a useful starting
  range, not a fixed rule. Slow into small targets, with a short arrival settle
  when needed. Do not teleport, cruise at constant speed or add random jitter.
- Aim inside the actual enabled hit area, usually near its center. Avoid paths
  that hide the label or imply an unrelated hover. A tiny corrective movement
  can feel natural; repeated overshoots and decorative wobble do not.
- Show a plausible press and release, often 60–120 ms apart, and the product's
  actual pressed, focus or hover response when it has one. Arrival, input and
  consequence must be visibly connected. Do not manufacture hover behavior.
- For drags, approach the handle, press, move with purposeful speed variation,
  then release. The controlled value follows cursor position exactly within
  real bounds. Preserve release position and velocity for any subsequent spring.
- Show typing at a readable, slightly varied cadence with brief word pauses,
  then the real keyboard confirmation when required. Do not add typos,
  backspaces or waiting just to simulate a human.
- Precompute paths, timing variation and key events from a fixed seed or authored
  schedule. Every cursor pose, button state and typed character comes from
  `seek(t)`, independently of playback history. No fresh randomness per frame.
- Transform the cursor, target and hit coordinates consistently with the camera.
  During a zoom, clicks still land on the same control and drags stay attached.
  For a loop, match cursor position and velocity at its boundary.

Do not compress believable input or reading time just to hit a duration target.

## Choreography and duration

Determine the runtime from the feature's communication needs. There is no
default duration, bar count or blanket short-film cap. Assess what this audience
already understands, the new concepts or relationships it must see, the density
of the proof, necessary input time and settled reading time. Menu count, code
complexity and total feature count do not determine length.

Budget seconds for the opening, each essential proof moment, the settled payoff
and the complete brand ending. Sum them into a recommended duration and explain
what needs that time. Choose it yourself for storyboard review; do not ask the
operator to supply a runtime when none is required. A simple feature can resolve
quickly; a comparison or unfamiliar concept may need more explanation. Avoid
fixed “simple/medium/complex” duration bands and filler added to reach a target.

Then fit the accents and ending to the chosen music. At a stable measured tempo,
`duration = beats × 60 / BPM`; choose the beat count to support the story.
Music phrasing may refine the budget without crowding the proof or padding it.
Respect an explicit user or placement limit. If the core cannot fit legibly,
propose a tighter scope or a changed limit instead of speeding up the actions.

Use musical beats to pace the story phrases, with actions and consequences on
useful accents. Mark inspection holds in the grid with what the viewer is
reading or comparing. A hold can span several beats with a still camera and
parked cursor. The payoff needs time after its last reframe or caption change;
time spent moving toward it is not settled reading time.

Derive the sequence from the feature's core and film purpose. Never force a fixed
button → loader → player → slider → toggle sequence. Maintain selected entities, values, filters,
documents, chart data and other persistent choices throughout.

Record `ending: loop | brand-card` in the storyboard. Default to `loop` unless
the brief or brand preset specifies a closing card. A brand card can fill the
frame with the logo and destination after the product outcome, then settle.
It does not return to the opening; leave room for the musical resolution and
brand motif. Place the card after the payoff and allow its full sound and blink
to finish within the proposed duration.

Never solve overcrowding with tiny text, impossible input speeds or an
artificially sped-up soundtrack. A visual loop must not imply a completed action
was undone. Reframe cinematically toward the
opening composition when the real workflow does not reset.

## Storyboard approval

When music is supplied or already chosen, read
[references/music.md](references/music.md), check its commercial-use license,
measure BPM and onsets, and validate the downbeat phase before preparing the
storyboard. This analysis is preparation, not animation code. Use its measured
grid and duration for approval; report any unresolved license or listening gap.

Before writing animation code, show:

1. The purpose, intended viewer, feature core and strongest visual proof.
2. The necessary UI states, their evidence and persistent data, plus preparation
   omitted from the film. Explain how the sequence serves the launch or walkthrough.
3. A complete beat grid: beat number, timestamp, visible state, input action,
   visible consequence and transition, including camera moves and cursor timing.
   Group beats into phrases with a focal subject, what the viewer learns and
   explicit settled reading intervals, especially for the payoff.
4. Product prerequisites, missing fixture support and unresolved factual gaps.
5. The ending mode and its transition, including how the completed outcome
   remains true and when any musical resolution or brand motif lands.
6. The recommended duration, time budget by phrase and why the feature needs it.
   Include any explicit placement limit and how the story fits it.

Bundle missing creative preferences and storyboard approval in one request.
Use a provisional 120 BPM grid only if music is still unselected, clearly marked
as provisional. Resolve factual gaps from available evidence; if a gap prevents
a faithful state, explain it and propose supported scope. Write no animation
code before approval. A material change to the approved story or duration that
the user has not already requested returns to that approval gate.

## Build

Read [references/pipeline.md](references/pipeline.md) after storyboard approval,
and [references/music.md](references/music.md) when choosing or analyzing audio.
The steps below create the first complete version. Subsequent feedback edits
use the iteration stage in [references/review.md](references/review.md), with
quick previews and no repeated verification.

1. Create one HTML composition entry, square 1440×1440. Bundle assets and fonts
   locally. Prefer actual product components and deterministic fixtures; report
   missing support before any recreation. Keep briefs in the task's dev-notes
   folder and renders in `~/.local/state/product-video/runs/<run-id>/`.
2. Reconstruct every frame-visible value inside `seek(t)`: geometry, color,
   content, chart or document data, cursor, camera and effects. No CSS
   transitions, wall-clock timers or state carried between frames. Seeking
   out of order must produce identical output.
3. Use closed-form spring responses. Repeated target changes are the initial
   value plus one spring response per target delta. For a real sliding selection
   indicator, animate leading and trailing edges with different springs; use
   this for a genuine toggle knob when appropriate. Do not invent controls.
4. Compute dragged values directly from the cursor. On release initialize any
   spring from release position and velocity. Respect real bounds; elastic
   decoration must not imply invalid values.
5. Give outgoing and incoming content separate timing envelopes. Keep outgoing
   text clear of incoming text and essential values sharp while inspected.
6. Analyze the selected music with numpy for tempo and onset timing. Listen to
   validate downbeat phase, start on a downbeat, verify commercial-use rights,
   and align UI sounds by measured transient peaks, including leading silence.
   Use the measured beat grid for final timing.
7. Render with Playwright using deterministic seeks, never video recording.
   Capture four temporal subframes per output frame, blend each group with
   ffmpeg `tmix`, and output at 60 fps. Wrap loop samples; clamp closing-card samples.
8. Before the full render, capture one frame per beat and settled frames for
   dense states. Inspect readability, spacing, cursor alignment, continuity and
   timing. Preview the assembled sequence at normal speed, muted and at delivery
   size. Check that the action and payoff are understandable without pausing.
   Fix the pacing and storyboard frames before full production.

## Verification and delivery

Follow the cadence and checks in [references/review.md](references/review.md):
verify the first complete version, skip verification during feedback iterations,
ask whether the user is ready to finalize, then verify the final candidate before
delivery. An explicit “finalize it” answers that question; casual praise does not.
Label intervening outputs as previews with verification deferred. This cadence
applies to film revisions, including under Clanker. A rendered fixture does not
prove a live backend action succeeded. Report missing verification plainly.

Never put `will-change` on text or elements the camera scales. For loops, match
opening and closing shell, content, camera and cursor trajectory, with
`seek(duration) === seek(0)` and periodic audio and blur samples. For closing
cards, retain the final composition and let sound tails finish; do not wrap to
the opening. Encode frame centers on `[0, duration)` without an extra endpoint.
Do not add latency for drama, invent confirmations, bypass a visible prerequisite
or show incompatible states together.

After the user's readiness confirmation and passing final checks, deliver the
film, composition, measured beat grid, audio license record and verification
findings. Under Clanker, use the project's renderer or supported local review
surface. Follow the review reference if final repairs change the approved cut.
