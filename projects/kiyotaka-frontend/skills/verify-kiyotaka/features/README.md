# kiyotaka-frontend verification map

The maintained source for verifying user-facing chart behavior. Read this index
before driving, then use the matching feature file as the recipe.

Maintenance pass: 2026-10-28 (nightly). Source read and live drive on the same
tree, `origin/main` `29c9cda0a2` (62 commits past the 2026-10-27 source read; it
installs again, `@orangecharts/trading-core@0.2.1` is published). Lane `18103`
in a detached worktree with the operator's `.env.local` linked in, a guest lane
with no JWT whose backend proxy is a remote dev box with a seeded catalog.
Driven: every guest-reachable sub-feature of the nine guides, the lone-bar wake
heal (first heal verdict since 2026-10-23), all 18 guest Panels rows, and the
new outcomes a guest can reach: Ask command rows in Super Search, the
chartless `?wrunRef=` package link, the Open Interest Profile `Display`
section, the shared interval-menu look and the symbol search's input-method
guard. Not driven: anything behind sign-in (no agent credentials), and voice,
which stays absent on a guest. Evidence (42 frames plus the wake ring, local,
`evidence check` passed):
`~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261028/r1/`.

## Baseline preconditions

- Launch the lane on its **assigned** port (`18097`–`18197`), bound to
  `127.0.0.1`: `./control-kiyotaka up`. Never pick a free port, never `8080`.
  `doctor` reporting `lane FOREIGN` means another checkout holds the default
  port — a neighbouring worktree's live lane, not residue. Do not reclaim it:
  take another slot with `KIYO_LANE_PORT`, and set `KIYO_SESSION` too so your
  browser commands cannot drive the neighbour's tab.
  Every later command in the run needs the same two variables exported.
- `./control-kiyotaka doctor` exits zero. The `chart-schema` line must read `ok`,
  or `not-aliased <version> (dev serves node_modules)` when there is no sibling
  `orange-shared` checkout, which is also fine.
- **The lane needs the operator's `.env.local`.** A new worktree has none, and
  the guest boot then gets `Backend error: unauthenticated` from the gateway and
  zero candles while `doctor` stays green. Link it in before `up` (see
  [chart boot](./chart-boot-and-data-plane.md) Gotchas). With it, `doctor`'s
  `backend :3000 DOWN` line is about `:3000` only; the lane talks to whatever
  `VITE_BACKEND_PROXY_TARGET` names.
- **Keep the tab visible.** A headless tab drifts to `visibilityState: hidden`
  mid-drive, which freezes rAF and runs the app's hidden path. Check
  `document.visibilityState` before each capture, and re-front with
  `./control-kiyotaka browser tab t1`.
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
- BOTH first-load overlays cleared: the once-per-device ink tutorial
  (`find testid ink-tutorial-close click`) and the signup modal. The order varies
  (2026-10-27: signup modal first, ink tutorial after it), so read the top
  overlay and dismiss what is there. They share the
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
  The union does not see an indicator's settings card either: since
  2026-10-28 it docks at the right of the chart as `[data-testid=settings-panel]`
  and the union reads `0` while it is open. Probe it by testid.
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
  stack's login form does not do password auth by default — it sends a
  **6-digit sign-in code by email**, which the harness cannot read. On 2026-10-27
  the form also offered `login-signup-use-password-btn` and a passkey, but no
  agent has credentials for either. So every "authed lane" claim in
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
mobile. Source-verified on `df3fdcb62e` (`isSearchV2` in
`src/components/symbolSelection/SymbolSelectionDialog.vue`) and driven
2026-10-27 on `7290d33d10` and 2026-10-28 on `29c9cda0a2`: a guest open read
`v2` 22, `legacy` 0 both times.

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
  backend, not a login: the operator's remote dev backend is seeded; a fresh
  local stack needs `node scripts/seed-official-catalog.mjs`)
- [Symbol search and the ticker bar](./symbol-search-and-ticker-bar.md) — guest
- [Script editor and kScript](./script-editor-and-kscript.md) — guest (authed for protected/wrun)
- [Watchlist](./watchlist.md) — guest proves the wall ONLY; every sub-feature
  behind it is unverified because this stack cannot be signed into by an agent
