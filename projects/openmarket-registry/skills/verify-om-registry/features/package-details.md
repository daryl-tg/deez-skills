# Package details

A package page shows a published package to anyone allowed to see it: its title and summary, the
price and install command, the details and author cards, and Readme, Versions and Contents tabs. An
Indicator's page adds its outputs, params and inputs. An agent-plugin is hidden from the public
while the community is off.

Last verified 2026-11-27 on openmarket-registry `098a3de` (fresh detached worktree, Bun 1.3.14, lane
18120, seed token `dev-token`). Scope: an ontology-pack's page, its Versions tab, the author link,
the share cards and preview tags, an Indicator's page reached from the catalog, and an agent-plugin
behind the internal-only gate. Limitations: no private or managed package was driven; "Open in
OpenMarket" and Copy were not pressed; the internal reader (SSO session, chart web token or a
platform-internal bearer) was not driven. Watch packs have their own guide:
[Watch pack page and trading record](./watch-pack-and-trading-record.md).

## Sub-features

- `package-header`: h1 `@scope/name`, then "<version> · <kind label> · published <when> · by
  @scope". The kind label is a display name: "ontology" for ontology-pack, "Indicator" for
  wrun-indicator.
- `package-tabs`: radios "Readme", "N Version(s)" and "Contents"; Versions shows a VERSION,
  PUBLISHED, NOTE table. A package with no README reads "No README in this version."
- `package-side`: "Free", the "Open in OpenMarket" button, `om install @scope/name` with a "Copy"
  button, and Details rows (Installs, Version, Versions, Last published, Type, Package).
- `package-author`: the Author card links to `/@scope` with "N package · N installs".
- `indicator-block`: an Indicator's Readme tab shows h2 "INDICATOR" with Outputs (OUTPUT, PLOT,
  PANEL, STYLE), Params (NAME, DEFAULT, MIN, MAX), Inputs (INPUT, SOURCE, SELECTION) and
  Provenance (ABI `wrun-1`).
- `package-card`: `GET /v1/packages/:scope/:name/card.jpg` returns a JPEG share card, and the page's
  `og:image` names it with a `?v=` hash.
- `internal-only`: with `OM_REGISTRY_COMMUNITY` off, an agent-plugin's page, report page, `/v1`
  reads and tarball answer an anonymous caller the same 404 as an unknown package; the scope
  owner's bearer reads the package, its summary and its tarball with 200.
- Private, unlisted and managed variants: live verification pending.

## How to get to it (user POV)

- Open `/@scope/name`, or follow `listing_url` from a publish.
- Select a package row in the catalog (listed kinds only).

## Driving it with control-om-registry

Preconditions:

- A package was published on this lane ([Publish a package](./publish-a-package.md)).
- `$CR doctor` passes.

- **Open the page.** `$CR browser open http://127.0.0.1:<port>/@acme/btc-dip-alerts` and
  `$CR browser snapshot -i -c`: h1 "@acme/btc-dip-alerts", radio "Readme" checked, button
  "Open in OpenMarket", link "@acme 1 package · 0 installs". Save the pair.
- **Open Versions.** `$CR browser find text "1 Version" click --exact`. Confirm with
  `$CR browser eval 'JSON.stringify([...document.querySelectorAll("input[type=radio]")].map(r=>[r.labels?.[0]?.textContent.trim(), r.checked]))'`
  that "1 Version" is checked; `get text main` shows the VERSION table with `1.0.0`.
- **Follow the author.** `$CR browser find role link click --name "@acme" --exact` lands on `/@acme`.
- **Share card.** `curl -sS -o /dev/null -w '%{http_code} %{content_type}' http://127.0.0.1:<port>/v1/packages/acme/btc-dip-alerts/card.jpg`
  reads `200 image/jpeg`; `curl -fsS …/@acme/btc-dip-alerts | grep og:image` names it.
- **Indicator page.** On a `REGISTRY_WRUN_KINDS=on` lane with `@acme/vol-bands`, follow its
  catalog row; `get text main` shows "INDICATOR", the Outputs, Params and Inputs tables and
  "Type Indicator".
- **Internal-only gate.** Publish the agent-plugin from [Publish a package](./publish-a-package.md).
  Anonymous: `curl -s -o /dev/null -w '%{http_code}' $O/@acme/desk-tutor` reads 404, and
  `diff <(curl -s $O/v1/packages/acme/desk-tutor) <(curl -s $O/v1/packages/acme/no-such)` is
  empty. The same reads with `-H 'authorization: Bearer dev-token'` answer 200.

## Gotchas

- The tab radios sit under the cover image, so a click by ref or by label is refused as covered.
  Click the visible label text with `find text "<label>" click --exact`.
- A new package gets a generated cover; the image is not the package's own artwork.
- `find role link --name "Report"` without `--exact` matches the footer's "Report abuse".
- A missing or hidden package page answers a JSON error body (`application/json`), not an HTML
  page, so a browser shows `{"error":{"code":"not_found",…}}` and there is no `main` to read.
