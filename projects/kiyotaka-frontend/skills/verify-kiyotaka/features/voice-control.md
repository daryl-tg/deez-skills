# Voice control

A user holds `⌥ Space` (or clicks the footer mic), says a chart command, and lets
go. A pill at the bottom-left of the chart grid shows the words, then one
readback line per step and, for indicator and drawing steps, the undo key. A
symbol that matches several markets asks "Which one?" before anything changes.
Trade verbs stop at Order Confirmation. Verified 2026-10-12 on product tree
`7347b94e69` (= `origin/main`), lane `18097`, no-JWT guest lane with the
`voice-control` flag forced on. Driven: the rig seam `window.__voiceControl.say`
(commit-only), the compound command, the remove-all command, the symbol tie and
its pick. NOT driven: the microphone itself (hold key, click mic, listening pill,
Deepgram or Web Speech), the parser route (needs auth), trade, drawings and
panels.

**Re-driven 2026-10-28 on tree `29c9cda0a2` (`origin/main`, lane `18103`, no
JWT): still unreachable.** `window.__voiceControl`, `voice-control-mic-btn` and
every `voice-control-chip*` were absent. The opening paragraph's `⌥ Space` is
the 2026-10-12 key; see the corrections below, and note that the key is now
user-changeable (`voice-key-change` in `VoiceKeyModeMenu.vue`), so read the
current binding before you press one. Source on `29c9cda0a2` adds an Ask-only
`runCommand` verb (it never runs on the mic path), a command grammar
(`src/utility/voice-control/voice-command-grammar.util.ts`) with new readbacks,
and the Options panel's asked-for names (`options chain`, `0dte`). None of it is
driven.

**Re-driven 2026-10-27 on tree `7290d33d10` (lane `18103`, real guest JWT): still
unreachable.** `window.__voiceControl`, `voice-control-mic-btn` and every
`voice-control-chip*` were absent. Source on `df3fdcb62e` adds multi-chart
targeting (`src/utility/voice-control/chart-target.util.ts`: "open eth on the
second chart", "heikin ashi on chart 2"); it is not driven.

**VERIFIED-UNREACHABLE on the guest lane as of 2026-10-23 (tree `2a1ed750db`).**
The unmet prerequisite is a signed-in session; the route attempted was the
standard `control-kiyotaka up` guest lane, which has no mic, no chip and no
`window.__voiceControl` seam to call. Source-corrected 2026-10-22 — and this
entry's preconditions are now wrong.** The `voice-control` flag GRADUATED on
2026-10-19: `voiceControlEnabled()` is now just `isSignedInSession()`. Setting
`kiyo.flag-overrides` for it does nothing, and a guest or no-JWT lane gets no
mic, no chip, no keybinding, and no `window.__voiceControl` seam at all (the seam
installs only when the footer mic or chart chip mounts). Every recipe below needs
a SIGNED-IN desktop session. Two further corrections: the push-to-talk key is
`Alt+Shift+V`, not `⌥ Space` (changed 2026-10-13, the day after this entry was
written), and the Super Search entry is a toggle labelled "Hold to talk (Voice
control key)", not a launcher.

Handles the entry omits but which exist: `voice-control-chip-transcript`,
`-chip-live`, `-chip-readback`, `voice-control-chip-option-<n>`,
`voice-control-mic-dot`, `voice-key-mode-menu` / `voice-key-mode-<mode>`, and
`voice-control-trade-heard` on the order-confirm dialog. A fake-microphone lane
already exists at `qa/voice-control/audio-lane.mjs`.

## Sub-features

- `vc-mic` the footer mic button renders while the flag is on.
- `vc-compound` one sentence changes symbol, interval and indicator, with a readback.
- `vc-ask` a symbol tie lists the candidates and waits for a pick.
- `vc-remove-all` "remove all indicators" clears the pane, undoable.
- `vc-listening` the listening pill (sine wave, interim words, "release to run"). Not live-verified.

## How to get to it (user POV)

- Hold `⌥ Space` (Mac) over the chart, speak, release.
- Or click the mic in the footer after Undo and Redo, speak, click again.
- Or pick "Push to talk (Voice control)" in Super Search.

## Driving it with control-kiyotaka

Preconditions:

- Baseline from [chart boot](./chart-boot-and-data-plane.md), overlays cleared.
- **A SIGNED-IN desktop session.** There is no flag to force any more:
  `voiceControlEnabled()` is `isSignedInSession()`, so the override below —
  which earlier versions of this entry prescribed — does nothing. A guest or
  no-JWT lane has no mic, no chip, no keybinding, and no `window.__voiceControl`
  seam to call, because the seam installs only when the footer mic or chart chip
  mounts. Sign in before attempting anything in this entry.

- Proof the feature mounted: `JSON.stringify({seam:!!window.__voiceControl,mic:!!document.querySelector('[data-testid=voice-control-mic-btn]')})`
  reads both `true`. Driven live: mic at x 185, y 868, 28×28 in a 1440×900 viewport.

- **Compound command (`vc-compound`).** Run through the seam, commit-only:

  ```bash
  ./control-kiyotaka browser eval \
    "(async()=>JSON.stringify(await window.__voiceControl.say('btc on the fifteen minute with vwap',{theater:false})))()"
  ```

  Driven live from ETH 1h with no indicators: `status: applied`, readback
  `["BTC/USDT on Binance · Perp","Interval 15m","Added VWAP"]`, `undoable: true`.
  The pill (`[data-testid=voice-control-chip]`, `data-status=applied`) shows the
  three lines and `⌘ Z undo`; the title reads `BTCUSDT`. The local grammar
  answers this shape, so it works on a guest lane with the backend down.
- **Tie (`vc-ask`).** From a BTC chart, `say('eth on the fifteen minute with vwap')`
  does not resolve on its own: `__voiceControl.state()` reads `status: asking`
  with options `ETH/USDT · Binance · Perp` and `ETH/USDC · Binance · Perp`.
  `say` stays pending until `window.__voiceControl.pick(0)`; then it applies.
- **Remove all (`vc-remove-all`).** `say('remove all indicators')` reads back
  `Removed 2 indicators` (or `Removed VWAP` for one) with `undoable: true`.
- Proof triple: the `say` result and `state()`, the pill's `innerText`, a screenshot.

## Gotchas

- `say` resolves only after an ask is answered. A script that awaits it with no
  `pick` hangs until the command timeout. Read `state().ask` on a timer instead.
- Phrases the local grammar does not certify go to the parser route, which needs
  a signed-in session. On a guest lane they fail as `error: unavailable`. Driven:
  `eth on hyperliquid` and `eth on hyperliquid on the fifteen minute with vwap`.
- Long readbacks truncate with an ellipsis in the 520 px pill. Driven:
  `Added Relative Strength Index (RSI)` cuts off after an ETH + 15m compound.
- The pill fades 4 s after `applied`. Capture within that window, or wait it out
  for a clean chart.
- The store keeps its phase private, so the listening pill cannot be forced from
  outside. Proving it needs a real or fake microphone.
- The guest lane's release spotlight ("wrun is here") covers the top right. Its
  `Got it` button dismisses it.
