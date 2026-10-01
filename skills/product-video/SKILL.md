---
name: product-video
description: Turn a product journey or feature into a continuous UI motion film with faithful product states, a human cursor, musical timing and deterministic rendering. Use for product reels, feature demos and UI launch films.
---

# Product Motion Film

Act as a product motion designer and creative engineer. Turn a supplied product
journey or feature into a polished, continuous UI motion film. Understand the
product before designing the choreography.

## Inputs

Accept a product repository or reference, the journey or outcome to demonstrate,
a feature map or verification skill if available, and any required states or
interactions. Creative inputs are pure black and white or one accent color, and
royalty-free music around 120 BPM with its commercial-use license.

Read supplied context before asking questions. Infer product facts from maps,
documentation and source; ask only for missing preferences. If given a journey,
propose 8–12 UI states yourself. Do not ask the user to design the sequence.

## Understand the product

When Clanker is available, resolve the project's verification skill and read its
`features/README.md` and matching guides. The hub's
`docs/project-verification.md` defines their canonical project folders. Otherwise
use the supplied map, product documentation and implementation. Existing
`references/projects/<project>.md` files are fixture leads; check them against
the current source and map.

Trace one complete journey:
entry point → user action → system response → next action → final outcome.

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

## Visual direction

Dribbble-level UI motion: one shape, never cut. A persistent outer shell morphs
in size, radius and color while its content swaps with a short blur. The shell
is cinematic framing; its controls remain faithful to the product.

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
  Match cursor position and velocity at the loop boundary.

Do not compress believable input or reading time just to hit a duration target.

## Choreography and duration

Default to 120 BPM, 4/4, seven bars: 28 beats over 14 seconds. Final timing uses
the selected track's measured tempo. Seven bars take `28 × 60 / BPM` seconds;
do not assume a track is exactly 120 BPM.

Prefer a finished edit **under 20 seconds** whenever the journey remains clear.
This is a guideline, not a hard cap. If it needs 20 seconds or more, raise it
with the user at storyboard approval: give the estimated duration, why it needs
that time, and a shorter scope or musical phrase as an alternative. The user
can approve the longer cut. If measured music or later revisions push the
approved cut past the guideline, flag the change before full production.

Something meaningful happens on every beat: an action, response, data reveal,
cursor movement, drag continuation or transition completion. A beat need not
introduce a new screen. Group actions into readable phrases:

- Establish the entry point and user intent.
- Reveal the feature through its real interaction.
- Show the consequence in context.
- Reach a recognizable outcome.
- Return continuously to the opening composition.

Derive the sequence from the journey. Never force a fixed button → loader →
player → slider → toggle sequence. Maintain selected entities, values, filters,
documents, chart data and other persistent choices throughout.

If the journey cannot fit legibly into 28 beats, propose a smaller scope or a
longer musical phrase before coding. Never solve overcrowding with tiny text,
impossible input speeds or an artificially sped-up soundtrack. A visual loop
must not imply a completed action was undone. Reframe cinematically toward the
opening composition when the real workflow does not reset.

## Storyboard approval

When music is supplied or already chosen, read
[references/music.md](references/music.md), check its commercial-use license,
measure BPM and onsets, and validate the downbeat phase before preparing the
storyboard. This analysis is preparation, not animation code. Use its measured
grid and duration for approval; report any unresolved license or listening gap.

Before writing animation code, show:

1. The journey in one sentence.
2. The proposed 8–12 UI states, with their product evidence and persistent data.
3. A complete beat grid: beat number, timestamp, visible state, input action,
   visible consequence and transition, including camera moves and cursor timing.
4. Product prerequisites, missing fixture support and unresolved factual gaps.
5. The opening-to-ending loop strategy, including how the completed outcome
   remains true.
6. Estimated duration and any exception to the under-20-second preference.

Bundle missing creative preferences and storyboard approval in one request.
Use a provisional 120 BPM grid only if music is still unselected, clearly marked
as provisional. Resolve factual gaps from available evidence; if a gap prevents
a faithful state, explain it and propose supported scope. Write no animation
code before approval. A material change to the approved journey or duration
returns to that approval gate.

## Build

Read [references/pipeline.md](references/pipeline.md) after storyboard approval,
and [references/music.md](references/music.md) when choosing or analyzing audio.

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
   ffmpeg `tmix`, and output at 60 fps. Sample periodically across the loop seam.
8. Before the full render, capture one frame per beat and settled frames for
   dense states. Inspect readability, spacing, cursor alignment, continuity and
   timing. Fix those storyboard frames before full production.

## Verification and delivery

Follow [references/review.md](references/review.md). Verify repeated and
random-order seeks, input consequences, pointer-attached drags, non-overlapping
content, meaningful beats, delivery-size readability, audio transient alignment,
continuous loop position and velocity, and evidence for every product claim.
Do not call a rendered fixture proof that a live backend action succeeded.
Report missing verification plainly.

Never put `will-change` on text or elements the camera scales. Match opening and
closing shell, content, camera and cursor trajectory. Make `seek(duration)`
identical to `seek(0)`; encode frames on `[0, duration)` with no duplicate endpoint
that causes a pause. Wrap motion-blur samples and audio across the same periodic
boundary. Do not add latency for drama, invent confirmations, bypass a visible
prerequisite or show incompatible states together.

When running under Clanker, publish the passing render and evidence for its
visual approval gate, using the supported local review surface if the project
has no configured renderer. Deliver the film, composition, measured beat grid, audio
license record and verification findings. Start by reading the supplied journey
and map, proposing product-specific states and beats, and requesting the
missing creative inputs and storyboard approval together.
