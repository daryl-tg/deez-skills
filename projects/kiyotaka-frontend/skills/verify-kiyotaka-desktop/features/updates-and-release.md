# Updates and release

A packaged build checks its channel's feed on launch and every four hours, downloads a newer version in the
background, and once it is installable shows a dock badge and Restart to Update; it installs on quit and never
downgrades. A build whose version has a prerelease suffix follows the beta feed unless its config names a channel. A
`desktop-v<semver>` tag on kiyotaka-frontend runs one CI job that checks the tag, packs signed installers and uploads
them with the feed files. The update round trip was last driven 2026-10-12 by the `update` scenario on `6e93464b59`
(unit 5, 15 checks), up to the boundary an ad-hoc build cannot pass: Squirrel.Mac refuses the update's signature. The
release path is proved by its unit tests, dry runs and a rehearsal of the job script; no tag pipeline has run, and
the signed-build, Gatekeeper and Windows-installer boxes wait on the operator's certificates, runner, bucket and VM.

## Sub-features

- `update-feed` the launch check reads the channel's feed and downloads nothing when nothing is newer.
- `update-download` Check for Updates finds the newer version and downloads its zip.
- `update-ready` macOS offers Restart to Update only after Squirrel.Mac stages the bundle.
- `update-beta-default` a prerelease build with no channel in its config reads `beta-mac.yml`.
- `release-tag` only `desktop-v<semver>` with an optional `-beta.<n>` matching `desktop/package.json` is accepted.
- `release-publish` the upload set and its order, stable and beta, with and without Windows.

## How to get to it (user POV)

- A new version arrives while the app runs. The dock shows a badge, and the app menu (the File menu on Windows)
  offers Restart to Update. Quitting installs it too.

## Driving it with control-kiyotaka-desktop

Preconditions:

- `doctor --prod` exit `0`. Port `18150` free (`lsof -nP -iTCP:18150 -sTCP:LISTEN`); `UPDATE_FEED_PORT` picks another
  agent port.

- **Update round trip.** `control-kiyotaka-desktop run launch <dir> update`. It packs `0.1.0-beta.1` and
  `0.1.0-beta.2`, serves a feed on `127.0.0.1:18150`, launches beta.1, publishes beta.2 and clicks Check for Updates
  from the main process. On an ad-hoc build it must log `desktop: update downloaded 0.1.0-beta.2, waiting for
  Squirrel.Mac to stage it`, then Squirrel's `code failed to satisfy specified code requirement(s)`, then
  `desktop: update not staged 0.1.0-beta.2`. All 15 checks true, among them `launchCheckReadBetaFeed`,
  `downloadedBeta2Zip`, `squirrelRefusedAdHoc`, `neverReady`, `restartToUpdateHidden` and `noDockBadge`.
- **Release tag check.** `control-kiyotaka-desktop cli -- pnpm --filter @openmarket/desktop test` runs
  `tests/scripts/release-tag.test.ts` and `tests/scripts/publish-r2.test.ts` among the shell's tests.
- **Upload set.** The publish script refuses unless every file it uploads exists and each feed file names the
  version, so a dry run needs a release build in `DIST_DIR` or placeholders. With placeholders, run:

  ```bash
  control-kiyotaka-desktop cli -- bash -c 'd=$(mktemp -d) && v=0.1.0 && for f in mac-arm64.dmg mac-x64.dmg mac-arm64.zip mac-arm64.zip.blockmap mac-x64.zip mac-x64.zip.blockmap win-x64.exe win-x64.exe.blockmap; do touch "$d/OpenMarket-$v-$f"; done && for f in latest-mac.yml latest.yml; do echo "version: $v" > "$d/$f"; done && cd desktop && DRY_RUN=1 DIST_DIR="$d" DESKTOP_VERSION=$v DESKTOP_CHANNEL=stable BUCKET=dry bash scripts/publish-r2.sh; rc=$?; rm -rf "$d"; exit $rc'
  ```

  It prints 13 `dry-run: upload` lines in order, versioned files, then `latest-mac.yml` and `latest.yml`, then the
  three fixed names under `desktop/stable/latest/`, and `exit 0`. Driven 2026-10-12 on `d554bfb38c` (unit 12).
- **Proof.** The lane's JSON summary and `unit-05-update-available.png`, which is the menu as the main process holds
  it, drawn in a hidden window and labelled as not a screen capture.

## Gotchas

- electron-updater reports a download before Squirrel.Mac has verified it. The shell offers the update only on
  Squirrel's staged signal on macOS, and withdraws the badge and item on a later error.
- A tag simulation through the CI lint API is impossible without a tag, and creating one is outward. The tag-only job
  set rests on reading every rule, including the shared template's.
- The release job needs the macOS runner to have Rosetta 2: electron-builder's bundled `makensis` is x86_64, and the
  Windows pack fails `spawn Unknown system error -86` without it.
- The lane deletes `desktop/dist-app` first and both builds at the end, so the next returns, notify or handoff run
  repacks.
