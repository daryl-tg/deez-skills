---
name: migrating-types-to-orange-shared
description: Use when centralising duplicated, hand-copied, or drift-guarded types/constants from kiyotaka-frontend (or another consumer repo) into an @orangecharts package in orange-shared as the single source of truth — e.g. src/shared/chart-schema or any "shared copy" folder synced by a check script.
---

# Migrating types to orange-shared

## Overview

A "shared copy" folder in a consumer repo is rarely one thing. **Classify every exported symbol before moving anything**, because the two classes need opposite treatment:

- **Category A — the folder is already the live source.** Repo code imports the symbol from the folder. Migration = move to the package + rewrite specifiers. Mechanical.
- **Category B — the folder is a MIRROR.** The value the app actually runs on is defined elsewhere in the repo (class fields, constants files, registries), and a drift script compares the two by text extraction. Migration must **invert the dependency** — the repo consumes the package value — or you have only relocated the duplication and the package never becomes the truth.

Classification predicate, per symbol: *who defines the value the running app uses?* If the answer is not the shared folder, it's Category B.

**REQUIRED SUB-SKILL:** `authoring-orange-shared-packages` for everything package-side (scaffold, exports map, dual build, release.sh, exact pins, dev loop).

## Step 0 — Gap audit (the deliverable that prevents misses)

Build an inventory table BEFORE moving anything. Nothing moves until every row has a home:

| Row type | Columns |
|---|---|
| Every exported symbol | module → consumers found → Category A/B → post-migration home (package / stays in repo / deleted-with-reason) |
| Every drift-guard check | what it compares → post-migration enforcement (import/type-level / retargeted script check / package self-test) |

The consumer sweep MUST cover the **whole repo**, not `src/` — the misses live outside it:

- `scripts/*.mjs` and `package.json` scripts — text-extraction guards read the folder **from disk**; a grep of `src/` never finds them
- CI config and husky hooks that run those scripts
- tests: `vi.mock('<specifier>')` strings, dynamic `await import(...)`, and any `tests/` subtree that mirrors the folder's path (it must be relocated when the folder dies)
- comments ("keep in sync with `shared/...`") and doc references
- `qa/` probes and codegen/tooling scripts

## Inversion recipes (Category B)

- **Literal class/registry fields** → read from the package constant: `overlayType = INDICATOR_TYPES.KEY.overlayType`.
- **Duplicated standalone constant** → re-export or derive from the package value; delete the local literal.
- **Keyed map whose VALUES must stay repo-side** (script bodies, icon components, theme lookups) → keep the map, type it `satisfies Record<PackageKeyType, V>` so a missing/extra key is a compile error instead of a text-diff finding.
- **Genuinely un-invertible checks** (repo-asset coverage like "every tool has an icon", vocabulary sweeps over repo source) → keep a slimmed drift script, retargeted to read the **installed package** for its vocabulary.

## Cutover rules

- Pin the package at an **exact version** (no `^`), per house convention.
- Rewrite every specifier the audit found — including `vi.mock` strings, dynamic imports, and comments.
- Relocate `tests/` subtrees that mirrored the deleted folder.
- Delete the folder outright — **no re-export shim**. A "temporary" shim keeps the old path importable, so new code keeps using it and the migration never finishes.
- Rewrite the drift script, keeping its npm-script name: delete each check now enforced by imports/types (each deletion justified in the audit table), keep + retarget the irreducible ones. Never leave it reading a deleted path — and never delete it wholesale, since the irreducible checks are the only guard left.

## Verification

- `grep -rn "<old path>" . --exclude-dir=node_modules` at the repo root → zero hits (catches scripts/, docs, comments — not just src/).
- Consumer repo: typecheck (`vue-tsc`), `pnpm test:node`, full `pnpm test`, the retargeted check script, and a production build.
- Package repo: build + typecheck + self-consistency test green before `release.sh`.
- Headless smoke of the load-bearing UI paths the types drive (use `headless-probe` / `verify-chart-fix`).

## First application: chart-schema

The audited Category A/B map, drift-guard disposition table, and FE cutover file list for migrating `src/shared/chart-schema` → `@orangecharts/chart-schema`: see [chart-schema-first-migration.md](chart-schema-first-migration.md).

## Common mistakes

| Mistake | Reality |
|---|---|
| Move folder + rewrite imports, done | Category B untouched — the package is a relocated copy, not the truth |
| Verification grep scoped to `src/` (or `src tests`) | The drift script in `scripts/` is left reading a deleted path |
| "Temporary" re-export shim at the old path | Lives forever; new code keeps importing the dead path |
| Deleting the drift script because "the package is the truth now" | Repo-asset checks and vocabulary sweeps have no other guard |
| Trusting the folder's README/barrel for the consumer list | Deep-path-only and mock/dynamic-import consumers don't appear in either |
| Deciding build format / first-publish per agent intuition | Both are pinned by `authoring-orange-shared-packages` — dual ESM/CJS, release.sh from 0.0.0 |
