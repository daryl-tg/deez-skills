# Notifications and app identity

The packaged app is named OpenMarket, with bundle id `xyz.openmarket.desktop` and the mascot icon, so the dock, the
menus ("Quit OpenMarket") and an OS notification's sender all read OpenMarket. The page's HTML5 `Notification` maps to
a native notification. An installed build keeps its profile in `OpenMarket`; an unpackaged launch in `OpenMarket Dev`.
The shell also hands eight analytics events (`app-opened`, `update-installed`, `update-ready`, `signin-started`,
`signin-completed`, `signin-failed`, `policy-shown`, `beta-notice-dismissed`) to the page through
`openmarketDesktop.analytics`, which forwards them through its own PostHog as `desktop:<event>`; the shell holds no key.
Last driven 2026-10-27 by the `notify` scenario on tree `7290d33d10`: 13 of 17 checks. Three reds are the known
ones, `osAuthorized`, `notificationCaptured` and `dockCaptured`: macOS never authorizes notifications for an ad-hoc
build. The fourth, `bridgeUnchanged`, is the lane's stale two-member bridge assertion (see
[returns](./return-channel-and-bridge.md)). A visible banner waits on a Developer ID build. The analytics hand-off has
no live driver; `desktop/tests/main/analytics.test.ts` covers it.

## Sub-features

- `identity-bundle` bundle name, id, icon and an ad-hoc seal under the bundle id.
- `identity-names` `app.getName()` is OpenMarket and the quit item reads "Quit OpenMarket".
- `identity-profiles` the packaged profile is `OpenMarket`, the unpackaged one `OpenMarket Dev`.
- `notify-native` the page's `Notification` fires `show`, and the OS accepts the request.
- `notify-banner` the banner and the dock appear on screen.
- `identity-analytics` the eight shell events reach the page's PostHog as `desktop:<event>`, and every web event
  carries `client: 'desktop'` and `desktopVersion`. Live verification pending: no lane observes PostHog.

## How to get to it (user POV)

- An alert fires while OpenMarket is open, and a notification from OpenMarket appears.

## Driving it with control-kiyotaka-desktop

Preconditions:

- `doctor --prod` exit `0`, and no OpenMarket bundle on disk outside this checkout's `desktop/dist-app/`.
- For the two captures: an unlocked console session, and a terminal app that holds Screen Recording (Terminal or
  Ghostty) running the command. An agent's process tree normally has neither.

- **Run it.** `control-kiyotaka-desktop run launch <dir> notify`. It packs the app, checks the bundle, fires
  `new Notification('OpenMarket', { body: 'test' })` from the chart page, reads the OS's answer from the unified log,
  and tries `screencapture` for the banner and then the dock.
- **Pass on an ad-hoc build.** Every check true except `osAuthorized`, `notificationCaptured`, `dockCaptured`, and
  `bridgeUnchanged` until the lane learns the new bridge; `osAddedRequest` reads
  `Added notification request: [ hasError: 0 ]`. Treat any other red as a regression.
- **Pass on a Developer ID build.** All 17 true. This needs the signed build installed and the lane pointed at it; the
  scenario packs its own ad-hoc build, so today the operator captures the banner by hand from the installed app.
- **Proof.** The JSON summary, `unit-04-bundle-icon.png`, and `unit-04-notification.png` and `unit-04-dock.png` when
  they could be taken.

## Gotchas

- An unsealed bundle (Electron's linker signature) is refused outright with `UNErrorDomain error 1`; `package:dev`
  seals ad-hoc under the bundle id for that reason. A release built with signing skipped would lose every
  notification, which is why `package:release` forces signing.
- `screencapture -x` fails with "could not create image from display" without Screen Recording, locked or not.
- The dock autohides on the mini. Rest the pointer on the bottom edge, or the dock capture shows no dock.
- The profile checks set `CFFIXED_USER_HOME` to a scratch home; `HOME` alone is ignored by the packaged app, and a
  probe that relied on it once created the real `~/Library/Application Support/OpenMarket`.
