# Music

## Providers, in order

1. **ACE-Step 1.5**: local, free, commercial use of outputs permitted. Installed
   by `setup-audio.sh --music` at repo commit
   `ca1e85fe9430179831e6bc6be790c332190a3866`.
2. **Google Lyria RealTime**: needs `GEMINI_API_KEY`. Whether its free tier
   permits commercial output is unverified. Ask the operator before publishing
   a Lyria bed.
3. **MusicGen**: drafts only. Its weights are CC-BY-NC. It is HyperFrames'
   local fallback, so never let HyperFrames source music.

## License record

The Hugging Face model card for `ACE-Step/Ace-Step1.5`, at commit
`19671f406d603126926c1b7e2adc169acbcade22`, says:

> **💰 Commercial-Ready:** Unlike many models trained on ambiguous datasets,
> ACE-Step v1.5 is designed for creators. You can strictly use the generated
> music for **commercial purposes**.

Code and weights are MIT. The permission lives in the model card, not the
LICENSE file, so cite the pinned commit. The upstream README asks users to
disclose AI involvement and to confirm outputs are original. Never prompt for a
named artist or a protected style.

## What generation actually produces

- **Only about 80% of a take is music.** A 20-second request ends at 15 to 16
  seconds and then goes silent. `generate` requests `ceil(seconds / 0.8) + 4`
  seconds.
- **A fixed seed does not reproduce a take.** The finished bed is an asset.
  Keep it, and never regenerate at render time.
- **Takes drift a little off the requested tempo.** A 120 BPM request measured
  117.98 by regression. `beats.py` fits tempo by regression over beat times,
  because a median interval is quantized to beat_this's 20ms frames. It accepts
  a take within ±3% of the request and exits 1 otherwise, for example on
  half-time, double-time or a misread. Move to the next take. `finish`
  time-stretches an accepted take onto the requested tempo with `atempo` before
  trimming, and records the ratio in provenance.
- **Takes are band-limited** to about 10 kHz and peak above -1.5 dBTP.
  `finish` runs a 4x-oversampled peak limiter before the two-pass loudnorm.
  Without the limiter, loudnorm falls back to dynamic mode and misses -14 LUFS.
- **beat_this can place a beat in the silent tail.** `finish` ends the music at
  the last audible sample before counting bars, so a loop never carries silence.
- **No take loops as generated.** `finish` trims to whole bars from the first
  downbeat and crossfades at a bar boundary.

A warm take takes about 2 minutes on an M4 Mac mini. A cold start adds about a
minute of model load.

## Provenance

Every finished bed has `<bed>.provenance.json` with:
- provider
- repo commit
- model card commit
- prompt
- seed
- source take sha256
- BPM
- trim points

Cite it in the publish captions.
