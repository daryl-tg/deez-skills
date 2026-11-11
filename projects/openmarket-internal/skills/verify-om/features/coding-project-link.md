# Link a coding project from a repo path and a server

*Verified: 2026-11-11 (nightly), tree `0ad4768f66` (origin/main, v0.494.0; #2438), bare lane on 18183 (dummy `OM_API_KEY`, dead service URLs) and guest lane on 18181. Driven: `om project --help`, `om project list` (empty, then one row, text and JSON), the daemon's link door with seven checkouts (one accepted, six refused), `om project link` stopping at the server lookup on both lanes, and `project_link` absent from MCP stdio. Not driven: a link through the CLI with a real server, the om chat card, a work agent starting in the linked project. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261111/r1/` (`cli/project-door.txt`).*

`om project link [path] --space <server>` links a repo checkout to a server so that server's coding agents (`feature`, `debugger`) can start, and `om project list` shows the links. Work starts from origin's default branch when the checkout has it, else the current branch, and lands as local commits that are never pushed. Before #2438 nothing linked a project, so every work agent stopped at `project_unlinked`.

## Sub-features

- `list`: `om project list` prints one row per link, `<repo>  <server>  <branch>`, with `unavailable` last when the daemon cannot use the checkout. With none it prints ``No linked projects. Run `om project link <repo path> --space <server>`.`` `--format json` is `{projects:[{id, repo, server:{id, name}, branch, delivery, available}]}`.
- `link`: `om project link [path] --space <server>` takes the server by name or id and prints `Linked`, `Server` and `Branch` rows. `path` defaults to `.`. The CLI looks the server up on the chat service first, so it needs a signed-in account.
- `link-door`: `POST /rpc/v1/roster/projects/link` with `{"spaceId", "checkout"}` and an `Idempotency-Key` header is what the CLI and the card call. It answers the stored project (`mode: "adopt"`), or 400 `project_not_allowed` with a `text` and a `fix`.
- `card`: in om chat, `project_link` asks on a card first (`Repo`, `Server`, `Branch`, `Delivery: local commits, never pushed`, `Setup: your Claude Code / Codex setup`). Source only.
- `not-on-mcp`: `project_link` and `project_list` are chat and CLI tools. MCP stdio answers `Tool project_link not found`.
- `dev-verbs`: `om project token|delivery|unlink` stay behind `OM_DEV=1` ([agent-creator-lifecycle.md](agent-creator-lifecycle.md)).

## How to get to it (user POV)

- In a terminal: `om project link ~/code/my-repo --space "My Server"`, then `om project list`.
- In om chat: ask it to link a repo for your coding agents and answer the card.
- A work ask stopped by a missing project says so in the room, with the same command as its fix.

## Driving it with control-om

A bare lane proves the list and the daemon's checks with no account: `control-om up --port <p>` with `--env OM_API_KEY=om_dummy_proto`, each of `OM_BASE_URL`, `OM_AUTH_BASE_URL`, `OM_COLLAB_REST_URL`, `OM_ROOM_CHAT_API_URL` and `OM_ALERT_TOPICS_URL` set to `http://127.0.0.1:9`, and the same variables exported for every `control-om om --` call. Export `OM_LANE_PORT` first.

1. `control-om om -- project list` prints the empty line; `--format json` is `{"projects":[]}`.
2. Make scratch checkouts outside any worktree: `git init -b main`, one empty commit, and `git remote add origin https://github.com/example/probe.git` for the good one.
3. Link it through the door:

   ```sh
   curl -s -X POST http://127.0.0.1:$OM_LANE_PORT/rpc/v1/roster/projects/link \
     -H 'content-type: application/json' -H 'Idempotency-Key: probe-1' \
     -d '{"spaceId":"s1","checkout":"/abs/path/to/checkout"}'
   ```

   Seen: 200 with `result.id` `project_<uuid>`, `spaceId: "s1"`, `mode: "adopt"`, `ownerId: "local:<id>"`.
4. `control-om om -- project list` now prints `<checkout>  s1  main`, and `--format json` reads `server: {id: "s1", name: null}`, `branch: "main"`, `delivery: "local"`, `available: true`.
5. The refusals, each 400 `project_not_allowed`:

   | Checkout | `text` | `fix` |
   |---|---|---|
   | a linked git worktree | `This is a linked worktree.` | `Link the main checkout it was made from.` |
   | no `origin` | `This checkout has no origin remote.` | `Add one with git remote add origin <url>, then link the project again.` |
   | `origin` is a local path | `This checkout's origin is not a hosted git remote.` | `Point origin at the repo's git@ or https URL, then link it again.` |
   | reached through a symlink | `This path goes through a symlink.` | `Link the real path, <path>.` |
   | detached HEAD | `This checkout is not on a branch.` | `Check out the branch agents should start from, then link the project again.` |

6. MCP stdio: `tools/call project_link` is `isError`, `Tool project_link not found`; `tools/list` holds neither name.

## Gotchas

- `om project link` cannot finish on a guest or bare lane: the server lookup fails first. A guest lane prints `om: Unauthorized` (exit 1); a bare lane with a dead chat URL prints `om: ECONNREFUSED: Unable to connect. Is the computer able to access the url?` Neither names a fix (reported gap). Use the door for the daemon half.
- The door does not check the server: any `spaceId` string links. Only the CLI and the card resolve a real one.
- A subdirectory of a checkout and a path that does not exist both answer 503 `daemon_offline`, `Projects service is unavailable.` The source has a `This path is not the repository's top-level directory.` refusal that the subdirectory drive did not reach (reported gap).
- `control-om om --` runs from the repo root, and every control-om tree is a linked worktree, so `om project link .` there names a checkout the daemon refuses. Link a scratch `git init` instead.
- A bare repository refusal (`This is a bare repository.`) is in the source and not driven.
- Nothing here unlinks. `om project unlink` needs `OM_DEV=1`; a lane home is disposable.
