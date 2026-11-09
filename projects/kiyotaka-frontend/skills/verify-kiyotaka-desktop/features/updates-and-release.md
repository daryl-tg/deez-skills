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
linux` and `desktop policy`; 0.1.0 and 0.1.1 shipped stable that way, and the version on tree `c2c02b7b42`
(`origin/main`, 2026-11-10) is 0.1.10 (`bbeb2ee20e` took it to 0.1.8 and `354da31277` to 0.1.9, both for the crash
recovery; `920afc7199` to 0.1.10, for the Linux full-screen view sizing). The update round trip was last driven
2026-11-10 by the `update` scenario on that tree, after `notify` in one `run launch ... notify update` (158 s for both at a load average of 4 to 6,
with three packs, feed on `18150`): 14 of 15 checks, up to the boundary an ad-hoc build cannot pass (Squirrel.Mac refuses the signature: `desktop: update check
http://127.0.0.1:<feed port>/ beta`, `desktop: update downloaded 0.1.0-beta.2, waiting for Squirrel.Mac to stage it`, `Code
signature at URL file://.../ShipIt/update.../OpenMarket.app/ did not pass validation: code failed to satisfy specified
code requirement(s)`, `desktop: update error ...`, `desktop: update not staged 0.1.0-beta.2`; the feed served
`GET /policy.json`, `GET /beta-mac.yml`, `GET /beta-mac.yml`, `GET /OpenMarket-0.1.0-beta.2-mac-arm64.zip`, so
`launchCheckReadBetaFeed` was the red one).
`launchCheckReadBetaFeed` is order-dependent, not stale: it asks that the first request the feed sees is
`GET /beta-mac.yml` (`desktop/tools/verify/launch.mjs:915`), but the launch check and the policy watcher both ask the
same feed at launch and race. The policy request came first on every run from 2026-10-27 to 2026-11-06 (14 of 15 on
2026-11-06, `8bcd72f8f5`, feed on `18151`), the beta feed came first on 2026-11-07 with `desktop/` unchanged, and the policy request came first again on
2026-11-08, 2026-11-09 and 2026-11-10 (`launchRequests` `GET /policy.json`, `GET /beta-mac.yml`).
The title-bar button, the restart dialog, the page toast, the policy notice and block, and the internal build have no
live driver; the release jobs need `mac-runner` (the office Mac mini, runner tag `macos`), the certificate, the notary
key and the bucket.

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
  agent port: export it before `run launch`, and the wrapper's environment reaches the lane (2026-11-06 `18151`,
  2026-11-07 `18150`).

- **Update round trip.** `control-kiyotaka-desktop run launch <dir> update`. It packs `0.1.0-beta.1` and
  `0.1.0-beta.2`, serves a feed on `127.0.0.1:18150`, launches beta.1, publishes beta.2 and clicks Check for Updates
  from the main process. On an ad-hoc build it logs `desktop: update check http://127.0.0.1:18150/ beta`, then
  `desktop: update downloaded 0.1.0-beta.2, waiting for Squirrel.Mac to stage it`, then Squirrel's `code failed to
  satisfy specified code requirement(s)`, then `desktop: update not staged 0.1.0-beta.2`. Every check is true except,
  on some runs, `launchCheckReadBetaFeed`: read the summary's `launchRequests`. When it holds `GET /policy.json`
  before `GET /beta-mac.yml`, the policy watcher won the launch race and the red is the lane's ordering, not the
  updater (both orders read the beta feed). Among the rest: `onePackagedCopy`, `downloadedBeta2Zip`,
  `downloadWaitsForSquirrel`, `squirrelRefusedAdHoc`, `stagingFailureLogged`, `neverReady`, `restartToUpdateHidden`,
  `noDockBadge` and `noCopyLeft`.
- **Unit level.** `control-kiyotaka-desktop cli -- pnpm --filter @openmarket/desktop test` runs `updater`,
  `update-bridge`, `titlebar`, `policy`, `build-site`, `dev-lane`, and `tests/scripts/release-tag.test.ts`,
  `publish-r2.test.ts` and `policy.test.ts`. 35 files and 422 tests passed on 2026-10-27, 2026-10-29 (`30481b57f8`),
  2026-10-31 (`5475ab32d5`, in 2.2 s), 2026-11-01 (`2646a76a83`, in 2.2 s), 2026-11-02 (`39b22dd2ec`, in 2.3 s), 2026-11-03 (`1af9ebbe07`, in 2.3 s), 2026-11-04 (`8436920004`, in 2.5 s) and 2026-11-05 (`bf1c9bac3c`, in 2.4 s). On 2026-11-06 (`8bcd72f8f5`) the suite
  had 38 files and 463 tests, all passed in 2.4 s, the three new files being `crash-reporter`, `process-gone` and
  `report-hand-over`; the same 38 files and 463 tests passed on 2026-11-07 (`dced88e06a`, in 2.4 s);
  on 2026-10-30 the subprocess tests timed out under machine load. Not a live proof.
- **Upload set.** The publish script refuses unless every file it uploads exists and each feed file names the
  version, so a dry run needs a release build in `DIST_DIR` or placeholders. With placeholders, run:

  ```bash
  control-kiyotaka-desktop cli -- bash -c 'd=$(mktemp -d) && v=0.1.0 && for f in mac-arm64.dmg mac-x64.dmg mac-arm64.zip mac-arm64.zip.blockmap mac-x64.zip mac-x64.zip.blockmap win-x64.exe win-x64.exe.blockmap; do touch "$d/OpenMarket-$v-$f"; done && for f in latest-mac.yml latest.yml; do echo "version: $v" > "$d/$f"; done && cd desktop && DRY_RUN=1 DIST_DIR="$d" DESKTOP_VERSION=$v DESKTOP_CHANNEL=stable BUCKET=dry bash scripts/publish-r2.sh; rc=$?; rm -rf "$d"; exit $rc'
  ```

  It printed 13 `dry-run: upload` lines on 2026-10-12 (`d554bfb38c`, unit 12) and again on 2026-11-02 on `39b22dd2ec`,
  2026-11-03 on `1af9ebbe07`, 2026-11-04 on `8436920004` and 2026-11-05 on `bf1c9bac3c` under macOS `/bin/bash` 3.2.57: the eight installers, `latest-mac.yml`, `latest.yml` and the three `latest/`
  aliases, then `Published OpenMarket 0.1.0 to s3://dry/desktop/stable`, exit 0. `DESKTOP_TARGETS` defaults to
  `mac win`, so the Linux target adds lines only when named. `c57cc3af80` (on 2026-11-02's tree) rewrote the script's
  five array loops as `${ARR[@]+"${ARR[@]}"}` so an empty array passes under bash 3.2's `set -u`; that dry run under
  `/bin/bash` is the live proof of the change. An unattended run keeps the placeholders in its own scratch folder and
  skips the `mktemp -d` and `rm -rf` halves of the recipe.
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
- The macOS jobs run on `mac-runner`, the office Mac mini, with a root-owned mise in `/usr/local/bin`, not Homebrew's
  (`desktop/README.md`, `.gitlab-ci.yml`, since `67c06d5b27`). Under `CI`, `scripts/check-toolchain.sh` fails a job
  whose user can reach `/opt/homebrew`.
- The lane deletes `desktop/dist-app` first and both builds at the end, so the next returns, notify or handoff run
  repacks.
