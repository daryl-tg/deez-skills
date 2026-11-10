# Indicators

A user adds an indicator from the Indicators dialog; it mounts as an overlay with
an engine-drawn legend carrying a settings button, a visibility toggle, a close
button, and a loading spinner. Overlays are either native (heatmap, volume, open
interest) or script-backed (TypeScript Indicators; kScript rows are retired and
leave the chart at restore). This entry was last DRIVEN on 2026-11-10 against
product tree `c2c02b7b42` (`origin/main`, 60 commits past `32dd0c6354`), lane
`18103`, a guest-JWT lane: the dialog's guest strip (still `popular, trending,
new, paid`, no Favorites tab), an `rsi` search (`Community 13`), and the
community package `RSI + Divergence [SolAtlas]`'s pane star raising the
`indicators` wall (see `ind-favorites`). Before that, last DRIVEN on 2026-11-09 against
product tree `32dd0c6354` (`origin/main`, 60 commits past `943281a2eb`), lane
`18103`, a guest-JWT lane: a programmatic `ORDERBOOK_PROFILE` on BINANCE.F
BTCUSDT and its new `Grouping mode` (see `ind-ob-grouping`), and the settings
search's three `Escape` steps on a `SESSION_VOLUME_PROFILE`. Before that, last
DRIVEN on 2026-11-08 against
product tree `943281a2eb` (`origin/main`, 59 commits past `dced88e06a`), lane
`18103`, a guest-JWT lane on the remote dev backend: an `Open Interest` search
(`Official 8`, `Community 2`) whose row Add raised the `indicators` wall, a
programmatic `OPEN_INTEREST` on BINANCE.F BTCUSDT (357 rows, `Indicators
2/3`), its settings card's `Plot type` switched from Candles to Line through
the new ComboBox (see `ind-oi-plot`), and the system-origin remove back to
`Indicators 1/3`. Not driven: the CVD flow dominance grey bar and the wrun
`has nothing to draw` note (see Gotchas). Before that, DRIVEN on 2026-11-07 against
product tree `dced88e06a` (`origin/main`, 81 commits past `8bcd72f8f5`), lane
`18103`, a guest-JWT lane on the remote dev backend: an `rsi` search
(`Official 4`, `Community 12`). Since `d02874f2a8` every wrun indicator runs
on US equities, NASDAQ tapes included, and an app-layer overlay such as the
stock Tape's `Dark pool prints` gets no window door and no gear or close in
its legend (source). Before that, DRIVEN on 2026-11-06 against
product tree `8bcd72f8f5` (`origin/main`, 119 commits past `87a325f4ab`), lane
`18103`, a guest-JWT lane on the remote dev backend. Driven that day: an `rsi`
search (`Official 4`, `Community 12`) whose `Add to chart` raised the sign-in
card (the add stopped at the wall, counter still `Indicators 1/3`), and on
COINBASE BTC-USD `15m` a programmatic `SESSION_VOLUME_PROFILE` whose docked
card read `Session Daily` and carried the new in-place settings search (see
`ind-settings-search` and `ind-session-default`). Before that, DRIVEN on 2026-11-05 against
product tree `87a325f4ab` (`origin/main`, 123 commits past `8436920004`),
lane `18103`, a guest-JWT lane on the remote dev backend (`See all 243`
official). Driven that day: an `rsi` search (`Official 4`, `Community 12`)
whose `RSI` row Add raised the `indicators` wall with the words left
unselected (the wall stops the add, so the new select-after-add was not
reached), programmatic `BITCOIN_DOMINANCE` (`Indicators 1/3`) and
`TIME_PRICE_OPPORTUNITY` (`Indicators 2/3`) mounts, the TPO settings card's
new `Trading hour` list (see the TPO bullet), and both removed through
`legends.closeBtn`. Not reached: a capped strip picture (every cover the dev
backend served was a 112 x 112 square). Before that, DRIVEN on 2026-11-04 against
product tree `8436920004` (`origin/main`), lane `18103`, a guest-JWT lane on
the remote dev backend. Driven that day: an `open interest` search (`Official
8`, `Community 2`), programmatic `OPEN_INTEREST`, `FUNDING_RATE` and
`LIQUIDATIONS` mounts on the spot COINBASE BTC-USD pane (gated hidden, see the
spot-pane bullet) beside a visible `AGGREGATED_OPEN_INTEREST`, the counter at
`Indicators 5/3` with the `Plus workspace · locked` strip, a guest's click on
a pane's merge button raising the `indicators` wall with no Plus prompt (see
the pane-merge bullet), and `chartStore.removeIndicator` clearing every
programmatic overlay. Before that, DRIVEN on 2026-11-03 against
product tree `215896e614` (`origin/main`), lane `18103`, a guest-JWT lane whose
`.env.local` proxies to the operator's remote backend. Driven that day: the
dialog at 1440 px as a **split view** (the store card beside
`indicator-pane`, which showed the first shelf card, `Key Levels`, with
`indicator-detail-apply-btn` `Add to chart`, `indicator-detail-favorite-btn`
and `indicator-pane-more-btn`; `See all 193`), the shorthand search `poc`
listing six volume-profile rows, two sentences that never reached the
sentence lane (see the search bullet), the `RSI` row Add raising the `indicators` wall, programmatic
`BITCOIN_DOMINANCE` and `MA_RIBBON` adds (`Indicators 3/3`), the docked
settings card (10 `setting-term` rows, `settings-panel-mode-btn`), the
legend's more menu with eight rows (see the pane-move bullet), and its
`Move to price pane` on the Bitcoin Dominance pane raising the same
`indicators` wall. Before that, DRIVEN on 2026-11-02 against product tree
`a4488341f6` (`origin/main`), lane `18103`, a guest lane with no JWT. Driven: the
store landing (`See all 243`, tabs `popular, trending, new, paid`, three shelf
cards, the Ask block with its hide and show; on BINANCE.F ETHUSDT the three
questions were `footprint, levels, market_structure`, see the Ask bullet), an
`RSI` query (`Official 4`, `Community 12`, the first row
`official-indicator-add-official-indicator-relative-strength-index-rsi-official-rsi-btn`
with `Oscillator 14, close` and an `Add · 1 slot` affordance), that row's Add
raising the `indicators` wall, programmatic `BITCOIN_DOMINANCE` and
`MA_RIBBON` adds (464 rows each, the counter `Indicators 3/3`, the ribbon's
legend `Moving Average Ribbon`), the docked settings card (10 `setting-term`
rows, `settings-templates-trigger` and `-value`, the Float/Dock toggle
`settings-panel-mode-btn`, `overlay-settings-close-btn`), the legend's more
menu (`indicator-menu` with `indicator-menu-{settings,copy,pane-move,show-on,remove}`;
the `-scale` and `-fold` rows were missed that day, see the pane-move bullet),
**the pane move, which is guest-walled**: `indicator-menu-pane-move` (`Move
to new pane`) raised the sign-in wall headed `Technical Indicators` with
`guestLoginFeatureId = "indicators"`, which is why the 2026-11-01 attempt saw
no move; `legends.closeBtn.click()` tearing both overlays down (`Indicators
1/3`); and the `?wrunRef=@om-core/trend-candles` link (URL stripped,
`indicators` wall, the package stashed in `sessionStorage`). Earlier,
2026-11-01 on `120d5d5d32` (`origin/main`, lane `18103`, no JWT). Driven: the
dialog on its store landing (`See all 243`, tabs `popular, trending, new,
paid`, three shelf cards, the Ask block's families `derivatives, order_book,
delta_cvd` and its hide and show), an `RSI` query (`Official 4`, `Community
12`, the first row `official-indicator-add-official-indicator-relative-strength-index-rsi-official-rsi-btn`
with the new plain-words subtitle `Oscillator 14, close`), a guest row Add
raising the `indicators` wall, programmatic `BITCOIN_DOMINANCE` and `MA_RIBBON`
adds (both mounted with 440 rows, the counter read `Indicators 3/3`), the
docked settings card (`settings-panel`, 10 `setting-term` rows, the Float/Dock
toggle `settings-panel-mode-btn`, `overlay-settings-close-btn`), the legend's
visibility and close controls, and a `?wrunRef=@om-core/trend-candles` link
(URL stripped, `indicators` wall, the package stashed). Attempted, not proven:
the pane move (`Move to new pane` was reached once through the legend's more
menu but the ribbon stayed on the price pane; a dispatched `contextmenu` on
the canvas opened no menu). Earlier, 2026-10-29 on `78ec9625d9`
(`origin/main`, lane `18103`, no JWT): the dialog
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
- `ind-settings-search` a long built-in's settings card filters its rows in
  place from a search field.
- `ind-session-default` a session volume profile on an intraday chart defaults
  to the Daily session.
- `ind-share-link` a package link opens the Indicators dialog on that package:
  `?indicator=@scope/name`, and since `58903c3f75` also a chartless
  `?wrunRef=@scope/name[@x.y.z]`, which the route rewrites to the share link.
- `ind-ob-grouping` Order Book Profile's `Grouping mode` keeps its bands fixed
  at every zoom, or joins them as you zoom out.
- `ind-oi-plot` Open Interest and Agg. Open Interest draw as Candles (the
  default) or as a Line of the closes, picked from the settings card's
  `Plot type`.

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
  The guest strip showed `popular, trending, new, paid` (again on 2026-11-10).
  A signed-in viewer also gets `indicator-store-tab-favorites`, last in the
  strip and shown even with nothing starred (`46208d6a31`, source); the strip's
  divider sits before Mine, or before Favorites when there is no Mine.
- **The dialog was rebuilt as a "store", and every tab handle this entry used is
  gone.** `indicator-control-bar-tab-indicators-btn`, `-tab-kscript-btn`,
  `-favorites-btn`, `-sort-btn`, `indicator-source-tab-official`/`-community`,
  `indicator-registry-tab-*`, `indicator-tab-discover-btn`/`-all-btn` and
  `indicator-browse-all-btn` have ZERO matches in source. The strip is now
  `indicator-store-tabs` with
  `indicator-store-tab-{popular,trending,new,following,paid,mine,favorites}`, and it hides
  itself when a viewer qualifies for fewer than two tabs. The empty state is
  `indicator-empty-state` / `-action-btn`.

  Handles that survived: `indicator-panel-v2` (root), `indicator-search-bar-input`
  (plus a skeleton twin `indicator-dialog-skeleton-input`),
  `indicator-search-bar-chart-only-btn`, `indicator-list-card-upgrade-btn`, and
  `indicator-catalog-unseeded-notice` — the last now gated on
  `import.meta.env.DEV` alone, so it is a dev-build banner rather than a
  catalog-state signal. Row adds are
  `official-indicator-add-official-indicator-<slug>-btn`; once that indicator
  is on the chart the same pill becomes `indicator-added-<slug>-btn`, which
  opens `indicator-added-menu-<slug>` with `indicator-add-another-<slug>-btn`
  and `indicator-remove-<slug>-btn`, and `indicator-count-<slug>` shows from
  two copies (`IndicatorAddPill.vue`, source). On the detail page and the
  pane, `indicator-detail-apply-btn` is Add (`Add to chart`, driven
  2026-11-03), `indicator-detail-added-btn` is Added, and
  `indicator-detail-add-btn` is now that menu's `Add another` item, not the
  Add button (`IndicatorDetailPanel.vue`).

  **At 1100 px and wider the dialog is a split view (`c6aad32e02`; driven
  2026-11-03 at 1440).** `SPLIT_VIEW_MIN_WIDTH_PX` is `1100`
  (`indicator-split-window.ts`). Beside the store card sits `indicator-pane`,
  which opened on the first shelf card (`Key Levels`) rather than on
  `indicator-pane-empty`. A row or shelf card under the pointer for 150 ms
  (`PANE_REST_MS`) or highlighted by the arrow keys fills the pane instead of
  opening the full page, so a "click a row, then go back" recipe holds only
  below 1100 px. Pane handles, read live: `indicator-pane-page`,
  `indicator-pane-picture` and `-picture-cover`, `indicator-pane-information`
  with `indicator-pane-info-{maker,category,version,updated,price,uses}`,
  `indicator-pane-more` / `-more-title` / `-more-<entryId>` (for example
  `indicator-pane-more-official:OPTIONS_HEATMAP`), and
  `indicator-pane-more-btn`, which opens `indicator-pane-menu` with
  `indicator-pane-door-<share|window|page|source|fork|post|like|people>`
  (source, not opened).

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
  an overlay added programmatically, neither `closeBtn.click()` nor a real
  browser click on that button removed it within 25s on an earlier tree, even
  though the button was connected, visible and `shouldShowCloseBtn` was true, so
  prove any legend claim on a dialog-added overlay and do not report a removal
  bug from a programmatic one. To clean up programmatic mounts, call the store
  with the system origin: on 2026-11-04 (`8436920004`)
  `await chartStore.removeIndicator(id, 0, {}, {origin:'system'})` took six
  programmatic overlays (`OPEN_INTEREST`, `FUNDING_RATE`, `LIQUIDATIONS` and
  three `AGGREGATED_*`) out of `metadata` within 4 s, and the counter went
  back to `Indicators 1/3`.
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
- **The card's menus are ComboBoxes, not native selects (`18c8a69659`;
  driven 2026-11-08 on `943281a2eb`).** On a programmatic `OPEN_INTEREST` the
  card held no `select` and three `combo-box-trigger-btn` buttons
  (`role=combobox`, `aria-expanded`), reading `USD`, `Candles` and `Symbol`.
  Several share the testid, so pick one by its text or by the row's own
  testid. A click lists `combo-box-option-<value>` rows (`role=option`).
- **`ind-oi-plot`: Open Interest as a line (`254c5ce876`; driven 2026-11-08
  on `943281a2eb`).** Add `OPEN_INTEREST` on a derivative
  (`chartStore.addIndicator('OPEN_INTEREST',{},0)` on BINANCE.F BTCUSDT), open
  its card with `legends.settingsBtn.click()`, click the
  `combo-box-trigger-btn` that reads `Candles` (the `Plot type` row under
  `Display`), then `find testid combo-box-option-spline click` (`Line`; the
  other option is `combo-box-option-candle`). Proof: the overlay's
  `settings.meta.plotType` went from `candle` to `spline` with its 357 rows
  kept, the trigger read `Line`, and the pane redrew as one line. Agg. Open
  Interest carries the same row (source,
  `src/indicators/controls/open-interest/plot-type.ts`).
- **`ind-ob-grouping`: Order Book Profile grouping (`0f3c552e1f`; driven
  2026-11-09 on `32dd0c6354`).** On a derivative, mount
  `await chartStore.addIndicator('ORDERBOOK_PROFILE',{},0)`, open the card with
  `legends.settingsBtn.click()`, and open the `Grouping mode` ComboBox (its
  trigger reads `Dynamic`; pick it by its text, `combo-box-trigger-btn` is
  shared). The menu lists `combo-box-option-dynamic` (`Bands join as you zoom
  out, so values stay readable`) and `combo-box-option-fixed` (`Keeps your
  grouping at every zoom`). `combo-box-option-fixed` wrote `settings.groupingMode`
  `fixed` and the trigger read `Fixed`. Remove with `legends.closeBtn.click()`.
- **`ind-settings-search`: search a built-in's settings in place (driven
  2026-11-06 on `8bcd72f8f5`).** Since `1235632725` and `fb01153fbe` the
  docked card shows a magnifier (`settings-search-btn`, `Search settings`)
  when the overlay is not the main chart, the device is not a phone, it is not
  a script row, and the form owns its own page rail (TPO, footprint) or has
  more than 12 rows. A card of 12 rows or fewer has no magnifier, so the
  10-row `BITCOIN_DOMINANCE` card is a negative. Wrun indicators keep their own
  filter. `Cmd+F` opens the field while the card holds focus. `Escape` takes three
  presses since `ee1fae1b4d`: the first clears the words (the field keeps
  focus and `settings-search-clear-btn` goes), the second leaves the search,
  the third closes the card (driven 2026-11-09 on `32dd0c6354`). On a programmatic
  `SESSION_VOLUME_PROFILE` (62 `.i-overlay-settings-row`) the magnifier came
  about 5 s after the card (poll for it), and `find testid
  settings-search-input fill "wid"` left 6 rows visible (`Session`, `Display`,
  `Bar width 70`, `Level lines`, `Width Default` …), the card carrying
  `data-settings-searching` and `data-search-ready`; hidden rows carry
  `data-search-hidden`. `fill "zzzz"` showed `settings-search-empty`: `No
  settings match “zzzz” Some settings show only when another setting is on.`
  Matching is by word start on the row name, its group head and its option
  names; the match highlight uses the CSS Custom Highlight API, so no DOM span
  marks it.
- **`ind-session-default` (driven 2026-11-06 on `8bcd72f8f5`).** Since
  `13acd4683c` a `SESSION_VOLUME_PROFILE` (and the aggregated one) with no saved
  session type defaults to Daily from `1m` up to below `1d`, and to Targeted
  below `1m` and from `1d` up; Delta, OI and Liquidation profiles keep
  Targeted. Assert the drawn session, not the stored word: on BTC `15m`
  `settings.sessionType` read `null` and `settings.session` `86400000`, and the
  card's Session row read `Session Daily`. The `1d` switch back to Targeted is
  not driven.
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
- **The Ask block — driven 2026-10-29 and 2026-11-02.** The store landing's
  `indicator-ask-block` carries `indicator-ask-promise` (`Nothing is added
  until you choose`), three `indicator-ask-question-<topic>` buttons and
  `indicator-ask-hide-btn`. Its click left the block with
  `indicator-ask-show-btn` and no questions; the show button brought all three
  back. **The three families rotate.** They read `derivatives, order_book,
  delta_cvd` on 2026-10-29 and 2026-11-01 and `footprint, levels,
  market_structure` on 2026-11-02 (BINANCE.F ETHUSDT): `ASK_QUESTION_FAMILIES`
  in `src/utility/chart/indicator-ask-questions.util.ts` advances by three on
  every open (`ASK_QUESTIONS_SHOWN`), and only families the
  chart's market answers (`askQuestionFits`) are offered, so assert three
  distinct `indicator-ask-question-*` ids, not which three.
- **The dialog remembers its last query (driven 2026-11-02).** A reopen after
  an `RSI` search lands on the results with `RSI` still in
  `indicator-search-bar-input`, so `indicator-store-landing`,
  `indicator-store-see-all-official-btn` and the Ask block are absent. Clear
  the field (`find testid indicator-search-bar-input fill ""`) and the landing
  returns within 2 s. `See all N` is `Math.max(storeShelfCount,
  entries.length)` for the active tab (`IndicatorOfficialShelf.vue`,
  `useIndicatorCatalogV2.ts`), so it is the official rows in that tab, not a
  backend total. The slot count is a caption under the row's Add,
  `indicator-slots-<slug>` (`1 slot`; `0 slots` when it costs none; read
  2026-11-03), and a row's favourite star carries no testid (match it by
  accessible name); the pane's star is `indicator-detail-favorite-btn`.
- **`ind-favorites`: the Favorites tab and stars on community packages
  (`46208d6a31`; the wall driven 2026-11-10 on `c2c02b7b42`).** A community
  (registry) package can now be starred: the pane star is enabled on it, titled
  `Add to favorites` or `Remove from favorites`, and it is disabled (titled
  `Favorites are not available for this indicator yet`) only on a row with no
  favourite key, such as a converted script. A signed-in star flips at once,
  writes `PATCH` or `DELETE /users/favoritePackages`, reverts with a toast if
  refused, and stops at 300. The Favorites tab lists starred rows from both
  the Official and Community sides (Official only on a governed CME chart);
  empty, it reads `Star an indicator to keep it here.` Unstarring the
  highlighted row on Favorites keeps it in the pane until the highlight moves
  (source). **For a guest:** fill `rsi`, click
  `indicator-name-rsi-divergence-solatlas-solatlas` (the community group head
  read `Community 13`); the pane star read enabled, `Add to favorites`. Its
  click raised the sign-in card headed `Technical Indicators`
  (`guestLoginFeatureId` `indicators`), sent no `favoritePackages` request (a
  wrapped `fetch` saw none) and left the star unchanged. Not driven: the tab
  and a real star (signed-in only).
- **Shorthand and sentence search (driven 2026-11-03).** Trader shorthand finds
  indicators (`e93440ac46`, `src/constants/indicator-names.ts`): `poc` listed
  `Sliding Volume Profile`, `Session Volume Profile`, `VRVP`, `Value Area
  Reversion`, `Volume Profile and Value Area` and `Agg. Session Volume
  Profile`. The sentence lane (`indicator-list-sentence`, its no-fit head
  `indicator-sentence-no-fit` "No exact fit" with
  `indicator-sentence-band-closest` and `-band-family`; source,
  `bdc652a36f`) did not engage for a guest: `show me where whales hide purple
  bananas at night` gave `No indicators found`, and `where are buyers more
  aggressive than sellers` showed no empty state, with no
  `indicator-sentence-*` node either time. The lane's `enabled()` needs a
  sentence host (`useIndicatorCatalogV2.ts`); why a guest had none was not
  traced, so the sentence bands stay unproven.
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

- **New in `dced88e06a..943281a2eb`, source only, not driven:** CVD flow
  dominance and CVD draw a bar grey (no side) where the spot or perps leg did
  not trade or has no venue, and keep every leg
  (`src/indicators/controls/cvd-flow-dominance/flow-side.ts`, `943281a2eb`). A
  wrun indicator that draws nothing says so in its legend: `{name} has
  nothing to draw on this chart.`, or that it reads a longer interval than
  this chart's history holds (`wrun.refusal.sentence.nothingDrawn` and
  `nothingDrawnReach`, `a169947dca`); a slow sandbox worker is now waited on
  for up to 180 s instead of being quarantined. The Price only pause also
  names the stock Tape's `Dark pool prints` layer (`b7ffd40d4b`). Each needs
  a market or a signed-in wrun add this guest lane did not reach.
- **New in `120d5d5d32..a4488341f6`, source only, not driven:**
  - A US stock's Live price feed lifts a row's wall through the Trades feed:
    the row shows `indicator-trades-feed-<slug>` (`Trades feed`), an Add on it
    asks to switch to Trades first, and the legend's diagnostic card offers
    `legend-diagnostic-card-switch-trades` (`IndicatorRow.vue`,
    `LegendDiagnosticCard.vue`; `dc92b520b5`, `94f2354f15`). The add doors are
    wrapped by `answerRefusedAdd` and `stockFeedWallFor`
    (`chart.add-indicator.ts`); a crypto lane never meets them, and a guest
    reads the `us-equities-full` flag off.
  - The settings card's template menu gains a "Save as default" row and
    `settings-template-default-note` (`SettingsTemplatesMenu.vue`,
    `3ed1679add`; toasts `defaultSaved` and `defaultNothingToKeep`). On
    2026-11-02 the docked card showed `settings-templates-trigger` and
    `-value`; the note was not in the DOM with the menu closed.
  - Every store-listed indicator carries a plain-words subtitle
    (`indicator-labels.builtin.json`, `indicator-label-basis.util.ts`;
    `6471ebc723`, `4f8f1a4bf4`); `ae55578e77` and `b10888e36c` record which
    row a sentence answer led to (`sentenceAnswered`, `sentencePicked`), with
    no surface.
  - The ten options overlays follow the chart's market after a switch
    (`8a69220785`); Cumulative Returns by Session draws only inside its session,
    closed hours faint, as unbroken steady lines (`c963ab53df`, `38bc469231`,
    `440d23be2d`, `f67ff294ef`); Big Trades 0.10.0 sets its minimum in coins
    on crypto charts (`c45a9f4e80`), and since `83d1683b82` Big Trades
    0.11.0 draws one bubble per aggressor order (fills that share a
    sub-millisecond stamp and side join) and Min size filters bubbles but
    never resizes one; a wrun banded order-book input with a
    `when` gate (`47fff639e5`); the kit was `0.109.0` on `a4488341f6`,
    `0.110.0` from `987eb6e7ac` (the Liquidation Map look) and is `0.118.0`
    since `49653af1f6` (source).
- **New on `849fb08e95`, source only, never driven:**
  - The moving average ribbon is a built-in, `MA_RIBBON` (`dedda2c7bf`,
    `src/indicators/controls/ma-ribbon/`, chart-schema `0.8.1`). It needs no
    catalog row and never fetches history. Mount it the way the other guest
    recipes do, `chartStore.addIndicator('MA_RIBBON', {}, 0)`; a fresh mount
    should draw four SMA lines (20, 50, 100, 200) with four EMA slots off, and
    the legend names each line (`SMA 20`).
  - A late read now says why in its legend row (`c4dbe3d045`):
    the chip's words (class `.kiyo-legend-chip-label`, not a testid) read
    `Waiting on network`, `Slow network` or `Still loading` with a seconds
    counter, `.kiyo-legend-chip-retry` retries, and the testid
    `pane-footer-slow-network` adds `· Slow network` to the footer. The words
    appear at 5 s with evidence of a stall, 15 s without. No deterministic guest
    trigger was found.
  - A settings row now hides only while its value has no effect (`d9727ce894`,
    `0c0f2ec4e5`, `587939bdaa`); toggle the controlling switch and assert the
    `-<fieldKey>-row` testid comes and goes.
  - The regular TPO marks each profile's open and close block (`cb070d70a5`),
    with Color-tab switches `highlightOpen` and `highlightClose`. Since
    `b477d40c8b` (titan `0.0.4-alpha.1292`) a closed session's block fills its
    whole span with no gap at its edges (source, engine-side).
  - A footprint whose rows set its geometry waits for the main candles and
    asks once, so a market switch no longer shows an aborted first ask and a
    re-ask (`64c9c0b522`, `9ed29c0009`; source).
  - **TPO follows the chart's session by default (driven 2026-11-05;
    `b9cc632661`, `4d858bf835`, `af3004b625`).** A new TPO stores
    `tradingHour: null` with `tradingHourVersion: 2`, which the settings card
    shows as `Trading hour` `Chart session`. Its list, read live: `Chart
    session` (`Follows the chart: regular hours on a stock chart that shows
    them, else the whole day`), `All hours`, `Pre-Market`, `Regular`,
    `Post-Market` (New York time), `Asia` and `Asia full` (Tokyo time),
    `London` and `London full` (London time), `New York` and `New York full`,
    `Pre-Close` (UTC) and `Custom`, with a `Custom sessions` switch above it.
    Open the card with `legends.settingsBtn.click()` and the list with the
    `.combo-box__trigger` that holds `Chart session`. On a crypto chart Chart
    session draws the whole day; the regular-hours case needs a US stock
    chart with the `us-equities-full` flag, which a guest reads off. TPO and
    range profiles now draw on US stock charts instead of `No data in range`
    (`e5dee82216`, source), and the order-flow and session tools start a
    regular-hours stock day at 09:30 (`e4bda0a273`, source).
  - **Store pictures cap their zoom (source, `ad2c5fc913`, `422b70b2ba`).** A
    strip-shaped cover drawn past 1.5 screen pixels per picture pixel is drawn
    at that cap on its right end over a `#0d0c11` ground, and its layer carries
    `data-picture-fit="capped"`; opening such a card's page skips the flight.
    Not driven: on 2026-11-05 the dev backend served only 112 x 112 square
    covers, so no `[data-picture-fit]` node existed.
  - **After an add the search words are selected (source, `2fba2696fa`).** The
    next name typed replaces them. A guest's dialog Add raises the
    `indicators` wall first, so this needs a signed-in session.
  - **Order-flow tools pause on a stock's free `Price only` feed (source,
    `315fa465d9`).** Their legend chip reads `Paused. {feed} has no trades.`
    and the legend card offers Back to Trades and Get real-time. Needs the
    `us-equities-full` flag, so not guest-reachable.
  - The Indicators dialog's favourite star reads disabled, with its reason in
    the title, on a row that cannot take one (`f6ba61116e`); a guest's
    favourite write is walled.

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
- **A retired kScript row refuses to add, and a saved one leaves the chart
  (source, `58903c3f75`, `d7500721fc`, `722911b50f`; read on `120d5d5d32`).** A
  row that `isRetiredKscriptDoc` matches raises a 3 s warning toast
  (`dialogs.indicatorDialog.kscriptRetire.cannotAdd`) and mounts nothing
  (`src/composables/chart/useIndicatorCatalog.ts`). A saved kScript row that
  reads `retired` is taken out of the restore and the workspace document once
  (`src/utility/chart/kscript-retired-rows.util.ts`); the `Retires in {n}
  days` chips, the sunset toast and the `legend-diagnostic-card-sunset` card
  are gone, and `KscriptSunsetNotice.vue` now only toasts a lossy twin
  conversion's settings reset (`kscript-sunset-settings-reset`). A missing
  overlay after such an Add, or after a restore, is the retirement, not a
  broken add. A guest has no saved rows, so none of it is guest-reachable.
