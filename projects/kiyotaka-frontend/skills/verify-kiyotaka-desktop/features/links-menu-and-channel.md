# Links and menu

A top-level navigation stays in the window only for an https `/chart/` page on the channel's own host (or the dev
lane's origin), any https page on `accounts.google.com` or `x.com`, and the `/api/v1/auth-v2/` sign-in routes on the
chart host; `/chart/desktop/sign` always leaves. A `window.open` of a `/chart/` page navigates the window in place;
any other `window.open` and any other navigation goes to the system browser, and only https, http and mailto reach it.
The native menu carries app (File on Windows and Linux), edit, view and window menus. View holds Back, Forward and
Return to OpenMarket plus reload and zoom; the app menu holds Check for Updates, which becomes Restart to Update.
Since `a2c0975b7b` a reload, Return to OpenMarket and Restart to Update ask first while the page holds a trading
session (see [leave guard](./leave-guard.md)).
There is no Developer menu and no Switch Channel in any build since 0.1.0-beta.6 (`desktop/src/main/menu.ts`,
`desktop/src/main/channels.ts`), and `launch.mjs` has no `channel` scenario. A right-click on a field gives a native
edit menu, downloads save to Downloads without a prompt, and only chart pages hold permissions (clipboard-read and the
microphone are asked once and remembered). Live verification pending since this file's last green run: the `links`
scenario was last green 2026-10-12 on `6e93464b59`. It has failed at its first click, before any check, on every run from 2026-10-27 to 2026-11-26 (again 2026-11-26 on `1d1a3e1410`, 180 s with `window` in one run, at `launch.mjs:237`, the same `dialog-style dialog-overlay backdrop-dim` interception of the watermark click; again 2026-11-25 on `ec531568de`, 168 s with `window` in one run, at `launch.mjs:237`, the same `dialog-style dialog-overlay backdrop-dim` interception of the watermark click; the scratch mirror was not re-run; and 2026-11-24 on `5a11c4970d`, 63 s, at `launch.mjs:237`, the guest signup prompt's `backdrop-dim` overlay intercepting the watermark click; the scratch mirror was not re-run that night), under high and low machine load and on a locked and an unlocked console; the last was
2026-11-21 on tree `92f4a841ef` (`origin/main`; `launch.mjs` gained only the `leave` scenario, three lines above the
click, and `GuestSignupPromptDialog.vue` is unchanged), run on its own (65 s on the locked console), with the same
`dialog-style dialog-overlay backdrop-dim` interception, now at `launch.mjs:237`. The same night the scratch drive that
closes the guest signup prompt first passed 14 of 14 again on that tree in 28 s (production chart,
`58,151.05 ▼ BTC-USD`; `links-scratch-external-link.png` shows the chart and its watermark with the prompt gone), so the
link policy, the menu and the close-then-activate lifecycle hold and the lane's red is still its missing step. Before
that, 2026-11-20 on tree `cf9dbea566` (`origin/main`; `launch.mjs` and `GuestSignupPromptDialog.vue` unchanged), run on its own
(63 s on the locked console), with the same `dialog-style dialog-overlay backdrop-dim` interception at `launch.mjs:234`.
The same night a scratch drive that mirrors the scenario and closes the guest signup prompt before the click passed 14
of 14 on that tree (see Driving): the link policy, the menu and the macOS close-then-activate lifecycle work, and the
lane's red is its missing step. That is the first live proof of the link policy since 2026-10-12; it is a scratch
drive, not the lane. Before that,
2026-11-19 on tree `70ca7763c6` (`origin/main`; `launch.mjs` and `GuestSignupPromptDialog.vue` unchanged), in the combined
`run launch ... window links` on the locked console (167 s), the same `dialog-style dialog-overlay backdrop-dim`
interception at `launch.mjs:234` over `chart-watermark-link`, which again lost the `window` summary. Before that,
2026-11-18 on tree `c5bba6b889` (`origin/main`; `launch.mjs` and `GuestSignupPromptDialog.vue` unchanged), in the combined
`run launch ... window links` on the locked console, which threw at `launch.mjs:234` with the same interception and so
printed no `window` summary either; run `window` on its own to read it. Before that,
2026-11-17 on tree `eb485636f1` (`origin/main`; `launch.mjs` and `GuestSignupPromptDialog.vue` unchanged), run on its own
(63 s on the locked console), with the same `dialog-style dialog-overlay backdrop-dim` interception at
`launch.mjs:234`. Before that, 2026-11-16 on tree `6bfc742bc8`, in the combined `run launch ... window links`
(92 s on the unlocked console), the same interception. Before that,
2026-11-14 on tree `c7d4eccfac` (`origin/main`; `launch.mjs` and `GuestSignupPromptDialog.vue` unchanged), in the
SKILL.md's combined `run launch ... window links` (185 s on the locked console at a load average of 5 to 7), the same
interception at `launch.mjs:234`, which again lost the `window` summary; on 2026-11-13 on `963af59de1` the same combined
run took 166 s; on
2026-11-12 on tree `74ccd3cdcc`, 104 s at a load average of 14 to 16, run on its own, with the same
`dialog-style dialog-overlay backdrop-dim` interception at `launch.mjs:234`; on 2026-11-10 on `c2c02b7b42`, 63 s, run on its own (on 2026-11-08 a combined `run launch ... window links crash`, and on 2026-11-10 the SKILL.md's own `run launch ... window links`, lost the `window` summary to this throw
and the 2026-11-08 one never reached `crash`, so run each scenario on its own): `locator.click: Timeout 30000ms exceeded` at `launch.mjs:234` (`:230` before the crash lane's lines), after `desktop: loaded
https://openmarket.xyz/chart/`, with the `dialog-style dialog-overlay backdrop-dim` element "intercepts pointer
events" over `chart-watermark-link`. That overlay is the guest signup prompt ("See what moves price.", Join for free;
`src/components/dialogs/guest-prompt/GuestSignupPromptDialog.vue`, `guestPrompt.*`, closed by
`guest-signup-modal-close-btn`), not the first-run onboarding: `FirstRunOnboarding.vue` never starts for a guest
(`firstRunStartBlocker`, `src/components/onboarding/first-run-handoff.ts`). On 2026-11-04 the same prompt showed
over the returns frame in the shell and in Chromium on the dev lane. It is a product-lane gap, not load: `launch.mjs`
clicks "Got it" on the "Draw by holding" tip and waits up to 10 s for `.dialog-overlay` to detach (`launch.mjs:226`,
`:231`; `:223` and `:228` before the leave lane's lines), then clicks the watermark (`:237`) without closing this prompt. `launch.mjs` changed between `bf1c9bac3c` and `8bcd72f8f5` only to add the `crash` scenario, and
`GuestSignupPromptDialog.vue` and `src/composables/dialogs/useGuestSignupPrompt.ts` did not change between `8436920004`
and `27fb2d4621`.
The context menu and the chart CSV download were last driven live by the gaps lane's guest rows (see
[Electron gaps](./electron-gaps.md)); since `12906d4136` a field on the chart page gets the native edit menu too (only
the plot, `#main-chart`, cancels the event).
The permission prompts, a download collision or failure, mouse side buttons and the Windows and Linux menus are proved
by unit tests only.

## Sub-features

- `links-external` a link or navigation off the allowlist opens in the system browser and the window stays put.
- `links-window-open` a `window.open` of a `/chart/` page navigates in place; any other URL leaves the window.
- `links-signin-routes` the auth-v2 sign-in routes stay in the window; Google and X sign-in started by the page leave
  for the browser (see [browser sign-in](./browser-signin-and-checkout.md)).
- `menu-items` the menus, their ids (`app`, `edit`, `view`, `window`) and the macOS close-then-activate lifecycle.
  View also holds Reload, Force Reload, Actual Size, Zoom In, Zoom Out and Toggle Full Screen (`desktop/src/main/menu.ts`
  item ids `reload`, `force-reload`, `reset-zoom`, `zoom-in`, `zoom-out`, `fullscreen`); the `links` lane reads only
  `menuTop` and `noDeveloperItems`, so those items are source-read, not driven (2026-11-02). On 2026-11-20, and again
  on 2026-11-21 on `92f4a841ef`, a scratch drive read the View menu's item ids from the running shell: `back`, `forward`, `home`, `reload`,
  `force-reload`, `reset-zoom`, `zoom-in`, `zoom-out` and `fullscreen`; it clicked none of them.
- `menu-history` View, Back (Cmd+[ or Alt+Left), Forward and Return to OpenMarket, plus mouse side buttons on Windows
  and Linux.
- `in-window-context-menu` undo, redo, cut, copy, paste and select all on a field, the chart page's fields included
  since `12906d4136`; Copy on selected text; on the plot, the app's own menu and no native one.
- `in-window-downloads` silent save to Downloads, `name (1).ext` on a collision, an error dialog on a failure.
- `in-window-permissions` notifications and fullscreen granted silently; clipboard-read and microphone asked once
  ("OpenMarket remembers your answer."); camera and everything else denied.

## How to get to it (user POV)

- Click the chart watermark's link, a docs link or a share link. The browser opens it; the app stays on the chart.
- Use Cmd+Q, copy and paste, zoom, full screen, and Back or Forward from the menus.
- Right-click in a text field, download a CSV or a screenshot, or paste into the chart.

## Driving it with control-kiyotaka-desktop

Preconditions:

- `control-kiyotaka-desktop doctor --prod` exit `0`. The scenario loads production and needs no lane.

- **Links and menu.** Run `control-kiyotaka-desktop run launch <dir> links`. When green, the shell logs
  `desktop: external https://percept.one/`, `desktop: external https://percept.one/?from=navigation` and
  `desktop: external https://openmarket.xyz/wrun`; the chart's `window.open` no longer logs an external line, because
  it lands in place on `https://openmarket.xyz/chart/?from=window-open`. Its checks are `menuTop`,
  `noDeveloperItems`, `clickStayedOnChart`, `clickOneExternalLine`, `clickOpenedInBrowser`, `clickNoNewWindow`,
  `navigationStayedOnChart`, `navigationOpenedInBrowser`, `windowOpenDocs`, `windowOpenSign`,
  `windowOpenChartInPlace`, `updateCheckSkippedUnpackaged`, `darwinStaysOpenWithNoWindow`,
  `darwinSecondInstanceReopens` and `darwinActivateReopens`. It saves `unit-02-external-link.png`.
- **Known red since 2026-10-27 (last 2026-11-21).** The scenario clicks "Got it" on the "Draw by holding" tip, then clicks `chart-watermark-link`.
  A `.dialog-overlay` (the guest signup prompt, `guest-signup-modal-close-btn`) intercepts the click and Playwright times out after 30 s at
  `launch.mjs:237` (`:234` until the leave lane's lines went in above it), so no summary prints. Until the lane dismisses that dialog, report every links sub-feature as
  pending and quote the timeout. The parity sweep closes the same prompt itself.
- **While the lane is red: a scratch drive.** Copy `linksScenario`'s steps into a script outside the repo (resolve
  `playwright` from `desktop/package.json` with `createRequire`, import `tools/verify/shell-page.mjs`, launch `.` with
  `-r tools/verify/quiet-mac.cjs` on its own fresh `.verify-userdata/<name>` profile, replace `shell.openExternal` with
  a recorder as the lane does) and add one step before the watermark click: wait up to 20 s for
  `guest-signup-modal-close-btn`, click it, and wait for `.dialog-overlay` to detach. Run it with `desktop/` as the
  working directory. On 2026-11-20 on `cf9dbea566` (production chart, `61,834.99 ▲ BTC-USD`, locked console) that drive
  passed 14 of 14: `menuTop`, `noDeveloperItems`, `clickStayedOnChart`, `clickOneExternalLine`, `clickOpenedInBrowser`
  (`https://percept.one/`), `clickNoNewWindow`, `navigationStayedOnChart`, `navigationOpenedInBrowser`,
  `windowOpenDocs`, `windowOpenSign`, `windowOpenChartInPlace`, `updateCheckSkippedUnpackaged`,
  `darwinStaysOpenWithNoWindow` and `darwinActivateReopens`; it has no second-instance step, so
  `darwinSecondInstanceReopens` stays the lane's. The "Got it" tip did not show; the guest signup prompt ("See what
  moves price.") did. On 2026-11-21 on `92f4a841ef` the same script passed the same 14 in 28 s. Report it as a scratch drive, never as the `links` lane, and keep the lane's red in the report.
- **Unit level.** `control-kiyotaka-desktop cli -- pnpm --filter @openmarket/desktop test` covers `link-policy`,
  `menu`, `navigation`, `context-menu`, `downloads`, `permissions` and `permission-consent`. It is not a live proof.
- **Proof.** The lane's JSON summary and its PNG.

## Gotchas

- `launch.mjs`'s usage string still lists `channel` (and since `a2c0975b7b` `leave`), but `SCENARIOS` has no `channel`: `run launch <dir> channel`, alone or in a
  list, throws `unknown scenario channel` before anything runs. Old `channel`, `updateChannel` and `developerMenu` keys
  in a profile's `config.json` are ignored.
- The scenario prints its JSON only after every requested scenario finishes. A throw in `links` loses the `window`
  summary from the same invocation; run `window` on its own.
- The lane replaces `shell.openExternal` with a recorder, so no browser tab opens on the machine. The proof is the
  recorded URL plus the `desktop: external` line, which only a dev lane logs.
- The guest chart has no docs link in its footer. The watermark pill (`chart-watermark-link`) is the one external link
  a guest sees.
