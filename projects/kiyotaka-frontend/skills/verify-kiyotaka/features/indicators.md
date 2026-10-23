# Indicators

A user adds an indicator from the Indicators dialog; it mounts as an overlay with
an engine-drawn legend carrying a settings button, a visibility toggle, a close
button, and a loading spinner. Overlays are either native (heatmap, volume, open
interest) or kScript-backed. This entry was DRIVEN on 2026-10-23 against product tree `2a1ed750db` on a real
guest-JWT lane: ind-add, ind-legend and ind-limit were all proven for the first
time. ind-catalog was not re-exercised this pass; guest coverage opened the V2 dialog, selected All,
searched RSI, and recorded the current empty official-catalog state. The
top-level Indicators/kScript strip, Pine paste offer, and WRUN catalog paths
remain flag- or auth-dependent and were not driven here.

## Sub-features

- `ind-dialog` the Indicators dialog opens and searches.
- `ind-add` an indicator mounts as an overlay.
- `ind-legend` the legend's settings / visibility / close controls work.
- `ind-catalog` official indicators are listed when the catalog is seeded.
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
  **Drift, driven 2026-10-12 on tree `1570b59d69` (the desktop parity sweep's `ind-dialog`, `ind-catalog` and
  `ind-search`, in the shell and in Chromium):** that tree renders the WRUN registry panel, `indicator-panel-v2`. Its
  search field is `indicator-search-bar-input` (`indicator-dialog-skeleton-input` while it loads), not the textbox
  named above; the official list sits under `OPENMARKET INDICATORS <n>` with each group's count in
  `indicator-list-group-count`, and the Technical chip is `indicator-category-chip-technical`. Drive these testids.
- **The dialog was rebuilt as a "store", and every tab handle this entry used is
  gone.** `indicator-control-bar-tab-indicators-btn`, `-tab-kscript-btn`,
  `-favorites-btn`, `-sort-btn`, `indicator-source-tab-official`/`-community`,
  `indicator-registry-tab-*`, `indicator-tab-discover-btn`/`-all-btn` and
  `indicator-browse-all-btn` have ZERO matches in source. The strip is now
  `indicator-store-tabs` with
  `indicator-store-tab-{popular,trending,new,following,paid,mine}`, and it hides
  itself when a viewer qualifies for fewer than two tabs. The empty state is
  `indicator-empty-state` / `-action-btn`.

  Handles that survived: `indicator-panel-v2` (root), `indicator-search-bar-input`
  (plus a skeleton twin `indicator-dialog-skeleton-input`),
  `indicator-search-bar-chart-only-btn`, `indicator-list-card-upgrade-btn`, and
  `indicator-catalog-unseeded-notice` — the last now gated on
  `import.meta.env.DEV` alone, so it is a dev-build banner rather than a
  catalog-state signal. Row adds are
  `official-indicator-add-official-indicator-<slug>-btn`, and the detail panel
  carries `indicator-detail-add-btn` / `-apply-btn`.

  **`wrun-registry` is no longer a flag at all** — the lane is unconditional and
  `kiyo.flag-overrides` cannot turn it off. Drop any "read the strip, it flipped
  twice" caveat.

- **Pine paste is a separate user path.** A Pine snippet in the search can render
  an `IndicatorPineOffer` above the list, and empty/searching states may offer
  Kata or paste guidance. Verify that affordance separately from ordinary rows.
