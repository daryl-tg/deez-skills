# OpenMarket registry verification map

The maintained source for proving user-visible registry behavior. Read this index before driving,
then use the matching feature file as the recipe.

## Baseline preconditions

- Run the lane from a disposable openmarket-registry worktree with a fresh
  `bun install --frozen-lockfile`, and start it with `$CR up` on an assigned port in 18097-18197.
  Bind `127.0.0.1`. The repo pins Bun 1.4.3 (`packageManager`); the 2026-11-27 and 2026-11-28
  passes ran the host's only Bun, 1.3.14, and the lanes booted and drove cleanly.
- A lane that publishes starts with a seed token:
  `OM_REGISTRY_STATIC_TOKENS='{"dev-token":{"account_id":"acct-dev","tier":"pro"}}' $CR up`.
  Leave `OM_REGISTRY_PLATFORM_API_URL` and `OM_REGISTRY_AUTH_BASE_URL` unset.
- Some kinds need their own lane, restarted with `$CR down` and `$CR up`: `REGISTRY_WRUN_KINDS=on`
  for Indicators, and the watch-pack env in
  [Watch pack page and trading record](./watch-pack-and-trading-record.md) for watch packs.
  `OM_REGISTRY_GUIDE=1` turns on [the om guide](./om-guide.md) and can share any lane.
- `$CR doctor` confirms the health route, the port owner and the working checkout.
- The lane holds metadata in memory and starts empty; tarballs go to `./data/tarballs` in the
  worktree.
- Never drive an instance this run did not start.

## Driving conventions

- Prefer ARIA roles and accessible names over CSS selectors or coordinates.
- Browser actions go through `$CR browser`; API commands go through `$CR cli --`.
- Seed packages through the real `POST /v1/publish` route, never through internal setters or test
  helpers.
- Write `<port>` as the lane's port and `<port+1>` as its metrics port; `$O` is the lane origin.
- `$CR` resolves its checkout from the working directory even for `cli --`. When you build fixtures
  in a scratch directory, export `REGISTRY_REPO=<driven worktree>`; set `ARTIFACTS` to keep the
  PID, log and evidence outside the worktree.

## Proof and skip reporting

- Capture the user action and the resulting state, not only the final screen.
- UI proof is a pair: an accessibility snapshot and a screenshot, both showing the registry.
- API proof includes the exact command, stdout, stderr and exit code.
- Mutation proof includes a second, read-only view of the stored value: the API read, the tarball or
  the metrics counter.
- Publish with `$CR evidence publish <run-id> <revision>` when the review renderer answers on 8098.
  Never hand back a lane URL.
- Report an unreachable path with the attempted command and the unmet precondition; do not count
  another entry point as proof.

## Feature entry contract

An H1 title, one paragraph of user-visible behavior, a provenance line, then exactly four H2s in
order: `Sub-features`, `How to get to it (user POV)`, `Driving it with control-om-registry`,
`Gotchas`.

## Features

- [Catalog and search](./catalog-search.md)
- [Publish a package](./publish-a-package.md)
- [Package details](./package-details.md)
- [Public scope page](./public-scope.md)
- [Report a package](./report-a-package.md)
- [Marketplace pages, terms and artwork](./marketplace-pages-and-artwork.md)
- [Owner account and package lifecycle](./owner-lifecycle.md)
- [Watch pack page and trading record](./watch-pack-and-trading-record.md)
- [The om guide](./om-guide.md)

## Surface inventory

