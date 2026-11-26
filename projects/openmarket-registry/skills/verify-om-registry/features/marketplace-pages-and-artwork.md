# Marketplace pages, terms and artwork

Static pages explain how the marketplace works and its terms; the terms also read as JSON. The cover
artwork collection is public, and the service reports its health and metrics.

Last verified 2026-11-26 on openmarket-registry `c0fbc81` (fresh detached worktree, Bun 1.4.3, lane 18120, seed token `dev-token`). Scope: the two pages, the terms API, the artwork listing, health and metrics. Limitations: the
cover editor and per-package artwork routes need an owner session and were not driven.

## Sub-features

- `how-it-works`: `/how-marketplace-works`, h1 "Two sides of every kScript" with "you're buying"
  (Browse listings, Check out, Run it) and "you're selling".
- `terms`: `/marketplace/terms` (200) and `GET /v1/terms` (JSON list of terms lines);
  `/policies` redirects (308).
- `artwork`: `GET /v1/artwork` lists the collection (`"version":"v1"`, each with `id`, `title`,
  `alt`, `image_url`); images serve from `/artwork/v1/<file>.webp`.
- `health`: `GET /v1/health`; metrics on the next port at `/metrics`.

## How to get to it (user POV)

- The footer's "How it works" and "Marketplace terms" links on any page.
- Clients read `/v1/terms` and `/v1/artwork`.

## Driving it with control-om-registry

Preconditions:

- `$CR doctor` passes. No package is needed.

- **How it works.** `$CR browser open http://127.0.0.1:<port>/how-marketplace-works`;
  `$CR browser snapshot -c` shows h1 "Two sides of every kScript". Save the pair.
- **Terms.** `curl -sS -o /dev/null -w '%{http_code}' http://127.0.0.1:<port>/marketplace/terms`
  reads 200; `$CR cli -- curl -fsS http://127.0.0.1:<port>/v1/terms` returns the JSON lines.
- **Artwork.** `$CR cli -- curl -fsS http://127.0.0.1:<port>/v1/artwork` starts
  `{"version":"v1","artworks":[`.
- **Health.** `$CR doctor` already reads `/v1/health`; `curl -fsS http://127.0.0.1:<port+1>/metrics`
  answers in Prometheus text.

## Gotchas

- The how-it-works copy still says "kScript", a retired name; record it as product copy, not drift.
