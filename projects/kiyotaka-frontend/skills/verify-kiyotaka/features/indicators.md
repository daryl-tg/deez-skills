# Indicators

A user adds an indicator from the Indicators dialog; it mounts as an overlay with
an engine-drawn legend carrying a settings button, a visibility toggle, a close
button, and a loading spinner. Overlays are either native (heatmap, volume, open
interest) or kScript-backed. This entry was last DRIVEN on 2026-10-29 against
product tree `78ec9625d9` (`origin/main`), lane `18103`, a guest lane with no JWT
whose `.env.local` proxies to the operator's remote backend. Driven: the dialog
on its store landing (`See all 241`, tabs `popular, trending, new, paid`) with
the restyled Ask block and its hide and show controls, a programmatic
`BITCOIN_DOMINANCE` add (it mounted, the counter read `2/3`, and its pane drew
367 rows at 1h), and its settings card, whose rows now explain themselves
(`setting-term` labels and a hover card). Earlier, 2026-10-28 on `29c9cda0a2`:
`RSI` listing `Official 4` / `Community 12`, a guest row Add raising the
`indicators` wall, the legend's visibility and close controls, the
`OPEN_INTEREST_PROFILE` `Display` section (`Display mode` reads `Net`), and the
chartless `?wrunRef=` package link, which a guest meets as the `indicators`
wall. The Pine paste offer, the paid and Mine tabs, a real cap REFUSAL (the
dialog path, so a signed-in session), the `Split` display option, the Options
Heatmap's new node-size and ink sliders and its dealer-flow basis (OPRA or CME
options data, signed-in), and the window doors of the built-in options
indicators were not driven.

## Sub-features

- `ind-dialog` the Indicators dialog opens and searches.
- `ind-add` an indicator mounts as an overlay.
- `ind-legend` the legend's settings / visibility / close controls work.
- `ind-catalog` official indicators are listed when the catalog is seeded.
- `ind-limit` the guest cap is enforced.
- `ind-share-link` a package link opens the Indicators dialog on that package:
  `?indicator=@scope/name`, and since `58903c3f75` also a chartless
  `?wrunRef=@scope/name[@x.y.z]`, which the route rewrites to the share link.

## How to get to it (user POV)

- Click `Indicators` in the ticker bar, search, and pick one.
- The mounted overlay's legend sits at the top-left of its pane.
- Open a package link someone shared (`?indicator=@scope/name`, or a chartless
  `?wrunRef=@scope/name`); a guest is asked to sign in first.

## Driving it with control-kiyotaka

Preconditions:

- Baseline from [chart boot](./chart-boot-and-data-plane.md), guest modal dismissed.

- **Open the dialog.** Run
  `./control-kiyotaka browser find role button click --name "Indicators" --exact`,
  then `./control-kiyotaka browser snapshot -i -c`. The dialog carries
  `textbox "Search official indicators"` and
  `textbox "Add a package by exact name (@scope/name)"`. It is a `.dialog-style`
  overlay, **not** a `.q-dialog`.
  **Current handles, driven 2026-10-27 on `7290d33d10`.** The root is
  `indicator-panel-v2` and the search field is `indicator-search-bar-input`
  (`indicator-dialog-skeleton-input` while it loads), not the textboxes named
  above. With no query the dialog opens on a store landing:
  `indicator-store-landing`, an Ask block (`indicator-ask-block`,
  `indicator-ask-question-<topic>`), the official shelf
  (`indicator-store-official-shelf`, `indicator-shelf-card-<slug>`, and
  `indicator-store-see-all-official-btn` reading `See all <n>`) and
  `indicator-store-community`. A query switches to grouped results: group heads
  are `indicator-list-head-<key>` with the count in `indicator-list-head-<key>-count`
  (`official`, `community`), inside `indicator-results-list` /
  `indicator-list-scroll`. `indicator-list-group-count` and
  `indicator-category-chip-technical` are GONE (zero matches live and in source).
  The guest strip showed `popular, trending, new, paid`.
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
- **Legend handles — driven 2026-10-23 and again 2026-10-27.** All fourteen
  documented handles were present on the programmatically added overlay, and
  `legends.closeBtn.click()` removed it cleanly (four overlays torn down in
  sequence, counter falling back to `1/3`). An older warning here said close was
  untrustworthy on a programmatic overlay; that is no longer true. Still poll
  after the click — each teardown took about a second. On 2026-10-27
  `settingsBtn.click()` opened the overlay's settings dialog (`Template`, `Style`,
  `Plot settings`, `Visibility`, `Pane`; `Escape` closes it), and
  `toggleVisibilityBtn.click()` flipped the metadata row's `isHidden` from `false`
  to `true` and back. The legend also exposes `copyBtns`, `moreBtn`,
  `rowActionBtn`, `bylineBtn`, `errorChipBtn`, `seriesChips` and `overflowChip`.
  One legend probe built from a shell variable holding an arrow-function filter
  failed with `SyntaxError: Unexpected token ';'` under `browser eval` (cause not
  isolated); the same probe written with `function` callbacks worked.


- **The settings open as a docked card, not a dialog — driven 2026-10-28.**
  `settingsBtn.click()` now opens a card at the right of the chart
  (`data-testid=settings-panel`, with `indicator-<slug>-settings` inside, for
  example `indicator-open-interest-profile-settings`). The overlay union
  `.q-dialog, .dialog-style, [role=dialog].open` reads `0` while it is open, so
  probe `[data-testid=settings-panel]` instead. Close it with
  `overlay-settings-close-btn`: on 2026-10-29 an `Escape` sent while a
  `setting-term-card` was up left the panel open. Since
  `a3fde686d1` a frame shows on the click while the settings chunk loads, so
  poll for the card's own fields before you assert them.
