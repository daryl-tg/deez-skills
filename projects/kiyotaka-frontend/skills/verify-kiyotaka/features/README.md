# kiyotaka-frontend verification map

The maintained source for verifying user-facing chart behavior. Read this index
before driving, then use the matching feature file as the recipe.

Watchlist entry added 2026-10-23 on product tree `2a1ed750db` (guest-side driven
only). Maintenance pass: 2026-10-23 on product tree `2a1ed750db` (= `origin/main`), lane
`18097`, on a REAL guest-JWT lane (`isGuest` true, metadata present — not the
no-JWT lane earlier passes hit). Driven: chart boot, the full ticker pinned set,
chart type, interval, the v2 symbol dialog and a symbol switch, the editor via
Super Search, and — for the first time — `ind-add`, `ind-legend` and `ind-limit`.
Not driven: `ind-catalog`, and voice control, which is verified-unreachable on
any guest lane because `voiceControlEnabled()` is `isSignedInSession()`.

## Baseline preconditions

- Launch the lane on its **assigned** port (`18097`–`18197`), bound to
  `127.0.0.1`: `./control-kiyotaka up`. Never pick a free port, never `8080`.
  `doctor` reporting `lane FOREIGN` means another checkout holds the default
  port — a neighbouring worktree's live lane, not residue. Do not reclaim it:
  take another slot with `KIYO_LANE_PORT`, and set `KIYO_SESSION` too so your
  browser commands cannot drive the neighbour's tab.
  Every later command in the run needs the same two variables exported.
- `./control-kiyotaka doctor` exits zero. The `chart-schema` line must read `ok`.
- Viewport set to `1440 900` before any layout assertion.
- Candles present: `window.tc[0].metadata[0].rawData.length > 50`. Budget two
  minutes on a cold boot.
- Interval read, never assumed: `chartStore.activeInterval` (a guest with no
  stored state lands on `1h`).
- The catalog endpoint serves AND is seeded. `doctor`'s `catalog` line probes
  `/scripts/query` and catches a `500`, but a `200` only means the endpoint
  answered: an unseeded local mongo serves `200` with zero official rows. The
  seeded check is in the dialog, under `Browse all indicators` — a header reading
  `OFFICIAL INDICATORS 0` plus a banner naming
  `node scripts/seed-official-catalog.mjs` means `ind-catalog` is unreachable, and
  that is an operator-stack blocker, not drift.
