# The om guide

A visitor reads the om guide at `/guide`: an index with a hero, a "Connect om to your AI" block of
copy buttons, the chapters and a glossary, then one page per chapter with its video, its sections
and a pager to the next chapter. The guide exists only where `OM_REGISTRY_GUIDE` is on; elsewhere
every `/guide` path answers 404 and the header has no Guide link.

Last verified 2026-11-28 on openmarket-registry `c263de6` (fresh detached worktree, Bun 1.3.14, lane
18152 with `OM_REGISTRY_GUIDE=1`, and lane 18150 without it). Scope: the off state, the header link,
the index, all eight page slugs, an unknown slug, chapter 1 with its video playing, the pager to
chapter 2, "For your agent", the "Copy the prompt" button, the media route's full, ranged and
unsatisfiable answers, and the request metrics. Limitations: the clipboard's contents were not read,
the per-AI copy buttons and the "Copy the guide for your agent" link were not pressed, and the light
theme was not captured.

## Sub-features

- `guide-off`: without the flag, `/guide`, `/guide/<slug>` and `/guide/media/<file>` answer 404
  with the JSON body `{"error":{"code":"not_found",…}}`, and the home page holds no `/guide` link.
- `guide-link`: with the flag, the header gains the link "Guide", between the two "Search
  packages" boxes in snapshot order. The boot log prints
  `registry: the om guide ENABLED (OM_REGISTRY_GUIDE=1)`.
- `guide-index`: `/guide` answers 200 HTML with `cache-control: no-store` and `media-src 'self'` in
  its CSP. It shows h1 "Watches that keep going when you don't.", the link "Start with chapter 1 ·
  1:06", the list "What om does, step by step", h2 "Connect om to your AI" with the button "Copy the
  prompt" and "Copy for Claude", "Copy for ChatGPT", "Copy for Grok", "Copy for Claude Code",
  "Copy for Codex", "Copy for Cursor", h2 "Chapters" (h3 "What om is", "Bring your own data",
  "Watches and AI steps", "om, Claude and your agents", "Share it", "Grok's computer"), h2
  "Glossary" and h2 "How to use this guide".
- `guide-chapter`: `/guide/01-what-om-is` through `/guide/06-groks-computer`, `/guide/reference`
  and `/guide/for-your-agent` answer 200; `/guide/nope` and `/guide/a/b` answer the JSON 404. A
  chapter page has h1 with its title, h2 sections ("How it works", "What you'll see in the video",
  "Do it yourself", "Commands" in chapter 1), and the navigations "Guide chapters", "On this page"
  and "More of the guide". Chapters 1 to 6 carry a `<video controls>` with a poster;
  `reference` and `for-your-agent` carry none.
- `guide-pager`: "More of the guide" links the next chapter ("Next Bring your own data" on
  chapter 1, to `/guide/02-bring-your-own-data`).
- `guide-copy`: a click on "Copy the prompt" turns the button's text to "Copied" and adds the class
  `is-done`; the accessible name stays "Copy the prompt".
- `guide-media`: `/guide/media/om-v1-what-om-is.mp4` answers `video/mp4` with `accept-ranges:
  bytes`, a quoted `etag` and `cache-control: public, max-age=86400, must-revalidate`; a `Range:
  bytes=0-99` answers 206 with `content-range: bytes 0-99/<size>`; a range past the end answers
  416; the `.jpg` poster answers `image/jpeg`; a name outside the list answers the JSON 404.
- `guide-metrics`: the request series count `path="/guide"`, `path="/guide/:page"` and
  `path="/guide/media/:file"`.

## How to get to it (user POV)

- On a registry with the guide on, select "Guide" in the header, or open `/guide`.
- From the index, select a chapter or "Start with chapter 1"; from a chapter, follow "Next".

## Driving it with control-om-registry

Preconditions:

- A lane started with `OM_REGISTRY_GUIDE=1` (also `true` or `on`; any other value leaves it off),
  for example `REGISTRY_WRUN_KINDS=on OM_REGISTRY_GUIDE=1 OM_REGISTRY_STATIC_TOKENS='…' $CR up`.
  No package is needed. For the off state, any lane without the flag.
- `$CR doctor` passes.

- **Off.** On a lane without the flag, `curl -sS -w ' %{http_code}' $O/guide` reads the JSON 404,
  and `curl -s $O/ | grep -c /guide` reads 0.
- **Header link.** `$CR browser open $O/`, then `$CR browser find role link click --name "Guide" --exact`;
  `$CR browser get url` reads `/guide`. Save `snapshot -c` and a screenshot.
- **Pages.** Loop the eight slugs with `curl -s -o /dev/null -w '%{http_code}' $O/guide/<slug>`
  (200 each), then `/guide/nope` (404).
- **Chapter and video.** `$CR browser open $O/guide/01-what-om-is`, snapshot and screenshot. Read
  the navigations and the video with
  `$CR browser eval 'JSON.stringify({navs:[...document.querySelectorAll("nav")].map(n=>n.getAttribute("aria-label")),video:[...document.querySelectorAll("video")].map(v=>({src:v.currentSrc,poster:v.poster,controls:v.controls}))})'`.
  Prove playback with an `eval` that sets `muted`, awaits `play()`, waits a second and returns
  `readyState` (4) and a non-zero `currentTime`.
- **Pager.** Click "Next Bring your own data" by its ref; the URL is
  `/guide/02-bring-your-own-data`.
- **Copy.** On `/guide`, `$CR browser find role button click --name "Copy the prompt" --exact`, then
  read `document.querySelector('button[aria-label="Copy the prompt"]').textContent` within 1.6 s:
  "Copied".
- **Media.** `curl -sS -D - -o /dev/null -H 'Range: bytes=0-99' $O/guide/media/om-v1-what-om-is.mp4`
  reads 206; `-H 'Range: bytes=999999999-'` reads 416.
- **Metrics.** `curl -fsS http://127.0.0.1:<port+1>/metrics | grep -E '^http_requests_total.*path="/guide'`.

## Gotchas

- A synthetic `element.click()` from `eval` does not copy: the clipboard refuses the write, and the
  button keeps "Copy". Use `find role button click`, which sends a real click.
- The copy feedback changes the text, not the accessible name, so a snapshot still reads "Copy the
  prompt". Read `textContent`, and read it quickly: it reverts after 1.6 s.
- The off state answers JSON, not an HTML page, like every other unknown path.
- The videos are served from the checkout's `guide-media/` folder, not from another service, so the
  lane needs no media env.
