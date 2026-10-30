# Electron gaps

Some behavior differs between Electron and Chrome by construction. In those places the shell is built to act as
Chrome does. Keys run the same app command and fire no native menu item. Alt+click on the plot copies the bar's time,
and Shift+click starts the ruler. A file dropped on the chart never navigates the window, and the image dialog's picker
and drop zone take a PNG. A field off the chart and selected text get a native edit or copy menu, while the chart page
keeps its own. `readText` reads text copied in another app, and `navigator.share` is undefined. A service worker
registers, and the offline and online events fire. A download saves to Downloads under the page's file name, with no
prompt. A same-origin `/chart/` `window.open` lands in the window, signed in. The product contract is the web repo's
`docs/features/desktop/desktop-shell.md#electron-gaps`, and the lane is `desktop/tools/verify/gaps.mjs`.

The guest rows were last driven through this map on 2026-10-31, on tree `5475ab32d5` (`origin/main`), straight after
the parity sweep on the same lane with `GAPS_REUSE_PACKAGE=1`, in 103 s. The run had the console session locked:

- 16 rows passed in both hosts: the five `contextmenu-*` rows, `drop-chart`, `clipboard-text-read`, `navigator-share`,
  `online-offline`, `service-worker`, `device-pixel-ratio`, the two gesture rows, `upload-image-picker`,
  `drop-image-dialog` and `download-chart-csv`.
- `device-pixel-ratio` ran for the first time, because two displays were attached (both 1920 by 1080 at scale 1): the
  shell moved the window and read `dpr 1, engine 1` after the move, and the browser side is "not moved: headless
  Chromium has no window". On 2026-10-29 one display was attached and the row was the allowed not-run. Two displays at
  the same scale prove the move, not a scale change.
- The eight `keys-*` rows were not run, because the console was locked ("the macOS console is locked: no app can
  become active, so the shell window is never key and a posted key reaches no page").

On 2026-10-29, on `30481b57f8`, the same 15 non-key rows passed. On 2026-10-28, on `5365748ef3`, the lane threw twice
before any row. The signed-in rows have not been driven through
this map. Those rows are the `window-open-*` rows, `download-workspace-json` and `download-screenshot-png`. They write
to the operator's real account. Windows and Linux are unprobed.

## Sub-features

- `gaps-keys` every default binding in `src/constants/keymap.constants.ts`, sent as a real macOS key event, runs the
  same app command in both hosts and fires no native menu item (rows `keys-calibration`, `keys-tools`, `keys-edit`,
  `keys-dialogs`, `keys-view`, `keys-watchlist-replay`, `keys-panels`, `keys-misc`).
- `gaps-contextmenu` the chart page prevents `contextmenu` (no native menu in either host). An editable field and
  selected text get the main-process `context-menu` event, so the shell draws its own edit or copy menu where Chrome
  draws one (rows `contextmenu-search-input`, `contextmenu-editor`, `contextmenu-chart`, `contextmenu-input`,
  `contextmenu-selection`).
- `gaps-files` a file dropped on the chart leaves the window on the chart. The image dialog's picker opens a file
  chooser, and its drop zone previews a dropped PNG (rows `drop-chart`, `upload-image-picker`, `drop-image-dialog`).
- `gaps-platform` `readText` returns text copied in another app. `navigator.share` is undefined. A service worker
  activates, and the offline and online events fire (rows `clipboard-text-read`, `navigator-share`, `service-worker`,
  `online-offline`, `device-pixel-ratio`).
- `gaps-gestures` Alt+click on the plot leaves the bar's time on the clipboard, and Shift+click arms the ruler (rows
  `gesture-copy-timestamp`, `gesture-ruler`).
- `gaps-downloads` the chart CSV saves under its own name with no prompt (`download-chart-csv`). The workspace JSON
  (`openmarket_workspace_<name>.json` since `dc9ed408ee`) and the screenshot PNG (`openmarket_chart.png`) are signed-in
  rows.
- `gaps-window-open` the API console and Streams commands land in the shell window, signed in (signed-in rows
  `window-open-console`, `window-open-streams` and `window-open-access`).

## How to get to it (user POV)

- Use the chart in the desktop app as in Chrome. Press a shortcut, right-click a field, drop a file on the chart or
  into the image dialog, Alt+click or Shift+click the plot, export the chart's data, or open the API console. Each
  should act as it does in a browser tab.

## Driving it with control-kiyotaka-desktop

Preconditions:

- Baseline from the [index](./README.md): `lane up`, `doctor` exit `0`. No other OpenMarket bundle on disk.
- The `keys-*` rows need an unlocked console session. On a locked screen they read not-run with "the macOS console is
  locked". To check, run `ioreg -n Root -d1 -a | grep -A1 CGSSessionScreenIsLocked`.
- The signed-in rows also need `~/.config/kiyotaka-qa/account.env` and the operator's say-so. An unattended run names
  the guest rows only.

- **Guest rows.** The wrapper has no `gaps` verb, so run the lane through `cli`. With `$OUT` an absolute evidence
  folder and `<port>` the lane port, run:

  ```bash
  ROWS="keys-calibration keys-tools keys-edit keys-dialogs keys-view keys-watchlist-replay keys-panels keys-misc contextmenu-search-input contextmenu-editor contextmenu-chart contextmenu-input contextmenu-selection drop-chart clipboard-text-read navigator-share service-worker device-pixel-ratio online-offline upload-image-picker drop-image-dialog gesture-copy-timestamp gesture-ruler download-chart-csv"
  control-kiyotaka-desktop cli -- bash -c "cd desktop && OPENMARKET_DESKTOP_URL=http://127.0.0.1:<port>/chart/ node tools/verify/gaps.mjs $OUT/gaps $ROWS"
  ```

  It packs the dev build first. `GAPS_REUSE_PACKAGE=1` launches the build already in `desktop/dist-app` (for example,
  the one the parity sweep just packed).
- **Read the result.** It prints `[gaps] <row>: pass|accepted|not-run|gap|web|error`, then a table. It writes
  `gaps-<row>-{shell,browser}.png`, `gaps-summary.json` and `gaps-summary.png`. It exits `0` only when every row passes
  or is accepted, or is a not-run on `NOT_RUN_ALLOWED` (`device-pixel-ratio` with one display). A locked console
  therefore exits `1` on the key rows alone.
- **Unit level.** `control-kiyotaka-desktop cli -- pnpm --filter @openmarket/desktop test` runs
  `tests/tools/gaps.test.ts` (the download file-name rule and the settle rule). It is not a live proof.
- **Proof.** The summary JSON and PNG, and the row pairs for anything other than a pass.

## Gotchas

- A row that is not a pass in both hosts is a web-app or lane question first. Read the row's shell and browser
  columns before calling it a shell difference.
- On 2026-10-28 the lane threw twice in `bootHosts` (`page.goto` 30 s at `gaps.mjs:1694`) before any row. That
  happened once on a lane warmed in Chromium. On 2026-10-29 it ran clean straight after the parity sweep on the same
  lane, with `GAPS_REUSE_PACKAGE=1` and parity's package. The cause of the earlier throw was not isolated.
- The signed-in rows run on the deployed chart (`GAPS_SIGNED_IN_URL`, default `https://openmarket.xyz/chart/`), not
  the dev lane, because the dev backend has no password route. They refuse Cloudflare's challenge script in both hosts,
  so no Turnstile widget renders under Playwright. They put the account's active layout and tabs back before the
  browser closes.
- `clipboard-text-read` writes to the macOS clipboard with `pbcopy`. Run it only on a machine where nobody is using
  the clipboard.
