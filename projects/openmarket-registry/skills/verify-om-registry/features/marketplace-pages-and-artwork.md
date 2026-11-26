# Marketplace pages, terms and artwork

Static pages explain how the marketplace works and its terms; the terms also read as JSON. The cover
artwork collection is public, and the service reports its health and metrics, including a count and
a timing of every API answer by route family.

Last verified 2026-11-27 on openmarket-registry `098a3de` (fresh detached worktree, Bun 1.3.14, lane
18120, seed token `dev-token`). Scope: the two pages, the terms API and redirect, the artwork
listing and one image, health, the metrics listener and the request counter for `/v1/search`.
Limitations: the cover editor and per-package artwork routes need an owner session and were not
driven; a custom `METRICS_APP` was not set.

## Sub-features

- `how-it-works`: `/how-marketplace-works`, h1 "Two sides of every kScript" with "you're buying"
  (Browse listings, Check out, Run it) and "you're selling" (List a kScript, Set your price, Get
  paid).
- `terms`: `/marketplace/terms` (200, h1 "OpenMarket Marketplace Terms"); `GET /v1/terms` answers
  `{"version","url","summary":[…]}`; `/policies` redirects (308) to `/marketplace/terms`.
- `artwork`: `GET /v1/artwork` lists the collection (`"version":"v1"`, each with `id`, `title`,
  `alt`, `width`, `height`, `image_url`, `thumbnail_url`); the URLs are paths such as
  `/artwork/v1/night.webp`, served as `image/webp`.
- `health`: `GET /v1/health` answers `{"ok":true,"contracts":"<version>"}`; metrics on the lane's
  metrics port at `/metrics`.
- `request-metrics`: `om_registry_http_requests_total{app,method,path,status_code}` and the
  histogram `om_registry_http_request_duration_ms` count every API answer; `path` is the route
  family (`/v1/search`), not the raw URL.
- Every series carries `app="openmarket-registry"` first (from `METRICS_APP`).

## How to get to it (user POV)

- The footer's "How it works" and "Marketplace terms" links on any page.
- Clients read `/v1/terms` and `/v1/artwork`; the operator's dashboards read `/metrics`.

## Driving it with control-om-registry

Preconditions:

- `$CR doctor` passes. No package is needed.

- **How it works.** `$CR browser open http://127.0.0.1:<port>/how-marketplace-works`;
  `$CR browser snapshot -c` shows h1 "Two sides of every kScript". Save the pair.
- **Terms.** `curl -sS -o /dev/null -w '%{http_code}' http://127.0.0.1:<port>/marketplace/terms`
  reads 200; `$CR cli -- curl -fsS http://127.0.0.1:<port>/v1/terms` returns the version and the
  summary lines; `curl -sS -o /dev/null -w '%{http_code} %{redirect_url}' …/policies` reads 308 and
  the terms URL.
- **Artwork.** `$CR cli -- curl -fsS http://127.0.0.1:<port>/v1/artwork` starts
  `{"version":"v1","artworks":[`; prefix an `image_url` with the lane origin to fetch it.
- **Health.** `$CR doctor` already reads `/v1/health`; `curl -fsS http://127.0.0.1:<port+1>/metrics`
  answers in Prometheus text.
- **Request metrics.** Read
  `curl -fsS http://127.0.0.1:<port+1>/metrics | grep -F 'path="/v1/search"'`, send one
  `GET /v1/search?q=x`, read again: the `status_code="200"` counter and the histogram count each
  rise by one.

## Gotchas

- The how-it-works copy still says "kScript", a retired name; record it as product copy, not drift.
- Metrics sit on the lane port + 1 only because `$CR up` sets `METRICS_PORT`; the product default
  is 9464.
- The request counter includes every earlier request on the lane. Read it before
  and after, never once.
