# Clip guest page

A chart clip's public link, `/chart/clip/<id>`, plays for anyone: a guest sees
the clip as a video with captions, its title, author and market, and a Copy
link button, with Open on my chart (when the clip carries a chart snapshot) and
Reply (when the clip is not itself a reply) sending them to sign in. A clip
that is not public, a malformed id and a server error each show their own
state. Re-driven 2026-11-06 on `8bcd72f8f5` (`origin/main`, lane `18103`, a
guest JWT): `/chart/clip/zzz` rendered `clip-guest-page`, `clip-guest-private`
and `clip-guest-home-link` (`This clip is not public`, `Open the chart`).
Re-driven 2026-11-05 on `87a325f4ab` (`origin/main`, lane `18103`, a
guest JWT): `/chart/clip/zzz` rendered the same three handles
(`clip-guest-page`, `clip-guest-private`, `clip-guest-home-link` to
`/chart/`), the text `This clip is not public Open the chart`, no sign-in wall
and no `clip-video-player`. That range rewrote the clip as a recorded video of
the pane plus a chart snapshot (`54331e6699`): the poster player and its
scene, hand and overlay layers are deleted, and the Take over door is gone
(source). A public clip is still not driven (no id). Created 2026-11-02 from a live drive on product tree
`a4488341f6` (`origin/main`), lane `18103`, a guest lane with no JWT: a
made-up id (`/chart/clip/zzz`) rendered `clip-guest-page` with
`clip-guest-private` (`This clip is not public`) and `clip-guest-home-link`
(`Open the chart`), with no sign-in wall. Re-driven 2026-11-04 on
`8436920004` (a guest JWT): the same three handles and no wall;
`ClipGuestPage.vue` has no diff in `215896e614..8436920004` (the clip
recorder and player now replay the author's surfaces, typed text, clicks and
keys, `6b7ef2cd2a`, which this page only shows on a published clip; replaced
by the video recording in `54331e6699`).
Re-driven 2026-11-03 on
`215896e614` (a guest JWT): the same three handles and text; `ClipGuestPage.vue`
and the `ClipGuest` route have no diff since `a4488341f6` (the clip commits in
between changed the recorder and the Board's hand overlay only). A real public clip was not driven
(no clip id is known to this map), nor the Board's own clip wall
(`/chart/board/clips`), which redirected the guest to `/chart/`.

## Sub-features

- `clip-private` a clip that is not public, or an id that is not a clip, shows
  the private state with a way back to the chart.
- `clip-play` a public clip plays as a video with its title, author, market and
  Copy link (live verification pending: needs a published clip id).
- `clip-signin-doors` Open on my chart and Reply send a guest to the sign-in
  page, which returns to the clip on the Board (source only).

## How to get to it (user POV)

- Open a clip link someone shared: `https://<host>/chart/clip/<id>`. No sign-in
  is asked for.
- Click `Open the chart` to leave a private clip for the chart.

## Driving it with control-kiyotaka

Preconditions: the lane is up (`./control-kiyotaka doctor` green). No chart
boot is needed; the page is its own route.

- **Use the `/chart/` base.** The app is served under `/chart/`, so the route
  is `http://127.0.0.1:<lane>/chart/clip/<id>`. A bare
  `http://127.0.0.1:<lane>/clip/<id>` is answered by vite's base-URL hint
  (`The server is configured with a public base URL of /chart/ - did you mean
  to visit /chart/clip/<id> instead?`), not by the app.
- **`clip-private`.** `./control-kiyotaka browser open
  "http://127.0.0.1:<lane>/chart/clip/zzz"`, then poll
  `[data-testid=clip-guest-page]`. Proof (driven 2026-11-02): `clip-guest-page`
  and `clip-guest-private` present, `clip-guest-home-link` present, the body
  text `This clip is not public Open the chart`, and the dialog store's
  `isAuthenticationDialogOpen` `false`. A malformed id is answered without a
  network call (source: `src/pages/ClipGuestPage.vue`,
  `src/services/academy-guest.service.ts`).
- **`clip-play`.** With a real public id, poll `clip-guest-title`,
  `clip-guest-author` and `clip-guest-market`; `clip-guest-copy-link-btn`
  copies the link. The player is `clip-video-player` around a `clip-video`
  element, with `clip-player-intro`, `clip-player-outro` (its
  `clip-player-outro-open-btn`) and a bar (`clip-player-bar`, `-play-btn`,
  `-time`, `-scrubber`, `-speed-btn`, `-mute-btn`, `-cc-btn`, `-open-btn`); a
  video that cannot play shows `clip-video-error`. A server error other than
  401, 403 or 404 shows `clip-guest-retry-btn`. Source only
  (`src/components/clips/ClipVideoPlayer.vue`, `ClipPlayerBar.vue`).
- **`clip-signin-doors`.** `clip-guest-open-chart-btn` (only when the clip has
  a `snapshotUrl`) and `clip-guest-reply-btn` (hidden on a clip that is itself
  a reply) push the `Auth` route with `redirect` set to the clip's Board path
  (`AcademyClip`, `clips/:id`); that is where a guest stops. A signed-in
  visitor is sent straight to that Board path. `clip-guest-take-over-btn` no
  longer exists (0 source matches on `87a325f4ab`). Source only.
- **The Board is not a guest door.** `/chart/board/clips` (and `clips/:id`,
  `setup/:key`, `c/:slug` under the Board) carry `meta.authorized: true` plus
  the `om-board` and `chart-clips` flags; a guest open of `/chart/board/clips`
  landed on `/chart/` (driven 2026-11-02).
- **Proof.** The page's testids, the private or title text, the wall state,
  and a screenshot of the page.

## Gotchas

- **The route is `authorized: false` by design (source, `routes.ts`,
  `ClipGuest`).** It is the only clip surface a guest reaches; the Super Search
  row `academy:open-clips` (`clips`, `reels`, `videos`) is listed only while
  `isChartClipsOn()` (`om-board` and `chart-clips`), so a guest's `clips`
  query lists nothing (driven 2026-11-02).
- **Opening the route reloads the lane's page**, so a later chart drive in the
  same tab starts from a fresh boot: dismiss the overlays and wait for candles
  again, and re-front the tab (it drifted `hidden` after the reload on
  2026-11-02; see [chart boot](./chart-boot-and-data-plane.md) Gotchas).
- **Clips are recorded as a video of the author's pane with a chart snapshot
  (source, `54331e6699`; before it `d5d9e33713`, `ec8e001d2d`, `479b782d5c`,
  `f63becdf6a`, `79b1c41da2`, `f6e068a812`).** The Board's `clips` and
  `clips/:id` routes render `chart.vue` itself with `immersive: true`, and a
  guest gets no record button (`clip-record*`: 0 in the DOM, driven
  2026-11-02).
