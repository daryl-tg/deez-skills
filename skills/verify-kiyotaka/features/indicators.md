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
  Registry keys are the `INDICATOR_TYPES` ids from
  `@orangecharts/chart-schema/indicator-types` — every type registered by
  `indicatorRegistry.set(...)` under `src/indicators/controls/*/index.ts`, and
  enumerable without importing anything as `KNOWN_INDICATOR_TYPES`.
  `src/constants/indicator-names.ts` is the cross-language search-alias map, not
  the registry. A kScript indicator is `TECHNICAL_SCRIPT` with `ovType` in params.

  **Controls load lazily, so warm the registry before an eval add.**
  `src/indicators/indicator-registry.ts` imports each of the ~84 controls on
  demand; a fresh boot holds only `ALWAYS_LOAD_TYPES` (`TRADING_TOTAL_VOLUME`,
  `TRADING_TOTAL_LIQUIDITY`, `ORDERBOOK_DEPTH`) plus whatever the workspace
  restored. Opening the Indicators dialog schedules `loadAllControls()` at idle
  with a 2000ms timeout, so **open it once, wait ~3s, close it, then eval-add**.
  `addIndicator` does `await loadControl(type)` itself, so a miss on a KNOWN type
  is the control module failing to import (the path settles `module-load`), not a
  missing recipe step — which is what happened on the run that wrote this note.
  It throws

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
  `./control-kiyotaka browser eval "(()=>JSON.stringify(window.tc[0].metadata.map(m=>m.settings?.ovType ?? m.overlayType ?? m.type)))()"`.
  Keep the `overlayType` rung: on an overlay row `type` is the SIDE
  (`onchart` / `offchart`), not an indicator key, so a bare `?? m.type` prints
  placeholders that read like overlays.
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
  to six entries. The gate runs only when the caller passes `opts.recordUndo` or
  `opts.enforceIndicatorLimit` (`src/store/chart.add-indicator.ts:1189`), and a
  bare `addIndicator(KEY,{},0)` passes neither. Re-reading `metadata` after a
  programmatic add therefore proves nothing about the cap, and reads as the cap
  being broken when it is not. Use eval adds to REACH three slots, then assert the
  at-limit surfaces: the refusal is **not** silent — at 3/3 the dialog shows a
  banner (`indicator-list-card-upgrade-btn`, "You've used all 3 free slots") and a
  UI add opens the upgrade dialog.
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
- **Every DIALOG add path is guest-walled, so `ind-add` via the UI is not a guest
  proof.** `useIndicatorCatalog.addIndicator` opens with
  `if (handleGuestAccess(FeatureId.INDICATORS)) return;`, so a guest row click
  raises the sign-in wall instead of mounting; the `/` hotkey is walled too, while
  the ticker-bar button that OPENS the dialog is not. On the guest lane the engine
  add (`chartStore.addIndicator`) is the only way to mount an overlay — and it is
  the one that bypasses the cap, so guest proves the cap's DISPLAY only.
- Persisted overlay visibility is user intent only. Never assert on
  `overlay.isHidden` to prove an app-side hide; app-side hides are engine-side
  gates.
- Some indicators are interval-sensitive: TPO sessions are daily, so at `1m` the
  profile is off-screen and the frame looks blank. Pin a sane interval first.
