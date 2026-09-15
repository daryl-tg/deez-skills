---
name: bump-rc
description: Release a new @openmarket/rooms-client version — pick the bump from what actually changed, run the repo's release script, then repin all three places the OM Chat workspace declares it. Trigger: /bump-rc [version]
---

# bump-rc — release rooms-client and repin its consumers

`@openmarket/rooms-client` lives in `~/github/openmarket-internal` and is
consumed by the `openmarket-chat` workspace, which pins it **exactly, in three
places that must agree**:

| File | Field | Why it is there |
|---|---|---|
| `package.json` | `dependencies` | the `/rooms` host |
| `apps/cloud/package.json` | `dependencies` | the `/chat/` host |
| `packages/chat-ui/package.json` | `peerDependencies` | the shared UI, which must resolve to whatever its hosts installed |

Before `f190644c` these were two separate repos on two package managers. They
are one Bun workspace now: one `bun.lock`, one install, **never pnpm**. Two
agreeing pins and one stale peer is the failure this skill exists to prevent —
the install resolves, and the peer warning is the only thing that says so.

Publishing without repinning leaves the workspace on the old version; repinning
without publishing leaves it unresolvable. This skill does the whole sequence.

**Announce at start:** "Using bump-rc to release rooms-client."

## Hard rules

- **Publishing is irreversible.** A version number can never be reused, even
  after `npm unpublish`. Confirm the version with Ryan before step 4 unless he
  named it in the invocation.
- **Never invent an npm token.** If auth fails, stop and ask — do not try other
  registries, other accounts, or `--force`.
- Commit the version bump via the `/commit` skill, never raw `git commit`.
- No pushing unless Ryan says so; the release script itself does not push.

## Steps

### 1. Read the current state

```bash
cd ~/github/openmarket-internal
git status --short                       # must be clean; the script refuses otherwise
git branch --show-current                # publish expects main
grep '"version"' packages/rooms-client/package.json
```

Also read all three current pins, so step 6 has a before/after:

```bash
cd ~/github/openmarket-chat
grep -n '"@openmarket/rooms-client"' \
  package.json apps/cloud/package.json packages/chat-ui/package.json
```

All three must already read the same version. If they do not, say so before
publishing anything — that is an existing bug, not something this run created.

### 2. Decide the bump from what actually changed

List what landed in the package since the last version bump:

```bash
git log --oneline "$(git log -1 --format=%H --grep='chore(rooms-client):' -- packages/rooms-client/package.json)"..HEAD -- packages/rooms-client/
```

Then pick by the strongest change present:

| Change | Bump |
|---|---|
| A removed or renamed export; a changed function signature, return shape, or wire type that existing callers must adapt to | **major** |
| A new module or export entry, a new optional field or parameter, new behavior behind a default that preserves today's semantics | **minor** |
| Bug fix or internal change with no surface movement | patch |

New modules with new `exports` entries are additive — that is a **minor**, not a
major. When a change looks major, say which caller breaks and how before
proposing the number.

State the proposed version and the one-line reason, then confirm with Ryan
unless he already named it.

### 3. Prepare (optional but preferred)

`prepare` writes the version and runs the package gates without committing,
tagging, or publishing — it fails loudly if the gates are red:

```bash
bun run rooms-client:release prepare 0.X.0
```

Then commit the version change (stage `packages/rooms-client/package.json`, plus
a CHANGELOG entry if the repo's recent releases carry one — check
`git log --oneline -5 -- CHANGELOG.md`), using the `/commit` skill with the
repo's convention: `chore(rooms-client): 0.X.0 (<what it adds>)`.

### 4. Publish

```bash
bun run rooms-client:release publish 0.X.0
```

The script asserts a clean worktree on `main`, that `package.json` already reads
the target version, runs `npm whoami`, runs the package gates, publishes, then
polls the registry until the version is readable (about a minute).

### 5. If auth fails

`npm whoami` failing, `ENEEDAUTH`, `E401`, or `E403` all mean the same thing:
the token is missing, expired, or lacks publish rights on the `@openmarket`
scope. Stop and ask Ryan for a token — quote the exact npm error, and offer him
the two ways to supply it:

- `npm login --scope=@openmarket` in his own terminal (interactive; the `!`
  prefix runs it in-session), or
- an automation token exported as `NPM_TOKEN` / written to `~/.npmrc`.

Never print a token back, never write one into a repo file, and never retry
publishing until he confirms.

If the script instead reports the version is already published, **do not bump
past it silently** — the release may have half-landed. Verify with
`npm view @openmarket/rooms-client@0.X.0 version` and report what you find.

### 6. Repin all three, in the one workspace

Once npm reports the new version. Both host pins go through `bun add`; the
shared package's peer range is edited by hand, because `bun add` writes a
dependency, not a peer:

```bash
cd ~/github/openmarket-chat
bun add @openmarket/rooms-client@0.X.0 --exact
bun add --cwd=apps/cloud @openmarket/rooms-client@0.X.0 --exact

# packages/chat-ui declares it as a peer — edit the value, then reinstall once
#   "peerDependencies": { "@openmarket/rooms-client": "0.X.0", ... }
bun install
```

Confirm all three moved before going on — a missed peer is invisible until a
consumer resolves a second copy:

```bash
grep -n '"@openmarket/rooms-client"' \
  package.json apps/cloud/package.json packages/chat-ui/package.json
```

Three traps, all real:

- `openmarket-chat` may have rooms-client **symlinked** to a local monorepo
  checkout (`tools/link-rooms-client.ts`). `bun add` replaces the link. Check
  `readlink node_modules/@openmarket/rooms-client` first; if it was linked and
  the session still needs the link, relink after the pin lands:
  `bun tools/link-rooms-client.ts --unlink && OM_REPO=<checkout> bun tools/link-rooms-client.ts`.
- **Never `pnpm add` here.** `apps/cloud` has no lockfile of its own; the root
  `bun.lock` covers both hosts. A pnpm install in this tree creates a second
  dependency graph that the workspace fences will not see.
- Pre-public-launch, the registry may not serve the package at all. If the add
  fails to resolve, report it and fall back to the local tarball flow rather
  than editing the pin by hand:
  `cd <monorepo>/packages/rooms-client && bun run build && npm pack`, then
  install that tarball in the consumer.

### 7. Verify and report

```bash
cd ~/github/openmarket-chat
grep -n '"@openmarket/rooms-client"' \
  package.json apps/cloud/package.json packages/chat-ui/package.json
bun run typecheck                        # /rooms host
bun run --cwd apps/cloud typecheck       # /chat/ host
```

Both hosts typecheck, not one — a protocol change lands in both at once through
`packages/chat-ui`, per **principle-prove-every-host**.

Commit the pin change as one unit (all three `package.json` files plus
`bun.lock`) via the `/commit` skill: `chore: rooms-client 0.X.0`. They are one
logical change; splitting them leaves a commit where the peer disagrees with
its hosts.

Report: the version published, why that bump, all three pins before/after, both
typecheck results, and anything left for Ryan (a relink, an unpushed commit, a
failed resolve).