- **Add through the dialog and assert the engine.** The current seeded guest lane
  added RSI through its official row and increased `window.tc[0].metadata` from
  two to three entries. A direct `chartStore.addIndicator` call is not equivalent
  to a user add: admission depends on caller options, duplicate-family checks, and
  pane budgets, so use the dialog path for user-facing proofs.

  **Use `BITCOIN_DOMINANCE` for a programmatic add.** It is exchange-independent
  (reads CRYPTOCAP `BTC.D`), needs no venue resolution, sets
  `onlySingleInstance = false`, is not row-capped, and returns a single real
  template — so it clears the gate that the old probe keys could never clear. On
  a COINBASE BTC-USD 1h lane no gate between entry and mount applies: the mode is
  `FULL`, a bare call skips the slot gate, and `addIndicator` awaits
  `loadControl` itself, so no dialog warm-up is needed. Pre-check, then add:

  ```js
  // expect COINBASE / 1h / budget null / tc true
  (()=>{const m=chartStore.mergedAllCharts[0].metadata;return JSON.stringify({ex:m.exchange,iv:m.interval,budget:chartStore.paneBudget?.maxIndicators,tc:!!window.tc?.[0]})})()
  ```

  ```js
  (async()=>{const seen=new Set();
   const iv=setInterval(()=>document.querySelectorAll('.q-notification').forEach(n=>seen.add(n.innerText.trim())),50);
   let r,err; try{ r=await chartStore.addIndicator('BITCOIN_DOMINANCE',{},0);}catch(e){err=String(e)}
   await new Promise(x=>setTimeout(x,300)); clearInterval(iv);
   return JSON.stringify({r,err,seen:[...seen],
     mounted:window.tc[0].metadata.some(m=>m.settings?.ovType==='BITCOIN_DOMINANCE')})})()
  ```

  **DRIVEN 2026-10-23 and it works.** On a guest lane at COINBASE BTC-USD 1h the
  call returned the id `BITCOIN_DOMINANCE…` with `mounted:true` in **439ms**, no
  toast and no error. That closes the question four earlier passes got wrong:
  the add path was never broken — those passes probed `ALWAYS_LOAD_TYPES` keys
  that cannot mount. Pre-check first (`COINBASE` / `1h` / `budget:null` /
  `tc:true`), then add.

  **Do not pick an `ALWAYS_LOAD_TYPES` key.**
  That list means "preload this control when a hardcoded panel restores", not
  "addable": `TRADING_TOTAL_LIQUIDITY`'s control returns
  `{side:'offchart', template: []}` and `addIndicator` refuses on
  `Array.isArray(template)`, while `TRADING_TOTAL_VOLUME` returns
  `side:'external'`. Neither can mount through this path, and earlier passes of
  this map spent four runs concluding the bypass was broken because they probed
  exactly those two keys. Use a dialog-addable native key instead —
  `AGGREGATED_FUNDING_RATE`, `AGGREGATED_OPEN_INTEREST`, `BITCOIN_DOMINANCE`.

  Two rules make the next failure readable:

  - **`undefined` is always a refusal.** A successful add returns the overlay id,
    and anything thrown is caught, logged, toasted AND rethrown — so a throw
    reaches your caller as a rejection, and `undefined` is a deliberate early
    return, never a silent success.
  - **A missing toast proves nothing.** Toasts default to 1500ms and the long wait
    happens BEFORE the refusal, so a separate snapshot misses them. Watch for
    notifications while awaiting, in one eval:

    ```js
    (async()=>{const seen=new Set();
      const iv=setInterval(()=>document.querySelectorAll('.q-notification')
        .forEach(n=>seen.add(n.innerText.trim())),50);
      const r=await chartStore.addIndicator('<KEY>',{},0);
      await new Promise(x=>setTimeout(x,300)); clearInterval(iv);
      return JSON.stringify({r,seen:[...seen]})})()
    ```

  Source-derived on `61d1e911cc`; not yet re-driven.

  **Driven 2026-10-12 on tree `1570b59d69` (the desktop parity sweep's `ind-add`, same result in both hosts):**
  `await chartStore.addIndicator('TRADING_TOTAL_VOLUME', {}, 0)`, with `chartStore` read from
  `document.querySelector('#tc-container-0').__vueParentComponent.setupState`, mounted `TRADING_TOTAL_VOLUME` into
  `window.tc[0].metadata` and then rejected with `TypeError: Cannot read properties of undefined (reading 'find')`. On
  that tree the key does mount through this path, and the throw reaches the caller instead of being caught and
  toasted. Read `metadata` for the mount and report the rejection as its own finding.
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
- **Guest cap — driven 2026-10-23, and the counter does NOT stay pinned.** A bare
  `addIndicator` still bypasses ENFORCEMENT: four successive adds all succeeded
  with no toast and no refusal. But the ticker counter tracks every one of them
  and goes visibly over the limit — `1/3` → `2/3` → `3/3` → `4/3` → `5/3`. An
  earlier note here claimed it stayed pinned at `3/3` while `metadata` grew; that
  is wrong. Assert the over-limit reading, not a pinned one. The cap gate only
  runs when the caller passes `opts.recordUndo` or `opts.enforceIndicatorLimit`,
  which the dialog path does and a bare call does not.
- **Legend handles — driven 2026-10-23.** All fourteen documented handles were
  present on the programmatically added overlay, and `legends.closeBtn.click()`
  removed it cleanly (four overlays torn down in sequence, counter falling back
  to `1/3`). An older warning here said close was untrustworthy on a
  programmatic overlay; that is no longer true. Still poll after the click — each
  teardown took about a second.


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
