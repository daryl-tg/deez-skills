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
- The flag is runtime and not on for a guest. Force it and reload:

  ```bash
  ./control-kiyotaka browser eval \
    "localStorage.setItem('kiyo.flag-overrides',JSON.stringify({'search-v2':true,'voice-control':true}))"
  ./control-kiyotaka browser open "$(./control-kiyotaka url)"
  ```

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
