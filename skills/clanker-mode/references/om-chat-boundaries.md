# OM Chat boundaries

## One workspace, two hosts, one shared package

`openmarket-chat` is a single Bun workspace. It stopped being two forks in
`f190644c`; there is no cloud repo to port to and no copy to keep in step.

| Path | Owns |
|---|---|
| `packages/chat-ui` | **All** UI components, screens, styles, assets, and common frontend state |
| `src/` (repo root) | The `/rooms` host: desktop and daemon boot, transport, `App.tsx` / `main.tsx` / `lib/media-ui.tsx` |
| `apps/cloud/` | The `/chat/` host: hosted boot, authentication, path routing, transport adapters |
| `@openmarket/rooms-client` (npm) | Browser-safe shared protocol: wire types, request clients, domain models |

**A change to `packages/chat-ui` changes both hosts at once.** That is the
whole point of the refactor, and it is also the trap: it is no longer possible
to change one host's rendering without changing the other's. Name which hosts a
change touches before editing, and prove each one — **principle-prove-every-host**.

Everything under a host's own `src/` that is not `App.tsx`, `main.tsx` or
`lib/media-ui.tsx` is a one-line re-export facade. `src/components/Shell.tsx`
is one line; the real 4512 are in `packages/chat-ui/src/components/Shell.tsx`.
Grep the package, not the host. Reading a facade and concluding the code is
gone is the standard way to waste an hour here.

Shared code reaches host capabilities only through `@openmarket/chat-host`,
never by importing a host's source directly. Never re-derive protocol behavior
in a consumer: it belongs in `packages/rooms-client` in the monorepo, published,
then repinned here.

**Do not fork a screen to make a host different.** `test/chat-ui-workspace.test.ts`
fences renderer ownership, the facades, dependency boundaries and stylesheet
order. Extend a host adapter for a capability difference. Do not widen that
test's app-local renderer exceptions, and do not restore a parity manifest or
copy-based sync tooling — both were deleted on purpose.

## Where the code lives

The source of truth is GitLab `openmarketxyz/frontend/openmarket-chat`, checked
out at `~/gitlab/openmarket-chat`. Review requests are MRs through **glab**.
Confirm `git remote get-url origin` names that remote before editing: it is
the only thing that tells the live checkout from the deprecated one.

- **Worktrees go at `~/gitlab/openmarket-chat-<slug>`,** beside the checkout.
  `tsconfig.json` resolves `@cli/*` from `../openmarket-internal`, then
  `../openmarket`, and `~/gitlab/openmarket-internal` is a symlink to
  `~/github/openmarket-internal`. A worktree anywhere else, including under
  `~/.local/state/om-chat-feature*/`, cannot typecheck anything that imports the
  daemon. Evidence still lives under `~/.local/state/om-chat-feature/`; only the
  worktrees moved.
- **Point every rig at its tree explicitly.** The daemon's `scripts/dev.ts`
  falls back to `../openmarket-chat` from `openmarket-internal`, which is the
  deprecated checkout. A lane that serves a worktree sets
  `OM_DEV_<PROFILE>_CHAT_REPO`, or `OM_DEV_CHAT_REPO` in its own environment,
  to that worktree. A shell value beats the profile key, which beats the base
  key in `.env.local`.
- **Deprecated, never used.** `~/github/openmarket-chat` and every
  `~/github/openmarket-chat-<slug>` worktree are GitHub-era history: never build,
  branch, edit, or drive from them. `openmarket-chat-cloud` is not used at all.
  Its chart renders nothing and it publishes no image.
- `openmarket-internal`, home of the daemon and `packages/rooms-client`, is
  still GitHub, so `gh` is still correct there.

## Retired, and dead if you see it cited

`tools/parity-manifest.json`, `tools/sync-shared.ts`, the shared-style coverage
ratchet and the import-closure fences are **deleted**. Any instruction to run
`sync-shared.ts --diff`, refresh a manifest, or cite a cross-fork drift result
cannot be carried out. Sharing is a package import; the import is the fence.

## Gates

Both, from the workspace root, whenever shared code changed:

```bash
bun install --frozen-lockfile     # root bun.lock covers both hosts; never pnpm
bun run lint && bun run typecheck && bun run build
bun --tsconfig-override ./tsconfig.json tools/check-dist.ts
bun --tsconfig-override ./tsconfig.json tools/test-fast.ts
bun run verify:cloud
```

The full install needs `NPM_READ_TOKEN` and `ORANGECHARTS_NPM_READ_TOKEN` in the
ignored `.env`. A daemon-only install skips the cloud host:
`bun install --frozen-lockfile --filter '!@openmarket/chat-cloud'`. Both repos
run Bun 1.3.14.

`bun --tsconfig-override` always prints `Internal error: directory mismatch ...
tsconfig.json`. It is harmless, and the deprecated checkout prints it too. Read
the exit code, never that line.

Canonical UI tests live in the root `test/`. Tests of a host's own wire paths,
authentication, routing, artifact shape and unavailable capabilities stay with
that host (`apps/cloud/test/`). Select the consuming host's tsconfig for any
direct `bun test` or tool invocation (`--tsconfig-override`).

Never green a failure by adding a skip, a baseline entry, a retry, or a longer
timeout. Isolate baseline failures against the branch point; a partially failing
suite is not green.

`@openmarket/rooms-client` is pinned in **three** places and they must agree:
the root `package.json`, `apps/cloud/package.json`, and
`packages/chat-ui` `peerDependencies`.

## Shipping

**Landing on `main` ships the hosted app.** A push or merge to the protected
`main` publishes the `/chat/` images automatically once `cloud:contract` passes,
per the repo's `docs/CLOUD_RELEASE.md`. So main must stay releasable, and a
merge is a production release, not a bookkeeping step. The image builds from
`apps/cloud` and the chart is `charts/openmarket-chat`.

`/rooms` ships separately. `openmarket-internal`'s
`.github/workflows/release-self-hosted.yml` embeds this repo's `main` into the
`om` binaries at a tagged release, taking its GUI source from the repo variable
`ROOMS_GUI_SOURCE`. Developers never touch that variable.

## Services and ports

Use the shared `openmarket` HTTP MCP at `http://127.0.0.1:31338/mcp`. Never
spawn an operator stdio server. `openmarket-chat` stays a session-local stdio
child and is run-owned cleanup input.

`8097` is the operator's local dev server: never bind, target, reuse, or stop
it. `31417` is the operator's source dev daemon, the `scripts/dev.ts` default,
and it is not tunnelled: never bind it from a lane either. Agent-only test servers take an allocated `18097`–`18197` port, recorded in
the run ledger, and are stopped only when run-owned. See
**principle-bind-assigned-ports** for the full table.

For daemon behavior use the real daemon-served rig. Use Vite directly only for
layout-only work.

## Git boundaries

Do not fetch, pull, merge, push local `main`, close a todo, deploy, or alter the
local `main` branch. Completion pushes only the promoted feature branch, creates
or reuses its review request, and announces that linked request.

The final branch is **checked out in the primary worktree, not merged into
main**. See **principle-promote-to-the-main-worktree**.