- [Voice control](./voice-control.md) — NOT guest-reachable: the `voice-control`
  flag graduated to `isSignedInSession()`, so the override is dead and a guest
  lane has no mic, chip or seam at all
- [Super Search and settings](./super-search-and-settings.md) — guest (Super
  Search, theme and formula rows, Keyboard Shortcuts, Release Notes, and the
  shared sign-in wall with its feature ids)
- [Right-side panels](./right-side-panels.md) — guest for Orderbook, Tape,
  Trades and Liquidations, the three stats panels, Journal, Alerts, Objects, the
  ETF screener and the heatmap popover; Options, alert creation and seven Panels
  rows stop at the wall
- [Drawing tools](./drawing-tools.md) — guest

## Surface inventory

Re-discovered 2026-10-28 from kiyotaka-frontend source on `origin/main`
`29c9cda0a2`; live column from the 2026-10-28 drive on the same tree unless a
row says otherwise. The rows come from the router (`src/router/routes.ts`, which
gained the `wrunRefRootLinkGuard`), the Super Search providers (new:
`askCommands`, `polymarket`), the 41 gate ids in
`src/constants/authFeatures.constants.ts` (unchanged since `fcc8e53b12`), the
panel registry (`src/constants/panels.constants.ts`) and the 62 commits in
`df3fdcb62e..29c9cda0a2`, not from the guides. Every source path was checked
with `git cat-file -e origin/main:<path>` at `29c9cda0a2`. Gates were read from
those registries and a usage grep, not from each component; "gate not checked"
says so where nothing was found. "Live" names the run that last drove the
outcome. An `unmapped` row has no recipe yet and has never been driven by this
map. Most of them stop at a sign-in wall, and no agent can sign in on this stack
(see Baseline preconditions).

