# Film verification

Verify the composition and beat previews before encoding. Then inspect the final
film at delivery size and collect the evidence below. A rendered fixture supports
a claim about represented UI behavior; only live verification proves a backend
action succeeded.

## Checks

| Claim | Evidence |
|---|---|
| Seeking is deterministic | Compare lossless frames for repeated timestamps and a seeded random-order schedule against direct seeks, including fresh page loads. Check all visible layers. Two sequential renders alone are insufficient. |
| Input causes the right response | Annotated frames or strips before input, at press/release or keyboard confirmation, and after the consequence; cite the map, source or live verification for the response. |
| Cursor feels human and targets correctly | Inspect curved approach paths, acceleration/deceleration, target settling, press duration and typing cadence. Measure the pointer tip inside the visible enabled target and clipping panel at press and release, after scroll/layout/camera transforms. Inspect the approach and moving-header transition too. |
| Scrolling reaches the requested data | Record scrollTop and scrollHeight − clientHeight; when showing the bottom, they differ by at most 1 px and the final row is visible. Inspect readability during the scroll and at its stop. |
| Accordion changes remain continuous | First transition frame preserves the clicked header position; strips show it moving upward as the outgoing panel closes and incoming panel opens. No instant scroll reset or cursor outside the component. |
| Drags follow the cursor | Compare the handle and controlled value with pointer coordinates throughout contact; inspect release position, velocity and bounds. |
| Content never overlaps | Strips at outgoing/incoming envelope boundaries and the densest morphs; inspect labels and essential values at output size. |
| Beats are meaningful | Review every measured beat against the approved grid. A readable inspection or continued gesture counts; decorative pixel movement alone does not. |
| Zooms and transitions help | Confirm each move directs attention to the action or consequence, preserves orientation and readable text, and gives dense states time to settle. |
| Audio aligns | Measured effect transient peaks against action timestamps, downbeat listening check and final beat grid; include leading-silence offsets. Report a listening gap plainly. |
| Loop position and velocity match (loop only) | Exact state comparison at 0 and duration plus derivatives or finite differences on either side for shell, camera, content and cursor. Inspect periodically sampled seam strips and audio continuity. |
| Closing card resolves (brand-card only) | Final encoded frame retains logo and destination; music resolves and all sound tails finish. If a motif is used, check exact blink count, open eyes between/after blinks, measured peak alignment within one frame and clear presence in the final mix. No opening-frame wrap. |
| Completed actions stay true | Trace persistent entity IDs, values, selections and data through the final outcome and chosen ending. No reset that visually undoes the action. |
| Delivery matches the plan | Probe for 1440×1440 and 60 fps by default, approved duration, four samples per frame and no duplicate endpoint. Flag an unapproved move to 20 seconds or more. |
| Product claims have evidence | Each state has its source or guide and provenance: documented, freshly live verified or cinematic framing. List missing fixtures or verification. |
| Audio can be used commercially | Source and license record for music and UI sounds, attribution requirements, excerpt/modification permission and saved provenance. |

Inspect essential states at the actual intended display size, including a compact
view if delivery is on a phone. Text must be understandable without pausing.

Existing checks such as `helpers/determinism.ts`, `sheets.ts`,
`loop-seam.ts` and `loudness.ts` can supply supporting evidence. Their limits
are in `pipeline.md`. First/last encoded frames are one frame interval apart;
do not add a duplicate endpoint just to raise a seam similarity score.

If mastering, a useful default is -14 ±0.5 LUFS and true peak ≤ -1.5 dBTP,
unless the delivery brief specifies another target. Measure the final muxed file,
because encoding can change true peaks. This audio target does not replace the
transient and applicable ending checks.

## Review and stop condition

Correct failed checks, then repeat the affected checks. Re-render the whole film
only when the change affects it. An independent visual review can help with
dense choreography; give the reviewer the approved storyboard, evidence-backed
state list, beat grid, frames and check report. Every finding should cite a
timestamp or frame. Measure timing findings directly.

Stop production when the required checks pass and the approved journey is
readable, faithful and continuous. Do not force arbitrary review rounds or
pixel movement to prolong an otherwise passing film.

## Delivery

Provide the MP4, local HTML composition and assets, measured beat grid, audio
license/provenance, beat previews and check report. State fixture coverage and
missing live verification plainly.

Under Clanker, publish evidence with the project's existing verification
renderer and wait for its visual sign-off. Check that the gallery actually
contains the expected frames and that the film is retrievable; a status code
alone does not prove the evidence is visible. If no renderer is configured,
provide local artifacts using the supported review surface.

Do not update a feature map's live-verification provenance from fixture footage.
A newly live-verified recipe follows the hub's project verification contract and
its map-only publisher.
