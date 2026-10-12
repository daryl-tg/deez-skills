# Parity sweep

The sweep replays every `verify-kiyotaka` recipe in the packaged dev build and in Playwright's Chromium on one dev
lane, captures both hosts together at 1440 by 900, and diffs each pair with masks over live data. A pair fails when
more than 0.5 percent of its unmasked pixels differ, when its masks cover more than a quarter of the frame, or when its
plot region is blank in either capture; a step also fails when the hosts disagree on its state. Last driven
2026-10-12 on `1570b59d69` by unit 11's fix round: 15 green, 4 green at the sign-in boundary, 2 findings read as
timing noise (F5, F6), 6 blocked at sign-in. The sign-in pair (F2) is judged by eye. The Windows sweep needs a VM and
has never run.

## Sub-features

- `parity-chart` boot, symbol search, intervals, plot types, layout picker, Panels menu and the editor open the same
  in both hosts.
- `parity-indicators` the Indicators panel, catalog, search and the engine add agree in both hosts.
- `parity-boundary` Enable trading, Connect Binance and Pulse reach the same signed-out step in both hosts.
- `parity-login` the sign-in screen, as two plain launches.

## How to get to it (user POV)

- None. This is a regression sweep over the web app's own recipes, run before a beta becomes stable.

## Driving it with control-kiyotaka-desktop

Preconditions:

- `lane up`, then `doctor` exit `0`. Label every result with the tree `doctor` printed and its distance behind
  `origin/main`.

- **Full sweep.** `control-kiyotaka-desktop run parity <dir>`. It packs the app first;
  `PARITY_REUSE_PACKAGE=1` reuses the build in `dist-app`. It writes `parity-mac-<step>-{shell,browser,diff}.png` per
  step, `parity-mac-summary.png` and `parity-mac-summary.json`, prints the table, and exits `1` while any step is a
  finding or blocked.
- **Some steps.** `control-kiyotaka-desktop run parity <dir> tb-panels sym-switch`.
- **Read the result.** A GREEN row needs every check true in both hosts, agreeing state, and a diff within threshold.
  The diff image tints masked pixels blue. A BLOCKED row names its sign-in stop; never count it as green.
- **Proof.** The summary PNG and JSON, and the pair and diff for every finding.

## Gotchas

- Steps that would raise the sign-in dialog are reported BLOCKED and close Turnstile at once if it ever appears; the
  sign-in pair is two plain launches, `capture.js` in the unpackaged shell and Chromium's headless shell with
  `--screenshot`. Its Turnstile halves differ ("Success!" against "Verifying...") by less than the threshold, so read
  that pair by eye.
- Playwright's Chromium hides scrollbars and the shell does not. F1, the Panels menu opening 6 px left, was a real
  web-app bug that only the shell showed; other pairs can hide the same class of bug.
- The v2 gateway failed twice during unit 11's run. Discard and rerun every pair taken while the chart showed
  "Connection lost" or data stopped.
- The packaged dev build checks the stable feed at launch and gets a 404 until a release exists. That line is expected.
- The sweep follows the web tree, not the `verify-kiyotaka` map text. Where they disagree, the map is stale; record the
  drift in that map's feature file with a provenance line.