| User outcome | Product source path | Guide / sub-feature | Live verification | Prerequisite or gap |
|---|---|---|---|---|
| Chart opens and draws candles from the worker-owned feed | `src/pages/chart.vue`, `src/workers/worker-manager.ts`, `src/workers/services/websocket.worker.service.ts` | [boot](./chart-boot-and-data-plane.md) `boot-mount`, `boot-candles`, `boot-worker` | 2026-10-28, `29c9cda0a2`, no-JWT guest lane, 250 bars in about 20 s, worker console grep clean | the operator's `.env.local` in the lane's tree |
| Ticker shows live price, 24h volume, OI and funding | `src/services/live-feed.service.ts`, `src/components/TickerBar/TBMarketStats.vue` | [boot](./chart-boot-and-data-plane.md) `boot-live` | 2026-10-28, `29c9cda0a2` (spot COINBASE BTC-USD and perp BINANCE.F ETHUSDT) | OI and funding exist only on derivatives; a tab that drifts `hidden` freezes the slots |
| A woken tab backfills the candles it missed | `src/composables/chart/useVisiblityChanges.ts`, `src/utility/chart/wake-resync-overlay-plan.util.ts` | [boot](./chart-boot-and-data-plane.md) `wake-heal` | 2026-10-28, `29c9cda0a2`, the lone-bar heal on 1m from a 414 s visibility override (5 blank slots to 0, `main-heal-commit` `row-width`) | the wake's token refresh needs the backend proxy reachable; a real sleep and the process-suspend lane not driven |
| Indicators dialog opens, searches and adds an overlay | `src/components/dialogs/IndicatorDialogV2.vue`, `src/store/chart.add-indicator.ts` | [indicators](./indicators.md) `ind-dialog`, `ind-add` | 2026-10-28, `29c9cda0a2`; a guest row Add walls on `indicators`, so the mount is programmatic | a dialog-path mount needs a signed-in session; a retired kScript row refuses with a toast (source) |
| The legend's settings, visibility and close controls work | `src/components/chart/ChartLegends.vue`, `src/store/chart.indicator-mgmt.ts` | [indicators](./indicators.md) `ind-legend` | 2026-10-28, `29c9cda0a2`; settings now dock as `settings-panel` | pin and window doors depend on the type (source) |
| Official indicators are listed | `src/services/indicator-catalog.service.ts`, `src/composables/chart/useIndicatorCatalogV2.ts` | [indicators](./indicators.md) `ind-catalog` | 2026-10-28, `29c9cda0a2`, seeded remote dev backend (`See all 241`) | a seeded backend; a fresh local stack needs `node scripts/seed-official-catalog.mjs`; the builtin seen marks (`e491d0feb9`) are a network side effect with no surface |
| The indicators-per-chart cap holds | `src/store/chart.add-indicator.ts`, `src/composables/chart/useSuiteApplication.ts`, `packages/wrun-chart-host/src/constants/feature-limits.constants.ts` | [indicators](./indicators.md) `ind-limit` | 2026-10-28, `29c9cda0a2`, display only (`2/3`) | the cap is per tier (free 3, plus 10), and enforcement runs only on the dialog path, which a guest cannot take |
| Symbol search finds and switches a market; scope chips filter | `src/components/symbolSelection/SymbolSelectionDialog.vue`, `src/components/symbolSearchV2/CategoryStrip.vue` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-search`, `sym-scope` | 2026-10-28, `29c9cda0a2`; ETHUSDT switch to 351 bars, Equities tab | none |
| A CRYPTOCAP index (BTC.D, TOTAL2 ...) is the main series | `src/utility/symbol-search-v2/crypto-index-search.util.ts`, `src/utility/chart/crypto-index-format.util.ts` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-cryptocap` | 2026-10-28, `29c9cda0a2`, BTC.D 250 bars | the alert gate and refusals in `docs/features/data/cryptocap-indices.md` are not driven |
| Memecoin lane, liquidity floor and Pulse rows | `src/components/symbolSelection/component/MemecoinRow.vue`, `src/components/symbolSearchV2/RefineControls.vue`, `src/components/pulse/PulseRow.vue` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-memecoins` | live verification pending | a signed-in session (the `memecoins` tab and Pulse need it) |
| Interval, chart type and layout pickers re-drive the chart | `src/components/TickerBar/TBIntervalSelector.vue`, `src/components/TickerBar/TBChartTypeSelector.vue`, `src/components/TickerBar/TBLayoutPicker.vue` | [ticker bar](./symbol-search-and-ticker-bar.md) `tb-interval`, `tb-plot`, `tb-layout` | 2026-10-28, `29c9cda0a2` (5m, the in-chart interval menu, Heikin Ashi, the `multi-chart` wall) | a multi-chart grid needs a signed-in session; the `ChartArea` interval menu not opened |
| Pickers peek on hover; the bar folds into the Panels menu | `src/components/TickerBar/TBChartTypeSelector.vue`, `src/composables/chart/useTickerBarFoldedControl.ts`, `src/composables/chart/useTickerBarFit.ts` | [ticker bar](./symbol-search-and-ticker-bar.md) `tb-hover`, `tb-more` | 2026-10-28, `29c9cda0a2` (chart-type and layout peeks; width-fold when a right panel opens) | there is no `⋯` button; a narrow viewport was not driven |
| The right-hand cluster toggles its panels | `src/components/TickerBar/TBPanelToggle.vue`, `src/components/TickerBar/TBPanelsMenu.vue` | [ticker bar](./symbol-search-and-ticker-bar.md) `tb-bar-toggles` | 2026-10-28, `29c9cda0a2` | Watchlist, News and Editor wall a guest |
| The script editor drawer opens | `src/components/scriptEditor/shell/EditorDrawer.vue`, `src/components/TickerBar/TBEditorToggle.vue` | [editor](./script-editor-and-kscript.md) `ks-open` | 2026-10-28, `29c9cda0a2`, through Super Search, read-only | the ticker-bar toggle and the Panels row raise the sign-in wall for a guest |
| An own kScript runs, or reports its lint error | `src/store/script.ts`, `src/workers/kscript-engine.worker.ts`, `src/workers/scriptEditor/editor-analysis.worker.ts` | [editor](./script-editor-and-kscript.md) `ks-run`, `ks-lint` | live verification pending | a signed-in session; no agent can sign in on this stack |
| A protected or WRUN script returns from the hosted lane | `src/services/protected-kscript-cache.service.ts`, `src/workers/services/kscript-ws.worker.service.ts` | [editor](./script-editor-and-kscript.md) `ks-protected` | live verification pending | a signed-in session |
| WRUN launch box and Pine conversion create a draft | `src/components/wrun/launch/KataPineBox.vue`, `src/components/scriptEditor/shell/PineConvertDialog.vue` | [editor](./script-editor-and-kscript.md) `ks-wrun-launch` | live verification pending | a signed-in session and the entitlement |
| OPRA data in user scripts | `packages/wrun-chart-host/src/utility/chart/opra-user-scripts-gate.util.ts`, `src/utility/chart/opra-user-scripts-gate.util.ts`, `src/utility/options/opra-user-scripts-rejudge.util.ts` | unmapped (a source note in [editor](./script-editor-and-kscript.md) Gotchas) | live verification pending | flag `opra-user-scripts` retired by `61f23cdf65`; a signed-in session plus the OPRA entitlement and tier |
| Watchlist panel opens; a guest gets the sign-in wall | `src/components/watchlist/Watchlist.vue`, `src/components/TickerBar/TBPanelToggle.vue` | [watchlist](./watchlist.md) `wl-open` | 2026-10-28, `29c9cda0a2`, the wall only, from the Panels row and `Alt+W` | none for the wall |
| Lists are picked, added to, pruned, reordered, imported and capped | `src/components/watchlist/WatchlistListMenu.vue`, `src/store/watchlist.ts`, `src/composables/watchlist/useWatchlistImport.ts`, `src/constants/watchlist-limits.constants.ts`, `src/ask/commands/rows/watchlist.ts` | [watchlist](./watchlist.md) `wl-lists` to `wl-limits`, `wl-ask-add` | live verification pending | a signed-in session |
| A spoken command changes symbol, interval and indicators | `src/components/voiceControl/VoiceControlNavButton.vue`, `src/utility/voice-control/voice-control-gate.util.ts`, `src/utility/voice-control/voice-grammar.util.ts`, `src/utility/voice-control/chart-target.util.ts` | [voice](./voice-control.md) `vc-*` | 2026-10-12, `7347b94e69`, through the rig seam with the flag forced; absence on a guest re-confirmed 2026-10-28 | a signed-in session; the microphone and multi-chart targeting were never driven |
| Super Search palette opens and runs rows | `src/composables/superSearch/useSuperSearch.ts`, `src/components/GlobalNav/NavSearchField.vue` | [Super Search](./super-search-and-settings.md) `ss-open` | 2026-10-28, `29c9cda0a2` | per-provider gates; `Mod+J` not driven; the Options panel's new names find nothing for a guest |
| Themes: dark and light; Gray and Cream appearance | `src/composables/superSearch/providers/themes.ts`, `src/utility/theme/appearance-modes-flag.util.ts` | [Super Search](./super-search-and-settings.md) `ss-theme` | 2026-10-28, `29c9cda0a2`, dark and light | Gray and Cream need the desktop shell and raise `LIGHT_MODE` for a guest |
| Compare mode and formula charts | `src/composables/superSearch/providers/formulas.ts`, `src/utility/symbol-selection/plot-typed-formula.util.ts` | [Super Search](./super-search-and-settings.md) `ss-formula` | 2026-10-28, `29c9cda0a2`, SPY / GLD (252 bars) | the compare overlay path not driven |
| Keyboard shortcuts | `src/pages/settings/KeyboardShortcuts.vue`, `src/components/dialogs/SettingsPagesDialog.vue` | [Super Search](./super-search-and-settings.md) `set-shortcuts` | 2026-10-28, `29c9cda0a2` | none |
| Release notes | `src/pages/settings/ReleaseNotes.vue` | [Super Search](./super-search-and-settings.md) `set-notes` | 2026-10-28, `29c9cda0a2`, 81 versions | announcements are not rendered (`src/store/announcements.ts`) |
| Guest sign-in wall and feature-aware signup prompt | `src/components/dialogs/LoginSignupDialog.vue`, `src/store/dialog.ts`, `src/store/guest-prompt.ts` | [Super Search](./super-search-and-settings.md) `guest-wall` | 2026-10-28, `29c9cda0a2`, fifteen doors | none for a guest lane |
| Sign in, sign up, code request with Turnstile, reset and verify | `src/pages/auth/auth.page.vue` | unmapped | live verification pending | no agent-readable sign-in code or password; Turnstile fails under Playwright |
| First-run onboarding: look and ask steps | `src/components/onboarding/FirstRunOnboarding.vue`, `src/components/onboarding/FirstRunLook.vue`, `src/components/onboarding/FirstRunAsk.vue` | unmapped | live verification pending | runs for a new account; a guest gets a light look (source) |
| Delete and restore account | `src/pages/DeleteAccount.vue`, `src/components/dialogs/RestoreAccountDialog.vue` | unmapped | live verification pending | a signed-in throwaway account |
| Settings dialog: profile, security, appearance, timezone, trade and workspace settings | `src/components/dialogs/SettingsPagesDialog.vue` | unmapped (the guest pages are `set-shortcuts`, `set-notes`) | live verification pending | `ACCOUNT_SETTINGS` wall; 2FA needs `TWO_FACTOR` |
| Guided tour | `src/components/tour/GuidedTour.vue`, `src/store/guidedTour.ts` | unmapped | live verification pending | excludes guests; the Super Search command needs a verified email |
| Referrals | `src/pages/settings/Referral.vue` | unmapped | live verification pending | `REFERRALS` wall |
| Support center and contact | `src/components/dialogs/ReachOutPopoverContent.vue`, `src/components/dialogs/SupportInboxDialog.vue` | unmapped | live verification pending | `SUPPORT_CENTER` wall |
| Plus subscription, upgrade, trial and payment status | `src/pages/console/ConsoleSubscription.vue`, `src/components/dialogs/UpgradeDialog.vue`, `src/pages/PaymentStatus.vue` | unmapped | live verification pending | signed-in; `BILLING`; flags `free-trial`, `prepaid-plus-cn`, `plus-usdc-autopay` |
| Developer console: plans, API keys, agents, usage | `src/pages/console/ConsoleLayout.vue` | unmapped | live verification pending | signed-in; `API_KEY`; flag `api-console` |
| Connect an AI agent | `src/components/dialogs/ConnectAgentDialog.vue`, `src/components/footer/FooterAgents.vue` | unmapped | live verification pending | `AGENTS`; flag `agents-surface` |
| Alerts panel opens; creating an alert | `src/components/alert/AlertSidebar.vue`, `src/components/alert/AddAlertMenu.vue` | [panels](./right-side-panels.md) `rp-alerts` | 2026-10-28, `29c9cda0a2`, the panel and the create wall | creating, listing and delivery need a signed-in session; OPRA alerts need flag `opra-alerts` (not re-verified) |
| Notifications panel | `src/components/GlobalNav/NotificationPanel.vue` | unmapped | live verification pending | `NOTIFICATION` wall |
| Drawing tools and the floating toolbar | `src/components/toolsSidebar/ToolsSidebar.vue`, `src/components/toolsSidebar/FloatingToolbar.vue` | [drawing tools](./drawing-tools.md) `dt-*` | 2026-10-28, `29c9cda0a2`, trend line only | favorites need `FAVORITES`; drawing sync (`drawings-sync:<scope>`) not driven |
| Object tree | `src/components/objects/ObjectsLayout.vue` | [panels](./right-side-panels.md) `rp-objects` | 2026-10-28, `29c9cda0a2`, opens with no wall | none |
| Replay | `src/components/replay/ReplayOverlay.vue`, `src/composables/chart/useReplayToggle.ts` | [panels](./right-side-panels.md) `rp-walled` (the wall only) | 2026-10-28, `29c9cda0a2`, the Panels row raises the `chart-actions` wall | a signed-in session, then the tier budget in `useReplayToggle` |
| Multi-chart grid, monitors and Trinity layouts | `src/composables/chart/useMonitorPicker.ts`, `src/components/chart/TrinityBar.vue` | unmapped (the picker is `tb-layout`) | live verification pending | `MULTI_CHART`, `MONITOR` walls; Trinity is a Super Search command |
| Workspace tabs: new, rename, duplicate, delete, import, share | `src/components/GlobalNav/workspace-tabs/WorkspaceTabStrip.vue` | unmapped | live verification pending | `WORKSPACE` wall; mutates an autosaving workspace |
| Layouts library and community publish | `src/components/dialogs/LayoutsDialog.vue`, `src/components/dialogs/LayoutPublishDialog.vue` | unmapped | live verification pending | `LAYOUTS` wall |
| Right-side panel grid and panel picker | `src/components/panels/RightSideGrid.vue`, `src/constants/panels.constants.ts` | [panels](./right-side-panels.md) (the toggles are `tb-bar-toggles`) | 2026-10-28, `29c9cda0a2`, all 18 guest rows | signed-in content of each panel |
| Scanner and Markets panels (the old Terminal tabs; the Terminal toggle is retired) | `src/constants/panels.constants.ts` | [panels](./right-side-panels.md) `rp-walled` (Scanner's wall only) | 2026-10-28, `29c9cda0a2`, Scanner raises the `terminal` wall | a signed-in session; Markets is not offered to a guest and needs an eligible chart |
| Orderbook ladder, DOM, delta and heatmap | `src/components/orderbook/Orderbook.vue`, `src/composables/chart/useHeatmapToggle.ts` | [panels](./right-side-panels.md) `rp-orderbook`, `rp-heatmap` | 2026-10-28, `29c9cda0a2`, live book levels and imbalance; the heatmap switch walls | `ORDERBOOK_DELTA`, `ORDERBOOK_HEATMAP` walls; the CME first-paint seed (`795ed05bfe`) not driven |
| Options panel: Levels, Flow, Volatility and Chain; Options Heatmap | `src/components/TickerBar/TBOptionsButton.vue`, `src/utility/options/options-panel-gate.util.ts`, `src/indicators/controls/options-heatmap/data-source.ts`, `src/composables/superSearch/providers/panels.ts` | [panels](./right-side-panels.md) `rp-options` | 2026-10-28, `29c9cda0a2`, the button's `terminal` wall; its Super Search names list nothing for a guest | a signed-in session; flag `options-panel`; OPRA data needs flag `opra` |
| Option chain browser page | `src/pages/options/OptionsChainPage.vue` | unmapped | live verification pending | signed-in route |
| Options flow tape | `src/components/options/OptionsFlowTape.vue` | unmapped | live verification pending | a launch needs a resolved chain (`launchable`) |
| ETF screener | `src/components/etf-screener/EtfScreenerPanel.vue` | [panels](./right-side-panels.md) `rp-etf` | 2026-10-28, `29c9cda0a2`, opens with no wall; 0 rows | the dev backend's ETF universe was empty again; saving a screen needs an account |
| OPRA and CME data purchase, registration and terms | `src/components/options/CmeTermsDoor.vue`, `src/components/options/OpraDelayDoor.vue`, `src/components/options/OpraRealtimeCard.vue`, `src/components/dialogs/market-data/MarketDataPurchaseFlow.vue` | unmapped | live verification pending | `BILLING`; flag `opra`; a purchase |
| Tape mode and the 1s interval | `src/composables/chart/useTapeMode.ts` | unmapped | live verification pending | `ONE_SECOND_INTERVAL`; `TAPE_MODE` on mobile |
| Footprint and TPO, including the TPO outline display mode | `src/composables/chart/chartTypePick.ts`, `src/components/dialogs/TimePriceOpportunityDialog.vue`, `src/indicators/controls/tpoSettingsTabs.ts` | unmapped (the Footprint panel's wall is `rp-walled`) | live verification pending | `VOLUME_FOOTPRINT` (the Panels row raised it 2026-10-28), `TIME_PRICE_OPPORTUNITY` walls |
| Trades and liquidations; market, volume and liquidity stats | `src/components/tradeAndLiquidations/TradeAndLiquidations.vue`, `src/components/tradingVolume/Stats.vue` | [panels](./right-side-panels.md) `rp-tape`, `rp-stats` | 2026-10-28, `29c9cda0a2`, every panel opens with no wall; Liquidity Stats drew data | no Tape or Trades and Liquidations prints arrived within 20 s; the Panels row does not raise `TRADE_LIQUIDATIONS` |
| News feed and synoptic streams | `src/components/topic-feed/TopicFeedPanel.vue` | unmapped (the wall is `rp-walled`) | live verification pending | `NEWS` wall (driven 2026-10-28); flags `feeds`, `synoptic-streams` |
| Market events, earnings calendar and the chart event lane | `src/components/earnings/EarningsPanel.vue`, `src/components/chart/ChartEventLane.vue` | unmapped | live verification pending | a signed-in session |
| Tweet callers bar | `src/components/tweet-callers/TweetCallerBar.vue` | unmapped | live verification pending | `TWEET_CALLERS` wall |
| Journal | `src/components/journal/JournalLayout.vue` | [panels](./right-side-panels.md) `rp-journal` | 2026-10-28, `29c9cda0a2`, opens with no wall | writes are gated on a guest session (source); entries need an account |
| Hyperliquid account dock, trade rail and order ticket | `src/components/hyperliquid/trade/HLTradeTicketPanel.vue`, `src/components/hyperliquid/account-panel/HLAccountDock.vue`, `src/components/trading-hub/AccountMenu.vue` | unmapped (the desktop map covers the shell's wallet handoff) | live verification pending | flag `ems-hyperliquid`; a funded testnet wallet; the account menu now reaches HIP-3 (`40a1989b6e`) and is signed-in only |
| Trading hub, CEX connect, paper trading and new venues | `src/components/trading-hub/TradingHubDialog.vue`, `src/components/dialogs/CexConnectDialog.vue`, `src/components/cex/link/` | unmapped | live verification pending | flags `trading-hub`, `paper-trading`, `robinhood-trading`, `lighter-execution`, `variational-markets` |
| Trading Volume page | `src/components/trading-hub/VolumePage.vue`, `src/composables/tradingVolume/useTradingVolume.ts` | unmapped | live verification pending | flag `TradingVolume` (dark in production) |
| Pulse board, token overview and onchain swap | `src/pages/pulse/PulsePage.vue`, `src/components/tokenOverview/TokenOverviewPanel.vue` | unmapped | live verification pending | a signed-in session |
| Marketplace store, purchases and seller hub | `src/components/marketplace/MarketplaceStoreLayout.vue` | unmapped | live verification pending | signed-in route |
| Sharing hub and the My access page | `src/components/sharing/SharingHost.vue`, `src/pages/MyAccessPage.vue` | unmapped | live verification pending | flags `sharing-hub`, `my-access`; signed-in route |
| Kata AI assistant | `src/components/kata/KataPanel.vue` | unmapped | live verification pending | `KATA` wall |
| Ask: plan cards and apply | `src/ask/execute/plan.ts`, `src/composables/superSearch/useSuperSearch.ts` | unmapped | live verification pending | a signed-in session (a guest gets no plan card, driven 2026-10-28); zoom-reset and go-to-date are Ask-only verbs (`e973f00e50`) |
| Community chat and DMs | `src/components/chat/CommunityChat.vue` | unmapped (the wall is `rp-walled`) | live verification pending | `COMMUNITY_CHAT` wall (driven 2026-10-28) |
| Go live, streams and spectating | `src/components/collab/GoLiveButton.vue`, `src/pages/LiveStreams.vue` | unmapped | live verification pending | `GO_LIVE`, `FOLLOWING`; signed-in routes |
| Author profiles and people search | `src/pages/AuthorProfile.vue`, `src/composables/superSearch/providers/people.ts` | unmapped | live verification pending | `AUTHOR_PROFILE`; people search needs a signed-in session and flag `people-search` |
| Board (Academy) | `src/pages/academy/AcademyPage.vue` | unmapped | live verification pending | signed-in route; flag `om-board`, default off |
| Chart clips: record a voiced clip, post it to the Board, replay it | `src/components/clips/ClipRecordButton.vue`, `src/clips/recorder/useClipRecorder.ts`, `src/components/academy/AcademyAttachmentCard.vue`, `src/composables/academy/useChartClipsFlag.ts` | unmapped | live verification pending | flags `om-board` AND `chart-clips` (`02c3fa9c01`) and a server flag; signed-in; no clip button for a guest (2026-10-28) |
| Screenshot and chart-data export; symbol watermark | `src/components/dialogs/ScreenshotDialog.vue`, `src/components/dialogs/ExportChartDataDialog.vue`, `src/components/chart/SymbolWatermarkHost.vue` | unmapped (the guest wall is `guest-wall`) | live verification pending | `SCREENSHOT` wall (driven 2026-10-28); charts carrying OPRA data can now be captured (`33059c5200`) |
| Simple mode, light charts and Layers | `src/composables/chart/useSimpleMode.ts`, `src/store/layers.ts` | unmapped | live verification pending | `SIMPLE_MODE`; flag `layers` |
| Strategy tester | `src/components/strategy-tester/StrategyTesterPanel.vue` | unmapped | live verification pending | gate not checked |
| History cap and Manage history | `src/utility/chart/history-cap.util.ts`, `src/components/dialogs/ManageHistoryDialog.vue` | unmapped | live verification pending | `CHART_HISTORY` wall |
| Beta invite and partner landings | `src/pages/BetaInvite.vue`, `src/pages/Partners.vue` | unmapped | live verification pending | an invite id; a partner referral |
| Script registry SSO handoff | `src/pages/RegistrySso.vue` | unmapped | live verification pending | a signed-in session |
| App commands as Super Search rows (hide candles, swap candle colours ...) | `src/composables/superSearch/providers/askCommands.ts`, `src/ask/commands/catalog.ts`, `src/ask/commands/rows/chart.ts` | [Super Search](./super-search-and-settings.md) `ss-ask-commands` | 2026-10-28, `29c9cda0a2`, `candles-visible:off` then `:on` for a guest | each row's own `available()`; `alert lines` lists nothing for a guest |
| Package share links: `?indicator=` and a chartless `?wrunRef=` | `src/router/guards/wrun-ref-root-link.guard.ts`, `src/utility/sharing/indicator-share-link.util.ts` | [indicators](./indicators.md) `ind-share-link` | 2026-10-28, `29c9cda0a2`, a guest meets the `indicators` wall with the package stashed | the dialog opening on the package needs a signed-in session |
| Open Interest Profile Net and Split display modes | `src/indicators/controls/MetricProfileSettings.vue`, `src/utility/chart/metric-profile.util.ts` | [indicators](./indicators.md) `ind-legend` | 2026-10-28, `29c9cda0a2`, the `Display mode` field (`Net`) on a programmatic mount | `Split` not opened; a dialog-path add needs a signed-in session |
| The symbol search leaves an input-method composition alone | `src/utility/dom/ime-composition.util.ts`, `src/components/symbolSelection/SymbolSelectionDialog.vue` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-ime` | 2026-10-28, `29c9cda0a2`, synthetic composition events | a real input method not driven; a composing `Escape` closes the dialog (`src/components/common/Dialog.vue`), a product gap |
| Built-in options indicators open as window cells | `packages/wrun-chart-host/src/utility/chart/window-owner.leaf.ts`, `src/composables/chart/useIndicatorMenu.ts` | unmapped (a source note in [indicators](./indicators.md) Gotchas) | live verification pending | options data needs a signed-in session |
| Saved chart themes: delete from the theme row with Undo | `src/components/dialogs/ChartThemeRow.vue`, `src/store/my-themes.ts` | unmapped | live verification pending | a saved theme, probably account-only (source not read far enough) |
| Trade prediction markets through a Polymarket lane | `src/composables/superSearch/providers/polymarket.ts`, `src/components/dialogs/PolymarketConnectDialog.vue`, `src/components/polymarket/trade/PredictionTicketPanel.vue`, `src/components/polymarket/account/PredictionAccountPanel.vue`, `src/utility/polymarket/pm-venue-flag.util.ts` | unmapped | live verification pending; absent for a guest (no `Link Polymarket` row, 2026-10-28) | flag `polymarket-execution` and a signed-in session; a linked Polymarket account |
| "What should we build next" feedback banner | `src/components/banners/BuildNextBanner.vue`, `src/utility/feedback/prompted-question-schedule.util.ts` | unmapped | live verification pending; absent for a guest (2026-10-28) | a signed-in account past its signup day, then the prompt schedule |
| Desktop sign page | `src/pages/desktop/sign.page.vue` | [desktop map](../../verify-kiyotaka-desktop/features/browser-handoff-wallet.md) `sign-page` | 2026-10-12, `133c5af8ca`, in the desktop map | none |
| Desktop browser sign-in and checkout returns | `src/pages/desktop/signin.page.vue`, `src/pages/desktop/return.page.vue`, `src/pages/desktop/checkout-return.page.vue` | unmapped (belongs with the desktop map) | live verification pending | the desktop shell |