- **The pane move is guest-walled (source, `66450484c2`, `fbb32ff5c2`;
  driven 2026-11-02 on `a4488341f6`).** `OWN_PANE_MOVABLE_TYPES` is `VWAP`
  and `MA_RIBBON` (`src/composables/chart/useIndicatorMenu.ts`): on the price
  pane their legend menu and the chart right-click menu (after Hide) offer
  `Move to new pane`, and in their own pane `Move to price pane`. The legend's
  `moreBtn.click()` opens the Vue menu `indicator-menu` (`IndicatorMenu.vue`)
  with `indicator-menu-settings`, `indicator-menu-copy`,
  `indicator-menu-pane-move` (`Move to new pane`), `indicator-menu-scale`
  (a submenu, `indicator-menu-scale-<side>`), `indicator-menu-show-on`,
  `indicator-menu-fold` (`Fold legend`) and `indicator-menu-remove`
  (`-move-up` and `-move-down` exist in source; read live 2026-11-03 on the
  Bitcoin Dominance pane: eight rows, header `BITCOIN DOMINANCE`). Pick the
  row's own legend `More` button: the price pane carries one per row, and the
  last `[class*=legend] button[aria-label=More]` was the Bitcoin Dominance
  pane's. The pane-move row is not only for `OWN_PANE_MOVABLE_TYPES`: an
  own-pane indicator gets `Move to price pane` as a pin
  (`indicatorMenuFacts`, `action: 'pin'`), and a merged row `unmerge`. On
  2026-11-03 the pin move on Bitcoin Dominance raised the same `indicators`
  wall and the overlay stayed `offchart`.
  A guest's click on `indicator-menu-pane-move` raises the sign-in wall headed
  `Technical Indicators` (`guestLoginFeatureId = "indicators"`) and the ribbon
  stays `type: "onchart"`; that is what the 2026-11-01 attempt saw as "the
  move not observed". Proving the move itself needs a signed-in session; read
  the overlay's `type` (`onchart` to `offchart`) and the Objects panel's `PANE
  n` badge (`Bitcoin Dominance PANE 2` showed there for the own-pane
  indicator).
