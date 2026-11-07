# Super Search, settings pages and the guest wall

Super Search is the command palette a user opens from the `Ask anything ⌘K`
capsule in the top navbar. One query searches panels, commands, themes,
formulas and more, and a row runs its action. The Settings pages dialog holds
keyboard shortcuts, language and release notes, and a guest can open all three.
Every guest-walled control raises the same sign-in dialog, and this entry is
where that shared wall is described. Created 2026-10-27; last DRIVEN on
2026-11-08 against product tree `943281a2eb` (`origin/main`, 59 commits past
`dced88e06a`), lane `18103`, a guest-JWT lane. Driven that day: `dark`
toggling `body--light` to `body--dark` and back with no wall, `heatmap`
listing the heatmap indicator rows and the `heatmapMagnifier` and
`openHeatmapPanel` commands, the footer's timezone menu (see `set-timezone`),
and a heatmap kind pill raising `orderbook-heatmap`. Before that, DRIVEN on
2026-11-07 against product tree `dced88e06a` (`origin/main`, 81 commits past
`8bcd72f8f5`), lane `18103`, a guest-JWT lane. Driven that day: `ninjatrader`
listing only `super-search-result-symbols:open-search-btn` (the new
NinjaTrader row is absent for a guest, see Gotchas), `release notes` to the
Release Notes page (82 versions, `4.53.0 Latest Spotlight The US tape.`
first; nav `settings-pages-nav-{shortcuts,language,notes}-btn` only),
`editor` to `super-search-result-panels:Editor-btn` and the drawer, and
`dark mode` to `themes:mode:dark` (`Dark Mode OFF`, then `ON`) flipping
`body--light` to `body--dark` and back. Before that, DRIVEN on
2026-11-06 against product tree `8bcd72f8f5` (`origin/main`, 119 commits past
`87a325f4ab`), lane `18103`, a guest-JWT lane. Driven that day: `anchored vwap`
listing an indicator row with its cover and a tool row tagged `Drawing tool`
(see `ss-rows`), `release notes` to the Release Notes page (82 versions,
`4.53.0 Latest Spotlight The US tape.` first) and the `4.53.0` spotlight with
its `Open AAPL on Trades` (see `set-notes`), `editor` to the drawer, and the
`watchlist` wall. Before that, DRIVEN on
2026-11-05 against product tree `87a325f4ab` (`origin/main`, 123 commits past
`8436920004`), lane `18103`, a guest-JWT lane. Driven that day: `carbon`
listing `super-search-result-themes:color:CarbonCore-btn`, whose click set
`theme-carbon`; `editor` opening the drawer (`New indicator`, `No indicators
yet`, `No script open`) with no wall; `Meta+/` (nav `shortcuts`, `language`,
`notes`) and Release Notes (`4.49.0` newest); the camera's `screenshot` wall
and its sign-in card with the Turnstile hold (see the wall bullet); and
`/chart/?twofa=true` (address cleaned, `twofa-verify-code-input` shown).
Before that, DRIVEN on
2026-11-04 against product tree `8436920004` (`origin/main`), lane `18103`, a
guest-JWT lane with the gateway resolving. Driven that day: `hide candles` and
`show candles` (`metadata[0].isHidden` true then false), `editor` opening the
drawer, `Meta+/` (nav `shortcuts`, `language`, `notes`), Release Notes (81
versions, `4.49.0` first), the rebuilt one-card sign-in wall from the
Watchlist seat (`watchlist`), its password pane, the `alert` wall, and
`?twofa=true` (`auth-return`). Before that, DRIVEN on
2026-11-03 against product tree `215896e614` (`origin/main`), lane `18103`, a
guest-JWT lane with the gateway name mapped in the browser (see the README).
Driven that day: `SPY / GLD`, which **charts the ETFs again** (`NYSE SPY /
GLD`, title `SPY / USD / GLD / USD`, 252 bars; see Gotchas), `hide candles`
and `show candles` (`candles-visible:off` then `:on`, `metadata[0].isHidden`
true then false), `volt` (`theme-kiyotaka`) and back through `terracotta`
(`theme-percept`), `gray` raising `light-mode`, `editor` listing
`super-search-result-panels:Editor-btn`, `Meta+/` to Keyboard Shortcuts
(nav `shortcuts`, `language`, `notes`), Release Notes (81 versions, `4.49.0`
first, no `4.52.0`, the list scrolling inside `.rn-sidebar__scroll`), the
walls named in the guest-wall bullet, and the new sign-in return flags
(`auth-return`). Before that, DRIVEN on 2026-11-02 against product tree
`a4488341f6` (`origin/main`), lane `18103`, a guest lane with no JWT.
Driven: the empty box (`super-search-directory`
present, no `super-search-section-toggle-*`, no starters), `liquidations`
listing the Tape row (`super-search-result-panels:Tape-btn`, the retired
panel's alias), `tape sounds` listing `super-search-result-tape:tape-toggle:sound-btn`
(`Tape sounds · Tape: play a sound on live prints`, `OFF`; listed for a
guest, not clicked), `clips` and `pepe` listing nothing, `Volt`
(`theme-kiyotaka`) and Terracotta back, `Dark Mode` both ways, `Gray`
raising `light-mode`, `SPY/GLD` charting `BINANCE.F SPYUSDT / NYSE GLD/USD`
(a third resolution, see Gotchas), `hide candles` and `show candles`
(`candles-visible:off` and `:on`, `metadata[0].isHidden`), a how-to question
(`No results found`), the `Explore` row's `workspace` wall, the camera's
`screenshot` wall, `Meta+/` (nav `shortcuts, language, notes`; no voice
text), Release Notes (81 versions, `4.49.0 Latest`, `4.0.0 Spotlight
OPENMARKET V4`), the Preferences page (13 `language-option-*`,
`appearance-mode-{dark,gray,light,cream}`, 8 `preferences-theme-*`), and
the walls from `tb-watchlist-toggle-btn` and `Alt+W` (`watchlist`),
`tb-options-btn` (`terminal`), `tb-news-toggle-btn` (`news`),
`tb-editor-toggle-btn` (`script-editor`), an official row's Add and the
legend menu's `Move to new pane` (`indicators`), a `?wrunRef=` link
(`indicators`), the heatmap switch (`orderbook-heatmap`),
`alert-add-menu-price-btn` (`alert`), the matrix cell (`multi-chart`) and the
seven walled Panels rows. Earlier, 2026-11-01 on `120d5d5d32`
(`origin/main`, lane `18103`, no JWT). Driven: the empty box (placeholder `Search the
platform`, directory sections `market, orderflow, build, automate, learn`, no
`trade`, no starters), `volt` (`theme-kiyotaka`) and back to `Percept`, whose
row is now titled **Terracotta** (`theme-percept`), the `Dark Mode` toggle
(`body--light` to `body--dark` and back), `gray` raising the `light-mode` wall,
`SPY / GLD` (it now charts Solana tokenized `SPYx/USDC` and `GLDx/USDC`, see
Gotchas), `candles-visible:off` and `:on` (`metadata[0].isHidden`), a how-to
question (still `No results found`, `surface:false`), `Meta+/` to Keyboard
Shortcuts, Release Notes (81 versions, `4.49.0` newest, `4.0.0` `OPENMARKET
V4`), the Preferences page (13 `language-option-*`, appearance modes `dark,
gray, light, cream`, 8 `preferences-theme-*`), and the wall from the camera
(`screenshot`), the matrix cell (`multi-chart`), `tb-watchlist-toggle-btn` and
`Alt+W` (`watchlist`), `tb-editor-toggle-btn` (`script-editor`),
`tb-options-btn` (`terminal`), the heatmap switch (`orderbook-heatmap`),
`alert-add-menu-price-btn` (`alert`), a `?wrunRef=` link (`indicators`) and
the seven walled Panels rows. Earlier, 2026-10-29 on `78ec9625d9`
(`origin/main`, lane `18103`, no JWT): the capsule and its empty box (directory groups
and key hints, no Ask starters for a guest), the `volt` theme row (Volt applied,
Percept restored), a how-to question (`No results found`: the dev backend's
`/ask/config` answers `surface:false`, so no Guides section), the `candles`
Ask command rows, the `editor` and `SPY / GLD` rows, `Meta+/` to Keyboard
Shortcuts with the close corner clear of the title row, Release Notes (81
versions, `4.49.0` newest, `4.0.0` now titled `OPENMARKET V4`), and the wall from
the camera, `tb-layout-entry-2H-btn`, `tb-options-btn`, the heatmap switch,
`alert-add-menu-price-btn`, `Alt+W` and the seven walled Panels rows. Earlier:
2026-10-28 on `29c9cda0a2` (`dark`, `orderbook`, `gex`, `0dte`, `options chain`,
`polymarket`, a package link). Not driven: the `Mod+J` key, the account
settings pages (they need a signed-in session), a Gray or Cream pick past its
wall, the Guides section (needs `surface:true`), the Ask plan cards and command
chips (signed-in), a Gray or Cream pick past its wall, and the per-provider
gates on the other providers. Also driven 2026-11-01: the new `Explore` row
(`super-search-result-featureCommands:layout-templates-btn`, the rebuilt
Layouts window's template catalogue, `5db5e38f15`) raises the wall with
`guestLoginFeatureId = "workspace"` for a guest.

## Sub-features

- `ss-open` the capsule opens Super Search with no guest gate.
- `ss-rows` an indicator row leads with its store cover, a drawing-tool row
  says `Drawing tool`, and the foot names what Enter does (`Add`, `Draw`,
  `Open`).
- `ss-theme` a `dark` or `light` query toggles the theme, and a theme name
  (`volt`, `percept`, ...) applies that colour theme.
- `ss-formula` a ratio query such as `SPY / GLD` plots a formula chart.
- `set-shortcuts` `Meta+/` opens Settings on the Keyboard Shortcuts page.
- `set-notes` the Release Notes page lists versions, and a release's
  Spotlight badge replays its spotlight.
- `ss-ask-commands` a query lists app commands as palette rows (hide candles,
  swap candle colours, and the rest) and a click runs them.
- `guest-wall` a walled control raises the sign-in dialog and names its feature.
- `auth-return` a sign-in return flag in the address (`?oauth=true`,
  `?twofa=true`) is spent from the address on arrival; `?twofa=true` opens the
  authenticator-code step.
- `ss-guides` a help question lists the best user-guide sections under `Guides`
  (live verification pending: it needs the backend's `/ask/config` to answer
  `surface:true`).
- `set-timezone` the footer's timezone menu sets the zone every chart time
  reads, each zone labelled with its UTC offset at the current instant.

The editor row is covered in [script editor](./script-editor-and-kscript.md)
`ks-open`.

## How to get to it (user POV)

- Click `Ask anything ⌘K` in the top navbar, then type.
- Press `⌘/` (`Meta+/`) for Keyboard Shortcuts; the same dialog's left nav has
  Preferences (the old Language page) and Release Notes.
- Click any walled control as a guest (the camera, a multi-chart layout, the
  watchlist seat) to meet the sign-in dialog.

## Driving it with control-kiyotaka

Preconditions: baseline from [chart boot](./chart-boot-and-data-plane.md), with
the top overlay cleared. Read the wall's state with:

```bash
DS="document.querySelector('#tc-container-0').__vueParentComponent.setupState"
./control-kiyotaka browser eval "JSON.stringify({auth:$DS.dialogStore.isAuthenticationDialogOpen,f:$DS.dialogStore.guestLoginFeatureId})"
```

- **`ss-open`.** `find testid global-nav-search-btn click`, then poll for
  `[data-testid=super-search-overlay]` before typing. The input is
  `super-search-input`. The overlay also carries
  `super-search-bubble-{indicators,tools,settings,shortcuts}-btn`. Result rows
  are sections with buttons `super-search-result-<id>-btn`, under
  `super-search-section-toggle-<category>-btn` headers keyed by the row
  CATEGORY, not the provider (`SuperSearchDialog.vue`; driven 2026-11-01:
  `orderbook` listed `-orderbook-`, `-panel-` and `-indicator-` toggles).
  **The empty box, driven 2026-10-29.** A guest's placeholder reads `Search the
  platform`, and the empty box shows the directory groups
  `super-search-directory-{market,orderflow,build,automate,learn}` under
  `super-search-directory`, plus the foot line `super-search-key-hints` and
  `super-search-key-hints-enter`. The Ask starters (`super-search-starters`,
  `super-search-starter-{rsi,funding,alerts}-btn`), `super-search-ask-examples`
  and `super-search-other-results` are absent for a guest: they need the Ask
  lane, which needs a signed-in session (`askLaneOn` in
  `src/composables/superSearch/useSuperSearch.ts`).
- **`ss-theme`.** Fill `dark`. The `THEMES` section shows `Dark Mode` with an
  `on-off-toggle-btn`. Click it and read
  `document.body.className.match(/body--(light|dark)/)[0]`: driven, it went
  `body--light` to `body--dark` with no wall. Toggle it back afterwards.
- **Colour themes, driven 2026-10-29 and 2026-11-01.** Fill `volt`: the `THEMES`
  section lists `super-search-result-themes:color:Kiyotaka-btn` titled `Volt`
  (theme id `Kiyotaka`, English name Volt). Its click set the body class from
  `theme-percept` to `theme-kiyotaka` with no wall. In light mode the frame
  barely changes, so the class is the proof. Restore with `percept` or
  `terracotta`: the row `super-search-result-themes:color:Percept-btn` is now
  titled **Terracotta** (`en.json` renamed the display name; the id and the
  `theme-percept` class did not change, and the alias still matches `percept`).
  The other colour ids are Seoul, Shanghai, Classic, Sourgum, Carbon and Quartz
  (Carbon's row is `themes:color:CarbonCore`; since `2a87dabdda` its volume
  bars are translucent greys and the candles show through them, driven
  2026-11-05),
  plus `themes:shuffle`. **Modes, driven 2026-11-01:** `dark` lists one row,
  `themes:mode:dark` titled `Dark Mode OFF`; its click flipped `body--light` to
  `body--dark` and a second click back. There is no `themes:mode:light` row.
  `gray` lists `themes:mode:gray`, whose click raised the wall with
  `guestLoginFeatureId = "light-mode"`; Cream is the same door. Both are
  offered on every desktop (`canPickAppearanceModes()` is `!isMobileDevice()`),
  not only in the desktop shell.
- **`ss-guides`, attempted 2026-10-29: pending.** Fill
  `how does the footprint work`. On the operator's dev backend a guest got `No
  results found` and no `super-search-guides-section`, because
  `GET /api/v1/ask/config` answered `{"enabled":false,"surface":false,...}`.
  With `surface:true` the code-only Guides section should list up to three
  `super-search-result-guides:<kbId>-btn` rows (source:
  `useSuperSearch.ts`, the Guides block). Read the config first with
  `eval "fetch('/api/v1/ask/config').then(r=>r.text())"`. The Apply card and the
  command chips (`e21fa5b62c`) need the Ask lane, so a signed-in session.
- **`ss-ask-commands`, re-driven 2026-10-29 with the same result.** Fill `candles`. The `command`
  section lists `super-search-result-askCommands:ask-command:candles-visible:off-btn`
  and its `:on` twin. A click closed the overlay and set
  `tc[0].metadata[0].isHidden` to `true` with no wall, and the frame shows only
  VWAP and volume; the `:on` row restored it. The rows come from
  `src/composables/superSearch/providers/askCommands.ts` over the catalog in
  `src/ask/commands/rows/`: only rows marked `palette: true` that take no
  argument or a toggle are listed, and a row whose `available()` refuses (a
  guest, a phone, one chart) is left out per build. `alert lines` listed nothing
  for a guest. `zoom` listed only the older `commands:zoomIn` / `zoomOut` and
  hover-lens rows: zoom-reset and go-to-date are Ask-only verbs, not palette
  rows. The Ask plan cards (`super-search-ask-plan-card`) are absent for a guest.
- **Options-panel words find nothing for a guest — driven 2026-10-28.** Since
  `29c9cda0a2` the Options panel row carries extra names (`options chain`,
  `0dte`, `options profile`, `options panel`, `the options` and variants). For a
  guest `0dte` and `options chain` returned no rows at all, because the panels
  provider lists only panels `canOpen` allows
  (`src/composables/superSearch/providers/panels.ts:172`) and the Options panel
  is signed-in. `orderbook` still lists `panels:OrderbookPanel`, and `gex` lists
  the `OPTIONS_GEX`, `OPTIONS_HEATMAP` and `OPTIONS_GEX_CURVE` indicator rows.
- **No Polymarket row for a guest — driven 2026-10-28.** `polymarket` returned
  only `symbols:open-search`. The `Link Polymarket` command
  (`providers/polymarket.ts`) is listed only when the `polymarket-execution`
  flag is on and the session is signed in.
- **`ss-formula`.** Fill `SPY / GLD`. The `FORMULA` section offers
  `super-search-result-formula:SPY/GLD-btn` (`Plot SPY ÷ GLD`). Driven, a click
  switched the chart to `NYSE SPY / GLD` with title `SPY / USD / GLD / USD` and
  252 bars, with no wall. Restore the symbol afterwards.
- **`set-shortcuts`.** Blur any focused editor first
  (`eval "document.activeElement.blur()"`), then `press Meta+Slash`. Proof:
  `settings-pages-body` and `keyboard-shortcuts-search-input`. A guest's nav is
  `settings-pages-nav-{shortcuts,language,notes}-btn`. Close with
  `settings-pages-close-btn`.
- **`ss-rows` (driven 2026-11-06 on `8bcd72f8f5`, `6c0164fd35`).** Typing
  `anchored vwap` listed `super-search-result-wrun-registry:wrun-registry:@om-core/anchored-vwap-btn`
  leading with its store cover (`.isp img`), then
  `super-search-result-tools:AnchoredVwap:Tool-btn` with a bare tool glyph
  (`.ss-row-tool-glyph`) and the kind line `.ss-row-kind` reading `Drawing
  tool`, then the `as window` row and `super-search-result-indicators:VWAP-btn`
  (`.isp` with no image: a built-in with no cover gets the store's Official
  picture box). Indicator rows no longer show a category pill in the Top band.
  The foot's Enter hint follows the active row: `Draw` on the tool row and
  `Add` after one `ArrowDown` (read the `kbd` parents; the hint has no
  testid). Only real drawing instruments carry `Drawing tool`; magnet,
  switch and Remove rows do not.
- **`set-notes`.** `find testid settings-pages-nav-notes-btn click`. Proof: the
  `release-notes-version-<ver>-btn` rows (81 on 2026-10-28, `4.49.0` newest).
  **Driven 2026-11-06 on `8bcd72f8f5`:** the Super Search row
  `super-search-result-settings:tab:notes-btn` (query `release notes`) opened
  the page with 82 rows, `4.53.0 Latest Spotlight The US tape. November 5,
  2026` first: its audience is `stocks`, and a guest reads `us-equities-full`
  ON. A version row's click only selects it. **The spotlight opens from the
  row's `Spotlight` badge**, which has no testid:
  `browser click '[data-testid="release-notes-version-4.53.0-btn"] .rn-ver__badge--spotlight'`.
  It raised the `The US tape.` spotlight (`NEW IN V4.53.0`, `Raw trade
  streams. Full order flow. Dark pools.`, `Free with a 15-minute delay,
  real-time for $19 a month`) with `release-spotlight-us-tape-open-btn`
  (`Open AAPL on Trades`) and `release-spotlight-us-tape-got-it-btn`, closed
  by `feature-spotlight-close-btn`. `Open AAPL on Trades` closed the spotlight
  and the settings page and charted POLYGON `AAPL/USD` (tab title `AAPL`). A
  guest never gets it at boot: the auto-open needs a known account creation
  date (source).
  Poll for the rows: a nav click made straight after `Meta+/` once left the page
  on Keyboard Shortcuts, and a second open and click switched it within 2 s.
  The nav ids are unchanged (`settings-pages-nav-{shortcuts,language,notes}-btn`)
  but the `language` row now reads `Preferences`.
  Re-driven 2026-10-29: 81 rows, `4.49.0` newest. The `4.0.0` row now reads
  `4.0.0 Spotlight OPENMARKET V4` (`dc9ed408ee`), and the page body carries no
  `Kiyotaka`. Source holds 88 entries on `215896e614`; `4.52.0` (`Trade
  futures.`, `audience: 'futures'`, `12f71dc90b`), `4.51.0` (`options`) and
  `4.50.0` (`wrun-launch`) are filtered by audience, so a guest's count is a
  viewer's, not the file's. Re-driven 2026-11-03: 81 rows, `4.49.0` first,
  `1.1.0` last, no `4.52.0`. The version list now scrolls inside
  `.rn-sidebar__scroll` (`overflow-y: scroll`, with an edge fade) and
  `.rn-sidebar` itself no longer scrolls (`90a639ffaa`). That day the first
  `find testid settings-pages-nav-notes-btn click` left the page on Keyboard
  Shortcuts again; an `eval` click on the same node switched it, so poll for
  `[data-testid^=release-notes-version-]` after the click and click once
  more if it reads `0`.
- **The close corner, driven 2026-10-29.** Since `4f5cc1622e` every settings
  page reserves the close button's gutter: `.settings-page-title-row` carries
  `padding-right: 30px` and `settings-pages-close-btn` sits in it. A guest's
  Keyboard Shortcuts page showed no `Reset all` button (it appears only with a
  customised shortcut), so the overlap fix itself was not seen.
- **`guest-wall`.** `find testid global-nav-screenshot-btn click` raised it with
  `guestLoginFeatureId = "screenshot"`. The form carries
  `login-signup-submit-btn`, `login-signup-use-password-btn`,
  `login-signup-passkey-btn`, `login-signup-google-btn`,
  `login-signup-twitter-btn`, `login-signup-forgot-password-btn` and
  `login-signup-tos-link`. Clear it with `press Escape`.

  Feature ids driven on 2026-10-27, by door:

  | Door | `guestLoginFeatureId` |
  |---|---|
  | `global-nav-screenshot-btn` | `screenshot` |
  | an official row's Add in the Indicators dialog | `indicators` |
  | `tb-layout-matrix-cell-1-1-btn` | `multi-chart` |
  | `tb-watchlist-toggle-btn` | `watchlist` |
  | `tb-news-toggle-btn` | `news` |
  | `tb-editor-toggle-btn` | `script-editor` |
  | `tb-options-btn` | `terminal` |
  | `tb-heatmap-toggle-btn` (turning the heatmap on) | `orderbook-heatmap` |
  | `tb-heatmap-kind-<kind>-btn` (2026-11-08) | `orderbook-heatmap` |
  | `alert-add-menu-price-btn` | `alert` |
  | `Alt+W` with the chart focused (2026-10-28) | `watchlist` |
  | `tb-panels-row-replay` (2026-10-28) | `chart-actions` |
  | `tb-panels-row-scanner` (2026-10-28) | `terminal` |
  | `tb-panels-row-footprint` (2026-10-28) | `volume-footprint` |
  | `tb-panels-row-chat` (2026-10-28) | `community-chat` |
  | a package link, `?indicator=` or `?wrunRef=` (2026-10-28) | `indicators` |
  | `tb-panels-row-watchlist`, `-news`, `-editor` (2026-10-28) | `watchlist`, `news`, `script-editor` |
  | `themes:mode:gray` or `themes:mode:cream` (2026-11-01) | `light-mode` |
  | `featureCommands:layout-templates`, the `Explore` row (2026-11-01) | `workspace` |
  | `indicator-menu-pane-move`, the legend menu's `Move to new pane` (2026-11-02) | `indicators` |

  Re-driven 2026-11-02 on `a4488341f6`, every id unchanged (the camera, the
  row Add, the matrix cell, the seat, `Alt+W`, News, Editor, Options, the
  heatmap switch, the alert price item, the seven Panels rows, Gray, Explore,
  `?wrunRef=`), plus the pane-move door above. The wall's heading is the
  feature's name (`Technical Indicators` for `indicators`) over `Sign in or
  create an account`.

  Re-driven 2026-10-28 with the same ids: the camera, an official row's Add,
  `tb-options-btn`, `tb-heatmap-toggle-btn` and `alert-add-menu-price-btn`;
  `multi-chart` from `tb-layout-entry-2H-btn` rather than the matrix cell; and
  `watchlist`, `news` and `script-editor` from their Panels rows
  (`tb-panels-row-<id>`) rather than the bar seats.
  Re-driven 2026-10-29 on `78ec9625d9`, every id unchanged: `screenshot`,
  `multi-chart` (`tb-layout-entry-2H-btn`), `terminal` (`tb-options-btn` and
  the Scanner row), `orderbook-heatmap`, `alert`, `watchlist` (`Alt+W` and its
  row), `news`, `community-chat`, `volume-footprint`, `script-editor` and
  `chart-actions`. The wall needs a moment to render: an `Escape` sent straight
  after the click can land first and leave the wall up, so read
  `isAuthenticationDialogOpen` before clearing.
  Re-driven 2026-11-01 on `120d5d5d32`, every id unchanged, plus `light-mode`
  from the Gray row and `watchlist` from `tb-watchlist-toggle-btn` itself (the
  seat is in the bar while no panel is open). The store's JSON comes back from
  `browser eval` with escaped quotes (`{\"open\":true}`), so a shell match
  on `"open":true` never fires; strip the backslashes or match `open\":true`.
  One pass lost its first seven wall drives to that.

- **`set-timezone`: the footer's timezone menu (`2cad385819`; driven
  2026-11-08 on `943281a2eb`).** `find testid footer-timezone-select click`
  opens a list of `role=option` rows (`.timezone-region`, no per-row testid),
  each a city under its offset for the current instant: after the US clocks
  went back, `Los Angeles` read `UTC-8`. Click the row by its city text. The
  pick wrote `user` store `settings.activeTimezone`
  (`{label:'UTC-8', timezone:'America/Los_Angeles'}`), the footer read
  `UTC-8` and its clock `12:06:18` against `20:06` UTC, and no wall rose for
  the guest. To restore, pick the zone the run started on: the bare `UTC`
  label's row stored `Atlantic/Reykjavik`, not the boot zone. Since `2cad385819` chart times read the
  zone's offset at each instant, so a time on the far side of a clock change
  shows its own offset (source, `src/utility/chart/display-timezone-offset.util.ts`).
  The Settings pages' Timezone page is the phone's
  (`platform: 'mobile'` in the settings provider); a desktop uses the footer.
- **Trade settings' menus are ComboBoxes (`18c8a69659`; source).** The fill
  sound and idle menus (`trade-settings-fill-sound-tone`,
  `trade-settings-idle`) are ComboBoxes: the row testid wraps a
  `combo-box-trigger-btn` with `combo-box-option-<value>` rows, not a native
  select. The page needs a
  signed-in trading context.

- **Proof.** The store read, the overlay or page testid, and a screenshot.

## Gotchas

- **NinjaTrader has a Super Search row and Connections aliases a guest never
  sees (`3dd3e5d0c3`; source, absence driven 2026-11-07).** The provider
  `ninjatrader.ts` lists one command, `Link NinjaTrader`
  (`tradingHub.unlinked.link`, subtitle `Trade ES, NQ and the other CME
  contracts from their charts…`, aliases such as `connect ninjatrader`,
  `tradovate`, `futures broker`), which opens the trading hub on its broker
  page. It is listed only when `isTradingHubDesktop()`,
  `isFuturesTradingFlagOn()` and `isNinjaTraderOn()` all hold
  (`futures-ninjatrader`, web only). `settings.ts` sends a word of three or
  more letters that starts `ninjatrader` or `tradovate` to the Connections
  page at `data-setting="futures-ninjatrader"`, and `rithmic`, `futures` or
  `broker` to `futures`, while those cards stand. A guest reads both flags
  off: `ninjatrader` lists only the symbols fallback, and the guest settings
  nav has no Connections page. The row's testid is presumably
  `super-search-result-ninjatrader:link-btn` (not seen live).
- **`guestLoginFeatureId` is not cleared when the wall closes.** It keeps the
  last id after `Escape`, so read `isAuthenticationDialogOpen` first. A stale id
  beside `auth:false` means nothing was walled.
- **The wall has no close button; `Escape` clears it.** It shares the
  `.dialog-style.dialog-overlay` shell with the signup modal, and
  `guest-signup-modal-close-btn` is absent on it.
- **The Settings dialog is a `.q-dialog`.** It stays open under a second
  `Escape` from some states, and it covers other controls. Close it with
  `settings-pages-close-btn` and re-count the overlays.
- **`Meta+/` goes to CodeMirror while the editor drawer has focus.** The first
  press on 2026-10-27 did nothing for that reason.
- **Light mode is open to guests.** An older inventory note said it raises
  `LIGHT_MODE`. Driven, dark and light toggled freely. Gray and Cream are listed
  for every desktop guest and their pick raises `light-mode` (driven
  2026-11-01), so a frame after a Gray pick is a frame of the wall.
- **`SPY / GLD` charts the ETFs again (driven 2026-11-03 on `215896e614`).**
  The row `super-search-result-formula:SPY/GLD-btn` switched the chart to
  `NYSE SPY / GLD` (title `2.07938 ▼ SPY / USD / GLD / USD`, 252 bars), as on
  2026-10-29. The switch took about 15 s behind a `Connecting` chip, so poll
  the title rather than reading it at once. Which commit in
  `a4488341f6..215896e614` restored it was not traced; the formula legs are
  picked in `pairTypedFormulaAssets` and `nativeFormulaVenues`
  (`src/utility/symbol-selection/typed-formula.util.ts`). The gap recorded
  below is closed on this tree.
- **History: `SPY / GLD` left the ETFs on two trees (driven 2026-11-01 on
  `120d5d5d32`, again 2026-11-02 on `a4488341f6`).** On 2026-11-02 the
  formula row `formula:SPY/GLD` (`Plot SPY ÷ GLD · Formula · Ratio`) charted
  `BINANCE.F · NYSE SPYUSDT / GLD/USD` with the title `SPYUSDT / GLD / USD`
  (464 bars): `GLD` is back on NYSE, but `SPY` resolves to a BINANCE.F
  `SPYUSDT` perp. On 2026-11-01 it resolved to Solana tokenized stocks
  (`SOLANA SPYx/USDC:4pCZ…` over `GLDx/USDC`, 440 bars), and on 2026-10-29 to
  `SPY / USD / GLD / USD` (252 bars). `9ffb5345bf` and `eb1f3b83be` (tokenized
  pools kept out of a plain search) moved it off Solana; `528a31b434` (search
  ranking) was the suspect for `SPY` leaving the ETF. It was a product gap,
  closed by 2026-11-03; `footer-undo-btn` (`Undo Change symbol`) puts the
  previous chart back. The 2026-11-01 frame also showed `Connection lost.
  Reconnecting…` from that chart on, which turned out to be the gateway outage
  below, not the formula.
- **`auth-return`: the sign-in return flags are spent on arrival (source,
  `0a0d1b8313`, `dd6c6f4161`; driven 2026-11-03).** The Chart route runs
  `signInReturnGuard` (`src/router/guards/sign-in-return.guard.ts`) before
  `chartBeforeEnter`, which no longer reads them. Open
  `/chart/?oauth=true`: 3 s later `location.search` was `''`, the page had
  one navigation entry (no reload loop) and the chart drew 488 bars. Open
  `/chart/?twofa=true` as a guest: the address was clean and
  `dialogStore.isOAuthTwoFADialogOpen` read `true`, with the dialog `Verify
  Code / Enter the 6-digit verification code from your authenticator app` on
  top. Press `Escape` to clear it. Completing either flow needs a real
  sign-in. Re-driven 2026-11-04 on `8436920004`: the same clean address and
  one navigation entry, and the dialog is now a shell around the card's 2FA
  panel, one code field instead of six boxes: `twofa-verify-close-btn`,
  `twofa-verify-code-input`, `twofa-verify-back-btn`,
  `twofa-verify-submit-btn` (`Verify & Continue`) and
  `twofa-verify-recovery-link-btn` (`Use a recovery code instead`).
- **The wall is one sign-in card, a sheet (`4b8f78a775`, driven
  2026-11-04).** Its visible title is still the feature's name (the
  Watchlist seat's wall is headed `Watchlist`, the camera's `Share Your
  Chart`, Replay's `Chart Actions`), then `Sign in or create an account / One
  email. We send you a code, no password.`, `Email me a code`, `Sign in with a
  password instead`, and an `Or continue with` row of pills: `Passkey`,
  `Google`, `X`. The overlay is `.dialog-style.dialog-overlay` with
  `dialog-style--sheet backdrop-dim login-signup-overlay`; the page behind it
  no longer scales or blurs (`d9636e8a6b`). A testid listing now starts with
  `login-signup-welcome-spoken` and `auth-mascot`, then
  `login-signup-field-message`, `-submit-btn`, `-use-password-btn`,
  `-passkey-btn`, `-google-btn`, `-twitter-btn` and `-tos-link`; the hidden
  `Back to log in / Forgot your password?` pane that used to sit first is gone.
  `login-signup-use-password-btn` swaps in the password pane (`Email`,
  `Password`, `Forgot Password`, `Log In`) with `-forgot-password-btn` and
  `-use-code-btn`. `Escape` clears it (`isAuthenticationDialogOpen` false), but
  the card leaves through an animation: while the tab is hidden the overlay
  stays in the DOM as `dialog-style--leaving` (pointer events off), and the
  overlay union reads `1` until the tab is visible again.
  **`Email me a code` waits for Cloudflare's checkbox (`37afa417b0`, driven
  2026-11-05 for clean traffic).** The card now lists
  `login-signup-turnstile` after `auth-mascot`, and a hidden
  `cf-turnstile-response` input. With an empty email the submit is disabled;
  after filling an email on the lane the token was present (21 characters), no
  checkbox drew (`login-signup-turnstile` 0 px high, no `is-challenging`) and
  `Email me a code` was enabled. When Cloudflare does show its checkbox the
  button stays disabled and the field message reads `Complete the security
  check above to continue.` until it is ticked (source; the code panel's
  `login-signup-code-turnstile` says `Complete the check above to continue.`),
  and a submit waits up to 5 s for the token. Never submit: that sends a real
  code. The sign-in form also fades out before the card shrinks to the welcome
  (`2ab15d9784`, source).
- **A gateway outage reads as `Reconnecting…` in `connection-status-chip`
  (seen 2026-11-01; on desktop since `b2623958e8` the yellow
  `connection-strip` says it instead, `Still reconnecting` with a Reload
  button after 30 s, driven 2026-11-05; see
  [chart boot](./chart-boot-and-data-plane.md)).** From about 21:55 UTC the tailnet-only name
  `tsdb-gateway.int.ore.kiyotaka.ai` stopped resolving on the mini (public DNS
  answers NXDOMAIN; only `100.100.100.100` knows it), the console filled with
  `v2 Streaming socket error` and `v2 Orderbook socket error`, OI and funding
  read `—`, Tape and Orderbook stayed empty, and `doctor`'s `v2 gateway` line
  flipped to `UNREACHABLE`. A reload still drew 440 candles from the OHLCV
  cache (`main-cache-painted-marked` in the ring). Read `doctor` and the chip
  before calling an empty live panel a regression.
- **Super Search mounts lazily.** `isSuperSearchOpen` goes true before the
  overlay is in the DOM, so poll for `super-search-overlay`.
- **Provider changes in `120d5d5d32..a4488341f6` (source, read on
  `a4488341f6`; the guest-visible ones driven 2026-11-02).** `panels.ts`
  gives the Tape row the aliases `liquidations`, `trades and liquidations`,
  `trade & liquidations` and the former name (`superSearch.panels.tapeFormerName`,
  `Trade & Liquidations`), and `TradeAndLiquidations` left `WIDGET_PANELS`
  (driven: `liquidations` lists `panels:Tape`). `tape.ts` adds the toggle row
  `tape-toggle:sound` (`Tape sounds`, `ba8e2cc280`; driven, listed `OFF`).
  `memecoins.ts` answers only a pasted Solana mint (`pastedSolanaAddress`;
  `9ffb5345bf`, `eb1f3b83be`, `89adcfc7d5`), so a word such as `pepe` lists
  no memecoin row (driven), and `symbols.ts` keeps `isBlkExchange` tokenized
  pools out of the exact-ticker row. `academy.ts` adds `academy:open-clips`
  (`clips`, `reels`, `videos`) behind `isChartClipsOn()` (`om-board` and
  `chart-clips`), so a guest sees no clips row (driven: `clips` lists
  nothing). `settings.ts` adds `trade:futures-order-confirm`, and since
  `215896e614` also `trade:futures-change-confirm`,
  `trade:futures-cancel-confirm` and `trade:futures-position-confirm`, all
  behind the futures flag on desktop (absent for a guest).
  `featureCommands.ts` dropped its `trade-history` and `open-trades` rows for
  a `show-on-chart` row and `show-on-chart:<family>` toggles, listed only while
  the trader's own account draws on a pane (`useOwnChartPanes().listed`), so
  a guest gets none (source). `tools.ts` makes the `magnet`
  toggle restore its last strength and adds `drawing-constrain` (`Align 45°`)
  on phones only. `indicators.ts` gains `chartLifts` for Big Trades on a stock
  Live price chart. Ask's do lane is now picked by Jev from the feature
  registry (`src/ask/pick/*`; `src/ask/decide/route.ts` and `parts.ts` are
  deleted, `8826196f40`) and `runUndo` undoes every record of a run; nothing a
  guest sees changed (`askLaneOn` still needs a signed-in session).
  `src/store/feature-flags.ts` only memoises its map (`flagsSnapshot`);
  `GUEST_DEFAULT_FLAGS` was `{}` then; since `726acfee48` and `b5d0fe6b0f`
  it is `{gateway-v3: false}` (a guest never rides the v3 wire).
- **The appearance modes carry testids (driven 2026-11-02).** The Preferences
  page's modes are `appearance-mode-{dark,gray,light,cream}` beside the 13
  `language-option-*` rows and the 8 `preferences-theme-*` tiles. The Release
  Notes nav is `settings-pages-nav-notes-btn` (a `-release-notes-` guess
  finds nothing).
