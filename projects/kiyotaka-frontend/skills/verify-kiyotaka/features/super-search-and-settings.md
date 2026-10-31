# Super Search, settings pages and the guest wall

Super Search is the command palette a user opens from the `Ask anything ⌘K`
capsule in the top navbar. One query searches panels, commands, themes,
formulas and more, and a row runs its action. The Settings pages dialog holds
keyboard shortcuts, language and release notes, and a guest can open all three.
Every guest-walled control raises the same sign-in dialog, and this entry is
where that shared wall is described. Created 2026-10-27; last DRIVEN on
2026-11-01 against product tree `120d5d5d32` (`origin/main`), lane `18103`, a
guest lane with no JWT. Driven: the empty box (placeholder `Search the
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
- `ss-theme` a `dark` or `light` query toggles the theme, and a theme name
  (`volt`, `percept`, ...) applies that colour theme.
- `ss-formula` a ratio query such as `SPY / GLD` plots a formula chart.
- `set-shortcuts` `Meta+/` opens Settings on the Keyboard Shortcuts page.
- `set-notes` the Release Notes page lists versions.
- `ss-ask-commands` a query lists app commands as palette rows (hide candles,
  swap candle colours, and the rest) and a click runs them.
- `guest-wall` a walled control raises the sign-in dialog and names its feature.
- `ss-guides` a help question lists the best user-guide sections under `Guides`
  (live verification pending: it needs the backend's `/ask/config` to answer
  `surface:true`).

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
  The other colour ids are Seoul, Shanghai, Classic, Sourgum, Carbon and Quartz,
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
- **`set-notes`.** `find testid settings-pages-nav-notes-btn click`. Proof: the
  `release-notes-version-<ver>-btn` rows (81 on 2026-10-28, `4.49.0` newest).
  Poll for the rows: a nav click made straight after `Meta+/` once left the page
  on Keyboard Shortcuts, and a second open and click switched it within 2 s.
  The nav ids are unchanged (`settings-pages-nav-{shortcuts,language,notes}-btn`)
  but the `language` row now reads `Preferences`.
  Re-driven 2026-10-29: 81 rows, `4.49.0` newest. The `4.0.0` row now reads
  `4.0.0 Spotlight OPENMARKET V4` (`dc9ed408ee`), and the page body carries no
  `Kiyotaka`. Source holds 87 entries; `4.51.0` (`options`) and `4.50.0`
  (`wrun-launch`) are filtered by audience, so a guest's count is a viewer's,
  not the file's.
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

- **Proof.** The store read, the overlay or page testid, and a screenshot.

## Gotchas

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
- **`SPY / GLD` no longer charts the ETFs (driven 2026-11-01 on
  `120d5d5d32`).** The formula row `formula:SPY/GLD` resolved to Solana
  tokenized stocks: the ticker read `SOLANA SPYx/USDC:4pCZ…` and the title
  `SPYx / USDC · 4pCZCV…iNXhRw / GLDx / USDC · 5tGLud…fzETV9` (440 bars). On
  2026-10-29 the same row charted `SPY / USD / GLD / USD` (252 bars). The ranking
  change `528a31b434` is the suspect; product gap, reported, not a map error.
  The frame also showed `Connection lost. Reconnecting…` from that chart on,
  which turned out to be the gateway outage below, not the formula.
- **The wall's visible title is the feature's name.** The camera's wall is
  headed `Share Your Chart`, Replay's `Chart Actions`, then `Sign in or create
  an account / One email. We send you a code, no password.` with `Email me a
  code`, `Sign in with a password instead`, `Use a passkey`, `Google` and `X`.
  The `login-signup-*` ids are unchanged (`-submit-btn`, `-use-password-btn`,
  `-passkey-btn`, `-google-btn`, `-twitter-btn`, `-forgot-password-btn`,
  `-tos-link`), and a hidden `Back to log in / Forgot your password?` pane
  (`forgot-password-back-btn`, `forgot-password-send-btn`) sits first in the
  same overlay, so a testid listing starts with those two. `Escape` clears
  every state of it (driven 2026-11-01 from the camera, Replay and the
  forgot-password pane).
- **A gateway outage reads as `Reconnecting…` in `connection-status-chip`
  (seen 2026-11-01).** From about 21:55 UTC the tailnet-only name
  `tsdb-gateway.int.ore.kiyotaka.ai` stopped resolving on the mini (public DNS
  answers NXDOMAIN; only `100.100.100.100` knows it), the console filled with
  `v2 Streaming socket error` and `v2 Orderbook socket error`, OI and funding
  read `—`, Tape and Orderbook stayed empty, and `doctor`'s `v2 gateway` line
  flipped to `UNREACHABLE`. A reload still drew 440 candles from the OHLCV
  cache (`main-cache-painted-marked` in the ring). Read `doctor` and the chip
  before calling an empty live panel a regression.
- **Super Search mounts lazily.** `isSuperSearchOpen` goes true before the
  overlay is in the DOM, so poll for `super-search-overlay`.
