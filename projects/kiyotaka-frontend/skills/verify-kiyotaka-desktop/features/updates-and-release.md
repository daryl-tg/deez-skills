# Updates and release

A packaged build checks its feed (`https://assets.openmarket.xyz/desktop/<channel>/`) on launch, every four hours and
when the window comes forward after an hour, downloads a newer version in the background, and once Squirrel.Mac has
staged it turns the title-bar update button blue, badges the dock, swaps the app menu item to Restart to Update and
asks once per version "OpenMarket X is ready" (Restart Now or Later); it installs on quit and never downgrades. Since
`a2c0975b7b` every restart door (the menu item, the title-bar button, the page's toast and Restart Now) asks "Leave
with a trading session open?" first while the page holds one, and Stay drops the restart (see
[leave guard](./leave-guard.md)). A
Microsoft Store install (`process.windowsStore`) is the exception: the Store updates it, so the shell never loads the
update client there, and a check only logs `desktop: update check skipped, the Microsoft Store updates this install`
(`desktop/src/main/updater.ts` `storeManaged`, since `d5f716e49d`, 2026-11-19; source-read and unit test only). The
channel is fixed by the version, `beta` for a prerelease and `stable` otherwise; no config or menu changes it. The page
shows its own "A new version of the OpenMarket app is ready." toast through `openmarketDesktop.updates`. A remote
policy (`<feed>/policy.json`, modes `off`, `notice`, `block`) can put a notice in the title bar or block the site below a
`minVersion`; both channel policies are `off`. A merge to `main` that changes `desktop/package.json`, or a hand-pushed
`desktop-v*` tag, runs `desktop release` (macOS, with Windows unless `DESKTOP_SKIP_WINDOWS=1`; with
`DESKTOP_WINDOWS_UNSIGNED=1` the Windows installer ships unsigned, on a beta and, since `286ae64e72` (2026-11-19), on
a stable release too), `desktop release linux` and `desktop policy`; 0.1.0 and 0.1.1 shipped stable that way, and the
version on tree `92f4a841ef` (`origin/main`, 2026-11-21) is 0.1.11 (`bbeb2ee20e` took it to 0.1.8 and `354da31277` to
0.1.9, both for the crash recovery; `920afc7199` to 0.1.10, for the Linux full-screen view sizing; `286ae64e72` to
0.1.11, with the unsigned Windows rule). On 2026-11-20 the public stable feed named 0.1.11 in all three files
(`latest-mac.yml`, `latest.yml` for Windows and `latest-linux.yml`, each dated 2026-11-19), the stable `policy.json`
read `{ "mode": "off" }`, and `beta/beta-mac.yml` and `beta/beta.yml` answered 404; the feed does not say whether that
Windows installer is signed. On 2026-11-21 `release-tag.mjs --main` still read the feed as naming 0.1.11
(`DESKTOP_ALREADY_RELEASED=1`); the feed files themselves were not re-read. The update round trip was last driven
2026-11-21 on tree `92f4a841ef` (`origin/main`; `desktop/` 0.1.11), on its own after `notify` (102 s with both packs, on
the locked console, feed on `18150`): 14 of 15, `launchCheckReadBetaFeed` red with `launchRequests` `GET /policy.json`
before `GET /beta-mac.yml`, to the same Squirrel.Mac refusal (`desktop: update not staged 0.1.0-beta.2`). The restart
path's new question was driven the same night by the `leave` scenario's `restartAskedOnce` and `restartWindowGone`,
through the shell's `restartToUpdate` hook and not through a staged update. Before that, the round trip was driven
2026-11-20 on tree `cf9dbea566` (`origin/main`; `desktop/` 0.1.11), on its own
after `notify` (98 s with both packs, on the locked console, feed on `18150`): 14 of 15, `launchCheckReadBetaFeed` red
with `launchRequests` `GET /policy.json` before `GET /beta-mac.yml`, to the same Squirrel.Mac refusal (`desktop: update
not staged 0.1.0-beta.2`). The packaged dev build logged `desktop: update check http://127.0.0.1:18150/ beta`, and the
unpackaged shell logged `desktop: update check skipped, unpackaged` on Check for Updates in a scratch drive the same
night, so `d5f716e49d`'s Store branch moved neither path on macOS. Before that, driven
2026-11-19 on tree `70ca7763c6` (`origin/main`; `desktop/` unchanged, still 0.1.10), after `notify` in one `run launch ... notify update` (156 s for both with the packs, on the locked console, feed on `18150`): 15 of 15, `launchRequests` `GET /beta-mac.yml` first, to the same Squirrel.Mac refusal. Before that, driven
2026-11-18 on tree `c5bba6b889` (`origin/main`; `desktop/` unchanged, still 0.1.10), after `notify` in one `run launch ... notify update` (153 s for both with the packs, on the locked console, feed on `18150`): 14 of 15, `launchCheckReadBetaFeed` red with `launchRequests` `GET /policy.json` before `GET /beta-mac.yml`, the policy watcher's race. Before that, it was driven
2026-11-17 on tree `eb485636f1` (`origin/main`; `desktop/` unchanged, still 0.1.10), after `notify` in one
`run launch ... notify update` (143 s for both with the packs, on the locked console, feed on `18150`): 15 of 15, with
`launchRequests` `GET /beta-mac.yml` first, so `launchCheckReadBetaFeed` passed, and the same Squirrel.Mac boundary
(`desktop: update downloaded 0.1.0-beta.2, waiting for Squirrel.Mac to stage it`). Before that, driven
2026-11-16 on tree `6bfc742bc8` (`origin/main`; `desktop/` unchanged, still 0.1.10), after `notify` in one
`run launch ... notify update`. Both took 162 s with the packs, on the unlocked console, with the feed on `18150`. The
result was 14 of 15, ending at the same Squirrel.Mac refusal, with `launchRequests` `GET /policy.json` first. Before that,
driven 2026-11-14 on tree `c7d4eccfac` (`origin/main`; `desktop/` unchanged, still 0.1.10), after `notify` in one
`run launch ... notify update` (180 s for both, with the packs, at a load average of 5 to 7 on the locked console, feed
on `18150`): 14 of 15, to the same Squirrel.Mac refusal (`desktop: update not staged 0.1.0-beta.2`), with
`launchRequests` `GET /policy.json` first. On 2026-11-13 on `963af59de1` the same 14 of 15, on its own after `notify`,
in 114 s. Before that,
2026-11-12 on tree `74ccd3cdcc` (`origin/main`; `desktop/` unchanged, still 0.1.10), on its own after `notify`, in 117 s
with both packs at a load average of 8 to 13, with the feed on `18151` because another run's process held `18150`:
14 of 15 again, to the same Squirrel.Mac refusal, and the feed again saw `GET /policy.json` first. Before that,
2026-11-10 by the `update` scenario on that tree, after `notify` in one `run launch ... notify update` (158 s for both at a load average of 4 to 6,
with three packs, feed on `18150`): 14 of 15 checks, up to the boundary an ad-hoc build cannot pass (Squirrel.Mac refuses the signature: `desktop: update check
http://127.0.0.1:<feed port>/ beta`, `desktop: update downloaded 0.1.0-beta.2, waiting for Squirrel.Mac to stage it`, `Code
signature at URL file://.../ShipIt/update.../OpenMarket.app/ did not pass validation: code failed to satisfy specified
code requirement(s)`, `desktop: update error ...`, `desktop: update not staged 0.1.0-beta.2`; the feed served
`GET /policy.json`, `GET /beta-mac.yml`, `GET /beta-mac.yml`, `GET /OpenMarket-0.1.0-beta.2-mac-arm64.zip`, so
`launchCheckReadBetaFeed` was the red one).
`launchCheckReadBetaFeed` is order-dependent, not stale: it asks that the first request the feed sees is
`GET /beta-mac.yml` (`desktop/tools/verify/launch.mjs:918`, `:915` before the leave lane's lines), but the launch check and the policy watcher both ask the
same feed at launch and race. The policy request came first on every run from 2026-10-27 to 2026-11-06 (14 of 15 on
2026-11-06, `8bcd72f8f5`, feed on `18151`), the beta feed came first on 2026-11-07 with `desktop/` unchanged, and the policy request came first again on
2026-11-08, 2026-11-09, 2026-11-10, 2026-11-12, 2026-11-13, 2026-11-14 and 2026-11-16 (`launchRequests` `GET /policy.json`, `GET /beta-mac.yml`).
The beta feed came first again on 2026-11-17 and 2026-11-19, with `desktop/` unchanged, and the policy request on
2026-11-18, 2026-11-20 and 2026-11-21.
The title-bar button, the restart dialog, the page toast, the policy notice and block, and the internal build have no
live driver; the release jobs need `mac-runner` (the office Mac mini, runner tag `macos`), the certificate, the notary
key and the bucket. Since `f15423d973` (2026-11-13) a `desktop canary` job (`.gitlab-ci.yml`, after `desktop release`)
runs only from a pipeline schedule whose description starts with "desktop canary", on `main`: on `mac-runner` with the
production signing variables it fails if `CSC_LINK`, `CSC_KEY_PASSWORD`, `APPLE_API_KEY`, `APPLE_API_KEY_ID`,
`APPLE_API_ISSUER` or `NPM_TOKEN` is unset, unsets the R2 keys, runs `package:release --mac`, checks both
`OpenMarket.app` bundles with `xcrun stapler validate` and `spctl --assess`, publishes nothing, sends one notarization
request to Apple, and deletes `.npmrc` and `desktop/dist-app` after. Source-read 2026-11-14 on `c7d4eccfac`; no run of
it was observed (it needs the schedule and `mac-runner`).

## Sub-features

- `update-feed` the launch check reads the channel's feed and downloads nothing when nothing is newer.
- `update-download` Check for Updates finds the newer version and downloads its zip.
- `update-ready` macOS offers Restart to Update only after Squirrel.Mac stages the bundle.
- `update-beta-default` a prerelease build reads `beta-mac.yml`; the version alone picks the channel.
- `update-titlebar` the bar's button: Check for updates, Checking…, Downloading OpenMarket X…, Update ready, OpenMarket
  is up to date, Couldn't check for updates. Live verification pending: no lane drives the bar.
- `update-prompt` the native "OpenMarket X is ready" dialog and the page's update toast. Live verification pending:
  ready needs a Developer ID build.
- `update-restart-asks` a restart from any door asks the leave guard's question first while the page holds a trading
  session; Leave restarts, and the window close the install brings within ten seconds asks no second time; Stay
  leaves the window as it was (`desktop/src/main/index.ts` `restartToUpdate`). Live 2026-11-21 on `92f4a841ef` through
  the `leave` scenario's hook (`restartAskedOnce`, `restartWindowGone`); the four doors themselves and a staged update
  are undriven.
- `policy-notice-block` a `notice` shows its message in the title bar; a `block` unloads the site for "This version of
  OpenMarket needs an update" with Update Now; a fetch error keeps the last policy, a 404 clears it. Live verification
  pending: no lane serves a policy, and an unpackaged launch never reads one.
- `update-store-skip` a Microsoft Store install loads no update client; its check only logs that the Store updates
  the install. Live verification pending: it needs an installed Store package on Windows; the `startUpdater, Microsoft
  Store` unit test is the only cover.
- `release-tag` `release-tag.mjs` accepts `desktop-v<semver>` with an optional `-beta.<n>` matching
  `desktop/package.json`, and in `--main` mode skips a version the feed already names. It reads the two Windows
  switches: `DESKTOP_SKIP_WINDOWS=1` packs `--mac` only, `DESKTOP_WINDOWS_UNSIGNED=1` ships the Windows installer
  unsigned on either channel, and it refuses both together or any value but `1`.
- `release-publish` the upload set and its order, stable and beta, with and without Windows, and the Linux target.
- `release-store` `pnpm package:store` packs the release config as a Microsoft Store appx for x64
  (`desktop/electron-builder.store.yml`, tiles in `desktop/build/appx/`). The Store signs and updates the package, so
  it needs no Windows certificate. Live verification pending: no CI job packs it, `publish-r2.sh` uploads none of it,
  and its `identityName` and `publisher` are still `TODO-from-Partner-Center`.
- `release-canary` the scheduled `desktop canary` job signs and notarizes the macOS app as a release would, checks it
  as a user's Mac would, and publishes nothing. Live verification pending: it runs only from its schedule on
  `mac-runner`.

## How to get to it (user POV)

- A new version arrives while the app runs. The title bar's update button turns blue, the dock shows a badge, a dialog
  offers Restart Now, and the app menu (the File menu on Windows) offers Restart to Update. Quitting installs it too.
- Click the title bar's update button to check by hand.
- A Microsoft Store install gets new versions from the Store, not from the app (source-read; the Store package's
  identity is still a placeholder).

## Driving it with control-kiyotaka-desktop

Preconditions:

- `doctor --prod` exit `0`. Port `18150` free (`lsof -nP -iTCP:18150 -sTCP:LISTEN`); `UPDATE_FEED_PORT` picks another
  agent port: export it before `run launch`, and the wrapper's environment reaches the lane (2026-11-06 `18151`,
  2026-11-07 `18150`, 2026-11-12 `18151` while another run's process held `18150`).

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
  `report-hand-over`; the same 38 files and 463 tests passed on 2026-11-07 (`dced88e06a`, in 2.4 s); on 2026-11-13 (`963af59de1`) 39 files and 469 tests passed in 2.7 s, on 2026-11-14 (`c7d4eccfac`) the same in 3.0 s, on 2026-11-16 (`6bfc742bc8`) the same 39 files and 469 tests in 3.9 s, on 2026-11-17 (`eb485636f1`) the same in 2.3 s, on 2026-11-18 (`c5bba6b889`) the same in 3.1 s, and on 2026-11-19 (`70ca7763c6`) the same in 2.4 s; on 2026-11-20 (`cf9dbea566`) 39 files and 470 tests passed in 2.4 s, the new test being `startUpdater, Microsoft Store` in `updater.test.ts`; on 2026-11-21 (`92f4a841ef`) 40 files and 476 tests passed in 2.3 s, the new file being `tests/main/leave-guard.test.ts`;
  on 2026-10-30 the subprocess tests timed out under machine load. Not a live proof.
- **Upload set.** The publish script refuses unless every file it uploads exists and each feed file names the
  version, so a dry run needs a release build in `DIST_DIR` or placeholders. With placeholders, run:

  ```bash
  control-kiyotaka-desktop cli -- bash -c 'd=$(mktemp -d) && v=0.1.0 && for f in mac-arm64.dmg mac-x64.dmg mac-arm64.zip mac-arm64.zip.blockmap mac-x64.zip mac-x64.zip.blockmap win-x64.exe win-x64.exe.blockmap; do touch "$d/OpenMarket-$v-$f"; done && for f in latest-mac.yml latest.yml; do echo "version: $v" > "$d/$f"; done && cd desktop && DRY_RUN=1 DIST_DIR="$d" DESKTOP_VERSION=$v DESKTOP_CHANNEL=stable BUCKET=dry bash scripts/publish-r2.sh; rc=$?; rm -rf "$d"; exit $rc'
  ```

  It printed 13 `dry-run: upload` lines on 2026-10-12 (`d554bfb38c`, unit 12) and again on 2026-11-02 on `39b22dd2ec`,
  2026-11-03 on `1af9ebbe07`, 2026-11-04 on `8436920004`, 2026-11-05 on `bf1c9bac3c`, 2026-11-13 on `963af59de1`, 2026-11-14 on `c7d4eccfac`, 2026-11-16 on `6bfc742bc8`, 2026-11-17 on `eb485636f1`, 2026-11-18 on `c5bba6b889`, 2026-11-19 on `70ca7763c6`, 2026-11-20 on `cf9dbea566` and 2026-11-21 on `92f4a841ef` under macOS `/bin/bash` 3.2.57: the eight installers, `latest-mac.yml`, `latest.yml` and the three `latest/`
  aliases, then `Published OpenMarket 0.1.0 to s3://dry/desktop/stable`, exit 0. `DESKTOP_TARGETS` defaults to
  `mac win`, so the Linux target adds lines only when named. `c57cc3af80` (on 2026-11-02's tree) rewrote the script's
  five array loops as `${ARR[@]+"${ARR[@]}"}` so an empty array passes under bash 3.2's `set -u`; that dry run under
  `/bin/bash` is the live proof of the change. An unattended run keeps the placeholders in its own scratch folder and
  skips the `mktemp -d` and `rm -rf` halves of the recipe.
- **Release switches.** `control-kiyotaka-desktop cli -- env DESKTOP_WINDOWS_UNSIGNED=1 node
  desktop/scripts/release-tag.mjs --main` prints the release job's five exports and changes nothing. `--main` takes the
  version from `desktop/package.json` and reads the public feed once for `DESKTOP_ALREADY_RELEASED`; a tag argument
  needs that tag in the checkout. On 2026-11-20 on `cf9dbea566` it printed `DESKTOP_VERSION=0.1.11`,
  `DESKTOP_CHANNEL=stable`, `DESKTOP_PLATFORMS='--mac --win'`, `DESKTOP_WINDOWS_UNSIGNED=1` and
  `DESKTOP_ALREADY_RELEASED=1`, exit 0: a stable version takes the unsigned switch. With no switch it printed
  `DESKTOP_WINDOWS_UNSIGNED=0`; with `DESKTOP_SKIP_WINDOWS=1`, `DESKTOP_PLATFORMS='--mac'`; with both switches,
  `release-tag: DESKTOP_SKIP_WINDOWS and DESKTOP_WINDOWS_UNSIGNED are both set; unset one` and exit 1; with
  `DESKTOP_WINDOWS_UNSIGNED=yes`, `release-tag: DESKTOP_WINDOWS_UNSIGNED is "yes"; set it to 1 or leave it unset` and
  exit 1. All five reads were the same on 2026-11-21 on `92f4a841ef`. This drives the script's gate, not the CI job that packs the unsigned exe.
- **Proof.** The lane's JSON summary and `unit-05-update-available.png`, which is the menu as the main process holds
  it, drawn in a hidden window and labelled as not a screen capture.

## Gotchas

- electron-updater reports a download before Squirrel.Mac has verified it. The shell offers the update only on
  Squirrel's staged signal on macOS, and withdraws the button, badge and item on a later error.
- The scenario reads the Menu, never the title bar, so a green run says nothing about the bar's button.
- The Microsoft Store build (`d5f716e49d`) is documented only in the header of `desktop/electron-builder.store.yml`:
  `desktop/README.md` and `docs/features/desktop/desktop-shell.md` have no Store section. No lane, CI job or upload
  touches it, and `builder-config.test.ts` does not read its config. Proving it needs a Windows machine for the appx
  target, the reserved app's Partner Center identity in place of the two `TODO-from-Partner-Center` values (the Store
  refuses a package whose identity differs), and an installed package to read the update skip and the scheme.
- An unsigned Windows installer still warns on install ("Windows protected your PC": More info, then Run anyway), and
  Windows 11's Smart App Control blocks it where it is on (`desktop/README.md`, "An unsigned Windows release"). Updates
  work unsigned, since electron-updater checks a Windows publisher only when the build names one.
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
