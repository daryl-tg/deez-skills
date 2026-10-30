# Parity sweep

The sweep replays the `verify-kiyotaka` recipes in the packaged dev build and in Playwright's headless Chromium on one
dev lane, captures both hosts together at 1440 by 900, and diffs each pair with masks over live data. A pair fails when
more than 0.5 percent of its unmasked pixels differ, when its masks cover more than a quarter of the frame, or when its
plot region is blank in either capture; a step also fails when the hosts disagree on its state. It has a guest phase (26
steps plus the `login-wall` pair) and a signed-in phase (about 70 `si-*` steps plus `si-oauth-<provider>`) that signs in
as the operator's real account on the deployed chart. Last driven 2026-10-31 on tree `5475ab32d5` (`origin/main`), guest
steps only, with the console session locked and the machine at a load average of 3 to 6: the same split as 2026-10-29
on `30481b57f8`, in 8 min 23 s with its pack. 9 green (`boot-candles`, `ind-catalog`, `ind-search`, `ind-add`,
`sym-dialog`, `sym-results`, `sym-scope`, `ks-super-search`, `ks-open`), 6 blocked at sign-in (`ind-legend`,
`tb-layout-apply`, `ks-run`, `hl-order`, `cex-order`, `oneclick-link`), 12 findings. `ind-dialog` is a finding with
every check true in both hosts (`searchBox`, `dialogStyleOverlay`, `guestCapShown`): 1.7 percent of the unmasked
pixels differ (1.6 on 2026-10-29), inside the dialog's suggestion and catalog cards, which draw different content in
the two hosts. That is content, not the shell. `sym-switch` failed `closed` in both hosts again (`ethTitle` and
`barsOver50` true in both), and every later step failed on a click or hover timeout in both hosts (`tb-interval` a 15 s
click, the peeks a 30 s hover, `hl-enable` and `cex-connect` a 15 s click plus a failed restore). `pulse-page` timed out
waiting for the Pulse page. `login-wall` wrote no shell capture (`captured` and `loadedLane` false): its shell half is a
`capture.js` launch, and a locked screen gives it no frame (see [launch](./shell-launch-and-window.md)). Chromium's half
wrote its frame. The runs of 2026-10-27, 2026-10-28, 2026-10-29 and 2026-10-31, at very different loads, give the same
cascade, so it is drift between the sweep and the web tree, not load. The signed-in phase has not been driven in this
map. The Windows sweep needs a VM and has never run.

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
- The sweep closes the first-run onboarding dialog itself (`meta.dismissed` lists `guest-signup-modal-close-btn` for
  both hosts); `launch.mjs`'s `links` scenario does not.
- A re-run on a reused package can fail before any step: `waitForCandles` timed out at 180 s once and
  `desktop: loaded` never came once, with `doctor` green both times. Check for leftover shells and Chromiums after a
  throw (none were left on 2026-10-27), and repack rather than reuse.
- Steps that would raise the sign-in dialog are reported BLOCKED and close Turnstile at once if it ever appears; the
  sign-in pair is two plain launches, `capture.js` in the unpackaged shell and Chromium's headless shell with
  `--screenshot`. Read that pair by eye.
- Playwright's Chromium hides scrollbars and the shell does not. F1, the Panels menu opening 6 px left, was a real
  web-app bug that only the shell showed; other pairs can hide the same class of bug.
- Discard and rerun every pair taken while the chart showed "Connection lost" or data stopped.
- The sweep follows the web tree, not the `verify-kiyotaka` map text. Where they disagree, the map is stale; record the
  drift in that map's feature file with a provenance line.
