# Film verification

Run the checks below at creation and finalization. Feedback iterations use the
preview stage below. A rendered fixture supports a claim about represented UI
behavior; only live verification proves a backend action succeeded.

## Verification cadence

This is the operator's requested cadence for product videos, including Clanker
runs. It does not change verification rules for product-code changes.

| Stage | Work and next step |
|---|---|
| Creation | Establish product and asset evidence, inspect beat previews, then run all applicable checks on the first complete film. Fix failures and repeat affected checks until a verified initial version exists. Record its revision and show it to the user. |
| Feedback iterations | Apply the requested edits and render a quick preview. Skip verification passes, live journey reruns, contact-sheet audits, determinism suites and audio/encode measurements. State what changed and label the output “Preview; verification deferred”. Initial evidence belongs to its original revision. |
| Ready to finalize | Ask “Ready for the final verification and export, or more changes?” before starting final checks. An explicit request to finalize, or a yes answering this question, is sufficient. “Looks good” outside that exchange is feedback, not an instruction to start verification. Continue requested edits while the answer is pending. |
| Final verification | After readiness is confirmed, render the final candidate at delivery quality and run all applicable checks against that exact revision and encoded file. Reuse unchanged asset/license records and setup; do not substitute the initial film's measurements for final evidence. |
| Delivery | Deliver the passing final file and report. Do not add another readiness question for an unchanged, verified cut. Finalization does not authorize external publication. |

Generating a viewable preview is part of the edit, not a verification round.
Resolve render errors needed to produce it. Fix an obvious defect encountered
during editing without launching a wider audit. If the user explicitly requests
a check during an iteration, run that named check only and report its scope.

When the user asks for another edit after final checks, return to the preview
stage. Previous final evidence no longer covers the revised cut. Obtain readiness
again before its final verification. Ordinary feedback does not restart the
creation checks or reopen an already-approved storyboard.

Keep the current stage, revision, last verified revision, pending edits and any
readiness confirmation in the run brief. This prevents a resumed session from
mistaking an unverified preview for a final file or restarting all the checks.

## Checks

| Claim | Evidence |
|---|---|
| The film serves its purpose | Watch at normal speed, muted and at delivery size. For a launch, identify the new capability, why it matters and the visible proof; navigation coverage is not the goal. For a walkthrough, check that the required steps can be followed. Cite timestamps and report an unavailable viewing. |
| The payoff has time to read | Record its settled interval after the final reframe or caption change and before the ending transition. Check that the result can be understood without pausing. Count moving reveals separately from reading time. |
| Seeking is deterministic | Compare lossless frames for repeated timestamps and a seeded random-order schedule against direct seeks, including fresh page loads. Check all visible layers. Two sequential renders alone are insufficient. |
| Input causes the right response | Annotated frames or strips before input, at press/release or keyboard confirmation, and after the consequence; cite the map, source or live verification for the response. |
| Cursor feels human and targets correctly | Inspect curved approach paths, acceleration/deceleration, target settling, press duration and typing cadence. Measure the pointer tip inside the visible enabled target and clipping panel at press and release, after scroll/layout/camera transforms. Inspect the approach and moving-header transition too. |
| Scrolling reaches the requested data | Record scrollTop and scrollHeight − clientHeight; when showing the bottom, they differ by at most 1 px and the final row is visible. Inspect readability during the scroll and at its stop. |
| Accordion changes remain continuous | First transition frame preserves the clicked header position; strips show it moving upward as the outgoing panel closes and incoming panel opens. No instant scroll reset or cursor outside the component. |
| Drags follow the cursor | Compare the handle and controlled value with pointer coordinates throughout contact; inspect release position, velocity and bounds. |
| Content never overlaps | Strips at outgoing/incoming envelope boundaries and the densest morphs; inspect labels and essential values at output size. |
| Beats support the story | Review the grid by phrase, checking its focal subject and what the viewer learns. Multi-beat inspection holds and continued gestures count. Camera poses and cursor movements do not require additional product states. |
| Zooms and transitions help | Confirm each move directs attention to the action or consequence, preserves orientation and readable text, and gives dense states time to settle. |
| Audio aligns | Measured effect transient peaks against action timestamps, downbeat listening check and final beat grid; include leading-silence offsets. Report a listening gap plainly. |
| Loop position and velocity match (loop only) | Exact state comparison at 0 and duration plus derivatives or finite differences on either side for shell, camera, content and cursor. Inspect periodically sampled seam strips and audio continuity. |
| Closing card resolves (brand-card only) | Final encoded frame retains logo and destination; music resolves and all sound tails finish. If a motif is used, check exact blink count, open eyes between/after blinks, measured peak alignment within one frame and clear presence in the final mix. No opening-frame wrap. |
| Completed actions stay true | Trace persistent entity IDs, values, selections and data through the final outcome and chosen ending. No reset that visually undoes the action. |
| Delivery matches the plan | Probe for 1440×1440 and 60 fps by default, the feature-based approved duration, four samples per frame and no duplicate endpoint. Check the story's reading budget and any explicit placement limit, not a generic runtime cap. |
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

At creation or final verification, correct failed checks and repeat only the
affected checks. Re-render only affected frames or audio. Technical repairs
that preserve the approved creative intent stay in this stage. If a repair
changes the approved story, appearance or pacing, show a new preview and return
to the readiness question. Do not deliver a failed or inconclusive final as verified.

Any additional visual review belongs to these verification stages, not every
feedback iteration. Give a reviewer the approved storyboard, state list, beat
grid, frames and check report. Findings cite timestamps or frames.

After readiness and passing final checks, stop production when the approved
journey is readable, faithful and continuous. Creation checks lead to the first
preview, not automatic final delivery. Do not add arbitrary review rounds or
pixel movement to prolong a passing film.

## Delivery

Provide the MP4, local HTML composition and assets, measured beat grid, audio
license/provenance, beat previews and check report. State fixture coverage and
missing live verification plainly.

Under Clanker, the user's readiness confirmation supplies the creative sign-off
for that cut before final verification. Show the passing film and evidence using
the project's renderer or local artifacts on the supported review surface.
Check that the final film and expected evidence are visible and retrievable;
a status code alone does not establish delivery. A changed cut follows the
readiness rules above.

Do not update a feature map's live-verification provenance from fixture footage.
A newly live-verified recipe follows the hub's project verification contract and
its map-only publisher.