Discovered 2026-11-26 from openmarket-registry `c0fbc81`, reconciled 2026-11-27 against `098a3de`,
and reconciled 2026-11-28 against `c263de6` (the commits since added the om guide, renamed the
request metrics and rewrote the trading record's page): the route chain in `src/server.ts`
(`createRegistryServer`), the route factories in `src/server/routes/`, `src/pages.ts`,
`src/pages-admin.ts`, `src/community/`, `src/trading-record-page.ts`, `src/guide/` and
`docs/features/`. "Bare lane" means a lane started with only the port, host and public URL, plus a
seed token where publishing is needed.

| User outcome | Product source path | Guide / sub-feature | Live verification | Prerequisite or gap |
|---|---|---|---|---|
| Browse the catalog, its empty state and its rows | `src/server.ts` `route` (home); `src/pages.ts` `renderHome` | [Catalog and search](./catalog-search.md) `catalog-empty`, `catalog-rows`, `catalog-cards` | 2026-11-28 `c263de6` | ranking between several rows and priced rows pending |
| Search from the page | `src/pages.ts` `renderHome`, `siteHeader` | [Catalog and search](./catalog-search.md) `catalog-search` | 2026-11-28 `c263de6` (no match and a hit) | ranking between several rows pending |
| Filter the catalog by kind | `src/pages.ts` `categoryCards`; `src/alert-share/kinds.ts` `listsKind` | [Catalog and search](./catalog-search.md) `catalog-kind` | 2026-11-28 `c263de6` (Indicators; Watch packs card) | the agents card needs `OM_REGISTRY_COMMUNITY=1` and watch-pack kinds on together |
| Agents closed to the public until the community is on | `src/alert-share/kinds.ts` `INTERNAL_ONLY_KINDS`, `internalOnlyKinds`; `src/server.ts` `internalOnlyGate`; `src/server/listing-predicate.ts` `isListingEligible` | [Package details](./package-details.md) `internal-only` | 2026-11-28 `c263de6` (anonymous 404s, owner reads) | an internal reader needs an SSO session, a chart web token, or a bearer the platform `/users/me` names internal; not driven |
| Search and Indicator store API | `src/server/routes/packages.ts` `search`, `storeFront`, `storeList` | [Catalog and search](./catalog-search.md) `search-api`, `store-api` | 2026-11-28 `c263de6` | official rows need a publisher mark |
| Publish a package | `src/server.ts` `publish`, `publishCore`, `ensureScopeOwnable` | [Publish a package](./publish-a-package.md) `publish-ok`, `publish-refused`, `listed-publish` | 2026-11-28 `c263de6` (ontology-pack, wrun-indicator, agent-plugin, recipe-only watch-pack) | followable watch packs, feeds and managed strategies pending |
| Validate and drafts | `src/server.ts` `publishValidate`, `putDraftRoute` | [Owner lifecycle](./owner-lifecycle.md) `publish-validate`, `drafts` | 2026-11-28 `c263de6` | drafts accept only the retired kscript-indicator kind, so only the refusal is drivable |
| Resolve and read package metadata | `src/server/routes/packages.ts` `getPackage`, `getSummary`, `postMetadata`; `src/server.ts` `getVersion`, `getVersionSource`, `resolveAliasRoute` | [Publish a package](./publish-a-package.md) `package-read`, `package-summary`, `version-read`, `alias-read` | 2026-11-28 `c263de6` | a resolving alias needs a migration-minted row; inline source needs a kind that carries it |
| Download a tarball | `src/server.ts` (`/tarballs`); `src/store/tarballs.ts` `FsTarballStore` | [Publish a package](./publish-a-package.md) `tarball-download` | 2026-11-28 `c263de6` | paid and custody rules pending |
| Package page | `src/server.ts` `packagePageAccess`; `src/pages.ts` `renderPackagePage` | [Package details](./package-details.md) | 2026-11-28 `c263de6` (ontology-pack, Indicator) | private, unlisted and managed variants pending |
| Share cards and preview tags | `src/share-card/serve.ts`, `render.ts`; `src/pages.ts` `layout` | [Package details](./package-details.md) `package-card`; [Public scope page](./public-scope.md) `scope-card` | 2026-11-28 `c263de6` | none |
| Publisher (scope) page | `src/server.ts` `route`; `src/pages.ts` `renderScopePage` | [Public scope page](./public-scope.md) | 2026-11-28 `c263de6` (empty listing and one row) | publisher marks pending |
| Report a package | `src/server/routes/reports.ts` `createReportRoutes` | [Report a package](./report-a-package.md) | 2026-11-28 `c263de6` (form, JSON door, limit) | the admin queue needs an admin session |
| Marketplace info and terms, and the `/policies` redirect | `src/pages.ts` `renderHowMarketplaceWorksPage`, `renderMarketplaceTermsPage`; `src/server.ts` (`/policies`) | [Marketplace pages](./marketplace-pages-and-artwork.md) | 2026-11-28 `c263de6` | none |
| Cover artwork collection | `src/server/routes/artwork.ts` `createArtworkRoutes`; `src/artwork/catalog.ts` | [Marketplace pages](./marketplace-pages-and-artwork.md) `artwork` | 2026-11-28 `c263de6` | none |
| Health and metrics, with request counts by route family | `src/server.ts` (health); `src/metrics.ts` `HTTP_REQUESTS_METRIC`; `src/server/request-metrics.ts` `requestLabels` | [Marketplace pages](./marketplace-pages-and-artwork.md) `health`, `request-metrics` | 2026-11-28 `c263de6` (`http_requests_total`, `unknown`, `preflight`) | a custom `METRICS_APP` not set; from source, `om_registry_executor_reads_total` now labels by `executor`, not driven |
| The om guide: index, chapters, videos, header link | `src/guide/` (`GUIDE_PAGES`, `guideMediaResponse`); `src/server.ts` (`/guide`); `src/pages.ts` `guideNavLink` | [The om guide](./om-guide.md) | 2026-11-28 `c263de6` (off and on, eight pages, video, pager, copy, media ranges) | the per-AI copy buttons and the clipboard contents not checked |
| Cover editor | `src/artwork/page.ts`; `artwork.getPage`, `postPage`, `putArtwork` | unmapped | live verification pending | session and scope owner |
| Discover home, agents directory, saved, surprise | `src/community/discover/*` | unmapped | live verification pending | `OM_REGISTRY_COMMUNITY=1`; saved needs a session |
| Reviews, discussion, votes, community report | `src/community/reviews`, `threads`, `moderation` | unmapped | live verification pending | community flag, session and CSRF |
| Key sign-in | `src/server/routes/key-login.ts`; `src/community/login-page.ts` | unmapped | live verification pending | `OM_REGISTRY_KEY_LOGIN=1` and a verifier; the session cookie is always `Secure` |
| SSO sign-in, sign-out, the signed-out page | `src/server.ts` `handleLogin`, `handleSso`, `handleLogout`, `handleSignedOutPage`; `src/sso-login.ts` | unmapped | live verification pending | `OM_REGISTRY_SSO` and the chart app, orange and service-auth URLs |
| Web tokens for the chart app | `src/server/routes/web-tokens.ts` | unmapped | live verification pending | `OM_REGISTRY_WEB_TOKENS=on` and SSO |
| Account page and listing edits | `src/server/routes/commerce.ts` `handleMePage`; `src/pages.ts` `renderMePage`; `src/server/routes/listing.ts` | unmapped | live verification pending | session |
| Owner catalog and terms acceptance | `src/server/routes/packages.ts` `getMe`, `getMePackages`; `acceptTermsRoute` | [Owner lifecycle](./owner-lifecycle.md) `me`, `me-packages`, `terms-accept` | 2026-11-28 `c263de6` | none |
| Owner lifecycle: yank, visibility, delete, listing, plan | `src/server.ts` `yankVersionRoute`, `patchPackage`, `deletePackageRoute`; `src/server/routes/listing.ts`, `plan.ts` | [Owner lifecycle](./owner-lifecycle.md) `yank`, `visibility`, `delete` | 2026-11-28 `c263de6` (yank, visibility, delete) | listing edits and plans pending (owner bearer) |
| Receipts, follow, seen, wanted | `src/server.ts` `installReceiptRoute`, `followReceiptRoute`; `src/server/routes/package-follow.ts`, `package-reach.ts`, `wanted.ts` | unmapped | live verification pending | bearer; follow and wanted need watch-pack kinds; from source, install receipts answer 404 unless watch-pack kinds or the community is on |
| Devices: enroll, approve, list, rename, revoke | `src/server/routes/devices.ts`, `devices-pages.ts` | unmapped | live verification pending | bearer and an https public URL (`canonicalRegistryOrigin`) |
| Saved watches and watch salt | `src/server/routes/saved-watches.ts`, `watch-salt.ts` | unmapped | live verification pending | own-account bearer |
| Grants, groups, Access API, access keys | `src/server/routes/access-api.ts`, `package-access.ts`, `package-access-keys.ts`, `owner-access-keys.ts` | unmapped | live verification pending | owner bearer; mostly Indicators |
| Sharing: invite links, access requests, hub, reach | `src/server/routes/package-sharing.ts`, `sharing-hub.ts`, `package-reach.ts` | unmapped | live verification pending | bearer; reach needs `OM_REGISTRY_REACH` |
| Discord and Whop connectors | `src/server/routes/connections.ts`; `src/connectors/*` | unmapped | live verification pending | `OM_REGISTRY_CONNECTORS=on` (fixtures through `OM_REGISTRY_CONNECTORS_FIXTURES`) |
| Browser publish handoff | `src/server/routes/web-publish.ts` | unmapped | live verification pending | `OM_REGISTRY_WEB_PUBLISH=on`, SSO and the chart app URL |
| Marketplace buy and sell pages, the public seller page | `src/server/routes/commerce.ts` `createCommerceRoutes`, `handleSellerPublicPage` (`/seller/:id`) | unmapped | live verification pending | `OM_COMMERCE=1` and orange |
| Report a marketplace listing | `src/server.ts` `handleListingReportPage` | unmapped | live verification pending | `OM_COMMERCE=1` and orange |
| Commerce and managed billing doors | `src/server/routes/package-grants-door.ts`, `package-sale-door.ts`, `managed-door.ts` | unmapped | live verification pending | service key on the commerce roster |
| Managed strategies | `src/server/routes/managed.ts` `managedApi` | unmapped | live verification pending | subscriber or owner bearer |
| Watch-pack package page | `src/watch-pack-page.ts`; `src/watch-packs.ts` | [Watch pack page](./watch-pack-and-trading-record.md) `watch-page`, `catalog-watch-row` | 2026-11-28 `c263de6` (recipe-only paper pack) | followable and shared packs need a device proof, the topics service and the relay |
| A trading watch's record on its page | `src/server/routes/trading-record.ts`; `src/trading-record-page.ts` `tradingRecordPanels`, `HIDDEN_WORDS`; `src/store/trading-records.ts`; `src/server.ts` `dropStaleTradingRecords` | [Watch pack page](./watch-pack-and-trading-record.md) `record-empty`, `record-shown`, `record-door`, `record-dropped` | 2026-11-28 `c263de6` (paper record with a loss and signals; refusals; a kind change) | `record-hidden` pending: real-money records need a signed wallet proof and venue access (`src/trading-record-verify.ts`), and a kind change drops the record before the page can say so |
| Feed (live-series) package page | `src/feeds/feed-page.ts`; `src/feeds/publish-check.ts` | unmapped | live verification pending | `FEEDS_PUBLISH_ENABLED=on`, `FEEDS_RELAY_ORIGIN`, and a relay that answers `GET /api/v2/feeds/{scope}/{name}` with the publisher as owner, or the publish answers 422 `feed_missing` |
| Internal and platform doors | `src/server/routes/stats-door.ts`, `paint-verdict-door.ts`; `src/server.ts` `mirrorPublish`, `enterpriseWrunCatalog` | unmapped | live verification pending | service keys on the named rosters |
| Admin moderation | `src/server/routes/admin-pages.ts`; `src/pages-admin.ts`; `src/server/routes/moderation.ts` | unmapped | live verification pending | session for an account in `OM_REGISTRY_ADMIN_ACCOUNTS` |
| Search judge and miss log | `src/search/judge.ts` | unmapped | live verification pending | community, search v2 and judge accounts |

## Known product gaps

- With only seed tokens configured, a request with no bearer or an unknown bearer answers 503
  `verifier_not_configured` rather than 401 (2026-11-26; seen again 2026-11-27 and 2026-11-28).
- The how-it-works page's h1 still names "kScript", a retired name (2026-11-26; seen again
  2026-11-27).
- The site footer's "Report abuse" link points to `#` on every page (2026-11-26; seen again
  2026-11-27).
- A missing package, a hidden package or an unclaimed scope answers a browser with a JSON error
  body (`application/json`, `{"error":{"code":"not_found",…}}`) instead of a page (2026-11-27;
  seen again 2026-11-28, and `/guide` on a lane without the guide answers the same).
