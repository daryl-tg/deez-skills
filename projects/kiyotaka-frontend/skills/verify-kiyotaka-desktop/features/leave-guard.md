# Leave guard

While the chart holds a futures trading session with working orders or open positions, the shell asks before the page
goes. The question is a native dialog: "Leave with a trading session open?", with the detail "This page holds working
orders or open positions. They stay at your broker, but this window stops showing and managing them until you connect
again." and two buttons, Leave and Stay. Stay is the default and Escape. It is asked on a window close, a quit and an
update's restart, at once and without waiting on the page, so a hung chart still closes on Leave. It is also asked on
a reload (Reload, Cmd+R, Return to OpenMarket and the page's own reloads), where it answers the page's own
`beforeunload`. Stay keeps the window and cancels the quit. Leave lets the close, quit, restart or reload go ahead.
Every other close and quit goes at once with no question, as before the guard. The page tells the shell through the
bridge's `holdsSession` member (`a2c0975b7b`, after `cf9dbea566`); the shell forgets it when a new document commits or
the page's process dies. Sources: `desktop/src/main/leave-guard.ts`, `desktop/src/main/index.ts`,
`desktop/src/preload/index.ts`, and on the page `src/store/futures-session.ts` (`tellShellHolding`, `holdsRows`); the
contract is `docs/features/desktop/desktop-shell.md#leaving-a-page-that-asks-to-stay`. Last driven 2026-11-27 on product tree `78e0c2f534` (`origin/main`, 81 commits after `1d1a3e1410`; `desktop/`, `desktop/tools/verify/` and the shell's own code unchanged; `src/pages/desktop/return.page.vue` and `src/utility/desktop/` changed only for cTrader's return, `c588843264`): `leave` 19 of 19 in 6 s on a stub chart, on the locked console; `src/store/futures-session.ts` changed (`e554e437d8` keeps the Rithmic login in a reopened tab) without touching `tellShellHolding` or `holdsRows`. Before that, driven 2026-11-26 on product tree `1d1a3e1410` (`origin/main`, 76 commits after `ec531568de`; `desktop/`, `src/pages/desktop/`, `src/utility/desktop/` and `desktop/tools/verify/` unchanged): `leave` 19 of 19 in 11 s on a stub chart, on the locked console. `c63633a376` makes a dropped Rithmic session log in again from the login the tab keeps, and leaves `tellShellHolding` alone (source-read; whether the flag goes false between the drop and the reopen is unproven). Before that, driven 2026-11-25 on product tree `ec531568de` (`origin/main`; `desktop/` 0.1.11 and `desktop/tools/verify/` unchanged since `5a11c4970d`): `leave` 19 of 19 in 7 s on a stub chart, on the locked console; the scratch drive over the real chart was not repeated. Before that, driven 2026-11-24 on product tree `5a11c4970d` (`origin/main`; `desktop/` 0.1.11; `leave.mjs` and `leave-guard.ts` unchanged): `leave` 19 of 19 in 9 s on a stub chart, on the locked console; the scratch drive over the real chart was not repeated. First driven 2026-11-21 on
product tree `92f4a841ef` (`origin/main`; `desktop/` 0.1.11), with the console session locked at a load average of 5
to 14 on 10 cores: the `leave` scenario, run on its own, passed 19 of 19 in 10 s on its first run, on a stub chart.
The same night a scratch drive of the unpackaged shell on the dev lane's real chart (`58,238.74 ▼ BTC-USD`) passed 11
of 11 in 16 s: the page's `holdsSession(true)` made a close and a quit each ask once, with the words above, and Stay
kept the window and the app; a reload with the page's `beforeunload` set asked once and Stay kept the document;
`holdsSession(false)` let the next close go with no question. Not driven: a real futures session turning the flag on
(it needs a signed-in account with a connected broker and a working order or position), a real staged update's restart
(it needs a Developer ID build), the dialog as a person sees it (both drives answer it from the main process, so no
frame shows it), Windows and Linux.

## Sub-features

- `leave-plain-close` a page that told the shell nothing closes at once with no question, even with its own
  `beforeunload` set; on macOS the dock's activate opens a new window (`plainCloseForgotten`, `plainCloseNoError`,
  `plainCloseNotAsked`, `reopenedFromDock`).
- `leave-stay-close` a close while the page holds a session asks once, and Stay keeps the window
  (`stayCloseAskedOnce`, `stayCloseKept`).
- `leave-stay-quit` a quit asks once, Stay keeps the app running and ends the quit, so a page that dies afterwards
  still reloads (`stayQuitAskedOnce`, `stayQuitKeptRunning`, `crashAfterStayQuitReloads`).
- `leave-forget` a reloaded or crashed page holds nothing until it says so again (`reloadedPageForgetsSession`,
  `reloadedPageNotAsked`).
