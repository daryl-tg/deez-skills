# Link a coding project from a repo path and a server

*Verified: 2026-11-12 (nightly), tree `82094c3a83` (origin/main, v0.495.0+11; #2450), bare lane on 18193 (dummy `OM_API_KEY`, dead service URLs on the daemon) with a fake model on 18192, and guest lane on 18191. Driven: the link door with a subdirectory of a checkout that has no `origin` (it linked the main checkout), the same checkout again (the same project id), `om project list` grouped by server in text and JSON, `om project unlink` and `om project link` stopping at the server lookup, and `project_link` listed on MCP stdio with `space` required. Not driven: a link or unlink with a real server, the om chat card, the `ask` grant path, the symlink, bare-repository and detached-HEAD refusals on this tree. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261112/r1/` (`cli/work-13-doors.txt`, `cli/work-14-project-list.txt`, `cli/work-16-unlink-nope.txt`, `cli/mcp-stdio.json`).*

*Verified before: 2026-11-11 (nightly), tree `0ad4768f66` (v0.494.0; #2438): the list, the door with seven checkouts, and `project_link` absent from MCP. #2450 changed the refusal set, the list format and the MCP reach, so those notes are history.*

`om project link [path] --space <server>` links a repo checkout to a server so that server's coding agents (`feature`, `debugger`) can start, and `om project list` shows the links. Since #2450 the agent does the work itself: by default it makes its own worktree, commits, pushes `om/<doc>` and opens a PR (`work.delivery pr`, see [coding-work-settings.md](coding-work-settings.md)). A repo with no hosted `origin` still links; push and PR delivery are refused later, at run time.

## Sub-features

- `list`: `om project list` prints a server heading, then one row per link under it: `<name>  <repo>  <branch>`, plus the note or `unavailable` last. With none it prints ``No linked projects. Run `om project link <repo path> --space <server>`.`` `--format json` is `{projects:[{id, name, note, repo, server:{id, name}, branch, delivery, available}]}`.
- `link`: `om project link [path] --space <server> [--note <text>]` takes the server by name or id and prints `Linked`, `Server`, `Branch` and, with a note, `Note`. Under `work.repo_grants ask` it prints `Waiting for your yes: <approve command>`. The CLI looks the server up on the chat service first, so it needs a signed-in account.
- `link-door`: `POST /rpc/v1/roster/projects/link` with `{"spaceId", "checkout"}` and an `Idempotency-Key` header answers the stored project (`mode: "adopt"`). A subdirectory or a linked worktree resolves to the main checkout, and a repeat returns the stored row with the same id.
- `unlink`: `om project unlink <name> --space <server>` is on for every user since #2450. It looks the server up first, like `link`.
- `mcp`: `project_link` is on MCP stdio (live) and follows `work.repo_grants` (source): under `agents` (the default) it lands at once; under `ask`, or for a repo outside `work.repo_roots`, it returns `{status: "pending", approval, approve}`. `project_list` is not on MCP.
- `card`: in om chat, `project_link` asks on a card first. Source only.
- `dev-verbs`: `om project token|delivery` stay behind `OM_DEV=1` ([agent-creator-lifecycle.md](agent-creator-lifecycle.md)).

## How to get to it (user POV)

- In a terminal: `om project link ~/code/my-repo --space "My Server"`, then `om project list`.
- In om chat: ask it to link a repo for your coding agents and answer the card.
- A work ask stopped by a missing project says so in the room, with the same command as its fix. With several linked repos and no clear pick, the thread asks `Which repo? a · b`.

## Driving it with control-om

A bare lane proves the list and the daemon's checks with no account: `control-om up --port <p>` with `--env OM_API_KEY=om_dummy_proto` and each of `OM_BASE_URL`, `OM_AUTH_BASE_URL`, `OM_COLLAB_REST_URL`, `OM_ROOM_CHAT_API_URL` and `OM_ALERT_TOPICS_URL` set to `http://127.0.0.1:9`. Export `OM_LANE_PORT` and the same variables for every `control-om om --` call.

1. `control-om om -- project list` prints the empty line; `--format json` is `{"projects":[]}`.
2. Make a scratch checkout outside any worktree: `git init -q -b main alpha`, one empty commit, and a `sub/` directory. No `origin` is needed.
3. Link the subdirectory through the door:

   ```sh
   curl -s -X POST http://127.0.0.1:$OM_LANE_PORT/rpc/v1/roster/projects/link \
     -H 'content-type: application/json' -H 'Idempotency-Key: probe-1' \
     -d '{"spaceId":"s1","checkout":"/abs/path/to/alpha/sub"}'
   ```

   Seen 2026-11-12: `ok: true`, `result.id` `project_<uuid>`, `mode: "adopt"`, `name: "alpha"`, `checkout` the top of `alpha`, not `sub`. The same call with the top-level path returned the same id.
4. `control-om om -- project list --format text` prints `s1` and then `alpha  <checkout>  main`. `--format json` reads `name: "alpha"`, `note: null`, `server: {id: "s1", name: null}`, `branch: "main"`, `delivery: "local"` (no `origin`), `available: true`.
5. `control-om om -- project unlink alpha --space s1` stops at the server lookup (see Gotchas). The row stays listed.
6. MCP stdio: `tools/list` holds `project_link` and not `project_list`. `tools/call project_link {"path": …}` answers `invalid_arguments`, `space: Invalid input: expected string, received undefined`.

## Gotchas

- `om project link` and `om project unlink` cannot finish on a guest or bare lane: the server lookup fails first, with a bare transport error and no fix (reported gap). Seen: `om: Unauthorized` on a guest lane, `om: ECONNREFUSED: …` with a dead chat URL in the CLI's env, and `om: Invalid Token` with an empty hint line when the CLI's env did not carry the dead URLs and reached the real service with the dummy key. Use the door for the daemon half.
- The door does not check the server: any `spaceId` string links. Only the CLI and the card resolve a real one.
- Without `--format`, a non-terminal stdout gets JSON. Pass `--format text` to capture the text rows.
- Refusals still in the source and not driven on this tree: `This path goes through a symlink.`, `This is a bare repository.`, `This checkout is not on a branch.` and `This repository has no main checkout to link.` (`packages/roster/src/projects.ts`). The worktree, no-`origin` and local-`origin` refusals from #2438 are gone.
- A lane home is disposable; nothing here needs an unlink to clean up.
