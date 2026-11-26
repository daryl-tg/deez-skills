# Package details

A package page shows a published package to anyone allowed to see it: its title and summary, the
price and install command, the details and author cards, and Readme, Versions and Contents tabs.

Last verified 2026-11-26 on openmarket-registry `c0fbc81` (fresh detached worktree, Bun 1.4.3, lane 18120, seed token `dev-token`). Scope: an ontology-pack's page, its Versions tab, the author link and the share card image.
Limitations: no listed kind, no readme, no private package and no managed or Indicator block was
driven; "Open in OpenMarket" and Copy were not pressed.

## Sub-features

- `package-header`: h1 `@scope/name`, then "<version> · <kind> · published <when> · by @scope".
- `package-tabs`: radios "Readme", "N Version(s)" and "Contents"; Versions shows a VERSION,
  PUBLISHED, NOTE table.
- `package-side`: "Free", the "Open in OpenMarket" button, `om install @scope/name` with a "Copy"
  button, and Details rows (Installs, Version, Versions, Last published, Type, Package).
- `package-author`: the Author card links to `/@scope` with "N package · N installs".
- `package-card`: `GET /v1/packages/:scope/:name/card.jpg` returns a JPEG share card.
- Private, unlisted, managed and Indicator variants: live verification pending.

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
  reads `200 image/jpeg`.

## Gotchas

- The tab radios sit under the cover image, so a click by ref or by label is refused as covered.
  Click the visible label text with `find text "<label>" click --exact`.
- A new package gets a generated cover; the image is not the package's own artwork.
- `find role link --name "Report"` without `--exact` matches the footer's "Report abuse".
