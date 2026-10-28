# Links and menu

A top-level navigation stays in the window only for an https `/chart/` page on the channel's own host (or the dev
lane's origin), any https page on `accounts.google.com` or `x.com`, and the `/api/v1/auth-v2/` sign-in routes on the
chart host; `/chart/desktop/sign` always leaves. A `window.open` of a `/chart/` page navigates the window in place;
any other `window.open` and any other navigation goes to the system browser, and only https, http and mailto reach it.
The native menu carries app (File on Windows and Linux), edit, view and window menus. View holds Back, Forward and
Return to OpenMarket plus reload and zoom; the app menu holds Check for Updates, which becomes Restart to Update.
There is no Developer menu and no Switch Channel in any build since 0.1.0-beta.6 (`desktop/src/main/menu.ts`,
`desktop/src/main/channels.ts`), and `launch.mjs` has no `channel` scenario. A right-click on a field gives a native
edit menu, downloads save to Downloads without a prompt, and only chart pages hold permissions (clipboard-read and the
microphone are asked once and remembered). Live verification pending since this file's last green run: the `links`
scenario was last green 2026-10-12 on `6e93464b59`. On 2026-10-27 on tree `7290d33d10` it failed twice at its first
click, before any check, and on 2026-10-28 on `5365748ef3` (`origin/main`) it failed the same way once: the first-run
onboarding dialog's `.dialog-overlay` covers the chart (a product-lane gap). The context
menu, downloads, permissions, mouse side buttons and the Windows and Linux menus are proved by unit tests only.

## Sub-features

- `links-external` a link or navigation off the allowlist opens in the system browser and the window stays put.
- `links-window-open` a `window.open` of a `/chart/` page navigates in place; any other URL leaves the window.
- `links-signin-routes` the auth-v2 sign-in routes stay in the window; Google and X sign-in started by the page leave
  for the browser (see [browser sign-in](./browser-signin-and-checkout.md)).
- `menu-items` the menus, their ids (`app`, `edit`, `view`, `window`) and the macOS close-then-activate lifecycle.
- `menu-history` View, Back (Cmd+[ or Alt+Left), Forward and Return to OpenMarket, plus mouse side buttons on Windows
  and Linux.
- `in-window-context-menu` undo, redo, cut, copy, paste and select all on a field; Copy on selected text; nothing on a
  canvas.
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
- **Known red on 2026-10-27.** The scenario clicks "Got it" on the old guest tip, then clicks `chart-watermark-link`.
  A `.dialog-overlay` (the first-run onboarding dialog) intercepts the click and Playwright times out after 30 s at
  `launch.mjs:230`, so no summary prints. Until the lane dismisses that dialog, report every links sub-feature as
  pending and quote the timeout.
- **Unit level.** `control-kiyotaka-desktop cli -- pnpm --filter @openmarket/desktop test` covers `link-policy`,
  `menu`, `navigation`, `context-menu`, `downloads`, `permissions` and `permission-consent`. It is not a live proof.
- **Proof.** The lane's JSON summary and its PNG.

## Gotchas

- `launch.mjs`'s usage string still lists `channel`, but `SCENARIOS` does not: `run launch <dir> channel`, alone or in a
  list, throws `unknown scenario channel` before anything runs. Old `channel`, `updateChannel` and `developerMenu` keys
  in a profile's `config.json` are ignored.
- The scenario prints its JSON only after every requested scenario finishes. A throw in `links` loses the `window`
  summary from the same invocation; run `window` on its own.
- The lane replaces `shell.openExternal` with a recorder, so no browser tab opens on the machine. The proof is the
  recorded URL plus the `desktop: external` line, which only a dev lane logs.
- The guest chart has no docs link in its footer. The watermark pill (`chart-watermark-link`) is the one external link
  a guest sees.