- `leave-hung-page` a page that holds a session and then stops answering is still asked at once, and Leave closes it
  (`hungCloseAskedOnce`, `hungCloseGone`, 28 ms on 2026-11-21).
- `leave-update-restart` every Restart to Update door (the menu item, the title-bar button, the page's update toast and
  the restart dialog's Restart Now) asks first; on Leave the window close the install brings within ten seconds asks no
  second time (`restartAskedOnce`, `restartWindowGone`). The lane calls the shell's `restartToUpdate` hook; it clicks
  none of the four doors and stages no update.
- `leave-quit` a quit answered Leave exits with no main-process error (`noErrorBeforeLeaveQuit`, `leaveQuitExited`,
  `noMainProcessError`).
- `leave-reload` a reload the page asks to keep shows the same question; Stay keeps the document. No lane check; the
  scratch drive below reads it.
- `leave-page-flag` the chart calls `holdsSession(true)` while any broker's session is connected, or reconnecting, with
  a working order or a position whose net quantity is not zero, and `holdsSession(false)` when none is
  (`src/store/futures-session.ts`). The shell takes the word only from the window's own page, from the main frame of a
  chart page, and only as a boolean. Live verification pending.

## How to get to it (user POV)

- In the app, connect a futures broker, leave a working order or an open position, then close the window, quit, press
  Cmd+R, or choose Restart to Update. The app asks "Leave with a trading session open?". Stay keeps everything as it
  was.
- With no working order and no position, the same actions go at once.

## Driving it with control-kiyotaka-desktop

Preconditions:

- `doctor --prod` exit `0` (the lane needs the checkout, the Electron binary and Playwright; it loads neither the dev
  lane nor production).
- Nothing else: no pack, no fixed port (the stub chart listens on an ephemeral `127.0.0.1` port), no unlocked console.

- **Run it.** `control-kiyotaka-desktop run launch <dir> leave`. It builds the shell, launches it unpackaged on a fresh
  profile (`desktop/.verify-userdata/leave`) against a stub page titled "Stub chart", swaps
  `dialog.showMessageBoxSync` from the main process to count the questions and answer them, and logs
  `desktop: loaded http://127.0.0.1:<port>/chart/` once per window.
- **Pass.** The JSON summary's `leave.checks` are all true and `pass` is true: 19 checks on macOS (`reopenedFromDock`
  is macOS only). A step that cannot run adds `ranToTheEnd: false` and `stoppedAt`. Run it under a watchdog of about
  300 s, as for `crash`.
- **Over the real chart.** The lane's page is a stub, so it does not show that the real chart page's word is taken. A
  scratch script outside the repo can: launch the unpackaged shell with Playwright's `_electron` on a fresh profile
  under `desktop/.verify-userdata/`, with `-r tools/verify/quiet-mac.cjs` and `OPENMARKET_DESKTOP_URL` set to the
  lane's `/chart/`; take the site page through `tools/verify/shell-page.mjs`; wait for a BTC title; swap
  `dialog.showMessageBoxSync` as the lane does, keeping the options it was called with; then run
  `globalThis.openmarketShell.page().executeJavaScript('window.openmarketDesktop.holdsSession(true)', true)` and close
  the window with `globalThis.openmarketShell.window().close()`. Read one question with the words above and an open
  window. For the reload, set `window.onbeforeunload` in the same `executeJavaScript` call (its second argument is the
  user gesture Chromium wants) and call `globalThis.openmarketShell.page().reload()`. Then send
  `holdsSession(false)`, clear the handler and close again: no question, and the window goes. Report it as a scratch
  drive beside the lane, never as the lane.
- **Unit level.** `control-kiyotaka-desktop cli -- pnpm --filter @openmarket/desktop test` runs
  `tests/main/leave-guard.test.ts` on fakes, and `tests/preload/index.test.ts` and `tests/main/contract.test.ts` hold
  the bridge member. Not a live proof.
- **Proof.** The lane's JSON summary with its check names and `desktop: loaded` lines. The lane writes no PNG.

## Gotchas

- Nothing draws the dialog in either drive: the main process answers it. A frame of the question needs a person at an
  unlocked console.
- A guest chart never sets the flag. `holdsSession(true)` typed from the page is what the drives use; it proves the
  shell's half, not the futures session's.
- `holdsSession` is absent in a shell from before the guard, so the page calls it as
  `window.openmarketDesktop?.holdsSession?.()`. The bridge now has seven members on a packaged build; see
  [returns](./return-channel-and-bridge.md) `bridge-shape`.
- A Stay on a close also clears the shell's `quitting` mark. Without that, a quit the user cancelled would leave crash
  recovery off for the rest of the launch; `crashAfterStayQuitReloads` is the check for it.
- The four Restart to Update doors have no driver of their own; see [updates](./updates-and-release.md)
  `update-titlebar` and `update-prompt`.
