# Marketplace pages, terms and artwork

Static pages explain how the marketplace works and its terms; the terms also read as JSON. The cover
artwork collection is public, and the service reports its health and metrics, including a count and
a timing of every answer, pages included, by route family.

Last verified 2026-11-28 on openmarket-registry `c263de6` (fresh detached worktree, Bun 1.3.14, lane
18150, seed token `dev-token`). Scope: the two pages, the terms API and redirect, the artwork
listing and one image, health, the metrics listener, the request counter and histogram for
`/v1/search`, and the `unknown`, `preflight` and `/` families. Limitations: the cover editor and
per-package artwork routes need an owner session and were not driven; a custom `METRICS_APP` was not
set.

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
- `request-metrics`: `http_requests_total{app,method,path,status_code}` and the histogram
  `http_request_duration_ms` count every answer, pages included; `path` is the route
  template (`/v1/search`, `/`, `/guide/:page`), not the raw URL. Every 404
  reads `path="unknown"`, and every OPTIONS request `path="preflight"`. There is no
  `om_registry_http_*` series any more.
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
  `curl -fsS http://127.0.0.1:<port+1>/metrics | grep -F 'path="/v1/search"' | grep -E '^http_requests_total|_count'`,
  send one `GET /v1/search?q=x`, read again: `http_requests_total{…,status_code="200"}` and
  `http_request_duration_ms_count` each rise by one. Then `curl $O/nope` and
  `curl -X OPTIONS $O/v1/search` add `path="unknown",status_code="404"` and
  `path="preflight",status_code="204"`.

## Gotchas

- The how-it-works copy still says "kScript", a retired name; record it as product copy, not drift.
- Metrics sit on the lane port + 1 only because `$CR up` sets `METRICS_PORT`; the product default
  is 9464.
- The request counter includes every earlier request on the lane. Read it before
  and after, never once.
- Grep the request series by their bare names (`^http_requests_total`); the `om_registry_` prefix
  stays only on the registry's own counters such as `om_registry_publishes_total`.
