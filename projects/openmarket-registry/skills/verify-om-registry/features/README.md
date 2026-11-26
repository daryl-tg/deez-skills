# OpenMarket registry verification map

The maintained source for proving user-visible registry behavior. Read this index before driving,
then use the matching feature file as the recipe.

## Baseline preconditions

- Run the lane from a disposable openmarket-registry worktree with a fresh
  `bun install --frozen-lockfile` under Bun 1.4.3, and start it with `$CR up` on an assigned port in
  18097-18197. Bind `127.0.0.1`.
- A lane that publishes starts with a seed token:
  `OM_REGISTRY_STATIC_TOKENS='{"dev-token":{"account_id":"acct-dev","tier":"pro"}}' $CR up`.
  Leave `OM_REGISTRY_PLATFORM_API_URL` and `OM_REGISTRY_AUTH_BASE_URL` unset.
- `$CR doctor` confirms the health route, the port owner and the working checkout.
- The lane holds metadata in memory and starts empty; tarballs go to `./data/tarballs` in the
  worktree.
- Never drive an instance this run did not start.

## Driving conventions

- Prefer ARIA roles and accessible names over CSS selectors or coordinates.
- Browser actions go through `$CR browser`; API commands go through `$CR cli --`.
- Seed packages through the real `POST /v1/publish` route, never through internal setters or test
  helpers.
- Write `<port>` as the lane's port and `<port+1>` as its metrics port.

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

## Surface inventory

Discovered 2026-11-26 from openmarket-registry `c0fbc81`: the route chain in `src/server.ts`
(`createRegistryServer`), the route factories in `src/server/routes/`, `src/pages.ts`,
`src/pages-admin.ts`, `src/community/` and `docs/features/`. "Bare lane" means a lane started with
only the port, host and public URL, plus a seed token where publishing is needed.

