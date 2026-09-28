# om-chat

- **Repo:** `~/gitlab/openmarket-chat`. The `~/github/openmarket-chat` checkout
  is deprecated and stale, so never build from it.
- **Fixtures:** `tools/visual/<name>-fixture.html`, one per surface.
  `shell-fixture` mounts the real Shell against a synthetic session and is the
  one to film the product from. Its header comment lists every query string.
- **Build:** `fixture-build.ts` works unmodified. It uses the repo's own
  `node_modules/.bin/vite` and `vite.config.ts`, and leaves `git status` empty.
- **removeClasses:** `["reduced-motion"]`. `shell-fixture.tsx` forces it on
  `<html>` alongside `dark`. `dark` stays unless the beat asks for
  `?theme=light`.
- **Routes to stub:** `{"path": "/healthz", "status": 200, "contentType": "application/json", "body": …}` with body
  `{"uptime_seconds":120,"channels":[],"loops":[]}`. This is the same stub
  `tools/visual/new-session-reveal.visual.ts` uses. With only this stub, the
  shell fixture also requests `/api/away`, `/rpc/v1/agent-grants/requests`,
  `/rpc/v1/agent-credentials/list` and `/events/v1`, and they return 404 (measured
  2026-09-28 on `view=agent`). The agent view renders correctly anyway. If a beat
  shows an error or empty state it should not, stub the request behind it.
- **Viewport:** below 768 CSS pixels renders the real mobile shell. 9:16 is
  360×640 at DPR 3. 16:9 is 960×540 at DPR 2, which renders the desktop
  three-column layout.

## States worth filming

All are `shell-fixture.html` query strings. Check the fixture header for the
current list before writing a beat.

| State | Query |
|---|---|
| A room with a live tape | `view=room` |
| Direct messages | `view=dm` |
| Your om, a new session with the greeting reveal | `view=agent&alerts=quiet&omSessions=drafts`, then click "New session" |
| Agents surface | `view=agents` |
| Library | `view=library` |
| Members, pins, library, voice panels | `&panel=members\|pins\|library\|voice` |
| A full server rail | `&rail=many` |
| Light theme, palettes, high contrast | `&theme=light`, `&palette=graphite\|warm\|slate\|brass`, `&contrast=high` |

Other fixtures give close-ups of a single surface:
- `reaction-scene`
- `agent-center`
- `poll-results`
- `persona-panel`
- `away-panel`
- `agent-usage`

Trigger controls by accessible role and name, as the visual tests do. For
example, button "Open om conversations", button "New session".

## What the shell fixture cannot show (measured 2026-09-28)

| Wanted | Why not | Nearest click-driven substitute |
|---|---|---|
| An agent replying, or a typing indicator | No reply is ever scheduled. `dmTyping` renders nothing, because the composer reads `session.ephemeral.typistsFor`, which the fixture never defines | `draft=<text>` plus button "Send message" appends the user's own bubble |
| A reaction count ticking in a room | The room's `toggleReaction` only records the click. Chips are off-screen on mobile | `view=dm`, button "👍 1, not reacted": 1→2 with its animation |
| Opening a library doc | `openLibrary` ignores `docId` | `view=library&lens=todos`, button "Open 2", then "Mark “<todo>” complete" (a check-off celebration) |
| A busy Agents surface | One agent only. Its sub-panels open on "cannot reach OM" states | `agent-center-fixture.html?state=busy` (seeded asks, live sessions, three agents). It needs its own `fixture-build.ts` run |

## Gotchas

- **On mobile, "New session" sits behind the drawer.** Click "Open om conversations" first.
- **`view=room` shows a store-5xx alert strip** over the first topic card. Add `alerts=quiet`.
- **A `draft=` query shows a character counter** above the composer.
- **DM views settle by frame 2 without reporting an animation.** Frames 0 and 1 lack the reaction chips and the "Request accepted" strip, so start a DM clip's cut at frame 3 or later.
- **Palettes `graphite`, `warm` and `slate` are nearly indistinguishable at phone width.** Only `theme=light` reads as a change.

## Brand

- **Tokens:** `packages/chat-ui/src/shared/tokens.css`. High-contrast variants
  are in `high-contrast.css`.
- **Font:** Spoqa Han Sans Neo. `src/fonts/spoqa-han-sans-neo.css` only
  `@import`s it. The woff2 files are in
  `packages/chat-ui/src/fonts/spoqa-han-sans-neo/`. Titles use the same face.
- **The om mark:** there is no SVG file. The path is inlined as `MascotMark` in
  `packages/chat-ui/src/components/Mascot.tsx` ("Logo 100px.svg"), with colors
  in `lib/mascot-grid.ts`. Extract it verbatim into the composition's assets.
- **Motion curve:** DESIGN-SYSTEM.md §6 defines the ease-out used for title
  reveals.
- **Rules:** `DESIGN-SYSTEM.md` §0 decides title cards and overlays too:
  - no colored borders
  - hierarchy by fill, spacing, size and weight
  - dark by default
  - one clay accent moment per surface

## Evidence renderer

Publish through the review renderer on 8098, without writing into the repo:

1. Put the frames, the MP4 and `evidence-manifest.json` in
   `$RUN/evidence/<run-id>/<rev>/`. `capture.screenshots` is a filename →
   caption map. The manifest also needs `runId`, `revision`, `goal`,
   `capturedAt`, `repository`, `branch`, `candidateCommit` (the product repo
   HEAD the fixtures were built from) and `diffSha256` (sha256 of the MP4).
2. From inside `~/gitlab/openmarket-chat`, run
   `ARTIFACTS="$RUN/evidence" control-om-chat evidence publish <run-id> <rev>`.
3. The operator opens `http://127.0.0.1:8098/<run-id>/<rev>/` through the
   tunnel. The MP4 is at `.../<rev>/<file>.mp4` beside the gallery.

The renderer is device-owned. Never start, restart or replace it, and never
write a revision `index.html`.

## Never

- **Never `?backend=real`.** It reaches the real daemon.
- **Never start the daemon or a dev server for a video.** Fixtures run from a
  static build.
- **Never edit product source to make a scene work.** Fix it in `scene.json`.
