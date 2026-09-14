# Indicators

A user adds an indicator from the Indicators dialog; it mounts as an overlay with
an engine-drawn legend carrying a settings button, a visibility toggle, a close
button, and a loading spinner. Overlays are either native (heatmap, volume, open
interest) or kScript-backed.

## Sub-features

- `ind-dialog` the Indicators dialog opens and searches.
- `ind-add` an indicator mounts as an overlay.
- `ind-legend` the legend's settings / visibility / close controls work.
- `ind-catalog` official indicators are listed (authed, DB-backed).
- `ind-limit` the guest cap is enforced.

## How to get to it (user POV)

- Click `Indicators` in the ticker bar, search, and pick one.
- The mounted overlay's legend sits at the top-left of its pane.

## Driving it with control-kiyotaka

Preconditions:

- Baseline from [chart boot](./chart-boot-and-data-plane.md), guest modal dismissed.

- **Open the dialog.** Run
  `./control-kiyotaka browser find role button click --name "Indicators" --exact`,
  then `./control-kiyotaka browser snapshot -i -c`. The dialog carries
  `textbox "Search official indicators"` and
  `textbox "Add a package by exact name (@scope/name)"`. It is a `.dialog-style`
  overlay, **not** a `.q-dialog`.
- **The dialog opens on the marketplace view, not the native one.** Its control bar
  has two modes and the default is `indicator-control-bar-wrun-registry-btn`
  ("Indicators"), which lists `REGISTRY` packages and the `PORTED FROM KSCRIPT` set.
  Native/official indicators — TPO, volume, open interest, RSI — live behind
  `indicator-control-bar-legacy-btn` ("kScript LEGACY"), whose own row of filters
  reads `Official`, `Community`, `All`, `Technical`, `Volatility`, `Statistics`,
  `Quant`, `Validation`, `Volume`, `Footprints`, `Market Analysis`:

  ```bash
  ./control-kiyotaka browser find testid indicator-control-bar-legacy-btn click
  ```

  Searching the default view for a native indicator returns
  `No registry packages found` / `No matches in the ported set`, which reads as the
  indicator being missing rather than as the wrong view. The control bar also
  carries `indicator-control-bar-favorites-btn` and
  `indicator-control-bar-build-btn`.
- **Add without the UI**, when the proof is about the overlay rather than the
  dialog — but only with a key whose CONTROL IS ALREADY LOADED:
  `./control-kiyotaka browser eval "document.querySelector('#tc-container-0').__vueParentComponent.setupState.chartStore.addIndicator('ORDERBOOK_DEPTH',{},0)"`.
  Registry keys are the SCREAMING_SNAKE ids in `src/constants/indicator-names.ts`;
  a kScript indicator is `TECHNICAL_SCRIPT` with `ovType` in params.

  **Controls load lazily, so most keys fail from a fresh boot.**
  `src/indicators/indicator-registry.ts` imports each control on demand: only the
  always-load set plus whatever the workspace restored is in `indicatorRegistry`,
  and the rest arrive when the picker loads them. A key outside that set throws

  ```
  addIndicator: no indicatorControl registered for type='TIME_PRICE_OPPORTUNITY'
  ```

  into the console and mounts nothing, while `addIndicator` itself returns
  normally — so the drive looks like a silent no-op, not an error. Read the console
  before concluding the indicator is broken. `ORDERBOOK_DEPTH`,
  `ORDERBOOK_HEATMAP`, `CUMULATIVE_VOLUME_DELTA`, `PM_SIGNAL`,
  `TRADING_TOTAL_VOLUME` and `TRADING_TOTAL_LIQUIDITY` were registered on a plain
  guest boot. For anything else, add it through the dialog, which is the user path
  the proof should be using anyway.
- **Confirm it mounted.** Run
  `./control-kiyotaka browser eval "(()=>JSON.stringify(window.tc[0].metadata.map(m=>m.settings?.ovType ?? m.type)))()"`.
  The new key is in the array — that is the assertion, not the legend text.