| User outcome | Product source path | Guide / sub-feature | Live verification | Prerequisite or gap |
|---|---|---|---|---|
| Browse the catalog and its empty state | `src/server.ts` `route` (home); `src/pages.ts` `renderHome` | [Catalog and search](./catalog-search.md) `catalog-empty` | 2026-11-26 `c0fbc81` | rows need a listed kind |
| Search from the page | `src/pages.ts` `renderHome`, `siteHeader` | [Catalog and search](./catalog-search.md) `catalog-search` | 2026-11-26 `c0fbc81` (no-match only) | ranking needs listed rows |
| Filter the catalog by kind | `src/pages.ts` `categoryCards`; `src/alert-share/kinds.ts` `listsKind` | [Catalog and search](./catalog-search.md) `catalog-kind` | live verification pending | needs listed rows (agent-plugin or `REGISTRY_WRUN_KINDS=on` Indicators) |
| Search and Indicator store API | `src/server/routes/packages.ts` `search`, `storeFront`, `storeList` | [Catalog and search](./catalog-search.md) `search-api` | 2026-11-26 `c0fbc81` (search) | store views need wrun rows |
| Publish a package | `src/server.ts` `publish`, `publishCore`, `ensureScopeOwnable` | [Publish a package](./publish-a-package.md) `publish-ok`, `publish-refused` | 2026-11-26 `c0fbc81` (ontology-pack) | listed kinds not yet published |
| Validate and drafts | `src/server.ts` `publishValidate`, `putDraftRoute` | [Publish a package](./publish-a-package.md) | live verification pending | seed token |
| Resolve and read package metadata | `src/server/routes/packages.ts` `getPackage`, `getSummary`, `postMetadata`; `src/server.ts` `getVersion`, `getVersionSource`, `resolveAliasRoute` | [Publish a package](./publish-a-package.md) `package-read` | 2026-11-26 `c0fbc81` (`GET /v1/packages/:s/:n`) | summary, version, source, metadata and aliases pending |
| Download a tarball | `src/server.ts` (`/tarballs`); `src/store/tarballs.ts` `FsTarballStore` | [Publish a package](./publish-a-package.md) `tarball-download` | 2026-11-26 `c0fbc81` | paid and custody rules pending |
| Package page | `src/server.ts` `packagePageAccess`; `src/pages.ts` `renderPackagePage` | [Package details](./package-details.md) | 2026-11-26 `c0fbc81` (ontology-pack) | agent, Indicator, managed, watch-pack and feed variants pending |
| Share cards and preview tags | `src/share-card/serve.ts`, `render.ts`; `src/pages.ts` `layout` | [Package details](./package-details.md) `package-card` | 2026-11-26 `c0fbc81` (package card) | scope card pending |
| Publisher (scope) page | `src/server.ts` `route`; `src/pages.ts` `renderScopePage` | [Public scope page](./public-scope.md) | 2026-11-26 `c0fbc81` (empty listing) | rows need a listed kind |
| Report a package | `src/server/routes/reports.ts` `createReportRoutes` | [Report a package](./report-a-package.md) | 2026-11-26 `c0fbc81` (form) | JSON door and limit pending |
| Marketplace info and terms | `src/pages.ts` `renderHowMarketplaceWorksPage`, `renderMarketplaceTermsPage` | [Marketplace pages](./marketplace-pages-and-artwork.md) | 2026-11-26 `c0fbc81` | none |
| Cover artwork collection | `src/server/routes/artwork.ts` `createArtworkRoutes`; `src/artwork/catalog.ts` | [Marketplace pages](./marketplace-pages-and-artwork.md) `artwork` | 2026-11-26 `c0fbc81` | none |
| Health and metrics | `src/server.ts` (health); `src/metrics.ts` | [Marketplace pages](./marketplace-pages-and-artwork.md) `health` | 2026-11-26 `c0fbc81` | none |
| Cover editor | `src/artwork/page.ts`; `artwork.getPage`, `postPage`, `putArtwork` | unmapped | live verification pending | session and scope owner |
| Discover home, agents directory, saved, surprise | `src/community/discover/*` | unmapped | live verification pending | `OM_REGISTRY_COMMUNITY=1`; saved needs a session |
| Reviews, discussion, votes, community report | `src/community/reviews`, `threads`, `moderation` | unmapped | live verification pending | community flag, session and CSRF |
| Key sign-in | `src/server/routes/key-login.ts`; `src/community/login-page.ts` | unmapped | live verification pending | `OM_REGISTRY_KEY_LOGIN=1` and a verifier; the session cookie is always `Secure` |
| SSO sign-in, sign-out | `src/server.ts` `handleLogin`, `handleSso`, `handleLogout`; `src/sso-login.ts` | unmapped | live verification pending | `OM_REGISTRY_SSO` and the chart app, orange and service-auth URLs |
| Web tokens for the chart app | `src/server/routes/web-tokens.ts` | unmapped | live verification pending | `OM_REGISTRY_WEB_TOKENS=on` and SSO |
| Account page and listing edits | `src/server/routes/commerce.ts` `handleMePage`; `src/pages.ts` `renderMePage`; `src/server/routes/listing.ts` | unmapped | live verification pending | session |
| Owner catalog and terms acceptance | `src/server/routes/packages.ts` `getMe`, `getMePackages`; `acceptTermsRoute` | unmapped | live verification pending | bearer (a seed token can drive it) |
| Owner lifecycle: yank, visibility, delete, listing, plan | `src/server.ts` `yankVersionRoute`, `patchPackage`, `deletePackageRoute`; `src/server/routes/listing.ts`, `plan.ts` | unmapped | live verification pending | owner bearer (a seed token can drive it) |
| Receipts, follow, seen, wanted | `src/server.ts` `installReceiptRoute`, `followReceiptRoute`; `src/server/routes/package-follow.ts`, `package-reach.ts`, `wanted.ts` | unmapped | live verification pending | bearer; follow and wanted need watch-pack kinds |
| Devices: enroll, approve, list, rename, revoke | `src/server/routes/devices.ts`, `devices-pages.ts` | unmapped | live verification pending | bearer and an https public URL (`canonicalRegistryOrigin`) |
| Saved watches and watch salt | `src/server/routes/saved-watches.ts`, `watch-salt.ts` | unmapped | live verification pending | own-account bearer |
| Grants, groups, Access API, access keys | `src/server/routes/access-api.ts`, `package-access.ts`, `package-access-keys.ts`, `owner-access-keys.ts` | unmapped | live verification pending | owner bearer; mostly Indicators |
| Sharing: invite links, access requests, hub, reach | `src/server/routes/package-sharing.ts`, `sharing-hub.ts`, `package-reach.ts` | unmapped | live verification pending | bearer; reach needs `OM_REGISTRY_REACH` |
| Discord and Whop connectors | `src/server/routes/connections.ts`; `src/connectors/*` | unmapped | live verification pending | `OM_REGISTRY_CONNECTORS=on` (fixtures through `OM_REGISTRY_CONNECTORS_FIXTURES`) |
| Browser publish handoff | `src/server/routes/web-publish.ts` | unmapped | live verification pending | `OM_REGISTRY_WEB_PUBLISH=on`, SSO and the chart app URL |
| Marketplace buy and sell pages | `src/server/routes/commerce.ts` `createCommerceRoutes` | unmapped | live verification pending | `OM_COMMERCE=1` and orange |
| Report a marketplace listing | `src/server.ts` `handleListingReportPage` | unmapped | live verification pending | `OM_COMMERCE=1` and orange |
| Commerce and managed billing doors | `src/server/routes/package-grants-door.ts`, `package-sale-door.ts`, `managed-door.ts` | unmapped | live verification pending | service key on the commerce roster |
| Managed strategies | `src/server/routes/managed.ts` `managedApi` | unmapped | live verification pending | subscriber or owner bearer |
| Watch-pack and feed package pages | `src/watch-pack-page.ts`; `src/feeds/feed-page.ts` | unmapped | live verification pending | `WATCH_PACK_KINDS_ENABLED=on` (a relay and an https origin) or `FEEDS_PUBLISH_ENABLED` |
| Internal and platform doors | `src/server/routes/stats-door.ts`, `paint-verdict-door.ts`; `src/server.ts` `mirrorPublish`, `enterpriseWrunCatalog` | unmapped | live verification pending | service keys on the named rosters |
| Admin moderation | `src/server/routes/admin-pages.ts`; `src/pages-admin.ts`; `src/server/routes/moderation.ts` | unmapped | live verification pending | session for an account in `OM_REGISTRY_ADMIN_ACCOUNTS` |
| Search judge and miss log | `src/search/judge.ts` | unmapped | live verification pending | community, search v2 and judge accounts |

## Known product gaps

- With only seed tokens configured, a request with no bearer or an unknown bearer answers 503
  `verifier_not_configured` rather than 401 (2026-11-26).
- The how-it-works page's h1 still names "kScript", a retired name (2026-11-26).
- On a package page the footer's "Report abuse" link points to `#` (2026-11-26).
