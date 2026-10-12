# Links, menu and channel

Every `window.open` leaves for the system browser. A top-level navigation stays in the window only for a `/chart/` page
on the chart hosts (`openmarket.xyz`, `kiyotaka.dev`, or a dev lane's origin) and for any https page on the OAuth hosts
`accounts.google.com` and `x.com`; `/chart/desktop/sign` always leaves. The native menu carries the standard app, edit,
view and window menus, plus a Developer menu with Check for Updates, Switch Channel, Update Channel and Toggle
Developer Tools that a packaged build hides unless its config enables it. Switch Channel stores the choice and
relaunches onto that channel's chart. Last driven 2026-10-12 by the `links` (16 checks) and `channel` (8 checks)
scenarios on `6e93464b59`, unit 5's regression run; first proved by unit 2. The Windows menu and quit behavior are
proved by unit tests only, and the packaged hiding of the Developer menu likewise.

## Sub-features

- `links-external` a link or navigation off the allowlist opens in the system browser and the window stays put.
- `links-window-open` a `window.open` of any URL, `/chart/` included, leaves the window.
- `menu-items` the menus, their ids and the macOS close-then-activate lifecycle.
- `menu-developer` the Developer menu shows unpackaged, or packaged after one launch with
  `OPENMARKET_DESKTOP_DEVELOPER=1`.
- `channel-switch` Developer, Switch Channel, Staging relaunches onto `https://kiyotaka.dev/chart/`.

## How to get to it (user POV)

- Click the chart watermark's link, a docs link or a share link. The browser opens it; the app stays on the chart.
- Use Cmd+Q, copy and paste, zoom and full screen from the menus.
- A developer opens Developer, Switch Channel, Staging.

## Driving it with control-kiyotaka-desktop

Preconditions:

- `control-kiyotaka-desktop doctor --prod` exit `0`. These scenarios load production and need no lane.

- **Links and menu.** Run `control-kiyotaka-desktop run launch <dir> links`. The shell logs
  `desktop: external https://percept.one/`, `desktop: external https://percept.one/?from=navigation`,
  `desktop: external https://openmarket.xyz/wrun` and `desktop: external https://openmarket.xyz/chart/`. All 16 checks
  must be true, among them `clickStayedOnChart`, `windowOpenDocs` and `windowOpenChart` at one window, and
  `darwinActivateReopens`. It saves `unit-02-external-link.png`.
- **Channel switch.** Run `control-kiyotaka-desktop run launch <dir> channel`. The first launch logs
  `menu-hook: clicked channel-staging`; the relaunch's window URL is `https://kiyotaka.dev/chart/`. All 8 checks must
  be true, among them `channelSurvivesBoundsWrite` and `developerFlagStored`.
- **Proof.** The lane's JSON summary and its PNGs.

## Gotchas

- The lane replaces `shell.openExternal` with a recorder, so no browser tab opens on the machine. The proof is the
  recorded URL plus the `desktop: external` line, which only a dev lane logs.
- `kiyotaka.dev` does not resolve from the mini, so the staging relaunch logs `desktop: load failed ...
  ERR_NAME_NOT_RESOLVED` and its PNG is blank. The window URL is the proof of the switch.
- The channel step clicks the menu from the main process with `tools/verify/menu-hook.js` in a plain launch. Under
  Playwright, `app.relaunch()` carries Playwright's loader and the relaunched process never reaches ready.
- The guest chart has no docs link in its footer. The watermark pill (`chart-watermark-link`) is the one external link
  a guest sees.
