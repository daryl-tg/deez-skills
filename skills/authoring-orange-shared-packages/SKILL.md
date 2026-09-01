---
name: authoring-orange-shared-packages
description: Use when creating or changing a package in the orange-shared workspace (/Users/dboon/Gitlab/orange-shared, @orangecharts npm scope) — adding a shared types/schema/constants module, setting up exports or builds, publishing or bumping a version, or iterating a consumer against an unpublished change.
---

# Authoring orange-shared packages

## Overview

orange-shared is a pnpm workspace of independently-versioned `@orangecharts/*` packages, published restricted to npmjs.org (token from `~/.npmrc`). Core principle: **the conventions are already encoded in the repo and its consumers — copy the precedents below, don't invent.**

Precedents to read before scaffolding:

- `packages/observability` — per-module subpath exports, plain `tsc`, `prepublishOnly` build.
- `@orangecharts/orange-v2-pb-common` (in orange-v2-backend; also in kiyotaka-frontend's node_modules) — the dual ESM/CJS template: `dist/cjs` + `dist/esm`, two `tsc` passes, one `exports` map with `import`/`require` conditions. Proven in the Vite app.

## Recipe: new type/contract package

Every step is required; the failure mode of each is silent.

1. **Layout**: `packages/<name>/{src/, package.json, tsconfig.json, tsconfig.esm.json, README.md}`. Contract packages carry **zero runtime `dependencies`** — pure data, pure functions, no framework imports. `devDependencies`: `typescript` only (release.sh strips devDeps from the published tarball).
2. **package.json**: `"version": "0.0.0"` (release.sh mints the real one — see Releasing), `"private": false`, `"publishConfig": {"access": "restricted"}`, `"sideEffects": false`, `"files": ["dist"]`, `"main"`/`"module"`/`"types"` pointing into `dist/cjs`/`dist/esm`.
3. **Exports map**: one `"."` entry for the barrel **plus a subpath entry for every module consumers deep-import** (`"./tools"`, `"./tool-field-specs"`, …), each with `import`/`require` conditions carrying their own `types`. Unlike the `@/` source alias this replaces, a deep import that is not in the exports map does not resolve at all. Modules that are internal-only get **no** subpath entry — the map is also how you keep them private.
4. **Dual build**: `tsconfig.json` (CJS: extends `../../tsconfig.base.json`, `outDir: dist/cjs`) and `tsconfig.esm.json` (`module: ES2022`, `moduleResolution: Bundler`, `outDir: dist/esm`). Scripts: `"build": "npm run build:cjs && npm run build:esm && npm run build:markers"`, `"typecheck": "tsc --noEmit"`, `"prepublishOnly": "npm run build"` (chain `&& npm test` when a test script exists). `build:markers` writes `dist/cjs/package.json` `{"type":"commonjs"}` and `dist/esm/package.json` `{"type":"module"}` — without them plain-Node ESM consumers get MODULE_TYPELESS_PACKAGE_JSON reparse warnings (pb-common ships with this latent gap; don't copy it).
5. **Relative imports inside `src/` must carry `.js`** (`from './types.js'`). `tsc` never rewrites specifiers; extensionless ESM emit typechecks fine under `moduleResolution: Bundler` and then fails at runtime for plain-Node ESM consumers.
6. **Self-consistency checks travel with the contract.** If the source folder had internal invariants (alias targets resolve to real keys, key sets closed over each other), port them as a `test` script (a plain node script beats a framework) and chain it into `prepublishOnly`. A contract package published without its checks has silently lost its guard.
7. **README**: keep the contract's "why", add a provenance line (`moved from <repo> src/... @ <commit>`), and add a row to the root `README.md` package table.
8. **Verify**: `pnpm install` at the workspace root, then `pnpm --filter @orangecharts/<name> build && pnpm --filter @orangecharts/<name> typecheck` (and `test`). Inspect that `dist/cjs` and `dist/esm` both exist.

## Releasing

`./release.sh <pkg> <patch|minor|major>` is the ONLY release path: bump → build → commit → tag `<pkg>/vX.Y.Z` → publish (devDeps stripped) → push. It requires a clean `main` and works for the **first** release too: commit the package at `0.0.0`, then `./release.sh <pkg> minor` publishes `0.1.0`. Never hand-edit `version`, never run bare `npm publish` (skips the devDep strip, tag, and push; the script also rolls back on failure).

## Consumers

- Pin **exact** versions (`"0.1.0"`, never `^`/`~`) — house style; `kscript`, `orange-v2-pb-common`, `titan-charts-next` are all exact pins.
- kiyotaka-frontend's `pnpm-workspace.yaml` already has `minimumReleaseAgeExclude: ['@orangecharts/*']`, so a fresh publish installs immediately. No workspace config change needed.

## Local dev loop against unpublished changes

The sanctioned pattern is the **dev-serve-only sibling-source alias** already in kiyotaka-frontend's `vite.config.ts` (see the `titan-dev` and `kscriptWorktreeAliasEntry` blocks): a `resolve.alias` pair gated on `existsSync(<sibling src>)` AND `command === 'serve'`, pointing `@orangecharts/<pkg>` at `../orange-shared/packages/<pkg>/src/index.ts` and `@orangecharts/<pkg>/(.*)` at `$1.ts`, plus the package in `optimizeDeps.exclude`. Vite transpiles the `.ts` source directly — no build step, inert when the sibling checkout is missing, and **production builds never bundle sibling source** (that's what the `serve` gate is for; copy it).

`pnpm link --global` also works but Vite's dep-optimizer caches symlinked deps — expect to nuke `node_modules/.vite` and restart after edits.

Before the consumer change merges: publish via release.sh and move the consumer to the new exact pin. Never commit a `file:`/link override in a lockfile or package.json.

## Common mistakes

| Mistake | Consequence |
|---|---|
| Hand-editing `version` / bare `npm publish` | Version–tag drift; devDeps in the tarball; no rollback |
| Missing subpath in `exports` | Consumer deep import fails to resolve at all |
| Extensionless relative imports in src | ESM output breaks plain-Node consumers at runtime |
| Caret/tilde pin in a consumer | Violates the exact-pin convention every @orangecharts dep follows |
| Skipping the self-consistency test script | Contract invariants silently unguarded after the move |
| Alias/dev override without the `serve` gate | Production build silently bundles sibling source |
