# Public scope page

A publisher's page at `/@scope` names the scope and lists its public, listed packages, with a count.
The scope's owner and claim state read at `/v1/scopes/:scope`.

Last verified 2026-11-26 on openmarket-registry `c0fbc81` (fresh detached worktree, Bun 1.4.3, lane 18120, seed token `dev-token`). Scope: a scope whose only package is an ontology-pack, reached from the package page's author
link, and its API read. Limitations: a scope with listed packages, and following a row to its
package, were not driven.

## Sub-features

- `scope-page`: breadcrumb "registry / @scope", h1 `@scope`, "N public packages", and "No public
  packages yet." when none is listed.
- `scope-api`: `GET /v1/scopes/:scope` returns `scope`, `claimed`, `owner_account_id` and
  `publisher`.
- `scope-rows`: rows linking to each listed package (live verification pending, needs a listed kind).

## How to get to it (user POV)

- Follow the author link on a package page.
- Open `/@scope` directly.

## Driving it with control-om-registry

Preconditions:

- A package was published on this lane ([Publish a package](./publish-a-package.md)).
- `$CR doctor` passes.

- **Open it from the package.** On the package page, `$CR browser find role link click --name "@acme" --exact`,
  then `$CR browser get url` reads `/@acme`. Save the pair; `get text main` reads "@acme",
  "0 public packages" and "No public packages yet." for an ontology-pack-only scope.
- **Read the scope.** `$CR cli -- curl -fsS http://127.0.0.1:<port>/v1/scopes/acme` returns
  `"claimed":true,"owner_account_id":"acct-dev"`.

## Gotchas

- The scope page counts listed kinds only, so an ontology-pack-only scope reads "0 public packages"
  while the package page's author card reads "1 package". Publish a listed kind to prove rows.
