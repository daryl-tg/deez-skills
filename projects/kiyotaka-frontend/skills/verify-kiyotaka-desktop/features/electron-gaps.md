# Electron gaps

Some behavior differs between Electron and Chrome by construction. In those places the shell is built to act as
Chrome does. Keys run the same app command and fire no native menu item. Alt+click on the plot copies the bar's time,
and Shift+click starts the ruler. A file dropped on the chart never navigates the window, and the image dialog's picker
and drop zone take a PNG. A field (on the chart page too, since `12906d4136`) and selected text get a native edit or
copy menu, while the plot keeps the app's own. `readText` reads text copied in another app, and `navigator.share` is
undefined. A service worker
registers, and the offline and online events fire. A download saves to Downloads under the page's file name, with no
prompt. A same-origin `/chart/` `window.open` lands in the window, signed in. The product contract is the web repo's
`docs/features/desktop/desktop-shell.md#electron-gaps`, and the lane is `desktop/tools/verify/gaps.mjs`.

Last driven 2026-11-04, on tree `8436920004` (`origin/main`; `gaps.mjs` unchanged since `8ce333e5e9`'s comment edit),
straight after the parity sweep on the same dev lane (250 bars in the engine) with `GAPS_REUSE_PACKAGE=1`, in 105 s,
with the console session locked:

- 16 rows passed in both hosts: the five `contextmenu-*` rows, `drop-chart`, `clipboard-text-read`, `navigator-share`,
  `online-offline`, `service-worker`, `device-pixel-ratio`, the two gesture rows, `upload-image-picker`,
  `drop-image-dialog` and `download-chart-csv`. This is the first live run under `12906d4136`'s chart-only cancel:
  `contextmenu-search-input` and `contextmenu-input` drew the native `undo, redo, cut, copy, paste, selectall` menu on
  an unprevented event (`isEditable` true); `contextmenu-editor` drew the same menu on CodeMirror's `.cm-content`
  (`isEditable` true), which settles that open question; `contextmenu-selection` drew `copy` alone; and
  `contextmenu-chart` was prevented on the plot's `CANVAS`, with no main-process event and the app's own menu, in
  both hosts.
- `device-pixel-ratio` ran because two displays were attached (both 1920 by 1080 at scale 1): the shell moved the
  window and read `dpr 1, engine 1` after the move, and the browser side is "not moved: headless Chromium has no
  window". With one display the row is the allowed not-run. Two displays at the same scale prove the move, not a
  scale change.
- The eight `keys-*` rows were not run, because the console was locked ("the macOS console is locked: no app can
  become active, so the shell window is never key and a posted key reaches no page").

On 2026-11-01 (`2646a76a83`) and 2026-11-03 (`1af9ebbe07`) the lane threw `page.waitForFunction: Timeout 180000ms
exceeded` in `waitForCandles` (`gaps.mjs:505`) from `bootHosts` before any row, because the dev lane had no candle
history (the v2 streaming host was unreachable or did not resolve; see the [index](./README.md)); that was an
environment block, not a row result. On 2026-11-05 (`bf1c9bac3c`), 2026-11-06 (`8bcd72f8f5`) and 2026-11-07 (`dced88e06a`) the lane was not run
for the same reason (0, 1 and 1 bars in the engine); `gaps.mjs` is unchanged and no testid it uses went dead since
`8436920004`. The same 16 rows passed on 2026-10-31 (`5475ab32d5`) and 2026-11-02
(`39b22dd2ec`) under the old document-wide cancel.
On 2026-10-29, on `30481b57f8`, the same 15 non-key rows passed. On 2026-10-28, on `5365748ef3`, the lane threw twice
before any row in `bootHosts` (`page.goto`), and on 2026-11-01 once, in `waitForCandles`. The signed-in rows have not
been driven through
this map. Those rows are the `window-open-*` rows, `download-workspace-json` and `download-screenshot-png`. They write
to the operator's real account. Windows and Linux are unprobed.

## Sub-features

- `gaps-keys` every default binding in `src/constants/keymap.constants.ts`, sent as a real macOS key event, runs the
  same app command in both hosts and fires no native menu item (rows `keys-calibration`, `keys-tools`, `keys-edit`,
  `keys-dialogs`, `keys-view`, `keys-watchlist-replay`, `keys-panels`, `keys-misc`).
- `gaps-contextmenu` each row holds the shell to Chrome's answer (`contextVerdict`): where Chrome's `contextmenu` goes
  unprevented, the shell must draw a native menu with the expected items; where Chrome's is prevented, the shell must
  draw none and match the app's own menu. Since `12906d4136` (2026-11-02, after `39b22dd2ec`) the chart page cancels
  the event on the plot alone (`#main-chart`, `ChartArea.vue` `handleContextMenu`), never in a field, a link or a
  `[data-allow-context-menu]` element (`keepsNativeContextMenu`, `src/utility/dom/native-context-menu.util.ts`), and the
  toolbar-stats and bottom-bar menus share that rule (`8ce333e5e9`). So `contextmenu-search-input` (super search's
  field) and `contextmenu-input` (the email field on `/chart/auth`) expect the edit menu, `contextmenu-selection` (the
  console's copy) expects Copy, and `contextmenu-chart` expects no native menu and the app's own. `contextmenu-editor`
  expects the edit menu, and gets it: CodeMirror's `.cm-content` reaches the shell as an editable target. Before
  `12906d4136` the page cancelled the event everywhere except inside `[data-allow-context-menu]`, and the 2026-11-02
  passes were judged against that. Live 2026-11-04 on `8436920004`, all five rows passing in both hosts.
- `gaps-files` a file dropped on the chart leaves the window on the chart. The image dialog's picker opens a file
  chooser, and its drop zone previews a dropped PNG (rows `drop-chart`, `upload-image-picker`, `drop-image-dialog`).
- `gaps-platform` `readText` returns text copied in another app. `navigator.share` is undefined. A service worker
  activates, and the offline and online events fire (rows `clipboard-text-read`, `navigator-share`, `service-worker`,
  `online-offline`, `device-pixel-ratio`).
- `gaps-gestures` Alt+click on the plot leaves the bar's time on the clipboard, and Shift+click arms the ruler (rows
  `gesture-copy-timestamp`, `gesture-ruler`).
- `gaps-downloads` the chart CSV saves under its own name with no prompt (`download-chart-csv`). The workspace JSON
  (`openmarket_workspace_<name>.json` since `dc9ed408ee`) and the screenshot PNG (`openmarket_chart.png`) are signed-in
  rows, and so are `clipboard-png-write` (the screenshot dialog's Copy leaves a PNG on the clipboard in both hosts) and
  `contextmenu-screenshot-preview` (a right-click on the preview, a `data-allow-context-menu` element, gets the native
  menu). `download-recovery-codes` is skipped by the lane itself: the file is offered only inside the 2FA setup dialog,
  which the probe never turns on. These rows are source-read (2026-11-02, `gaps.mjs` `signedInRows`), never driven here.
- `gaps-window-open` the API console and Streams commands land in the shell window, signed in (signed-in rows
  `window-open-console`, `window-open-streams` and `window-open-access`; the last is an allowed not-run while the
  my-access flag is off for the account, `NOT_RUN_ALLOWED`). `upload-import-picker` and `drop-import-dialog` are
  skipped by the lane because the import-workspace dialog has no desktop entry.

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

- `contextmenu-editor` falls back to clicking `kscript-template-blank-legacy-btn` when the editor drawer opens on the
  starter list instead of CodeMirror (`gaps.mjs:865`, `:869`). That testid is gone from `src/`; the starter list's
  blank row is `kscript-template-blank-btn` (`src/components/scriptEditor/shell/IndicatorStarterList.vue`). On
  2026-11-04 the drawer opened straight on `.cm-content`, so the dead fallback did not fire; on a profile where it does,
  the row fails on a 15 s click timeout. That is a lane gap in the product repo.
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
