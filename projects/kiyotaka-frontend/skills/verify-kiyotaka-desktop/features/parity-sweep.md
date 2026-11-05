# Parity sweep

The sweep replays the `verify-kiyotaka` recipes in the packaged dev build and in Playwright's headless Chromium on one
dev lane, captures both hosts together at 1440 by 900, and diffs each pair with masks over live data. A pair fails when
more than 0.5 percent of its unmasked pixels differ, when its masks cover more than a quarter of the frame, or when its
plot region is blank in either capture; a step also fails when the hosts disagree on its state. It has a guest phase (26
steps plus the `login-wall` pair) and a signed-in phase (about 70 `si-*` steps plus `si-oauth-<provider>`; `ad67d47c62`,
on 2026-11-02's tree, retired `si-panel-trades-liquidations` and renamed the `panel-tape` inventory row "Tape /
Footprint panel", since one tape now serves every market, and left the guest steps alone) that signs in as the
operator's real account on the deployed chart. Last driven 2026-11-04 on tree `8436920004` (`origin/main`, `parity.mjs`
unchanged since `30481b57f8`), guest steps named, with the console session locked and the machine at a load average of
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
packed the app and threw in `waitForCandles` (`parity.mjs:457`, 180 s) before any step, and on 2026-11-05
(`bf1c9bac3c`) and 2026-11-06 (`8bcd72f8f5`, 1 bar) it was not run, because the dev lane's v2
streaming host (`tsdb-gateway.int.ore.kiyotaka.ai`) was unreachable or did not resolve while the lane's REST health
read `ok`; that was an environment block, not a sweep finding (see the [index](./README.md)). Source reads on
2026-11-04, 2026-11-05 and 2026-11-06 found no testid the sweep uses that went dead between `1af9ebbe07` and
`8bcd72f8f5`. Since `bda0563ab1` (after `bf1c9bac3c`) a guest gets the US stocks tape (`UsEquitiesFull` on for guests,
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
  but `ind-catalog` (Chromium alone) did. The likely chain is that
  `sym-switch` left its dialog open (`closed: false`) and blocked every later click. That is unconfirmed, and it points
  at drift between the sweep and the web tree, to be recorded in the `verify-kiyotaka` map. It does not point at the
  shell.
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
