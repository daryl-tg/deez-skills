# Review

The checks run first because they are cheap and objective. The judge runs only
on a revision that passes them. The operator sees only a revision the judge
passed.

## Checks

Run all of them on every revision `r<N>` in `$RUN/out/`.

| Check | Command | Pass |
|---|---|---|
| Determinism | render twice, `bun helpers/determinism.ts a.mp4 b.mp4` | exit 0 |
| Motion | `bun helpers/dead-beats.ts r<N>.mp4 $RUN/music/beats.json` | exit 0, no dead beat |
| Loudness | `bun helpers/loudness.ts` on the final mix | -14 ±0.5 LUFS, true peak ≤ -1.5 dBTP |
| Loop seam | `bun helpers/loop-seam.ts r<N>.mp4` | exit 0, only when the brief asks for a loop |
| Sheets | `bun helpers/sheets.ts r<N>.mp4 --out $RUN/review/r<N> --strip <t>...` | contact, phone and one strip per fast action exist |

A failing check is a finding, not a flake. Localize a determinism failure with a
lossless render. One differing frame changes every later frame hash in the GOP.

## Judge

A fresh-context subagent judges, never the agent that built the revision, per
**principle-delegate-implementation-review-stays-here**. Hand it only these
things:
- the brief
- `style_guide.md`
- the sheets for this revision and the previous one
- the check report

It never gets the build history.

Round one scores the revision against the checklist alone. Every later round is
**pairwise**: this revision against the last one, with the order randomized and
the order recorded. Pairwise judging tracks human preference far better than
absolute scores. Models judging their own model family lean lenient, so every
verdict must cite a timestamp and a frame.

The checklist asks for a yes or no on each item, each with a timestamp and the
sheet or strip it was read from:
- The first two seconds show the product and carry the hook.
- Text is readable at phone width (`phone.png`).
- No text overlaps during a swap (strips).
- Nothing slides linearly where the project's motion eases or springs.
- No shot is centered text on a gradient, corner labels, frame borders or
  generic particles.
- Colors and type match the project tokens.
- Every UI state shown is a real product state. Nothing is redrawn.
- Cuts land on beats (checked against `beats.json` times).

The judge returns the three worst problems with timestamps and, from round two,
the preferred revision with a reason. Fix those three, re-render only the
affected clips, and run the checks again. Stop after round three once the
checklist is all yes and the judge prefers the new revision. Keep every round's
verdict in `$RUN/review/log.md`.

## Publish

Publish the passing revision through the project's evidence renderer (the
project file says how). The gallery holds:
- `contact.png`
- `phone.png`
- the strips
- a poster frame

The MP4 sits beside them in the same revision directory. The captions state:
- the check results
- the judge's final verdict
- the music provenance

Verify the gallery by content: fetch it and count images, then fetch the MP4
URL and confirm a 200 with a video content type. A gallery that renders empty
still returns 200.

Then stop for the operator's sign-off. Passing the checks and the judge makes a
revision eligible for review. It is not approval.