- `doctor`'s `freshness` line read before anything else. A clean tree on `main`
  says nothing about whether it is CURRENT: a checkout hundreds of commits behind
  `origin/main` serves stale code while every other doctor line reads green, and
  a whole pass can then describe an app nobody is running. This has happened —
  one pass drove a tree 324 commits behind, so its live evidence and its
  source findings were about different code. When the line says BEHIND, either
  bring the checkout forward first (the operator's call, not yours) or label
  every finding with which tree it came from.
- `doctor` run twice on a freshly-`up`ed lane, with the second run believed. Its
  first transform probe compiles the module graph cold and has exceeded the
  budget, printing `the tree does not compile` about a healthy tree.
- BOTH first-load overlays cleared, in order: the once-per-device ink tutorial
  (`find testid ink-tutorial-close click`) and then the signup modal, which
  raises as soon as the tutorial stops suppressing it. They share the
  `.dialog-style.dialog-overlay` shell, so probing only the signup modal's testid
  on a fresh device reports `No element found` and reads as a stuck modal.
- Guest signup modal dismissed
  (`find testid guest-signup-modal-close-btn click`) — dismiss it immediately
  before each capture, never once up front. Do **not** drive it by the name
  `Close`: three buttons answer to that name and the matcher picks one under the
  overlay.
- Nothing on top:
  `eval "document.querySelectorAll('.q-dialog, .dialog-style, [role=dialog].open').length"`
  reads `0`. Do **not** count bare `[role=dialog]`: the signup modal and both
  app dialogs are `.dialog-style` overlays carrying no `role=dialog`, so that
  count stays `0` whether or not something is on top.
- **`jwtStore.isGuest` is not a guest check.** A lane started by
  `control-kiyotaka up` can carry NO JWT at all: `jwtMetadata` stays absent, so
  `isGuest` AND `isLoggedIn` both read `false` and the role is `null`, while the
  UI still says `Guest Workspace`. Record which state you drove.

  **The flag-override recipe a previous pass recorded here is DEAD.**
  `GUEST_DEFAULT_FLAGS` is now `{}` — `search-v2`, `option-chain`, `pulse`,
  `wrun-registry`, `free-tier-v2`, `voice-control` and the rest were all
  graduated out of the flag system during October 2026. Setting
  `kiyo.flag-overrides` for any of them does nothing. Delete that step from any
  recipe that still carries it.

  What replaced them is a **signed-in check**, not a flag: most graduated gates
  read `isSignedInSession()`, which needs a real JWT `id` and a non-guest role.
  So a no-JWT lane and a real guest both fail them, and the practical split is
  now signed-in versus not:

  - The V2 symbol dialog is **structural**, not flag-gated: V2 renders whenever
    the dialog is opened from a main chart on desktop and is not pair/screener/
    comparison mode. Guests get V2 there. The legacy `intent-filter-class-*`
    dialog appears only in those excluded contexts.
  - Surfaces that now need a signed-in session include the `memecoins` and
    `options` category tabs, Events/Earnings panels, the Pulse lane, the 4x4
    free-tier grids, and voice control.

  Source-verified on `fcc8e53b12`; not driven.
- **Identify the overlay before dismissing it — there are now two, and they
  alternate.** A guest boot raises the ink tutorial AND the signup modal, and the
  signup modal re-raises ~15s after the last blocking surface closes, so a
  multi-step drive gets interrupted repeatedly. Three drives were lost this pass
  clicking `guest-signup-modal-close-btn` while the INK TUTORIAL was the thing on
  top. Read what is there, then dismiss that:

  ```bash
  ./control-kiyotaka browser eval \
    "(()=>{const d=[...document.querySelectorAll('.dialog-style,.q-dialog')];return JSON.stringify(d.map(x=>[...x.querySelectorAll('[data-testid]')].map(y=>y.dataset.testid)[0]))})()"
  ```

  A `covered by <div.dialog-style.dialog-overlay>` failure means re-read, not
  retry.
- **An authed lane cannot be self-served.** Driven 2026-10-23: the local dev
  stack's login form does not do password auth — it sends a **6-digit sign-in
  code by email**, which the harness cannot read. So every "authed lane" claim in
  this map is currently unverifiable by an agent alone, and a guest-walled
  surface can only ever be proven as far as its wall. Ask the operator for a code
  or a password-capable account before planning an authed run; do not burn a pass
  discovering this again.
- Never drive an instance this verification run did not start.

## Driving conventions

- Start every recipe from the baseline unless its preconditions say otherwise.
- Prefer ARIA roles and accessible names over CSS selectors or DOM position.
  Where a control has no accessible name — layout grid cells, Panels rows, drawing
  tools — fall back to `find testid <data-testid>`, which this app populates well,
  rather than concluding there is no handle. Chart-type entries DO carry names, but
  as `generic` nodes, so match their text rather than a button role.
- **A name is not a handle if several controls share it.** A guest boot carries
  three buttons named `Close`; `--name "Close" --exact` picks one of the two that
  sit under the signup overlay and the drive dies as `covered by
  <div.dialog-style.dialog-overlay>`. Where a name is ambiguous, use the testid.
- Never key on an accessible name that is really *content*. The symbol-search
  field's name is the current symbol; match its placeholder instead.
- Browser actions run through `control-kiyotaka browser`, terminal actions
  through `control-kiyotaka cli -- <command>`.
- Treat every command as literal. Keep quoted names and flags unchanged.
- `agent-browser`'s fill text is **positional**:
  `find <locator> <value> fill "<text>"`. There is no `--text` flag; passing one
  types the literal string `--TEXT <text>` into the field and the failure looks
  like a search that returned nothing.
- Check an exit code unpiped. `cmd | tail` reports `tail`'s status, which has
  produced both a false "the wrapper swallows failures" finding and a false
  `doctor` pass in this map's own history.
- Assert engine state (`window.tc`) for anything the a11y tree cannot see. The
  chart canvas is WebGL and carries no accessible structure.
- Restore seeded state after a mutation. Never remove proof artifacts.

## Lanes

Each entry names the lane it needs. **Guest** needs only the lane; **authed**
needs the operator's local stack (`:3000`, `:4001`) plus a login, and mutates a
real account's autosaving workspace — use a throwaway account.

A guest-lane surface can still stop at a sign-in wall partway through: the entry
point opens, the control responds, and the *commit* raises
`Sign in or create an account`. `src/constants/authFeatures.constants.ts` is the
registry of every gated surface — 41 ids, among them `MULTI_CHART`, `MONITOR`,
`SCRIPT_EDITOR`, `TERMINAL`, `INDICATORS`, `WORKSPACE`, `ALERT`, `WATCHLIST`,
`FAVORITES`, `ONE_SECOND_INTERVAL`, `TAPE_MODE` and `LAYOUTS` — and
`promptGuestLogin` is what raises the wall. Read it before mapping something as
guest-reachable, and report the wall as the unmet precondition rather than
photographing a click that did nothing. Clear the wall with `Escape` before the
next step: it has no close button but it is not sticky, and
`dialogStore.guestLoginFeatureId` names the surface that raised it.

## Proof and skip reporting

- Capture the user action and the resulting state, not only the final screen.
- Chart proof is a **triple**: the engine-state read, the accessible name, and a
  screenshot. The first is the side effect, the last is the only thing that
  proves pixels were drawn.
- CLI proof includes the command, stdout, stderr, and exit code.
- Frames and `evidence-manifest.json` go in `artifacts/<run-id>/<revision>/`;
  validate with `./control-kiyotaka evidence check <run-id> <revision>` and hand
  back that path. There is no publish step on this seat. Never hand back a lane
  URL.
- Report an unreachable path with the attempted command and the unmet
  precondition. Never report a skipped entry point as verified via another path.

## Feature entry contract

An H1 title, one paragraph of user-visible behavior, then exactly four H2s in
order: `Sub-features`, `How to get to it (user POV)`,
`Driving it with control-kiyotaka`, `Gotchas`.

Keep implementation detail out. Name only user paths, stable handles, required
state, commands, and observable proof.

## Which dialog am I on?

No flag picks the dialog any more. `search-v2` graduated and
`GUEST_DEFAULT_FLAGS` is `{}`. The dialog is V2 when it opens from a main chart
on desktop and is not in pair, screener or comparison mode. Every lane, guest
included, gets V2 there, so `sym-scope` is a guest proof. The legacy
`intent-filter-class-*` dialog appears only in the excluded contexts and on
mobile. Source-verified on `fcc8e53b12` (`isSearchV2` in
`src/components/symbolSelection/SymbolSelectionDialog.vue`); not driven.

The gate has changed three times, so read it off the DOM at the start of any
symbol run:

```bash
./control-kiyotaka browser eval \
  "JSON.stringify({v2:document.querySelectorAll('[data-testid^=search-v2-category-]').length,legacy:document.querySelectorAll('[data-testid^=intent-filter-class-]').length})"
```

## Features

- [Chart boot and the data plane](./chart-boot-and-data-plane.md) — guest (the
  wake heal recipe needs the backend reachable for the wake's token refresh)
- [Indicators](./indicators.md) — guest (the official catalog needs a SEEDED
  stack, not a login: `/scripts/query` is unauthenticated, so the blocker is
  `node scripts/seed-official-catalog.mjs`, not the authed lane)
- [Symbol search and the ticker bar](./symbol-search-and-ticker-bar.md) — guest
- [Script editor and kScript](./script-editor-and-kscript.md) — guest (authed for protected/wrun)
- [Watchlist](./watchlist.md) — guest proves the wall ONLY; every sub-feature
  behind it is unverified because this stack cannot be signed into by an agent
- [Voice control](./voice-control.md) — NOT guest-reachable: the `voice-control`
  flag graduated to `isSignedInSession()`, so the override is dead and a guest
  lane has no mic, chip or seam at all

## Surface inventory

Discovered 2026-10-26 from kiyotaka-frontend source on product tree `fcc8e53b12`
(`origin/main`). The rows come from the router (`src/router/routes.ts`), the
Super Search providers, the 41 gate ids in
`src/constants/authFeatures.constants.ts` and the panel registry
(`src/constants/panels.constants.ts`), not from the guides. Gates were read from
those registries and a usage grep, not from each component; "gate not checked"
says so where nothing was found. "Live" names the run that last drove the
outcome. An `unmapped` row has no recipe yet and has never been driven by this
map. Most of them stop at a sign-in wall, and no agent can sign in on this stack
(see Baseline preconditions).

| User outcome | Product source path | Guide / sub-feature | Live verification | Prerequisite or gap |
|---|---|---|---|---|
| Chart opens and draws candles from the worker-owned feed | `src/pages/chart.vue`, `src/workers/worker-manager.ts`, `src/workers/services/websocket.worker.service.ts` | [boot](./chart-boot-and-data-plane.md) `boot-mount`, `boot-candles`, `boot-worker` | 2026-10-23, `2a1ed750db`, guest-JWT lane; the worker console grep last ran 2026-10-06 | none |
| Ticker shows live price, 24h volume, OI and funding | `src/services/live-feed.service.ts`, `src/components/TickerBar/TBMarketStats.vue` | [boot](./chart-boot-and-data-plane.md) `boot-live` | 2026-10-06; not re-run 2026-10-23 | OI and funding exist only on derivatives |
| A woken tab backfills the candles it missed | `src/composables/chart/useVisiblityChanges.ts`, `src/utility/chart/wake-resync-overlay-plan.util.ts` | [boot](./chart-boot-and-data-plane.md) `wake-heal` | live date not recorded in the guide | the wake's token refresh needs the backend reachable |
| Indicators dialog opens, searches and adds an overlay | `src/components/dialogs/IndicatorDialogV2.vue`, `src/store/chart.add-indicator.ts` | [indicators](./indicators.md) `ind-dialog`, `ind-add` | 2026-10-23, `2a1ed750db`, guest-JWT lane | none |
| The legend's settings, visibility and close controls work | `src/components/chart/ChartLegends.vue`, `src/store/chart.indicator-mgmt.ts` | [indicators](./indicators.md) `ind-legend` | 2026-10-23, `2a1ed750db` | none |
| Official indicators are listed | `src/services/indicator-catalog.service.ts`, `src/composables/chart/useIndicatorCatalogV2.ts` | [indicators](./indicators.md) `ind-catalog` | 2026-10-12, `1570b59d69`, desktop parity sweep; not re-run 2026-10-23 | a seeded catalog (`node scripts/seed-official-catalog.mjs`) |
| The indicators-per-chart cap holds | `src/store/chart.add-indicator.ts`, `packages/wrun-chart-host/src/constants/feature-limits.constants.ts` | [indicators](./indicators.md) `ind-limit` | 2026-10-23, `2a1ed750db` | the cap is per tier (free 3, plus 10), so a guest lane proves only the free cap |
| Symbol search finds and switches a market; scope chips filter | `src/components/symbolSelection/SymbolSelectionDialog.vue`, `src/components/symbolSearchV2/ScopeChips.vue` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-search`, `sym-scope` | 2026-10-23, `2a1ed750db`; the ETHUSDT reload stayed at zero candles with the backend down | none |
| Memecoin lane, liquidity floor and Pulse rows | `src/components/symbolSelection/component/MemecoinRow.vue`, `src/components/symbolSearchV2/RefineControls.vue`, `src/components/pulse/PulseRow.vue` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-memecoins` | live verification pending | a signed-in session (the `memecoins` tab and Pulse need it) |
| Interval, chart type and layout pickers re-drive the chart | `src/components/TickerBar/TBIntervalSelector.vue`, `src/components/TickerBar/TBChartTypeSelector.vue`, `src/components/TickerBar/TBLayoutPicker.vue` | [ticker bar](./symbol-search-and-ticker-bar.md) `tb-interval`, `tb-plot`, `tb-layout` | 2026-10-23, `2a1ed750db` (interval, Heikin Ashi) | the 4x4 free-tier grids need a signed-in session |
| Pickers peek on hover; the bar folds into an overflow menu | `src/components/TickerBar/tb-popover-open.util.ts`, `src/composables/chart/useTickerBarFoldedControl.ts` | [ticker bar](./symbol-search-and-ticker-bar.md) `tb-hover`, `tb-more` | not driven 2026-10-23; live date not recorded in the guide | the overflow menu needs a viewport narrow enough to fold the bar |
| The right-hand cluster toggles its drawers | `src/components/TickerBar/TBPanelToggle.vue`, `src/components/TickerBar/TBPanelsMenu.vue` | [ticker bar](./symbol-search-and-ticker-bar.md) `tb-bar-toggles` | 2026-10-23, `2a1ed750db` (the pinned set) | several drawers raise the sign-in wall for a guest |
| The script editor drawer opens | `src/components/scriptEditor/shell/EditorDrawer.vue`, `src/components/TickerBar/TBEditorToggle.vue` | [editor](./script-editor-and-kscript.md) `ks-open` | 2026-10-23, `2a1ed750db`, through Super Search on a guest lane | the ticker-bar toggle raises the sign-in wall for a guest |
| An own kScript runs, or reports its lint error | `src/store/script.ts`, `src/workers/kscript-engine.worker.ts`, `src/workers/scriptEditor/editor-analysis.worker.ts` | [editor](./script-editor-and-kscript.md) `ks-run`, `ks-lint` | live verification pending | a signed-in session; no agent can sign in on this stack |
| A protected or WRUN script returns from the hosted lane | `src/services/protected-kscript-cache.service.ts`, `src/workers/services/kscript-ws.worker.service.ts` | [editor](./script-editor-and-kscript.md) `ks-protected` | live verification pending | a signed-in session |
| WRUN launch box and Pine conversion create a draft | `src/components/wrun/launch/KataPineBox.vue`, `src/components/scriptEditor/shell/PineConvertDialog.vue` | [editor](./script-editor-and-kscript.md) `ks-wrun-launch` | live verification pending | a signed-in session and the entitlement |
| Watchlist panel opens; a guest gets the sign-in wall | `src/components/watchlist/Watchlist.vue`, `src/components/TickerBar/TBPanelToggle.vue` | [watchlist](./watchlist.md) `wl-open` | 2026-10-23, `2a1ed750db`, the three doors and the wall only | none for the wall |
| Lists are picked, added to, pruned, reordered, imported and capped | `src/components/watchlist/WatchlistListMenu.vue`, `src/store/watchlist.ts`, `src/composables/watchlist/useWatchlistImport.ts`, `src/constants/watchlist-limits.constants.ts` | [watchlist](./watchlist.md) `wl-lists` to `wl-limits` | live verification pending | a signed-in session |
| A spoken command changes symbol, interval and indicators | `src/components/voiceControl/VoiceControlNavButton.vue`, `src/utility/voice-control/voice-control-gate.util.ts`, `src/utility/voice-control/voice-grammar.util.ts` | [voice](./voice-control.md) `vc-*` | 2026-10-12, `7347b94e69`, through the rig seam with the flag forced; unreachable on a guest lane since the flag graduated | a signed-in session; the microphone path was never driven |
| Sign in, sign up, code request with Turnstile, reset and verify | `src/pages/auth/auth.page.vue` | unmapped | live verification pending | no agent-readable sign-in code on this stack; Turnstile fails under Playwright |
| Guest sign-in wall and feature-aware signup prompt | `src/components/dialogs/LoginSignupDialog.vue`, `src/store/guest-prompt.ts` | unmapped (each guide proves its own wall) | live verification pending | none for a guest lane |
| Delete and restore account | `src/pages/DeleteAccount.vue`, `src/components/dialogs/RestoreAccountDialog.vue` | unmapped | live verification pending | a signed-in throwaway account |
| Settings dialog: profile, security, appearance, language, timezone, trade and workspace settings | `src/components/dialogs/SettingsPagesDialog.vue` | unmapped | live verification pending | `ACCOUNT_SETTINGS` wall; 2FA needs `TWO_FACTOR` |
| Keyboard shortcuts | `src/components/dialogs/KeyboardShortcutsDialog.vue`, `src/store/keybinding.ts` | unmapped | live verification pending | none known |
| Release notes and announcements | `src/components/dialogs/ReleaseNotesDialog.vue`, `src/store/announcements.ts` | unmapped | live verification pending | none known |
| Guided tour | `src/components/tour/GuidedTour.vue` | unmapped | live verification pending | gate not checked |
| Themes and light mode | `src/composables/superSearch/providers/themes.ts`, `src/store/my-themes.ts` | unmapped | live verification pending | light mode raises `LIGHT_MODE` for a guest |
| Referrals | `src/pages/settings/Referral.vue` | unmapped | live verification pending | `REFERRALS` wall |
| Support center and contact | `src/components/dialogs/ReachOutPopoverContent.vue`, `src/components/dialogs/SupportInboxDialog.vue` | unmapped | live verification pending | `SUPPORT_CENTER` wall |
| Plus subscription, upgrade, trial and payment status | `src/pages/console/ConsoleSubscription.vue`, `src/components/dialogs/UpgradeDialog.vue`, `src/pages/PaymentStatus.vue` | unmapped | live verification pending | signed-in; `BILLING`; flags `free-trial`, `prepaid-plus-cn`, `plus-usdc-autopay` |
| Developer console: plans, API keys, agents, usage | `src/pages/console/ConsoleLayout.vue` | unmapped | live verification pending | signed-in; `API_KEY`; flag `api-console` |
| Connect an AI agent | `src/components/dialogs/ConnectAgentDialog.vue`, `src/components/footer/FooterAgents.vue` | unmapped | live verification pending | `AGENTS`; flag `agents-surface` |
| Alerts: create, list, history and delivery | `src/components/alert/AlertSidebar.vue`, `src/components/alert/AddAlertMenu.vue` | unmapped | live verification pending | `ALERT` wall; OPRA alerts need flag `opra-alerts` |
| Notifications panel | `src/components/GlobalNav/NotificationPanel.vue` | unmapped | live verification pending | `NOTIFICATION` wall |
| Drawing tools and the floating toolbar | `src/components/toolsSidebar/ToolsSidebar.vue`, `src/components/toolsSidebar/FloatingToolbar.vue` | unmapped | live verification pending | favorites need `FAVORITES`; flag `tools-delta` |
| Object tree | `src/components/objects/ObjectsLayout.vue` | unmapped | live verification pending | the panel's guest wall is `TERMINAL` |
| Replay | `src/components/replay/ReplayOverlay.vue`, `src/composables/chart/useReplayToggle.ts` | unmapped | live verification pending | tier budget in `useReplayToggle` |
| Compare mode and formula charts | `src/composables/superSearch/providers/formulas.ts` | unmapped | live verification pending | none known |
| Multi-chart grid and monitors | `src/composables/chart/useMonitorPicker.ts` | unmapped (the picker is `tb-layout`) | live verification pending | `MULTI_CHART`, `MONITOR` walls |
| Workspace tabs: new, rename, duplicate, delete, import, share | `src/components/GlobalNav/workspace-tabs/WorkspaceTabStrip.vue` | unmapped | live verification pending | `WORKSPACE` wall; mutates an autosaving workspace |
| Layouts library and community publish | `src/components/dialogs/LayoutsDialog.vue`, `src/components/dialogs/LayoutPublishDialog.vue` | unmapped | live verification pending | `LAYOUTS` wall |
| Right-side panel grid and panel picker | `src/components/panels/RightSideGrid.vue`, `src/constants/panels.constants.ts` | unmapped (the toggles are `tb-bar-toggles`) | live verification pending | each panel's `available()` and `guestFeature` |
| Terminal: Scanner, Markets and Orderbook tabs | `src/constants/panels.constants.ts` | unmapped | live verification pending | `TERMINAL` wall; Markets and Orderbook need an eligible chart |
| Options panel: Levels, Flow, Volatility and Chain | `src/components/TickerBar/TBOptionsButton.vue`, `src/utility/options/options-panel-gate.util.ts` | unmapped | live verification pending | flag `options-panel`; OPRA data needs flag `opra` |
| Option chain browser page | `src/pages/options/OptionsChainPage.vue` | unmapped | live verification pending | signed-in route |
| Options flow tape | `src/components/options/OptionsFlowTape.vue` | unmapped | live verification pending | offered only when the chart has a chain |
| ETF screener | `src/components/etf-screener/EtfScreenerPanel.vue` | unmapped | live verification pending | gate not checked |
| OPRA and CME data purchase, registration and terms | `src/components/options/CmeTermsDoor.vue`, `src/components/options/OpraRegistrationDoor.vue` | unmapped | live verification pending | `BILLING`; flag `opra`; a purchase |
| Orderbook ladder, DOM, delta and heatmap | `src/components/orderbook/Orderbook.vue`, `src/composables/chart/useHeatmapToggle.ts` | unmapped | live verification pending | `ORDERBOOK`, `ORDERBOOK_DELTA`, `ORDERBOOK_HEATMAP` walls |
| Tape mode and the 1s interval | `src/composables/chart/useTapeMode.ts` | unmapped | live verification pending | `ONE_SECOND_INTERVAL`; `TAPE_MODE` on mobile |
| Footprint and TPO | `src/composables/chart/chartTypePick.ts`, `src/components/dialogs/TimePriceOpportunityDialog.vue` | unmapped | live verification pending | `VOLUME_FOOTPRINT`, `TIME_PRICE_OPPORTUNITY` walls |
| Trades and liquidations; market, volume and liquidity stats | `src/components/tradingVolume/Stats.vue` | unmapped | live verification pending | `TRADE_LIQUIDATIONS` wall |
| News feed and synoptic streams | `src/components/topic-feed/TopicFeedPanel.vue` | unmapped | live verification pending | `NEWS`; flags `feeds`, `synoptic-streams` |
| Market events, earnings calendar and the chart event lane | `src/components/earnings/EarningsPanel.vue`, `src/components/chart/ChartEventLane.vue` | unmapped | live verification pending | a signed-in session |
| Tweet callers bar | `src/components/tweet-callers/TweetCallerBar.vue` | unmapped | live verification pending | `TWEET_CALLERS` wall |
| Journal | `src/components/journal/JournalLayout.vue` | unmapped | live verification pending | gate not checked |
| Hyperliquid account dock, trade rail and order ticket | `src/components/hyperliquid/trade/HLTradeTicketPanel.vue`, `src/components/hyperliquid/account-panel/HLAccountDock.vue` | unmapped (the desktop map covers the shell's wallet handoff) | live verification pending | flag `ems-hyperliquid`; a funded testnet wallet |
| Trading hub, CEX connect and paper trading | `src/components/trading-hub/TradingHubDialog.vue`, `src/components/dialogs/CexConnectDialog.vue` | unmapped | live verification pending | flags `trading-hub`, `paper-trading`, `robinhood-trading` |
| Pulse board, token overview and onchain swap | `src/pages/pulse/PulsePage.vue`, `src/components/tokenOverview/TokenOverviewPanel.vue` | unmapped | live verification pending | a signed-in session |
| Marketplace store, purchases and seller hub | `src/components/marketplace/MarketplaceStoreLayout.vue` | unmapped | live verification pending | signed-in route |
| Sharing hub and the My access page | `src/components/sharing/SharingHost.vue`, `src/pages/MyAccessPage.vue` | unmapped | live verification pending | flags `sharing-hub`, `my-access`; signed-in route |
| Kata AI assistant | `src/components/kata/KataPanel.vue` | unmapped | live verification pending | `KATA` wall |
| Ask | `src/ask/execute/plan.ts` | unmapped | live verification pending | gate not checked beyond `ALERT` in the plan |
| Community chat and DMs | `src/components/chat/CommunityChat.vue` | unmapped | live verification pending | `COMMUNITY_CHAT` wall |
| Go live, streams and spectating | `src/components/collab/GoLiveButton.vue`, `src/pages/LiveStreams.vue` | unmapped | live verification pending | `GO_LIVE`, `FOLLOWING`; signed-in routes |
| Author profiles and people search | `src/pages/AuthorProfile.vue`, `src/composables/superSearch/providers/people.ts` | unmapped | live verification pending | `AUTHOR_PROFILE`; people search needs a signed-in session and flag `people-search` |
| Board (Academy) | `src/pages/academy/AcademyPage.vue` | unmapped | live verification pending | signed-in route; flag `om-board`, default off |
| Screenshot and chart-data export | `src/components/dialogs/ScreenshotDialog.vue`, `src/components/dialogs/ExportChartDataDialog.vue` | unmapped | live verification pending | `SCREENSHOT` wall |
| Simple mode, light charts and Layers | `src/composables/chart/useSimpleMode.ts`, `src/store/layers.ts` | unmapped | live verification pending | `SIMPLE_MODE`; flag `layers` |
| Strategy tester | `src/components/strategy-tester/StrategyTesterPanel.vue` | unmapped | live verification pending | gate not checked |
| CRYPTOCAP indices as the main series | `src/store/omSeries.ts`, `src/components/chart/OmSeriesHost.vue` | unmapped | live verification pending | gate not found |
| History cap and Manage history | `src/utility/chart/history-cap.util.ts`, `src/components/dialogs/ManageHistoryDialog.vue` | unmapped | live verification pending | `CHART_HISTORY` wall |
| Super Search palette | `src/composables/superSearch/useSuperSearch.ts` | unmapped (used as a door by `ks-open`) | live verification pending | per-provider gates |
| Beta invite and partner landings | `src/pages/BetaInvite.vue`, `src/pages/Partners.vue` | unmapped | live verification pending | an invite id; a partner referral |
| Script registry SSO handoff | `src/pages/RegistrySso.vue` | unmapped | live verification pending | a signed-in session |
| Desktop sign page | `src/pages/desktop/sign.page.vue` | [desktop map](../../verify-kiyotaka-desktop/features/browser-handoff-wallet.md) `sign-page` | 2026-10-12, `133c5af8ca`, in the desktop map | none |
