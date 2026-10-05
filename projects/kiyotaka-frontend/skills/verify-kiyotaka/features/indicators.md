# Indicators

A user adds an indicator from the Indicators dialog; it mounts as an overlay with
an engine-drawn legend carrying a settings button, a visibility toggle, a close
button, and a loading spinner. Overlays are either native (heatmap, volume, open
interest) or kScript-backed. This entry was re-verified on 2026-10-02 against
product tree `40b1271aac`; guest coverage opened the V2 dialog, confirmed seeded
official rows, added RSI, and observed the guest sign-in/slot surfaces. The
top-level Indicators/kScript strip, Pine paste offer, and WRUN catalog paths
remain flag- or auth-dependent and were not driven here.

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
- **The dialog has explicit source and result modes.** Current source tabs include
  `indicator-source-tab-official` and `indicator-source-tab-community`, with
  optional registry, personal, and marketplace lanes depending on auth and flags.
  The result tabs are `indicator-tab-discover-btn` and `indicator-tab-all-btn`; do
  not assume a guest always opens directly in a kScript catalog or that the
  source strip is absent. The legacy control-bar handles are not the current
  route. Driven live, the guest dialog held these stable controls:

  ```
  indicator-source-tab-official   indicator-source-tab-community
  indicator-tab-discover-btn      indicator-tab-all-btn
  ```

  Read which modes render before driving a gated lane; signed-in and flag-enabled
  sessions can add registry, personal, or marketplace sources.

  Below the source pair sit seven category buttons: `All`, `Technical`,
  `Volatility`, `Statistics`, `Quant Validation`, `Volume Footprints`,
  `Market Analysis`. `Quant Validation` and `Volume Footprints` are each ONE
  label — matching `Quant` or `Volume` alone finds nothing.
- **The top-level mode strip is conditional.** When `tabStripVisible` is true,
  `indicator-control-bar-tab-indicators-btn` and
  `indicator-control-bar-tab-kscript-btn` switch between registry Indicators and
  kScript sources. Governed CME or a missing feature flag can hide the strip.
- **Discover and All are distinct result states.** Under the category row sits a
  second tab pair,
  `tab "Discover"` and `tab "All"`, beside `button "Browse all indicators"` when
  the empty state offers it. The current guest lane exposed seeded official rows
  after selecting All. Drive the tabs by
  testid rather than that button's text: `indicator-tab-discover-btn`,
  `indicator-tab-all-btn`, and the source pair `indicator-source-tab-official` /
  `indicator-source-tab-community` (a guest sees only those two; `My Scripts` and
  `Marketplace` render for signed-in and flag-enabled sessions). The unseeded
  banner has its own handle, `indicator-catalog-unseeded-notice`, which is a
  cleaner assertion than the banner text. `indicator-browse-all-btn` renders only
  in the empty state, so do not depend on it being there.
- **Pine paste is a separate user path.** A Pine snippet in the search can render
  an `IndicatorPineOffer` above the list, and empty/searching states may offer
  Kata or paste guidance. Verify that affordance separately from ordinary rows.
- **Add through the dialog and assert the engine.** The current seeded guest lane
  added RSI through its official row and increased `window.tc[0].metadata` from
  two to three entries. A direct `chartStore.addIndicator` call is not equivalent
  to a user add: admission depends on caller options, duplicate-family checks, and
  pane budgets, so use the dialog path for user-facing proofs.
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
- **Guest cap.** Read the live counter after workspace restoration, not during
  first paint. The current fresh guest dialog exposes `button "1 / 3"`, and adding
  RSI raised the engine metadata to three rows. The dialog carries the same count
  as its chart-only counter (testid
  `indicator-search-bar-chart-only-btn`). Assert that text — and assert it through
  the DIALOG's Add button, because **the cap is a UI gate that
  `chartStore.addIndicator` does not enforce**. A programmatic fourth add mounts
  regardless: the counter stayed pinned at `Indicators 3/3` while `metadata` grew
  to six entries. The gate runs only when the caller passes `opts.recordUndo` or
  `opts.enforceIndicatorLimit` (`src/store/chart.add-indicator.ts:1375`, the flag computed at `:1370`), and a
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
  render a warning banner naming that command — but only under `Browse all
  indicators`, never on the `Discover` tab the legacy view opens on.
- **A catalog endpoint that ERRORS looks nothing like an unseeded one, and doctor
  calls it green.** When the stack answers but fails, the LEGACY view renders
  `Couldn't load indicators / Check your connection, then try again. Retry` and
  `Retry` never succeeds. Probe the endpoint directly before blaming the frontend:

  ```bash
  curl -s -o /dev/null -w '%{http_code}\n' -X POST \
    http://127.0.0.1:3000/api/v1/scripts/query -H 'Content-Type: application/json' -d '{"limit":1}'
  ```

  `500` means `ind-catalog` and every dialog-driven add are unreachable on this
  stack, and that is an operator-stack blocker, not drift.

  **A `200` is not a seeded catalog, and this is the trap that looks like drift.**
  The endpoint answering says nothing about whether the rows exist: an unseeded
  local mongo answers `200` and returns zero official rows, so a search for `RSI`
  reads `RESULTS 0 / No indicators found` — indistinguishable from a broken search
  until you open `Browse all indicators`, which names it outright:

  ```
  OFFICIAL INDICATORS 0
  Official catalog is empty: this local stack has no seeded official indicators.
  Run: node scripts/seed-official-catalog.mjs
  ```

  That banner is the only unambiguous signal, and it does **not** render on the
  `Discover` tab the view opens on. `doctor`'s `catalog` line probes the endpoint,
  so it goes green on exactly this stack.
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
