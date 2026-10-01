# Music and sound

## Choose and verify an asset

Accept the user's royalty-free track or select one around 120 BPM to match the
creative brief. Save the audio locally. Royalty-free does not by itself establish
commercial-use permission.

Record the track title, creator, source URL, license URL or supplied license
document, retrieval date, file hash, commercial-use rights, attribution terms,
and permission to trim, loop, synchronize and publish the excerpt. Keep the
license evidence beside the asset. Check UI sound effects too. If rights are
unclear, report the gap before delivering a published mix; do not imply a
license was verified.

Read the actual license for the chosen asset. Do not assume a provider's current
catalog or an old model card covers this file.

## Measure timing

Use numpy to analyze the waveform or onset-strength envelope and estimate tempo
and onsets. A beat detector can assist, but listen to establish the downbeat phase
and check half-time or double-time estimates. If listening is unavailable, state
that gap instead of claiming the phase was heard.

Record measured BPM, beat and downbeat timestamps, excerpt start, and uncertainty.
For a stable tempo, fit beat time against beat index rather than using a median
of quantized intervals. Use the measured grid for the final choreography.
A varying-tempo track needs its actual beat timestamps.

Start the excerpt on a verified downbeat. Seven 4/4 bars are 28 beats, taking
`28 × 60 / measured_BPM` seconds at a stable tempo. Do not assume 120 BPM or
change playback speed just to hit 14 or 20 seconds. If the phrase reaches
20 seconds or longer, follow the duration discussion in `SKILL.md`.

Measure each UI sound's transient peak and leading silence with numpy. To place
the peak at action time `a`, offset a file with peak time `p` to `a - p`.
Check the transient in the finished mix against the visible input or response.

Create a periodic excerpt that preserves the beat phase at the seam. Wrap sounds
and crossfade only where musically appropriate; check the final waveform and
listen for clicks, missing tails or a beat that doubles at the boundary.
Video blur sampling and audio use the same period.

## Existing audio tooling

`helpers/setup-audio.sh` installs analysis tools. Use `--music` only when local
generation is actually wanted; do not download a model just to analyze a supplied
track. `helpers/beats.py` emits measured `bpm_detected`, beats, downbeats and
a phase-fitted `grid` for tracks near its requested BPM. The acceptance tolerance
is an estimate check, not a reason to reject a deliberately selected tempo.

`helpers/music.py` supports ACE-Step generation. Generation is optional and
requires verifying the chosen provider, model and output terms for this run.
Previous setup pinned ACE-Step repo commit
`ca1e85fe9430179831e6bc6be790c332190a3866` and model-card commit
`19671f406d603126926c1b7e2adc169acbcade22`; those are lookup leads, not fresh
license verification.

The helper's `finish` time-stretches to the requested BPM. Preserve measured
tempo for this film and use suitable trimming, periodic mixing and mastering
instead. A seed does not guarantee generated audio reproducibility: freeze the
selected source and finished mix as assets before rendering.

An existing `<bed>.provenance.json` may contain provider, repo/model-card commits,
prompt, seed, source hash, BPM and trim points. Add asset-specific license
evidence and the final measured grid. Never regenerate audio at render time.
