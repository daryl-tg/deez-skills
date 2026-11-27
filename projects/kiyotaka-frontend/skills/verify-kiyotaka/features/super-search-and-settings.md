# Super Search, settings pages and the guest wall

Super Search is the command palette a user opens from the `Ask anything ⌘K`
capsule in the top navbar. One query searches panels, commands, themes,
formulas and more, and a row runs its action. The Settings pages dialog holds
keyboard shortcuts, performance, language and release notes, and a guest can
open all four.
Every guest-walled control raises the same sign-in dialog, and this entry is
where that shared wall is described. Created 2026-10-27; last DRIVEN on
2026-11-28 against product tree `511ce25e50` (`origin/main`, 125 commits
past `a79bf68710`), lane `18110`, a no-session lane: Chart settings is now
a list of pages (`set-pages`), Super Search's `Price line width` row opened
Scales & Spacing on that row, the settings search found `tooltips` but
showed the row blank (see Gotchas), and Shift+T opened My layouts with no
wall (`set-layouts`). Not driven: the Trading page (an account that draws
on a chart), the Events rows (`market-events` flag), `Save as theme` past
its wall. Before that, last DRIVEN on
2026-11-27 against product tree `a79bf68710` (`origin/main`, 78 commits past
`1d1a3e1410`), lane `18109`, a no-session lane: `dark` listed
`super-search-result-themes:mode:dark-btn` (`Dark Mode OFF`) on a
`body--light` page; `release notes` and `Enter` opened Release Notes with
86 rows led by `4.61.0 Latest`, `4.59.0`, `4.53.0 Spotlight`, `4.50.0`
(the guest JWT counted 84 the night before and named no `4.50.0`; the
releases table has no diff, so the extra rows follow the viewer's audience,
not traced); `editor` opened the Script Editor drawer with no wall; every
wall read as the email card (`Verify your email to unlock <feature>`,
empty address). Before that, last DRIVEN on
2026-11-26 against product tree `1d1a3e1410` (`origin/main`, 76 commits
past `ec531568de`), lane `18108`, a guest JWT: Super Search's `release
notes` row opened Release Notes with 84 versions led by `4.61.0 Latest`
(see `set-notes`), and the guest's `/chart/plans` showed the new `Strategy
backtest` row and the Plus card's backtest line, with no `Custom
intervals` line (see `plans-page`); `voice` listed no voice row. Not
driven: the checkout buttons' busy look (signed-in). Before that, last
DRIVEN on 2026-11-25 against product tree `ec531568de` (`origin/main`, 142 commits
past `8cd7ad448e`), lane `18107`, a guest JWT: Super Search's `release
notes` row opened Release Notes with 83 versions led by `4.59.0 Latest`
(see `set-notes`), and the guest's `/chart/plans` drew no Black Friday sale
(see `plans-page`). Not driven: the palette's typed store search for
indicators (`wrunRegistry`, from two characters) and every signed-in row.
Before that, last DRIVEN on
2026-11-24 against product tree `8cd7ad448e` (`origin/main`, 269 commits
past `92f4a841ef`), lane `18106`, a guest JWT with the backend answering:
the plans page's live-data section with its new US options card, its place
above `Compare features` and the US stocks billing switch, and a guest's
US-options `Add` raising `Purchases` (see `plans-page`); the new
`OPRA real-time options data` row for a guest (see `ss-opra-data`); no
`Draw a trade` and no voice row; an OSI code listing no contract row (see
`ss-long-code`); Release Notes, still 82 versions (see `set-notes`); and
the walls `watchlist`, `script-editor`, `news`, `multi-chart`, `billing`
and the TPO chart type's `Time Price Opportunity`. Not driven: the cart
with a plan in it and the live-data ask after Get Plus (signed-in), and the
sign-up marketing box (needs a fresh email and a code). Before that, last
DRIVEN on 2026-11-21 against product tree `92f4a841ef` (`origin/main`, 103 commits past `7c937b0a1f`),
lane `18104`, a guest JWT with the backend answering: digits
typing an interval into the palette (see `ss-typed-interval`); the rows
`plans` (`See OpenMarket plans`, which opens `/chart/plans` in a new tab),
`trade panel` with its `⌥ ⇧ T` chord, and no row for `ctrader`, `black
friday`, `one click` or `ninjatrader` (see `ss-rows`); the plans page at
its new address with `/chart/plus` redirecting to it (see `plans-page`,
rewritten); the footer timezone menu with its `Exchange` row and search
(see `set-timezone`, rewritten); Release Notes with 82 versions led by
`4.53.0` (see `set-notes`); a first settings nav click that took, five
times in five (see Gotchas); and the guest walls `watchlist`, `news`,
`script-editor`, `multi-chart`, `alert`, `chart-actions`, `billing` and
`default`. Not driven: the Black Friday surfaces, a Max holder's look,
the moved-member card and the plan limit messages (signed-in). Before
that, last DRIVEN on
2026-11-20 against product tree `7c937b0a1f` (`origin/main`, 82 commits past
`413f86e5af`, lane `18104`, a no-session lane with the backend unreachable):
Super Search whole on its first frame, `channel` leading with the Parallel
Line tool, `one click trading` listing nothing, `auto scale` listing
`axis:auto-scale` (see `ss-rows`); the settings pages with all ten nav items
and a first nav click that did not take (see Gotchas); Release Notes with 84
versions led by `4.53.0` and no `4.57.0` row (see `set-notes`); the Lite
charts chip, card and Performance switch (see `set-lite`); the plans page
with no member-only content (see `plans-page`); and the Watchlist and editor
walls as verify-email cards. Not driven: any guest wall, the moved-member
notice and `Add a year`, and share links. Before that, last DRIVEN on
2026-11-19 against product tree `413f86e5af` (`origin/main`, 184 commits past
`cff04f9a01`, lane `18103`, a guest JWT with the backend answering):
`global-nav-search-btn` and `release notes` to
`super-search-result-settings:tab:notes-btn`, whose page led with `4.53.0`
(82 versions) and, under the `pane-sides` dev override, with `4.56.0` (83;
see `set-notes`), and `/chart/plus`'s broker answer in its plain wording (see
`plans-page`). Before that, last DRIVEN on
2026-11-18 against product tree `cff04f9a01` (`origin/main`, 79 commits past `60b7e6b190`, lane `18103`,
a guest JWT on the internal gateway): `dark mode` to
`super-search-result-themes:mode:dark-btn` (`Dark Mode OFF`) and back,
`options chain` (no rows), `polymarket` and `variational` (only
`symbols:open-search-btn`), the Watchlist (`watchlist`), editor
(`script-editor`) and heatmap (`orderbook-heatmap`) walls, and `/chart/plus`
(see `plans-page`). Before that, last DRIVEN on
2026-11-17 against product tree `60b7e6b190` (`origin/main`, 60 commits past `6bfc742bc8`, lane `18103`, a no-session lane on the internal gateway: the backend was unreachable, so there was no guest token; see the README's Baseline preconditions): Super Search's
`theme` fill (four theme rows and a `THEMES 12` group) and, with no
session, the wall's other face: every `handleGuestAccess` door (Indicators
Add, Watchlist, Indicator Editor) raised `Verify your email to unlock
<feature>` with an empty address, because the account was neither a guest
nor verified (see Gotchas). Before that, last DRIVEN on
2026-11-16 against product tree `6bfc742bc8` (`origin/main`, 187 commits past
`c7d4eccfac`), lane `18103`, a guest-JWT lane on the internal gateway: a long
market code in the palette (see `ss-long-code`), the Highlights and Clean
look rows (see `set-highlights`), and the plans page at `/chart/plus` (see
`plans-page`). Before that, last DRIVEN on
2026-11-14 against product tree `c7d4eccfac` (`origin/main`, 62 commits past
`963af59de1`), lane `18103`, a guest-JWT lane with the v2 gateway pointed at the public `wss://api.chart.ore.openmarket.xyz/v2/` (see the README's Baseline preconditions): the price line style rows (see `set-price-line`), the
Tooltips row and switch (see `set-tooltips`), a typed `EURUSD` in the palette
(see `ss-forex`), the absent trade rows, the password pane's refusal line (see
`guest-refusal`) and Release Notes for a guest. Before that, last DRIVEN on
2026-11-13 against product tree `963af59de1` (`origin/main`, 87 commits past
`74ccd3cdcc`), lane `18103`, a guest-JWT lane: the `Settings` row and its
dialog (see `ss-settings`), `performance`, the formula gate (see
`ss-formula`), Release Notes still leading with `4.53.0` for a guest (see
`set-notes`), `editor`, a `Fixed Range Volume Profile` tool row, and the
`watchlist`, `script-editor` and `indicators` walls. Before that, last DRIVEN on
2026-11-12 against product tree `74ccd3cdcc` (`origin/main`, 113 commits past
`c2c02b7b42`), lane `18103`, a guest-JWT lane: the first-row cursor, joined
words, the Tape section row, `Go to date` and the typed interval (see
`ss-cursor` and `ss-typed-interval`), plus the `watchlist`, `script-editor`,
`indicators` and multi-chart walls. Before that, last DRIVEN on
2026-11-10 against product tree `c2c02b7b42` (`origin/main`, 60 commits past
`32dd0c6354`), lane `18103`, a guest-JWT lane. Driven that day: the palette's
one row per action (`chat`, `hide all drawings`, `magnet`, `keyboard
shortcuts`, `candle`, `spline`, see `ss-one-row`), `dark` flipping
`body--light` to `body--dark` and back, `expand` running full chart with no
pointer, `editor` to `panels:Editor`, `Meta+/` to the four-page nav, and the
Lite charts notice on a cold boot reading its words (the raw-key gap is
closed, see Gotchas). Before that, last DRIVEN on
2026-11-09 against product tree `32dd0c6354` (`origin/main`, 60 commits past
`943281a2eb`), lane `18103`, a guest-JWT lane. Driven that day: `dark` flipping
`body--light` to `body--dark` and back, `heatmap` listing the indicator rows and
the two commands, `editor` to `panels:Editor`, the empty palette's
`super-search-keycap` (`⌘ K`), the clear control's new name `Clear`, the
Performance page and Lite charts (see `set-lite`), the `4.53.0` Release Notes
row first, and the timezone list (`UTC-8 Los Angeles`). Before that, last
DRIVEN on 2026-11-08 against product tree `943281a2eb` (`origin/main`, 59 commits past
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
- `ss-settings` a `settings` query lists one `Settings` row that opens the
  Settings dialog, and a launch word (`open`, `go to`, `show`) before a name
  finds the same rows.
- `set-shortcuts` `Meta+/` opens Settings on the Keyboard Shortcuts page.
- `set-lite` the Performance page's Lite charts switch, its chip, and the
  notice a slow device gets when the preset turns itself on.
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
  reads: a pinned `Exchange` row shows each chart on its market's own
  clock, then one row per city with its UTC offset at the current
  instant, and a search box narrows the list (`2c00cd33c6`, `c75024f3ca`).
- `ss-cursor` until the pointer or an arrow moves, the highlighted row is the
  first row after every keystroke, and words typed apart find one name.
- `ss-typed-interval` the comma key, a number-row digit or a Numpad digit
  opens the palette to type an interval (`30e7cf86f1`).
- `set-pages` Chart settings opens on a list of pages, Appearance, Scales &
  Spacing, Trading Hours and On Screen (plus Trading for an account that
  draws on a chart), then `On this chart` Indicators; each row opens its
  page with a back arrow, and a search field finds a setting on any page.
  The nine tabs are gone (`1607afdb85`).
- `set-layouts` My layouts (Shift+T) lists the layouts by group with Select
  and the sort in the list head; an empty search offers `Clear search`
  (`6f7a1e7619`).
- `set-price-line` the Scales & Spacing page (its Price axis group's
  Advanced fold) sets the last price line's width and its bullish and
  bearish colours, and the palette finds each row.
- `set-tooltips` one switch hides or shows the app's tooltips, on the On
  Screen page (the `Every chart` group's Advanced fold) and as a palette
  row.
- `ss-forex` a forex pair typed in the palette (`EURUSD`, `XAU/USD`) lists the
  pair and charts it.
- `guest-refusal` a refused sign-in says so in the app's words, never the
  server's.
- `ss-long-code` a market code longer than 12 characters (an OSI option code,
  `1000000MOGUSDT`, `FRED:CPIAUCSL`) still offers `Open symbol search`, and
  an OSI code lists its contract where `opra` is on (a guest included since
  `6b3e077975`).
- `ss-opra-data` an `options` or `opra` query lists `OPRA real-time options
  data` wherever `opra` is on, a guest included; it opens the US options
  purchase, which a guest meets as the `Purchases` wall.
- `set-highlights` the chart's `Highlights` switch calms volume bars and bar
  indicators unless a bar stands far above its usual size; the palette row and
  the On Screen page row toggle it.
- `plans-page` `/chart/plans` (moved from `/chart/plus`, which redirects,
  `7e88ad6552`) shows the plans, the live exchange data add-ons (CME
  futures, US stocks with a monthly or yearly switch, US options) with
  their bag, then the compare list and the questions to a guest; the top plan is
  named Max in customer copy (`0ebf5de381`). A member moved from annual Plus to Ultimate also
  gets a `4.57.0` notice at boot and an `Add a year` control here
  (`ebbd08ef1d`; signed-in members only, source).

The editor row is covered in [script editor](./script-editor-and-kscript.md)
`ks-open`.

## How to get to it (user POV)

- Click `Ask anything ⌘K` in the top navbar, then type.
- Press `⌘/` (`Meta+/`) for Keyboard Shortcuts; the same dialog's left nav has
  Preferences (the old Language page) and Release Notes.
- Click any walled control as a guest (the camera, a multi-chart layout, the
  watchlist seat) to meet the sign-in dialog.
- Right-click the chart and pick `Chart settings…` for the list of pages;
  the magnifier in its head searches every page.
- Press Shift+T for My layouts.

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
  rows (still so on 2026-11-10: `zoomIn` and `zoomOut` have no second door).
  The Ask plan cards (`super-search-ask-plan-card`) are absent for a guest.
- **`ss-one-row`: one row per action (`e1ce349c4a`; driven 2026-11-10 on
  `c2c02b7b42`).** A keyboard command that has a palette row of its own
  (`src/constants/keymapSecondDoors.constants.ts`) folds into that row, which
  keeps the key caps; the `commands:` row is dropped when both would list.
  The pairs: `showKS` into `settings:tab:shortcuts`, `advancedSettings` into
  `settings:chart-settings`, `hideToolSidebar` into
  `settings:global:tool-sidebar`, `toggleMagnetMode` into `tools:magnet`,
  `toggleChat` into `panels:Chat`, `toggleWatchlistPanel` into
  `panels:WatchlistPane`, `toggleObjectsPanel` into `panels:Objects`,
  `toggleJournalPanel` into `panels:Journal`, `openHyperliquidView` and
  `openCallsPanel` into their `featureCommands:` rows, `hideAllDrawings` into
  `objects:objects-hide-all-drawings`, `spline` and `candle` into
  `chartStyle:`, and every tool key into its `tools:<tool>` row. Driven:
  `hide all drawings` listed one row, under `SHORTCUTS`, with `⌘ ⌥ H` caps;
  `chat` listed only `panels:Chat`; `magnet` listed `tools:magnet` and no
  `commands:toggleMagnetMode`; `keyboard shortcuts` listed
  `settings:tab:shortcuts` with `⌘ /`; `candle` and `spline` listed their
  `chartStyle:` rows (`spline` is titled `Chart Style: Line`). The Top band
  repeats rows that also list in their section, so count unique testids. A
  Top band row can carry a `.ss-row-badge` naming its section (`TOOLS`,
  `SETTINGS`, `CHART STYLE`, `SYMBOLS` were read). `Chat` and `Hide all
  drawings` now toggle from the palette (source); `market events` listed
  nothing for a guest. `expand` lists `commands:expandChart` (`⌥ Enter`),
  which since the same commit runs with no pointer on the chart: its click
  set the chart store's `activeExpandChartIndex` from `null` to `0` (driven;
  see the ticker bar guide's `tb-full-chart`).
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
  (`providers/polymarket.ts`) is listed only for a signed-in session (the
  `polymarket-execution` flag graduated in `b1f10f1e3b`). Re-driven
  2026-11-18: `polymarket` and `variational` listed only
  `symbols:open-search-btn`; Variational is a signed-in venue like Bitget.
- **`ss-formula`.** Fill `SPY / GLD`. The `FORMULA` section offers
  `super-search-result-formula:SPY/GLD-btn` (`Plot SPY ÷ GLD`). Driven, a click
  switched the chart to `NYSE SPY / GLD` with title `SPY / USD / GLD / USD` and
  252 bars, with no wall. Restore the symbol afterwards. **Since `e023fe8c84`
  and `f3f2993a12` (driven 2026-11-13 on `963af59de1`) a hyphen with no
  spaces is a formula only between two known tickers**: `BTC-ETH` listed
  `super-search-result-formula:BTC-ETH-btn` (`Plot BTC − ETH`, `Formula ·
  Spread`), while `bid-ask` and `order-book` listed no formula row (`bid-ask`
  led with `axis:bid-ask-line` and `axis:bid-ask-label`). `SPY / GLD` still
  lists `Plot SPY ÷ GLD` (`Formula · Ratio`). The terms are checked against
  the local market list, so on a fresh device with no list loaded yet the
  syntax alone decides (source).
- **`ss-settings` (driven 2026-11-13 on `963af59de1`; `f3f2993a12`).** Fill
  `settings`: `super-search-result-settings:dialog-btn` (`Settings`) led,
  then `settings:tab:my-info`, `settings:chart-settings:display` and the
  other tabs. Its click opened `settings-pages-body` with a guest's nav
  `shortcuts`, `performance`, `language` and `notes`, and no wall. `open
  settings` listed it second (behind `Toolbar after drawing`): the launch
  word is stripped and ranks no higher than a synonym. `performance` listed
  `super-search-result-settings:tab:performance-btn` first, then
  `settings:global:high-performance` (`Performance Mode`). Close with
  `settings-pages-close-btn`.
- **`set-shortcuts`.** Blur any focused editor first
  (`eval "document.activeElement.blur()"`), then `press Meta+Slash`. Proof:
  `settings-pages-body` and `keyboard-shortcuts-search-input`. A guest's nav is
  `settings-pages-nav-{shortcuts,performance,language,notes}-btn` (driven
  2026-11-09 on `32dd0c6354`). Close with
  `settings-pages-close-btn`.
- **`ss-rows`, re-driven 2026-11-20 on `7c937b0a1f`.** The overlay shows
  whole on its first frame (`28f0ccf993`): a `MutationObserver` read
  `.ssv3-overlay` and `.ssv3-pill-input` at `opacity` `1`, `animation-name`
  `none`, no `entered` class, at insert. Tool rows take their aliases from
  the tool search's registry (`9a0ab7a3cf`): `channel` led with
  `super-search-result-tools:ParallelLine:Tool-btn` (`Parallel Line`,
  `Drawing tool`), then CCI, Donchian and Keltner, then Fib Channel,
  Disjoint Channel and Flat Top/Bottom. `auto scale` listed
  `axis:auto-scale` (`Auto Scale ON`), `axis:scale-price-only` and
  `commands:changeScaleMode`; the row's return to Auto now eases
  (`02de83a38a`, source). `one click trading` listed nothing: the
  `one-click-trading` row exists only with a connected Hyperliquid session
  (`2426af0110`, source). `hyperliquid btc` listed only the `Open symbol
  search` row. A symbol row under the cursor warms its market (see the
  chart boot guide's `boot-intent-warm`; not driven here).
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
  **Driven 2026-11-26 on `1d1a3e1410` (a guest JWT)** from Super Search
  (`release notes`, `Enter`): 84 rows led by `4.61.0 Latest` (`Custom
  intervals, free on every plan.`, November 25, 2026), then `4.59.0`,
  `4.53.0 Spotlight`, `4.49.0`; no `4.60.0` and no `4.58.0` row. `4.61.0`
  has no audience, so every viewer sees it and it takes `Latest`. Its body
  reads `Chart on candle sizes between the presets, like 18m, 90m and 2d,
  on every plan, Free included. Open the interval menu, press Custom, type
  a size and press Use.` and `Where they do not run yet: Alerts, Replay and
  the order book heatmap stay on the regular intervals.` That last clause
  is out of date: `3cacf4483d`, an hour later, runs the Order Book Heatmap
  at seven custom sizes (a product copy gap). Count the rows with a quoted
  prefix selector, `[data-testid^="release-notes-version-"]`, and re-read
  before trusting a `0`: an unquoted prefix read three seconds after the
  palette's `Enter` gave `0` while the page was up, and the quoted read a
  minute later gave 84 (timing and quoting were not separated).
  **Driven 2026-11-25 on `ec531568de` (a guest JWT)** from Super Search
  (`release notes`, `Enter`): 83 rows led by `4.59.0 Latest` (`TPO chart,
  trading in replay and more.`, November 24, 2026, no spotlight badge),
  then `4.53.0 Spotlight` (`The US tape.`), `4.49.0`, `4.48.0`; no
  `4.60.0` row. `4.60.0` is the cTrader launch with the `ctrader`
  audience (`fx-ctrader` on a computer), and the list hands `Latest` to
  the newest entry the viewer can see (`releasesForViewer`), so a guest's
  `Latest` is `4.59.0`. The `4.53.0` spotlight replay now starts from the
  second row. A testid holding dots breaks a CSS attribute selector
  without quotes: select by prefix and read `dataset.testid`.
  **Driven 2026-11-24 on `8cd7ad448e` (a guest JWT)** from the palette row
  `super-search-result-settings:tab:notes-btn`: 82 rows led by `4.53.0
  Latest Spotlight The US tape. November 5, 2026`, then `4.49.0`, `4.48.0`
  and `4.45.0`, down to `1.1.0`; the nav read Keyboard Shortcuts,
  Performance, Preferences and Release Notes.
  **Driven 2026-11-21 on `92f4a841ef` (a guest JWT):** 82
  `release-notes-version-<ver>-btn` rows, `4.53.0` (`Latest`, `Spotlight`,
  `The US tape.`, `November 5, 2026`) first, then `4.49.0`, `4.48.0` and
  `4.45.0`, down to `1.1.0`; no `4.57.0` row and no `4.58.0` row (`Black
  Friday.`, dated 2026-11-24, for signed-in Free and Plus accounts with
  the flag `black-friday-2026` on, `3686b10ead`, source). The palette row
  is `super-search-result-settings:tab:notes-btn`. The nav reads Keyboard
  Shortcuts, Performance, Preferences and Release Notes for a guest.
  **Driven 2026-11-20 on `7c937b0a1f` (no session):** 84 versions, led by
  `4.53.0 Latest Spotlight The US tape. November 5, 2026`, then `4.50.0`
  and `4.49.0`; no `release-notes-version-4.57.0-btn`, whose audience is
  the moved-to-Ultimate member (`ebbd08ef1d`, source). The first nav click
  after the open may not take (see Gotchas).
  **Driven 2026-11-19 on `413f86e5af`:** a guest's page led with `4.53.0
  Latest Spotlight The US tape.` (82 versions). With
  `kiyo.flag-overrides` `{"pane-sides":true}` and a reload it led with
  `4.56.0 Latest Spotlight Panes on any side. November 18, 2026` (83
  versions). `4.56.0` (`92d1f0f188`) has the audience `pane-sides`, which
  needs the flag on a desktop layout, so with the flag dark nobody gets it.
  Its spotlight (`PanesLaunchHero`, CTA
  `release-spotlight-panes-browse-layouts-btn`) opens once per established
  account (source); a guest never gets a spotlight at boot.
  **Driven 2026-11-13 on `963af59de1`:** a guest's page still led with
  `4.53.0 Latest Spotlight The US tape.` and listed no `4.54.0`. `4.54.0`
  (`Alerts on drawings.`, `3b007b5f4f`) has the audience `drawing-alerts`,
  which lists it only for a signed-in session since `06e62c10c2` graduated
  `drawing-alert-one-click`; a guest never sees it. For a signed-in session its spotlight carries
  `release-spotlight-drawing-alerts-draw-btn` (`Draw a line`, which arms the
  trend line tool) and `release-spotlight-drawing-alerts-got-it-btn` (source).
  **Driven 2026-11-06 on `8bcd72f8f5`:** the Super Search row
  `super-search-result-settings:tab:notes-btn` (query `release notes`) opened
  the page with 82 rows, `4.53.0 Latest Spotlight The US tape. November 5,
  2026` first: its audience is `stocks`, and a guest then read `us-equities-full`
  ON (since `06e62c10c2` the flag is gone and the spotlight is everyone's). A version row's click only selects it. **The spotlight opens from the
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
  The `language` row reads `Preferences`.
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
  | `tb-options-btn` (absent for a guest since `b1f10f1e3b`) | `terminal` (until then) |
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

- **`set-lite`: Lite charts (`14e97da372`, `b62ef4c998`, `fe722ed806`; driven
  2026-11-09 on `32dd0c6354`).** `find testid settings-pages-nav-performance-btn
  click` opens `performance-settings-page`, whose `light-charts-setting-row` holds
  one `on-off-toggle-btn` (`aria-checked`). The state is `localStorage`
  `kiyo:pref:light-charts` (`1`, or absent when off); a click also writes
  `kiyo:pref:light-charts:decided`. While on, the chart carries
  `light-charts-chip` (name `Lite charts on`, no visible text); a click opens
  `light-charts-card` with `light-charts-turn-off`, and turning it off raises a
  `Lite charts off. Change it anytime in Settings. Undo` notice. Drive that
  notice's `Undo` by its row, not `find role button --name "Undo"`, which picks
  the footer's undo first. No gate: a guest reaches it. Not driven: the chart
  settings On Screen page's copy of the row and the phone drawer's.
  **Only the hardware class offers it now (`21126deb8b`, source).** The
  `Panning choppy?` ask after choppy drags is gone: measured stutter is
  telemetry only. A device the older boot-time probe alone had switched on,
  with no decision stored and no hardware group, is switched off once and
  silently when its settled probe reads a fast display (source,
  `src/utility/chart/lite/lite-hint.ts`), so a reused profile can lose
  `kiyo:pref:light-charts` with no notice. A fresh profile is unaffected.
  **`Keep` stores the decision (driven 2026-11-10 on `c2c02b7b42`).** The
  auto-on writes `kiyo:pref:light-charts` `1` but no `:decided` key; `Keep`
  wrote `kiyo:pref:light-charts:decided` `on`, the chip stayed, and a later
  navigation back to `/chart/` raised no notice.
- **`set-timezone` rebuilt with an `Exchange` zone and a search
  (`2c00cd33c6`, `c75024f3ca`; driven 2026-11-21 on `92f4a841ef`, a guest
  JWT).** `find testid footer-timezone-select click` opens a list of 109
  `role=option` rows (`.timezone-region`) under a search field
  `footer-timezone-search` (placeholder `Search time zones`). The first
  row is `timezone-row-exchange` (`Exchange`, `Market's own time`, and the
  current chart's zone, `UTC` on a crypto chart); it is the only row with
  a testid. The rest are one row per city with its offset (`Honolulu
  UTC-10`, `Alaska UTC-9` and on); `New York` also carries `ET`. Filling
  the search with `tok` left `Tokyo UTC+9` and `Tokelau UTC+13` and hid
  the Exchange row; `new y` left `New York ET UTC-5`; `zzzz` read `No time
  zone matches`. Clicking `timezone-row-exchange` set the `user` store's
  `settings.timezoneMode` to `exchange` and left `settings.activeTimezone`
  alone. In that mode the footer read `UTC` on BINANCE.F BTCUSDT and, on
  `EQUITIES · TRADES AAPL`, `UTC-5` with the clock `15:46:13` against
  `20:46:13` UTC. A city row returns to a fixed zone: the `Reykjavik` row
  (search `utc` lists Casablanca, Dublin, Lisbon, London and Reykjavik,
  all `UTC`) set `timezoneMode` `fixed` with `Atlantic/Reykjavik`, the
  boot zone; there is no bare `UTC` row any more. No wall rose for the
  guest, and a reload drops a guest's pick. Not driven: a CME chart on
  Chicago time, the time axis's menu row and the phone Settings page.
- **`set-timezone` as driven 2026-11-08 on `943281a2eb` (`2cad385819`; the
  list and the `UTC` row below are stale since `c75024f3ca`).** `find testid footer-timezone-select click`
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
- **`set-price-line` (driven 2026-11-14 on `c7d4eccfac`; `fd7c368a8c`).** Fill
  `price line width` and click `super-search-result-axis:price-line-width-btn`
  (the palette also lists `Bullish price line` and `Bearish price line`; all
  three open the page and toggle nothing; the row's subtitle still reads
  `Price axis`). **Since `1607afdb85` (driven 2026-11-28 on `511ce25e50`)**
  the docked settings card opens on `chart-settings-page-scales`
  (`chart-settings-page-title` `Scales & Spacing`), scrolled to the row, with
  the Price axis group's Advanced fold (`price-axis-advanced`) already open;
  `price-axis-line-width` (`Price line width`, `1 px`),
  `price-axis-line-bullish` and `price-axis-line-bearish` (colour pickers)
  sit in that fold under `Last price`. The old `chart-settings-page-priceAxis`
  page is gone. They show only while Last price is
  `Line` or `Both`: its `segmented-label-btn` hid all three, and
  `segmented-line-btn` brought them back. The width is a scrub number whose
  value span covers its input, so a click on the input fails with `covered by
  <span.scrub-number__value>`: run `browser click "[data-testid=price-axis-line-width]
  .scrub-number__value"`, type the width and press `Enter`. Proof:
  `chartStore.mergedAllCharts[0].metadata.customChartStyles` read
  `{"priceLineWidth":2}`; the card's `overlay-settings-reset-defaults-btn`
  cleared it to `{}`. An edit made while the tab is hidden never reaches the
  store (the write waits for an animation frame): re-front the tab first.
- **`set-pages` (driven 2026-11-28 on `511ce25e50`; `1607afdb85`).** Open
  Chart settings from the chart's context menu (`mouse move 400 400`,
  `mouse down right`, `mouse up right`, then `find testid chart-ctx-settings
  click`). The panel's head reads `Main` and the body is `chart-settings-root`:
  `chart-settings-page-appearance-btn` (`Appearance`, value `Terracotta`),
  `chart-settings-page-scales-btn` (`Scales & Spacing`),
  `chart-settings-page-hours-btn` (`Trading Hours`),
  `chart-settings-page-screen-btn` (`On Screen`), then under `On this chart`
  `chart-settings-page-indicators-btn` (`Indicators`, value `1 indicator` in
  `chart-settings-page-indicators-value`). A guest sees no
  `chart-settings-page-trading-btn` (listed only for an account that draws on
  a chart). A page row opens `chart-settings-page-<id>` with
  `chart-settings-page-title` and `chart-settings-back-btn` back to the list.
  The old tab ids live on as sections: `chart-settings-section-{style,
  priceAxis,pane,source,sessions,timeAxis,events,display,trading}`
  (Appearance holds `style`; Scales & Spacing holds `priceAxis`, `pane` and
  `source`; Trading Hours holds `sessions`, `timeAxis` and `events`; On
  Screen holds `display`). Less used rows sit in closed `Advanced` folds
  (`price-axis-advanced`, `pane-space-advanced`, `chart-source-fold`,
  `chart-style-{volume,chart}-fold`, `display-settings-fold-{chart,app}`),
  each opened by its `<fold>-toggle` button (`Advanced`, `N more` while
  shut). **Search:** `settings-search-btn` opens `settings-search-input`;
  a match shows under a caption with its page's name
  (`.i-settings-search-page`), and `zzqqxx` showed `settings-search-empty`
  (`No settings match “zzqqxx”` / `Some settings show only when another
  setting is on.`). `scale mode` showed the `Scale mode` row normally, but a
  row inside a closed fold shows blank (see Gotchas). Close the panel with
  `overlay-settings-close-btn`; `Escape` leaves it open. Not driven: the
  Appearance theme tiles (`chart-settings-theme-<key>-btn`) and the live
  `chart-style-preview`.
- **`set-layouts` (driven 2026-11-28 on `511ce25e50`; `6f7a1e7619`).**
  `press Shift+T` opened `layouts-dialog` on `layouts-my-layouts-pane` with
  no wall for a guest (tabs `layouts-tab-my-workspaces` and
  `layouts-tab-community-browse`, `layouts-search-input`,
  `layouts-dialog-new-layout-btn`, `layouts-dialog-close-btn`). The list
  head carries `layouts-select-btn` (`Select`) and `layouts-sort-btn`
  (`Last Opened`) beside the group (`layouts-group-previous7`, `Previous 7
  days`, `layouts-group-count` `1`); the `n layouts` total is gone. The
  guest's one row is `layouts-row-guest-workspace` (`Guest Workspace BTC-USD
  · 1h Active`) with `layouts-row-favorite-…` and `layouts-row-more-…`
  (shown on hover). `Select` is `disabled` while the only row is the active
  layout, so a guest cannot reach select mode (`layouts-select-toggle-all-btn`,
  `layouts-select-done-btn` and the bottom bar are source only). Fill
  `zzqqxx`: `layouts-my-layouts-empty` read `No layouts match` / `Try another
  name, or clear the search.` with `layouts-clear-search-btn` (`Clear
  search`), whose click emptied the field and brought the row back.
- **`set-tooltips` (driven 2026-11-14; `af600b6397`).** Fill `tooltips`: the
  row `super-search-result-tooltips:global:tooltips-btn` reads `Tooltips Hide
  tooltips ON`. Its click wrote `localStorage['kiyotaka:tooltips:v1']` `off`
  and put `tips-off` on `document.body`; the row then read `Show tooltips
  OFF`, and a second click wrote `on`. Since `1607afdb85` (driven
  2026-11-28 on `511ce25e50`) the row lives on the On Screen page
  (`chart-settings-page-screen-btn`), under the `Every chart` caption
  (`display-settings-group-app`) inside its Advanced fold
  `display-settings-fold-app`, shut by default and remembered per device
  (the old `display-settings-group-general` and
  `chart-settings-page-display-btn` are gone): `tooltips-setting-row`
  (`Tooltips`, `The small box that names a button when the pointer rests on
  it`) with an `on-off-toggle-btn` (`aria-checked` `true`). Desktop only.
  The app now draws its own tooltip in
  place of the browser's `title` box.
- **`ss-forex` (driven 2026-11-14; `40c9e7f45c`).** Fill `EURUSD`:
  `super-search-result-symbols:forex:EUR-btn` (`EURUSD Euro · Forex`) leads,
  then `symbols:open-search`. `XAU/USD` listed `symbols:forex:XAU-btn`
  (`XAUUSD Gold (one troy ounce) · Forex`). The EUR row charted `FX_OTC`
  `EUR/USD` (252 bars), and on `4h` the bars held through 65 s
  (`9089a0c6c6`).
- **`ss-long-code` (driven 2026-11-16 on `6bfc742bc8`; `b68e436042`).** Fill
  `AAPL261120C00360000`: the list read `No results found` over
  `super-search-result-symbols:open-search-btn` (`Open symbol search for
  "AAPL261120C00360000"` with `Tab`); before `b68e436042` a market text over
  12 characters was dropped. `queryShape.ts` now reads the shape
  (`symbolQueryShape`, `symbolLookupText`), and `No results found` waits while
  an OSI lookup is pending. The contract row (`symbols:contract:OPRA|…`, a
  title like `AAPL 20 Nov 2026 360 Call`) needs the `opra` flag. **A guest
  reads it on since `6b3e077975`** (`GUEST_DEFAULT_FLAGS`; `isOn('opra')`
  read `true` on 2026-11-24 on `8cd7ad448e`), yet that night
  `AAPL261218C00300000`, `AAPL261218C00250000` and `SPY261218C00600000`
  each listed only the `open-search-btn` row after 5 to 12 s, most likely
  because the OPRA plane is unrouted on this seat, as the stocks and CME
  planes are. The sample code above expired on 2026-11-20: use a live
  expiry and a strike the chain lists.
- **`ss-opra-data` (driven 2026-11-24 on `8cd7ad448e`, a guest JWT).** Fill
  `options`: the list leads with
  `super-search-result-featureCommands:opra-realtime-data-btn` (`OPRA
  real-time options data`, under `SHORTCUTS`), then the Trinity layout rows
  and the options wrun registry rows. The row shows wherever `opra` reads
  on, which now includes a guest (its aliases include `opra`, `options
  data` and `us options data`). Clicking it raised the sign-in card headed
  `Purchases` (`toggleOpraPurchaseFlow`; the flow itself is signed-in).
- **`set-highlights` (driven 2026-11-16 on `6bfc742bc8`; `8f44e9c9cc`).**
  Fill `highlights`: `super-search-result-settings:toggle:bar-highlights-btn`
  leads (`Highlights ON`); a click turned it to `Highlights OFF` and a second
  back on. The store field is the main pane's `axis.barHighlights`
  (`chartStore.setBarHighlights`); `window.tc[0].metadata[0]` does not carry
  it, so read the row. The On Screen page row (the Display page before
  `1607afdb85`; the settings search found it there on 2026-11-28) is
  `display-settings-row-barHighlights` after Momentum arrows (source). The
  same commit ends the VWAP line in a plate (`VWAP Session 64877.03` in
  every frame of the pass) with a `Label` switch in VWAP's Display group
  (source). Fill `clean look`: `settings:toggle:layout-look-clean-btn`
  (`Look: Clean OFF`, `d8a23b47d6`) is listed, and it acts only in a
  multi-chart layout, which a guest cannot open.
- **`plans-page` states the backtest reach (`9bb0a4f8f7`, `c81044a554`;
  driven 2026-11-26 on `1d1a3e1410`, a guest JWT).** The compare table's
  Build group carries `console-subscription-compare-backtestCandles`
  between Private scripts and Published layouts: `Strategy backtest` / `How
  far back one test goes on a 1m chart, for a strategy added from
  Indicators.` / `50,000 candles`. The Plus card's key features list
  `console-subscription-plus-point-backtestCandles` `50,000 candles per
  backtest`. A guest's page has one paid column (Plus); the source gives
  Ultimate `100,000` and Free no line. A guest sees no `Custom intervals`
  row or card line: both follow `typed-interval-widths`, which reads off for
  a guest; a signed-in viewer sees the row on every plan since `7248dba544`
  (source). Since `9fd6809fe0` a checkout button shows a spinner with
  `aria-busy="true"` and, after 1 s, `Taking you to secure checkout`
  (`BusyLabel.vue`, `CheckoutWaitLine.vue`; the Plus sheet, the bag's Pay
  and the `/plus` confirm; source, signed-in). Since `62b247cf99` the Black
  Friday headline reads the public campaign through an anonymous price-list
  read, so a guest sees the same headline as a member while the campaign is
  on (source; no sale on the guest page on 2026-11-26).
- **`plans-page` moved and rebuilt (`7e88ad6552`, `2bf8b7cd57`,
  `c16023b51a`; driven 2026-11-21 on `92f4a841ef`, a guest JWT).** `open
  /chart/plus?ref=vk` landed on `/chart/plans?ref=vk`: the old address
  redirects and keeps the query. The page reads `Elite charting` over
  `console-subscription-billing-{monthly,annual}-btn` (`Monthly`,
  `Yearly` with `Save 17%`, Yearly picked), one
  `console-subscription-plus-card` (`Plus`, `$29/mo` with `$35` struck,
  `$348 a year`, `console-subscription-cta-plus-btn` `Get Plus`, `10
  indicators on every chart`, a `KEY FEATURES` list and
  `console-subscription-plus-point-<key>` rows), a top bar
  `console-subscription-toolbar` holding
  `console-subscription-start-free-btn` (`Start with Free`),
  `console-subscription-compare` (`Compare features`, the views
  `-compare-view-differences` and `-view-all`, the note `18 features.`,
  group heads `-compare-group-<key>` and rows such as
  `-compare-watchlistSymbols` reading `500` for Plus),
  `console-subscription-exchange-data` (`Live exchange data`, `Add-ons,
  billed on their own. They work with any plan. Crypto is live on every
  plan.`) with `console-subscription-cme-addon-card` (`$7/mo`, `Without
  it: 10 min delayed`, tiers `-cme-addon-tier-{l1,depth}`,
  `-cme-addon-cta-btn` `Add live data`; `Add` on 2026-11-24) and
  `console-subscription-stocks-addon-card` (`-stocks-addon-cta-btn`
  `Add`), the bag `market-data-bag-bar` (`market-data-bag-count` `0
  add-ons`, `-sum` `$0/mo`, `market-data-bag-continue` `Continue`), `Have
  a code?`, and `console-subscription-faq` (`Questions`) with five
  `console-subscription-faq-q-<n>-btn` rows: `What happens when I
  upgrade?`, `What happens to my charts if I downgrade?`, `Can I switch
  between monthly and yearly?`, `Which markets can AI agents read?` and
  `Are yearly payments refundable?`. A guest's press on
  `console-subscription-stocks-addon-cta-btn` raised the sign-in card
  headed `Purchases` (`guestLoginFeatureId` `billing`) and the bag stayed
  at `0 add-ons`. The words `Max` and `Ultimate` appeared nowhere on a
  guest's page and no `black-friday-*` or sale node was present. **On
  2026-11-25 (`ec531568de`, a guest JWT) the page still read `Elite
  charting` and `Yearly` `Save 17%` with `$29/mo` over a struck `$35`, and
  no `console-subscription-bf-hero`, `[role=timer]` or `-bf-tag` node,
  although since `d8ace37f9d` the sale draws from the viewer's own quoted
  offers with no flag (`PlansHeroSale.vue`): the server quoted a guest no
  Black Friday campaign. A viewer it is quoted to sees the `h1` `Black
  Friday`, `Up to {N}% off.`, `Ends November 30.`, a `Time left` timer
  (Days, Hours, Minutes, Seconds), per-plan `-bf-tag` and `-bf-was`, and
  `Save up to {percent}%` (source).** Gone
  from the 2026-11-19 page: `console-subscription-free-bar`,
  `console-subscription-faq-live-link`, the eleven-question list and its
  broker answer (`q-10`). Super Search's `plans` leads with
  `featureCommands:plus-page` (`See OpenMarket plans`; `ultimate` finds it
  too) and `Enter` opened `/chart/plans` in a new browser tab: close it
  with `browser tab close t2` and return with `browser tab t1`. Not
  driven: a Max card and a Max holder's look (`ad5a38e0d5`), the bag's
  sheet and checkout (`market-data-bag-sheet`, signed-in), the Black
  Friday page and doors (`21e174ae02`, `black-friday-2026`, dark), and
  the moved member's flipping card (`2a9b9d4e9c`).
  **Re-driven 2026-11-24 on `8cd7ad448e` (a guest JWT).** The section
  `console-subscription-exchange-data` (`Live exchange data`, the same
  subtitle) now comes BEFORE `console-subscription-compare` in the page
  (`bf28d48d70`), and it holds three cards: CME futures (`$7/mo`, `Top of
  book` and `Full depth`, button `Add`), US stocks and, new for a guest,
  US options (`console-subscription-opra-addon-card`, `Live trades and
  quotes on every listed US option.`, `$4.95/mo`, `Without it: 15 min
  delayed`, `console-subscription-opra-addon-cta-btn` `Add`). The US
  stocks card gained a `Billing` switch,
  `console-subscription-stocks-addon-cycle-1m` and `-cycle-1y`
  (`aria-checked`); `Yearly` kept `console-subscription-stocks-addon-price`
  at `$19/mo` and showed `-stocks-addon-billed` `Billed $228 a year.` (no
  `-offer` line without a server sale). A guest's press on
  `console-subscription-opra-addon-cta-btn` raised `Purchases` and the bag
  stayed at `0 add-ons`. The Plus card, the billing pills, the five
  questions and the absence of `Max`, `Ultimate` and `black-friday` nodes
  were unchanged. Source only: with a plan in the cart the bar adds
  `market-data-bag-bar-plan` and the sheet is titled `Cart`
  (`72628180ca`); payment comes first and the exchange forms follow the
  paid return (`784eeb5207`); Get Plus and Get Max ask about live data
  (`PlanAddonAskDialog.vue`, `9380ec3b8c`); and a buy link signs the
  visitor in first and keeps the link through the reload (`f1905618f7`).
- **`plans-page` as driven before the move (2026-11-16 on `6bfc742bc8`; re-driven 2026-11-19 on
  `413f86e5af`: `console-subscription-faq-q-10-btn` `My broker is connected.
  What goes live?` expanded to its plain last sentence, `The heatmap, the DOM,
  TPO and alerts stay 10 minutes delayed.` Since `37d2147e5e` that sentence
  becomes the depth wording (`The DOM and the heatmap's newest columns are
  live when your broker account has market depth; …`) where a connected
  session may write the book (`isNinjaTraderDepthOn()` or
  `isFuturesByofKindOn('book')`), which a guest never reads (source).
  Re-driven 2026-11-18 on
  `cff04f9a01`: the Plus card with `50 indicator alerts` and `200 price
  alerts`, still no Ultimate card; an Ultimate card lists 1,000 price and 250
  indicator alerts since `5bdb3ba1fc`, source).** Open
  `/chart/plus` as a guest: `console-subscription-billing-{monthly,annual}-btn`,
  `console-subscription-plus-card` (`Plus`, `$29/mo` annual, `$348 a year`,
  `console-subscription-cta-plus-btn` `Get Plus`), the indicator row and
  points, `console-subscription-free-bar` with
  `console-subscription-start-free-btn`, `console-subscription-compare`, the
  live-data add-ons, `Have a code?`, and since `6231da90e9` a `Questions?`
  block of eleven `console-subscription-faq-q-<n>-btn` rows and
  `console-subscription-faq-live-link`. `console-subscription-faq-q-0-btn`
  opened `What data is included on the Free plan?` (`Every market and every
  chart type. Crypto is live. CME futures are free on a 10 minute delay and US
  stocks on a 15 minute delay …`, `See what is live, by market`). The page
  fades in behind a loader, so wait about 10 s before shooting. No Ultimate
  card and no `console-subscription-sale-strip` showed: the plan list and the
  sale come from the backend (`b4a028d14d`, `427c082876`), and the Ultimate
  offer at a plan limit is signed-in only.
- **`guest-refusal` (driven 2026-11-14; `c93de362ff`).** Raise the wall
  (`global-nav-screenshot-btn`), click `login-signup-use-password-btn`, fill
  `.login-signup-overlay input[type=text]` with a made-up address and
  `input[type=password]` with 8 to 20 characters (a 21-character password
  keeps `Log In` disabled: the rules cap it at 20), then
  `login-signup-submit-btn`. Proof: `login-signup-failure` read `Could not
  sign in with that email and password. Try again.`, and the console logged
  `[auth] signIn refused` with `ZKP_USER_NOT_FOUND`. An unknown address and a
  wrong password read the same line on purpose. Never submit `Email me a
  code` (it sends a real code).
- **Release Notes for a guest (driven 2026-11-14).** The `4.55.0` `Trade with
  Tradovate.` spotlight (`1a7075d760`, `TradovateLaunchHero`, CTAs
  `release-spotlight-tradovate-connect-btn` and `-not-now-btn`) is for the
  `ninjatrader` audience (`futures-trading` and `futures-ninjatrader` on), so
  a guest's list still starts at `release-notes-version-4.53.0-btn` (`4.53.0
  Latest Spotlight The US tape.`) with no `4.55.0` row.


## Gotchas

- **The Chart settings search shows a row inside a closed `Advanced` fold
  as a blank gap (product gap, driven 2026-11-28 on `511ce25e50`).** Fill
  `tooltips` in `settings-search-input`: the `On Screen` caption shows and
  `tooltips-setting-row` is in the DOM with its text, but the frame is
  empty under the caption, because its fold's `.saf__rows` computes
  `visibility: hidden`. The fold's scoped rule `.saf:not(.saf--open)
  .saf__rows[data-v-…]` outranks `[data-settings-searching]
  .saf__rows[data-v-…]` (`src/components/common/SettingsAdvancedFold.vue`).
  A row outside a fold (`scale mode`) shows, and a fold the user opened
  shows. Do not read a match off `offsetParent` or a DOM count; read the
  computed `visibility` and open the PNG.
- **The first settings nav click right after the dialog opens can be undone
  (driven 2026-11-20 on `7c937b0a1f`).** `press Meta+Slash`, a 1 s wait and
  a click on `settings-pages-nav-language-btn` (or `-notes-`) left
  `.nav-item.active` on `shortcuts`, four times in four. A later click on
  the same item took (`notes` then listed 84 versions), and so did every
  click after it. Click, read `.nav-item.active`, and click again when it
  has not moved. Seen on a no-session dev lane only; the cause was not
  traced, and whether a built app does the same was not checked.
  **Not reproduced with a guest JWT (driven 2026-11-21 on `92f4a841ef`):**
  `press Meta+/`, a 1.2 to 1.5 s wait and one click on
  `settings-pages-nav-language-btn` moved the active nav item and showed
  the Preferences page (`APPEARANCE`, `Dark`, `Gray`, `Light` …), five
  times in five. Read the page under the nav, not
  `settings-pages-body`'s first line: the body's text starts with the nav
  list itself.
- **A no-session lane shows the signed-in settings nav (driven 2026-11-20).**
  `settings-pages-nav-{my-info,subscriptions,connections,api,referral,support,shortcuts,performance,language,notes}-btn`
  with `Sign Out` at the foot, where a guest gets four items.
- **With no session the wall is the email card (driven 2026-11-17 on
  `60b7e6b190`).** `handleGuestAccess` (`src/composables/useGuestAccess.ts`)
  raises the sign-in wall only for a guest; an account that is not a guest
  and not verified gets `promptEmailVerification` instead. A lane whose
  backend is unreachable has no token at all, `jwt.isGuest` reads `false`,
  and every walled door then shows `Verify your email to unlock <feature>`
  with `We'll send a 6 digit code to .` (no address) and `Send me a code`,
  while `dialogStore.guestLoginFeatureId` stays `null`. Do not count that card
  as the guest wall; restore the backend (see the chart boot guide's Gotchas)
  and re-drive.
- **A fresh headless device gets Lite charts by itself, with a staying notice
  (driven 2026-11-09 on `32dd0c6354`).** The software GL lane counts as a weak
  class: about 12 s into a boot with no stored decision the preset turned on and a
  `.q-notification` read `Lite charts is on. Smoother panning on this computer,
  same charts. Keep Turn off` with no timeout. It stays over the bottom of the
  frame until you act, so include it in the overlay check, and record the state
  in any drag or performance read. **It waits for its words (`bf17ae49cd`;
  driven 2026-11-10 on `c2c02b7b42`).** The 2026-11-09 cold boot read raw keys
  (`perfHints.liteCharts.autoOnLine`, `autoOnSub`, `keep`); boot toasts now
  wait, capped, for their locale bundle. The 2026-11-10 cold boot read the
  words, and a page-text match on `perfHints.` found nothing. A raw key there
  is now a regression. When the notice fires: at mount for a 2-core or a
  4-core 8 GB device, otherwise after the probe settles (5 s plus an idle
  slot) once the GPU reads as software (source, `lite-hint.ts`).

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
  code. **A failed check retries, and a refused code goes back to the address
  (`abcb149af8`, `1b5ad78f88`, `4fe6fb323e`; source).** Cloudflare retries a
  failed challenge itself (every 2 s), the 5 s wait is unchanged (it went to
  10 s and back), and a first send with no token still goes out. When the
  server refuses a code for its bot check, the code panel toasts `We couldn't
  confirm you're human. Complete the check on the sign-in screen and request a
  new code.` and returns to the address step, not to `invalid code`. Not
  driven: it needs a real code. The sign-in form also fades out before the card shrinks to the welcome
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
- **`ss-cursor` (driven 2026-11-12, `a44bdd903d`).** The active row carries
  `.ss-row--active`; read it with
  `document.querySelector('.ss-row--active').closest('[data-testid]')`. With
  no pointer move, `are` and then `area` each left the first row active
  (`area` led with `chartStyle:area`), so Enter runs what is shown first. The
  Ask card's Edit selects all the words (source). Words typed apart read as
  one name (`compounds.ts`): `heat map` listed the Order Book and Options
  heatmaps, and `full screen` and `fullscreen` both listed only
  `commands:toggleExpandChart` (`Toggle chart fullscreen`). `go to date`
  lists `commands:history-btn` (`Go to date ⌥ G`). `move chart` lists nothing
  on one chart; the four `Move chart left/right/up/down` rows need a layout
  of two or more, which a guest cannot open (source, `6d36f36a68`).
- **`ss-typed-interval` (driven 2026-11-12, `3a64fcc3af`).** Click the chart,
  `press Comma`, then `keyboard type "15"`: the palette opened with `Select
  15m interval` first and active, and Enter set `activeInterval` to `15m`.
  `7` listed `customIntervals:typed-interval-unavailable-btn` (`Not available
  on this chart`) first; `7q` is not read as an interval and listed only
  `Open symbol search for "7q"`. The `typeInterval` command has no palette
  row of its own.
  **Digits are doors too (`30e7cf86f1`; driven 2026-11-21 on
  `92f4a841ef`).** With the page holding the keys, `press 5` opened the
  palette with `5` typed and `commands:select5mInterval` first (then an
  indicator, `featureCommands:layout-preset-big-topleft-5` and
  `customIntervals:interval-5s`); `Enter` set `5m`. `press 1`, `press 5`,
  `Enter` set `15m`. See the ticker guide's `tb-digit-keys`.
- **`ss-rows` on 2026-11-21 (`92f4a841ef`, a guest JWT).** `trade panel`
  listed `commands:toggleTradePanel` (`Trade panel`, `⌥ ⇧ T`,
  `ef98d427d4`) and `panels:Tape`. `plans` led with
  `featureCommands:plus-page` (`See OpenMarket plans`). `ctrader` listed
  no `Link cTrader` row (an indicator and two registry rows matched the
  letters) and `spotware` only `Open symbol search`: the door needs the
  flag `fx-ctrader`, which read `false` for the guest (`249761fa12`).
  `black friday` and `one click` listed nothing, and `ninjatrader` only
  `Open symbol search`. `release notes` listed `settings:tab:notes`.
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
  nothing). `settings.ts` holds the four `Ask before sending` rows,
  `trade:confirm-order` (`New orders`), `trade:confirm-change` (`Changes`),
  `trade:confirm-cancel` (`Cancels`) and `trade:confirm-position` (`Flatten,
  Reverse and Cancel all`), one set for every account since `72b80f37c7`
  (they replaced the `trade:futures-*-confirm` rows), behind the signed-in
  trading gate on desktop and phone. `quickTrade.ts` adds `quick-trade-pill`
  (`Quick trade pill`), listed only while a mounted pill has published its
  pane. A guest gets neither (driven 2026-11-14: `ask before sending` and
  `quick trade` list nothing).
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
