# Parity sweep

The sweep replays the `verify-kiyotaka` recipes in the packaged dev build and in Playwright's headless Chromium on one
dev lane, captures both hosts together at 1440 by 900, and diffs each pair with masks over live data. A pair fails when
more than 0.5 percent of its unmasked pixels differ, when its masks cover more than a quarter of the frame, or when its
plot region is blank in either capture; a step also fails when the hosts disagree on its state. It has a guest phase (26
steps plus the `login-wall` pair) and a signed-in phase (about 70 `si-*` steps plus `si-oauth-<provider>`; `ad67d47c62`,
on 2026-11-02's tree, retired `si-panel-trades-liquidations` and renamed the `panel-tape` inventory row "Tape /
Footprint panel", since one tape now serves every market, and left the guest steps alone) that signs in as the
operator's real account on the deployed chart. Last driven 2026-11-12 on tree `74ccd3cdcc` (`origin/main`;
`parity.mjs` unchanged, and no testid it reads went dead since `c2c02b7b42`), guest steps named, with the console session
unlocked, at a load average of 4 to 15, on a lane with candles (250 bars, `nc -z` to the v2 host before and after), in
8 min 33 s with its pack: the same 0 green, 6 blocked and 21 findings, from the same Escape cascade from `ind-search` on
and the Lite charts toast (completed pairs 1.75 to 2.71 percent apart; `boot-candles` 2.45). Two things changed.
`ind-catalog` now fails `officialListed` and `kindNarrows` in both hosts: `all` read 0 where it read 181 on 2026-11-10,
while the narrowed Official list still counted 26 oscillators; `parity-mac-ind-dialog-*.png` shows the Official shelf
still drawing its skeleton cards, so the step read `indicator-store-see-all-official-btn` before the shelf's count
arrived. That is both hosts, so it is the web tree or the step's timing, not the shell; the cause is not isolated
(`49d3816c92`, which cuts repeat registry and panel requests, is the candidate in the range). And `login-wall` wrote its
shell capture on the unlocked console (`captured` and `loadedLane` true, `73,635.4 ▲ BTC-USD`), so its pair ran
(2.71 percent, the toast again). The browser host was Playwright's `chromium_headless_shell-1234`, which a
`playwright install` from `desktop/` (Playwright 1.64) had removed from the shared cache as unregistered; a sweep needs
that build present. Before that, driven 2026-11-10 on tree `c2c02b7b42` (`origin/main`, `parity.mjs`
unchanged since `30481b57f8`), guest steps named, with the console session locked, at a load average of 4 to 7, on a lane with
candles (250 bars, `nc -z` to the v2 host before), in 9 min 48 s with its pack: the same 0 green, 6 blocked and 21 findings as on
2026-11-09, from the same two causes below. `ind-search` again failed its restore ("timed out waiting for indicator-panel-v2
to close") in both hosts and every chart step from `sym-dialog` on timed out behind it; the completed pairs differed by
1.8 to 2.9 percent (`boot-candles` 2.449, `ind-dialog` 2.887), and `parity-mac-boot-candles-browser.png` again shows the
Lite charts toast, now with its caption "Smoother panning on this computer, same charts.", and the legend bolt.
`46208d6a31`'s Favorites tab in the Indicators dialog moved no testid the sweep reads, and `21126deb8b` removed only the
"Panning choppy?" ask, not the weak-class toast. Before that, on 2026-11-09 on tree `27fb2d4621`, guest steps named, with the console session locked, at a load average of 15 to 19, on a lane with candles (250 bars), in 10 min 21 s with its pack: 0 green, 6 blocked and 21
findings, against 10, 6 and 11 on 2026-11-08, and it is the web tree, not the shell. Two causes are read from the run. First, `ee1fae1b4d` (one search field across the app, after `537639ebca`): the first Escape in the Indicators
search box only clears its words (`src/components/common/SearchField.vue:183`), so `ind-search`'s one `pressEscape` (`parity.mjs:605`) leaves the dialog open in both hosts (restore failed, "timed out waiting for indicator-panel-v2 to close"), and every later
chart step times out behind it, from `sym-dialog` on. Second, `b62ef4c998`'s Lite charts default: Playwright's headless Chromium took Lite charts on (its frames show it; the class was not read, and a software GPU fits `classReason`) and shows the staying toast "Lite charts is on." with Keep and Turn off (`src/utility/chart/lite/lite-hint.ts` `autoOnForWeakClass`, `timeout: 0`), plus a bolt in the legend, and the shell does neither on this machine, so every completed pair differs by about 2.4 to 2.9 percent (the toast's area), against 0.02 to 0.46 percent before. In `parity-mac-boot-candles-browser.png` the toast is visible and in the shell frame it is not. A scratch drive in the real shell the same night confirmed the Escape rule: after typing RSI, the first Escape left the dialog open with the words gone, and the second closed it. `sym-switch` timed out behind the open dialog, so the "Draw by holding" tip's own cascade could not show. `login-wall`'s shell half again wrote no capture (locked console). Before that, on 2026-11-08 on tree `537639ebca`, guest steps named, with the console session locked, at a load average of 4 to 6, on a
lane with candles (250 bars) after three blocked nights, in 8 min 31 s with its pack: the same 10 green, 6 blocked and
11 findings as on 2026-11-04, `ind-dialog` again just under the line (0.46 percent, 5,316 of 1,149,194), and
`sym-switch` failing `closed` in both hosts on `DERIBIT.F ETH_USDC-PERPETUAL` (0.07 percent apart). Its pair shows the
cause of the cascade in both hosts: the symbol dialog closed, and the "Draw by holding" tip (`InkTutorialDialog.vue`,
`ink-tutorial-close`) stood open over the ETH chart, so every later click and hover timed out. Before that, on
2026-11-04 on tree `8436920004`, guest steps named, with the console session locked and the machine at a load average of
3 to 7, on a lane with candles (250 bars in Chromium's engine before the sweep), in 8 min 36 s with its pack (Electron
44.9.3, Chromium 152 in the shell; the sweep dismissed `guest-signup-modal-close-btn` in both hosts). 10 green
(`boot-candles`, `ind-dialog`, `ind-catalog`, `ind-search`, `ind-add`, `sym-dialog`, `sym-results`, `sym-scope`,
`ks-super-search`, `ks-open`), 6 blocked at sign-in (`ind-legend`, `tb-layout-apply`, `ks-run`, `hl-order`,
`cex-order`, `oneclick-link`), 11 findings. `ind-dialog` turned green with every check true in both hosts
(`searchBox`, `dialogStyleOverlay`, `guestCapShown`, cap `1 / 3`): 0.46 percent of the unmasked pixels differed (5,307
of 1,148,915, masks over 11 percent of the frame), just under the 0.5 percent line; on 2026-10-29, 2026-10-31 and
2026-11-02 it was a finding at 1.6 to 1.7 percent, inside the dialog's suggestion and catalog cards, which draw
different content in the two hosts. Read it as content close to the line, not as a shell change. `sym-switch` failed
`closed` in both hosts again (`ethTitle` and `barsOver50` true in both, symbol `BINANCE.F ETHUSDT`, its pair 0.02
percent apart), and every later step failed on a click or hover timeout in both hosts (`tb-interval`, `tb-plot`,
`tb-panels` a 15 s click, the peeks a 30 s hover, `tb-plot`, `hl-enable` and `cex-connect` with a failed restore too).
`pulse-page` timed out waiting for the Pulse page. `login-wall` wrote no shell capture (`captured` and `loadedLane`
false): its shell half is a `capture.js` launch, and a locked screen gives it no frame (see
[launch](./shell-launch-and-window.md)). Chromium's half wrote its frame. The runs of 2026-10-27, 2026-10-28,
2026-10-29, 2026-10-31, 2026-11-02 and 2026-11-04, at very different loads, give the same cascade, so it is drift
between the sweep and the web tree, not load. On 2026-11-01 (`2646a76a83`) and 2026-11-03 (`1af9ebbe07`) the sweep
packed the app and threw in `waitForCandles` (`parity.mjs:456`, 180 s) before any step, and on 2026-11-05
(`bf1c9bac3c`), 2026-11-06 (`8bcd72f8f5`, 1 bar) and 2026-11-07 (`dced88e06a`, 1 bar) it was not run, because the dev lane's v2
streaming host (`tsdb-gateway.int.ore.kiyotaka.ai`) was unreachable or did not resolve while the lane's REST health
read `ok`; that was an environment block, not a sweep finding (see the [index](./README.md)). Source reads on
2026-11-04 to 2026-11-09 found no testid the sweep uses that went dead between `1af9ebbe07` and `27fb2d4621`.
`cex-connect`'s `keyFieldAbsent` check (`parity.mjs:935`) reads `link-paste-key-input`, a testid no revision of `src/`
has carried (`git log -S` finds none), so it is true in both hosts whatever the dialog shows and proves nothing.
Since `bda0563ab1` (after `bf1c9bac3c`) a guest gets the US stocks tape (`UsEquitiesFull` on for guests,
`src/constants/guest-default-flags.constants.ts`), so a guest step on a stock symbol sees its trades and time and
sales; no guest step has run against that yet; the dead alternatives
it carries are older (`global-nav-pulse-btn` at `parity.mjs:220`, beside the live `pulse-main-feed` and
`pulse-main-notice`; `option-chain-row` in `si-option-chain`, beside the live `option-chain-strike*`;
`live-streams-card` and `marketplace-card` in masks; `workspace-more-0-btn` in the signed-in layouts rows). The
signed-in phase has not been driven in this map. The Windows sweep needs a VM and has never run.

## Sub-features

- `parity-chart` boot, symbol search, intervals, plot types, layout picker, Panels menu and the editor open the same
  in both hosts.
- `parity-indicators` the Indicators store, catalog, search and the engine add agree in both hosts.
- `parity-boundary` Turn on trading, Connect Binance and Pulse reach the same signed-out step in both hosts.
- `parity-login` the sign-in screen, as two plain launches.
- `parity-signed-in` the `si-*` and `si-oauth-*` rows on the deployed chart with the QA account. Live verification
  pending.

## How to get to it (user POV)

- None. This is a regression sweep over the web app's own recipes, run before a beta becomes stable.

## Driving it with control-kiyotaka-desktop

Preconditions:

- `lane up`, then `doctor` exit `0`. Label every result with the tree `doctor` printed and its distance behind
  `origin/main`.
- The signed-in phase also needs `~/.config/kiyotaka-qa/account.env` (`KIYO_QA_EMAIL`, `KIYO_QA_PASSWORD`, optional
  testnet keys; `QA_ACCOUNT_ENV` overrides the path) and the operator's say-so, because it writes to a real account.

- **Guest steps.** Name them, because no step list means every step, the signed-in phase included:
  `control-kiyotaka-desktop run parity <dir> boot-candles ind-dialog ind-catalog ind-search ind-add ind-legend
  sym-dialog sym-results sym-scope sym-switch tb-interval tb-interval-peek tb-plot-peek tb-plot tb-layout-peek
  tb-layout-apply tb-panels ks-super-search ks-open ks-run hl-enable hl-order cex-connect cex-order pulse-page
  oneclick-link login-wall`. It packs the app first; `PARITY_REUSE_PACKAGE=1` reuses the build in `dist-app`. It writes
  `parity-mac-<step>-{shell,browser,diff}.png` per step, `parity-mac-summary.png` and `parity-mac-summary.json`, and
  prints `[parity] <step>: STATUS (reason)` lines and a `not settled:` line.
- **Signed-in steps.** `run parity <dir> signed-in` (or named `si-*` steps). It creates a `qa-desktop-*` layout per
  host, restores the account's tabs afterwards, withholds layout deletes, and saves and restores the macOS clipboard.
  `PARITY_SIGNED_IN_URL` overrides the deployed chart. The wrapper still demands a lane for these, though the script
  does not.
- **Read the result.** Statuses are GREEN, FINDING, BLOCKED and NOT-RUN. A GREEN row needs every check true in both
  hosts, agreeing state, and a diff within threshold. The diff image tints masked pixels blue. A BLOCKED row names its
  sign-in stop; never count it as green. Exit `0` only when the sweep settles, which includes the account restore.
- **Proof.** The summary PNG and JSON, and the pair and diff for every finding.

## Gotchas

- **A finding in both hosts is not a shell finding.** Read `hosts.shell.checks` against `hosts.browser.checks` in the
  summary. On 2026-10-27 every FINDING but `ind-dialog` failed the same way in both hosts; on 2026-10-28 every FINDING
  but `ind-catalog` (Chromium alone) did. The chain starts at `sym-switch`: its `closed` check (`parity.mjs:720`,
  nothing on top) fails because the "Draw by holding" tip is open over the new symbol's chart, which
  `parity-mac-sym-switch-{shell,browser}.png` showed in both hosts on 2026-11-08. The sweep looks for that tip only in
  `clearFirstLoadOverlays` (at boot, `parity.mjs:468`, and after the flow reload, `:3889`), where on 2026-11-08 it had not shown yet (`meta.dismissed` lists
  only `guest-signup-modal-close-btn` in both hosts), and `beforeCapture` closes only the guest signup prompt, so the
  tip, once up, blocks every later click and hover. That is a lane gap in the product repo, to be fixed in `parity.mjs`. It
  does not point at the shell.
- **Two product-lane gaps as of 2026-11-09, still open 2026-11-10 (`parity.mjs` unchanged), both in `parity.mjs`.** `ind-search`'s `after` needs a second Escape, or a clear before it, and the same holds for any other step that types into a `SearchField` and closes with one Escape. The diff needs the Lite charts toast handled in both hosts. Seeding `kiyo:pref:light-charts:decided` before load is the source's route (`src/utility/chart/light-charts.util.ts:42`), untried here. Read a fraction near 2.5 percent as that toast before anything else. The signed-in `si-settings` step also went dead in `b62ef4c998`: `light-charts-setting-row` moved off the Source page to the Display page (`parity.mjs:2436` to `:2437`, `LiteChartsSettingRow.vue`), and the row label is now Lite charts; source-read, the signed-in phase was not run.
- The sweep closes the guest signup prompt itself (`meta.dismissed` lists `guest-signup-modal-close-btn` for
  both hosts); `launch.mjs`'s `links` scenario does not.
- A re-run on a reused package can fail before any step: `waitForCandles` timed out at 180 s once and
  `desktop: loaded` never came once, with `doctor` green both times. Check for leftover shells and Chromiums after a
  throw (none were left on 2026-10-27), and repack rather than reuse.
- **`doctor` green is not candles.** `doctor` reads the lane's REST health, and the chart's candles come over the v2
  streaming socket to another host. On 2026-11-01 health was `ok` and the sweep still threw in `waitForCandles` on a
  fresh pack, because that socket's host was unreachable; on 2026-11-02 `nc -z tsdb-gateway.int.ore.kiyotaka.ai 443`
  succeeded, Chromium on the lane read a priced title, and the sweep ran every step. A priced title is not enough: on 2026-11-03 Chromium read
  `76,718.5 ▲ BTC - USD` with 2 bars in the engine, and the sweep threw. Before a sweep, read
  `window.tc[0].metadata[0].rawData.length` in a browser on the lane (the sweep waits for more than 50), or the lane log
  for `v2 Streaming socket error`; with no history, report the sweep as blocked on the environment and name the host.
- Steps that would raise the sign-in dialog are reported BLOCKED and close Turnstile at once if it ever appears; the
  sign-in pair is two plain launches, `capture.js` in the unpackaged shell and Chromium's headless shell with
  `--screenshot`. Read that pair by eye.
- Playwright's Chromium hides scrollbars and the shell does not. F1, the Panels menu opening 6 px left, was a real
  web-app bug that only the shell showed; other pairs can hide the same class of bug.
- Discard and rerun every pair taken while the chart showed "Connection lost" or data stopped.
- The sweep follows the web tree, not the `verify-kiyotaka` map text. Where they disagree, the map is stale; record the
  drift in that map's feature file with a provenance line.