- **Drive the legend.** It is engine-built DOM, not Vue:
  `./control-kiyotaka browser eval "window.tc[0].metadata.find(m=>m.settings?.ovType==='<KEY>').legends.settingsBtn.click()"`.
  Also available: `closeBtn`, `toggleVisibilityBtn`, `loader`, plus `codeBtn`,
  `infoBtn`, `guideBtn`, `alertBtn`, `maximizeBtn`, `moveUpBtn` / `moveDownBtn`,
  `collapseLegendBtn`, `pinToChartBtn` and `mergePaneBtn`. For a deterministic
  spinner state in a layout proof, use
  `window.tc[0].updateLoadState(<metaId>, true)`.
  **Poll after a legend click, never assert straight after it** — a `closeBtn`
  click took several seconds to leave `metadata`, so an immediate re-read reports
  the overlay still mounted and the teardown looks broken.
  **The legend controls are only trustworthy on an overlay the DIALOG added.** On
  an overlay added programmatically, neither `closeBtn.click()`, nor a real browser
  click on that button, nor `chartStore.removeIndicator` removed it within 25s,
  even though the button was connected, visible and `shouldShowCloseBtn` was true.
  Whether that is the engine or the bypassed add path is unresolved — so prove any
  legend claim on a dialog-added overlay, and do not report a removal bug from a
  programmatic one.
- **Guest cap.** The ticker bar reads `Indicators 2/3` as a guest, rising to
  `3/3`; the dialog carries the same count as `button "2 / 3"` (testid
  `indicator-search-bar-chart-only-btn`). Assert that text — and assert it through
  the DIALOG's Add button, because **the cap is a UI gate that
  `chartStore.addIndicator` does not enforce**. A programmatic fourth add mounts
  regardless: the counter stayed pinned at `Indicators 3/3` while `metadata` grew
  to six entries. Re-reading `metadata` after a programmatic add therefore proves
  nothing about the cap, and reads as the cap being broken when it is not.
- **Proof.** Screenshot the pane with the legend visible, plus the engine-state
  read naming the overlay. Capture the settings dialog as its own frame if the
  claim is about settings.

## Gotchas

- **A fresh local stack lists NO official indicators.** The dialog renders only
  backend catalog rows; the FE registry never synthesizes them. An unseeded local
  mongo therefore shows zero official indicators — RSI, Open Interest, the whole
  options suite — which reads as a broken feature. Fix with
  `./control-kiyotaka cli -- node scripts/seed-official-catalog.mjs`. Dev builds
  render a warning banner in the dialog when this state is detected.
- **A catalog endpoint that ERRORS looks nothing like an unseeded one, and doctor
  calls it green.** When the stack answers but fails, the LEGACY view renders
  `Couldn't load indicators / Check your connection, then try again. Retry` and
  `Retry` never succeeds. Probe the endpoint directly before blaming the frontend:

  ```bash
  curl -s -o /dev/null -w '%{http_code}\n' -X POST \
    http://127.0.0.1:3000/api/v1/scripts/query -H 'Content-Type: application/json' -d '{"limit":1}'
  ```

  `200` is a usable catalog; `500` means `ind-catalog` and every dialog-driven add
  are unreachable on this stack, and that is an operator-stack blocker, not drift.
  `doctor` reports `backend :3000 up` off a bare `curl` to `/` that accepts any
  status code, so a 500-ing stack passes it.
- On the guest lane the dialog still lists WRUN packages and `@parity/*` ports,
  so "the dialog has content" is not proof the catalog loaded.
- Do not assert an overlay mounted by reading the legend — the legend is engine
  DOM that appears a frame later. Read `metadata`.
- Persisted overlay visibility is user intent only. Never assert on
  `overlay.isHidden` to prove an app-side hide; app-side hides are engine-side
  gates.
- Some indicators are interval-sensitive: TPO sessions are daily, so at `1m` the
  profile is off-screen and the frame looks blank. Pin a sane interval first.