- **The settings card docks, and floats on a toggle (driven 2026-11-01).**
  `settings-panel` opened docked at the right (`union 0`, 10 `setting-term`
  rows, header `Bitcoin Dominance Template No template Style …`);
  `settings-panel-mode-btn` switched it to floating and back without closing
  it; `overlay-settings-close-btn` closed it. The ticker reads `Indicators
  n/3` with the word in front again (`Indicators 3/3` with three overlays,
  `Indicators 1/3` after their close).
- **Not every legend shows the pin and window doors (source, `672415eaff`).**
  `hasPinToChartDoor(type)` in `src/constants/indicator.constants.ts` hides the
  pin button, `Move to price pane` and the Objects pin for foreign-domain and
  on-chart types, and the nine built-in options indicators in
  `WINDOW_NATIVE_OWNER_TYPES`
  (`packages/wrun-chart-host/src/utility/chart/window-owner.leaf.ts`) now get
  the window doors and skip the pane move. Check `shouldShowPinToChartBtn`
  before asserting `pinToChartBtn`.
- **A spot pane refuses Open Interest, Funding Rate and Liquidations
  (`cdfa9c212d`; driven 2026-11-04 as far as a guest reaches).** The add gate's
  spot row (`RESTRICTED_MODES` in `src/store/chart.ts`, block list
  `SPOT_BLOCKED_INDICATORS` in `src/constants/tradfi.constants.ts`, the venue
  rule in `src/utility/exchange/derivative-venue.leaf.ts`) is meant to say why:
  `Needs open interest data, which this market doesn't have`, `Needs funding
  rate data, …` and `Needs liquidation data, …` (`handleIndexModeErrorMessage`
  writes it into the engine's `errorMessage`). The aggregated and sector
  versions stay allowed. On COINBASE BTC-USD 1h a guest's programmatic
  `addIndicator('OPEN_INTEREST'|'FUNDING_RATE'|'LIQUIDATIONS', {}, 0)` mounted
  each one gated (`isHidden` true, no pane on screen) while
  `AGGREGATED_OPEN_INTEREST` drew its own pane; 2.5 s later the engine's
  `settings.errorMessage.text` read `No data in range` (OI, liquidations) and
  `Slow network` (funding), not the `Needs …` words, and no `Needs` text was
  anywhere in the page. Whether the dialog path, which a guest cannot take,
  shows the words is live verification pending on a signed-in session; read
  the `errorMessage` from `window.tc[0].metadata` and the legend row.
- **Pane merge is open to every plan (`ee80751357`; driven 2026-11-04).**
  `FEATURE_LIMITS.paneMerge` is `{ free: true, plus: true }` and the Plus
  sheet's pane merge line is gone, so a free account no longer meets `Pane
  Merge is part of Plus`. A guest still meets the sign-in wall: with
  `AGGREGATED_OPEN_INTEREST` and `AGGREGATED_FUNDING_RATE` in their own panes,
  `metadata.find(m=>m.settings?.ovType==='AGGREGATED_FUNDING_RATE').legends.mergePaneBtn.click()`
  raised the wall with `guestLoginFeatureId` `indicators` and no Plus text.
  The target picker and the merge itself (`settings.hostPaneId` on the
  member) need a signed-in session; `docs/features/indicators/pane-merge.md`
  in the product is the contract.
- **Options indicators carry shorter names (`db24918a6e`, source).** For
  example `options flow by expiry` and `options implied move`
  (`src/constants/indicator-names.ts`, `indicator-labels.builtin.json`); the
  OPRA tier shows as filed. Re-read any name-based search or legend-text
  assertion on an options indicator.
- Some indicators are interval-sensitive: TPO sessions are daily, so at `1m` the
  profile is off-screen and the frame looks blank. Pin a sane interval first.
- **A relay feed pane (`FEED`) drives on the guest lane (live, production tree
  `aa214b9c43`, 2026-11-10).** Add it through the store, the call the feed
  picker makes:
  `$pinia._s.get('chart').addIndicator('FEED', {address:'@scope/name', scope, name, title, cadence_s, units:'', version:1, plot:'line', color:'#8b5cf6', pane:'lower', column:''}, 0, undefined, undefined, undefined, {recordUndo:false, enforceIndicatorLimit:false})`.
  A guest lane sends `chart=guest-workspace` as the grant, so a private feed
  answers `403`; wrap `window.fetch` to rewrite `chart=` on
  `relay.openmarket.xyz/api/v2/feeds` URLs to a chart that references the feed.
  The stream door answers `404` there and the session polls `head` every 10 s.
  Read the pane with
  `tc.metadata.find(m=>/FEED/.test(m.id))`: `rawData.length` is the rows
  mounted, `subsetRange` the draw window. Seen on this tree: rows mounted with
  `subsetRange` `[0,0]` and a blank pane until `tc.processData()` ran, so a
  legend value is not proof of a drawn line. Open the PNG.
