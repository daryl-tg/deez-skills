# Public scope page

A publisher's page at `/@scope` names the scope and lists its public, listed packages, with a count.
The scope's owner and claim state read at `/v1/scopes/:scope`, and the page has its own share card.

Last verified 2026-11-27 on openmarket-registry `098a3de` (fresh detached worktree, Bun 1.3.14, lane
18120, seed token `dev-token`). Scope: a scope whose only package is an ontology-pack, and a scope
with a listed Indicator, each reached from the package page's author link; following a row to its
package; the API read and the share card. Limitations: a scope with several rows, publisher marks
and paid rows were not driven.

## Sub-features

- `scope-page`: breadcrumb "registry / @scope", h1 `@scope`, "N public package(s)", and "No public
  packages yet." when none is listed.
- `scope-rows`: each listed package is a row (link `@scope/name`, kind label, version,
  description) that opens its package page.
- `scope-api`: `GET /v1/scopes/:scope` returns `scope`, `claimed`, `owner_account_id` and
  `publisher`.
- `scope-card`: `GET /v1/scopes/:scope/card.jpg` returns a JPEG, named by the page's `og:image`.

## How to get to it (user POV)

- Follow the author link on a package page.
- Open `/@scope` directly.

## Driving it with control-om-registry

Preconditions:

- A package was published on this lane ([Publish a package](./publish-a-package.md)); for rows, the
  Indicator on a `REGISTRY_WRUN_KINDS=on` lane.
- `$CR doctor` passes.

- **Open it from the package.** On the package page, `$CR browser find role link click --name "@acme" --exact`,
  then `$CR browser get url` reads `/@acme`. Save the pair; `get text main` reads "@acme",
  "0 public packages" and "No public packages yet." for an ontology-pack-only scope.
- **Rows.** With `@acme/vol-bands` published, the page reads "1 public package" and the row
  "@acme/vol-bands Indicator 1.0.0". `$CR browser find role link click --name "@acme/vol-bands" --exact`
  lands on `/@acme/vol-bands`.
- **Read the scope.** `$CR cli -- curl -fsS http://127.0.0.1:<port>/v1/scopes/acme` returns
  `"claimed":true,"owner_account_id":"acct-dev"`.
- **Share card.** `curl -sS -o /dev/null -w '%{http_code} %{content_type}' …/v1/scopes/acme/card.jpg`
  reads `200 image/jpeg`.

## Gotchas

- The scope page counts listed kinds only, so an ontology-pack-only scope reads "0 public packages"
  while the package page's author card reads "1 package". Publish a listed kind to prove rows.
- A scope nobody claimed answers a JSON 404, not an HTML page.
