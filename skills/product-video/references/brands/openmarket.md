# OpenMarket film preset

Use for OpenMarket films unless the user supplies a different direction. This
captures the approved October 2026 options film; it does not prescribe its
contracts, dates, duration or journey for other features.

This is the reusable OpenMarket identity record. Follow
[preferences and continuity](../preferences.md) when applying feedback to it.
Keep one-film exceptions in the run brief. Reuse the approved mascot and blink
assets across films; a new feature does not call for a newly generated signature.

## Identity and framing

- Warm-gray canvas (`#F0EEEA`), black/white product chrome and the original
  terracotta mascot (`#D97757`, cream eyes `#F3F2EF`). Use the product font;
  the approved chart film used Inter. Preserve semantic colors when necessary.
- Use the [bundled mascot](../../assets/openmarket/mascot.svg), with subtle
  time-derived motion. At the top, show the logo alone, without an added
  “OpenMarket” heading. Keep real product labels and branding in their context.
- Show the feature in its actual dialog/page. For an options journey, the
  approved progression was symbol-selection options → calls/puts → Back → full
  chain → scroll to the bottom → another contract. That sequence records a prior
  film; it does not make launches follow a walkthrough. Select each new film's
  proof moments from its feature core and purpose.
- When an exchange strip is appropriate, use the supported exchanges' actual
  icons from the product. Do not replace essential instrument/venue labels in
  the data with decorative icons or invent unsupported exchange coverage.
- Keep production disclaimers such as “illustrative market snapshot” off the
  film chrome. Record fixture provenance in the delivery notes; never describe
  synthetic data as live or omit a disclosure the brief requires.

## Closing signature

Default to `ending: brand-card`. Transition continuously to a full-page mascot
and destination. For the chart product, show `openmarket.xyz/chart`; use the
actual destination for other products. Place the signature after the feature's
proof and readable payoff. The approved film was 18 seconds; new runtimes follow
their own communication needs, not that historical duration.

Resolve the music at the destination reveal, then perform exactly two mascot
blinks with the bundled sound. Leave the eyes open between and after the blinks.
Keep the final frame settled long enough to read the destination and hear the
release. A user-requested seamless loop overrides this ending mode and must
place the motif before its continuous return.

## Reusable double blink

Copy [double-blink.wav](../../assets/openmarket/double-blink.wav) and consult
[manifest.json](../../assets/openmarket/manifest.json) for measured timing,
levels, hashes and provenance. Reuse this approved sound, not a newly designed
notification cue or an older mascot demo's random/timer animation.

The 700 ms stereo asset contains two identical warm G5 plips. Their peaks are
at 0.200 and 0.450 seconds, 250 ms apart. Choose first eye-close time `B` on the
musical grid and start the asset at `B - 0.200`; the second closes at `B + 0.250`.
Do not align the WAV's start to eye closure. Keep its complete tail in the edit.

The approved source peak is −12 dBFS. Start at unity asset gain, then balance
against the resolved bed. The previous −22 dBFS treatment was too quiet; the
motif should be clearly audible at normal playback volume. Do not blindly add
another 10 dB to this already boosted asset. Master the mix and measure the
encoded audio using the shared review targets.

For the approved eye motion, for each close time `c` evaluate
`pulse(t,c) = exp(-((t-c)/sigma)^2)`, where `sigma` is 0.035 seconds before `c`
and 0.055 after. Apply
`scaleY = 1 - 0.95 * max(pulse(t,B), pulse(t,B+0.250))` to each eye about its own
center. Keep the eye centers fixed; do not squash the entire mascot. This is a
pure function of time. Check open → closed → open → closed → open strips and
both encoded sound peaks within one 60 fps frame of their corresponding closes.

The mascot is a first-party brand asset. The sound was synthesized for this
film without external samples. The manifest records provenance, not a blanket
license for unrelated music or third-party use of OpenMarket branding.