- **Every settings row explains itself — driven 2026-10-29.** Since
  `899c3b1af2` a row label is a `setting-term` (`src/components/common/SettingTerm.vue`).
  `BITCOIN_DOMINANCE`'s card carried 10 (`Width`, `Smoothing effect`,
  `Color mode`, `All intervals`, `Axis label`, `Name label`, ...). Hover one
  (`find testid setting-term hover` takes the first) and `setting-term-card`
  opens with the explanation: `Width` read `How thick the line draws, from 1 to
  10. Every line this indicator draws takes the same width.`
  `setting-term-learn-more` shows only when a docs origin is configured (absent
  on the lane) and `setting-term-staff` only for staff (absent). The form's own
  testids are templated: `indicator-<slug>-settings`,
  `-section-<group>`, `-<fieldKey>-row`, `-note-<fieldKey>`, `-<toggle>-toggle`.
  The on and off controls are the app-wide pill since `8b8b211759`:
  `[role=switch][data-testid=on-off-toggle-btn]` read by `aria-checked` (four on
  this card).
- **The Ask block — driven 2026-10-29.** The store landing's
  `indicator-ask-block` now carries `indicator-ask-promise` (`Nothing is added
  until you choose`), three `indicator-ask-question-<topic>` buttons
  (`derivatives`, `order_book`, `delta_cvd`) and `indicator-ask-hide-btn`. Its
  click left the block with `indicator-ask-show-btn` and no questions; the show
  button brought all three back.
- **Open Interest Profile `Display` — driven 2026-10-28.** On BINANCE.F
  ETHUSDT, `addIndicator('OPEN_INTEREST_PROFILE',{},0)` mounted and its settings
  `Source` tab showed a `Display` section: `Display mode` (`Net`), `Bar width`,
  `Hollow bars`, `Background`, `Behind candles`. The modes come from
  `metricProfileDisplays` (`src/utility/chart/metric-profile.util.ts`); the
  source adds `Split` for this member. A synthetic `click()` on the select did
  not open its list, so `Split` is source-only. Mount it on a derivative: open
  interest does not exist on spot.
- **`ind-share-link` — driven 2026-10-28 as a guest.** Open
  `http://127.0.0.1:<lane>/chart/?wrunRef=@om-core/trend-candles`. The address
  bar ends at `/chart/` with both params stripped, the sign-in wall rises with
  `guestLoginFeatureId=indicators`, and `sessionStorage` holds
  `kiyotaka:indicator-share-link` = `{"package":"@om-core/trend-candles",...}`,
  which the sign-in reload acts on. So a guest never sees the dialog open on the
  package; that half needs a signed-in session. A link that names a chart keeps
  its mount instead (`applyWrunRefDeepLink`). Source:
  `src/router/guards/wrun-ref-root-link.guard.ts`,
  `createIndicatorShareDeepLink` in
  `src/utility/sharing/indicator-share-link.util.ts`, wired in
  `src/pages/chart.vue`.
- **Proof.** Screenshot the pane with the legend visible, plus the engine-state
  read naming the overlay. Capture the settings dialog as its own frame if the
  claim is about settings.

## Gotchas

- **Whether the catalog is seeded depends on which backend the lane proxies.**
  With the operator's `.env.local` the lane proxies to a remote dev backend that
  IS seeded (2026-10-27: `See all 241` official, `RSI` gave four official rows,
  `official-indicator-add-official-indicator-relative-strength-index-rsi-official-rsi-btn`
  first). The unseeded case below applies to a lane pointed at a fresh local
  stack.
- **A fresh local stack lists NO official indicators.** The dialog renders only
  backend catalog rows; the FE registry never synthesizes them. An unseeded local
  mongo therefore shows zero official indicators — RSI, Open Interest, the whole
  options suite — which reads as a broken feature. Fix with
  `./control-kiyotaka cli -- node scripts/seed-official-catalog.mjs`. Dev builds
  render a warning banner naming that command
  (`indicator-catalog-unseeded-notice`, dev builds only). `Browse all indicators`
  and `Discover` are LEGACY names; the current dialog opens on the store landing,
  so look for the notice in the results list, not under those tabs.
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
- **A retired kScript row refuses to add (source, `58903c3f75`).** A row that
  `isRetiredKscriptDoc` matches raises a 3 s warning toast
  (`dialogs.indicatorDialog.kscriptRetire.cannotAdd`) and mounts nothing
  (`src/composables/chart/useIndicatorCatalog.ts`). A missing overlay after such
  an Add is the refusal, not a broken add.
- **Not every legend shows the pin and window doors (source, `672415eaff`).**
  `hasPinToChartDoor(type)` in `src/constants/indicator.constants.ts` hides the
  pin button, `Move to price pane` and the Objects pin for foreign-domain and
  on-chart types, and the nine built-in options indicators in
  `WINDOW_NATIVE_OWNER_TYPES`
  (`packages/wrun-chart-host/src/utility/chart/window-owner.leaf.ts`) now get
  the window doors and skip the pane move. Check `shouldShowPinToChartBtn`
  before asserting `pinToChartBtn`.
- Some indicators are interval-sensitive: TPO sessions are daily, so at `1m` the
  profile is off-screen and the frame looks blank. Pin a sane interval first.
