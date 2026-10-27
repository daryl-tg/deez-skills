# Updates and release

A packaged build checks its feed (`https://assets.openmarket.xyz/desktop/<channel>/`) on launch, every four hours and
when the window comes forward after an hour, downloads a newer version in the background, and once Squirrel.Mac has
staged it turns the title-bar update button blue, badges the dock, swaps the app menu item to Restart to Update and
asks once per version "OpenMarket X is ready" (Restart Now or Later); it installs on quit and never downgrades. The
channel is fixed by the version, `beta` for a prerelease and `stable` otherwise; no config or menu changes it. The page
shows its own "A new version of the OpenMarket app is ready." toast through `openmarketDesktop.updates`. A remote
policy (`<feed>/policy.json`, modes `off`, `notice`, `block`) can put a notice in the title bar or block the site below a
`minVersion`; both channel policies are `off`. A merge to `main` that changes `desktop/package.json`, or a hand-pushed
`desktop-v*` tag, runs `desktop release` (macOS, with Windows unless `DESKTOP_SKIP_WINDOWS=1`), `desktop release
linux` and `desktop policy`; 0.1.0 and 0.1.1 shipped stable that way, and the version on tree `7290d33d10` is 0.1.7. The
update round trip was last driven 2026-10-27 by the `update` scenario on that tree: 14 of 15 checks, up to the
boundary an ad-hoc build cannot pass (Squirrel.Mac refuses the signature). The red one, `launchCheckReadBetaFeed`, is a
stale lane assertion: with a feed override the policy watcher now asks `GET /policy.json` before `GET /beta-mac.yml`.
The title-bar button, the restart dialog, the page toast, the policy notice and block, and the internal build have no
live driver; the release jobs need the operator's runner, certificate, notary key and bucket.

## Sub-features

- `update-feed` the launch check reads the channel's feed and downloads nothing when nothing is newer.
- `update-download` Check for Updates finds the newer version and downloads its zip.
- `update-ready` macOS offers Restart to Update only after Squirrel.Mac stages the bundle.
- `update-beta-default` a prerelease build reads `beta-mac.yml`; the version alone picks the channel.
- `update-titlebar` the bar's button: Check for updates, Checking…, Downloading OpenMarket X…, Update ready, OpenMarket
  is up to date, Couldn't check for updates. Live verification pending: no lane drives the bar.
- `update-prompt` the native "OpenMarket X is ready" dialog and the page's update toast. Live verification pending:
  ready needs a Developer ID build.
- `policy-notice-block` a `notice` shows its message in the title bar; a `block` unloads the site for "This version of
  OpenMarket needs an update" with Update Now; a fetch error keeps the last policy, a 404 clears it. Live verification
  pending: no lane serves a policy, and an unpackaged launch never reads one.
- `release-tag` `release-tag.mjs` accepts `desktop-v<semver>` with an optional `-beta.<n>` matching
  `desktop/package.json`, and in `--main` mode skips a version the feed already names.
- `release-publish` the upload set and its order, stable and beta, with and without Windows, and the Linux target.

## How to get to it (user POV)

- A new version arrives while the app runs. The title bar's update button turns blue, the dock shows a badge, a dialog
  offers Restart Now, and the app menu (the File menu on Windows) offers Restart to Update. Quitting installs it too.
- Click the title bar's update button to check by hand.

## Driving it with control-kiyotaka-desktop

Preconditions:

- `doctor --prod` exit `0`. Port `18150` free (`lsof -nP -iTCP:18150 -sTCP:LISTEN`); `UPDATE_FEED_PORT` picks another
  agent port.

- **Update round trip.** `control-kiyotaka-desktop run launch <dir> update`. It packs `0.1.0-beta.1` and
  `0.1.0-beta.2`, serves a feed on `127.0.0.1:18150`, launches beta.1, publishes beta.2 and clicks Check for Updates
  from the main process. On an ad-hoc build it logs `desktop: update check http://127.0.0.1:18150/ beta`, then
  `desktop: update downloaded 0.1.0-beta.2, waiting for Squirrel.Mac to stage it`, then Squirrel's `code failed to
  satisfy specified code requirement(s)`, then `desktop: update not staged 0.1.0-beta.2`. Every check true except
  `launchCheckReadBetaFeed` until the lane allows the policy request first; read the summary's `launchRequests`
  (`GET /policy.json`, `GET /beta-mac.yml` on 2026-10-27). Among the rest: `onePackagedCopy`, `downloadedBeta2Zip`,
  `downloadWaitsForSquirrel`, `squirrelRefusedAdHoc`, `stagingFailureLogged`, `neverReady`, `restartToUpdateHidden`,
  `noDockBadge` and `noCopyLeft`.
- **Unit level.** `control-kiyotaka-desktop cli -- pnpm --filter @openmarket/desktop test` runs `updater`,
  `update-bridge`, `titlebar`, `policy`, `build-site`, `dev-lane`, and `tests/scripts/release-tag.test.ts`,
  `publish-r2.test.ts` and `policy.test.ts`. 35 files and 422 tests passed on 2026-10-27; not a live proof.
- **Upload set.** The publish script refuses unless every file it uploads exists and each feed file names the
  version, so a dry run needs a release build in `DIST_DIR` or placeholders. With placeholders, run:

  ```bash
  control-kiyotaka-desktop cli -- bash -c 'd=$(mktemp -d) && v=0.1.0 && for f in mac-arm64.dmg mac-x64.dmg mac-arm64.zip mac-arm64.zip.blockmap mac-x64.zip mac-x64.zip.blockmap win-x64.exe win-x64.exe.blockmap; do touch "$d/OpenMarket-$v-$f"; done && for f in latest-mac.yml latest.yml; do echo "version: $v" > "$d/$f"; done && cd desktop && DRY_RUN=1 DIST_DIR="$d" DESKTOP_VERSION=$v DESKTOP_CHANNEL=stable BUCKET=dry bash scripts/publish-r2.sh; rc=$?; rm -rf "$d"; exit $rc'
  ```

  It printed 13 `dry-run: upload` lines on 2026-10-12 (`d554bfb38c`, unit 12). Not re-driven since; `publish-r2.sh`
  has gained a Linux target and `DESKTOP_TARGETS`, so the count may differ.
- **Proof.** The lane's JSON summary and `unit-05-update-available.png`, which is the menu as the main process holds
  it, drawn in a hidden window and labelled as not a screen capture.

## Gotchas

- electron-updater reports a download before Squirrel.Mac has verified it. The shell offers the update only on
  Squirrel's staged signal on macOS, and withdraws the button, badge and item on a later error.
- The scenario reads the Menu, never the title bar, so a green run says nothing about the bar's button.
- `OPENMARKET_DESKTOP_FEED_URL` is honoured only by a dev lane or the OpenMarket Internal build
  (`electron-builder.internal.yml`, bundle `xyz.openmarket.desktop.internal`, site `chart.int.tharamine.com`); its
  CI job was removed and nothing publishes its feed.
- A tag simulation through the CI lint API is impossible without a tag, and creating one is outward. The release job
  set rests on reading every rule, including the shared template's.
- The macOS release job needs Rosetta 2: electron-builder's bundled `makensis` is x86_64, and the Windows pack fails
  `spawn Unknown system error -86` without it.
- The lane deletes `desktop/dist-app` first and both builds at the end, so the next returns, notify or handoff run
  repacks.
