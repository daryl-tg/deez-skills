---
name: kiyotaka-user-docs
description: >-
  Carry a kiyotaka-frontend user-facing change into its docs in the same
  cycle. Use when shipping a retail-visible feature or setting, when asked to
  "document X" or "update the user guides", or when docs are stale after a UI
  change. Guides live in the landing repo (kiyotaka-landing-page-v2), so this
  spans two repos.
---

## Scope

A user-facing change in `kiyotaka-frontend` must carry its docs in the same
cycle. The docs are NOT in that repo: the guide content lives in the
**landing** repo `kiyotaka-landing-page-v2`
(`app/content/user-guides/`, GitBook-flavored markdown). This skill takes a
frontend change across to those docs. It produces TWO branches/MRs — the
feature in the frontend, the docs in landing — because they are different
repos.

Not user-facing (internal refactor, dev-gated, backend-only)? Say so in the
MR description and skip.

## Locate the landing repo

Docs edits happen in a `kiyotaka-landing-page-v2` checkout. Look for it as a
sibling of, or near, the frontend checkout. If there is no local clone, ask
the user for the path rather than cloning blindly. Make every docs edit on a
feature branch there — never on its `main`.

## What a docs change carries

1. **The guide page** — new or updated markdown under
   `app/content/user-guides/<section>/`, matching the existing page voice and
   GitBook conventions (`{% hint %}`, `{% stepper %}`, `<table data-view="cards">`).
   Draw every fact from the live app, never from memory or an old MR.
2. **Both navigation sources, kept in sync.** Adding, moving, or removing a
   page means editing BOTH `app/content/user-guides/SUMMARY.md` (the website
   nav) AND `app/content/user-guides/llms.toc.yaml` (the machine-readable
   index). Touch only one and they drift silently. Verify with
   `pnpm build:llms` (expect 0 orphans).
3. **Screenshots**, only if the UI changed — never hand-crop. Render them with
   the `docs-screenshot` skill / the `qa/docs-shots` engine in the frontend,
   then re-home the PNGs into landing `public/learn/<section>/`
   (strip the `@2x` suffix), and reference each image from the markdown by its
   root-absolute path (`/learn/<section>/<name>.png`). The guides are served at
   `/learn`, so public assets and image URLs use `/learn` — even though the
   content source dir is still `app/content/user-guides/`.
4. **The release note is automatic.** The release-notes bot writes it from
   your commit messages — do not hand-write a release entry. For a flagship
   launch, a human adds hero media + `featureSpotlight: true` to the release
   entry before merging; the bot writes copy only.

## Conventions

- Brand is **OpenMarket** in prose (the platform, the API host
  `api.openmarket.xyz`, everything). The one deliberate exception: the color
  theme literally named "Kiyotaka" — a product feature name, not a brand ref.
- Screenshots are generated, never edited by hand; a clean runner exit is not
  proof — open the PNG.
- Never commit to `main` or `production` in either repo. Land on feature
  branches and open MRs; the two MRs (frontend feature + landing docs) merge
  independently.
