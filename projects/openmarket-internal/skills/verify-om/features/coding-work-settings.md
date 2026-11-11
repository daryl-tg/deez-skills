# Choose how coding agents work, and which coding agents om can use

*Verified: 2026-11-12 (nightly), tree `82094c3a83` (origin/main, v0.495.0+11; #2450, merged as `139f318641`), bare lane on 18193 (dummy `OM_API_KEY`, dead service URLs on the daemon) with a fake model on 18192. Driven: `om agent work show` (seven defaults), `work set` with a bad value, a good value read back as `owner`, and `default` clearing it; `om agent coding list` in text and JSON and `om agent coding add`; the daemon's `GET` and `POST /rpc/v1/roster/work/settings`; `agent_work_show` over MCP stdio. Not driven: `--space` and `--repo` levels (they need a linked project and a server name), the repo-grant card, a coding run end to end (mention, worktree, PR, the two thread messages), the `Which repo?` reply. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261112/r1/` (`cli/work-*.txt`, `cli/mcp-stdio.json`).*

Since #2450 a mention of `feature` or `debugger` hands a coding agent a brief and the agent does the work itself. Work settings say how: where it works, how it delivers, which coding agent runs, and how much om may grant on its own. Each setting resolves repo first, then server, then owner, then the default. `om agent coding` lists the coding agents om can hand work to and adds your own.

## Sub-features

- `work-show`: `om agent work show [--space <server>] [--repo <name>]` prints `key  value  source` rows; source is `repo`, `server`, `owner` or `default`. Keys and defaults: `work.repo_grants agents`, `work.repo_roots none`, `work.workspace worktree`, `work.delivery pr`, `work.setup yours`, `work.coding_agent auto`, `work.repo_choice_confidence 0.85`. `--format json` is `{server, repo, settings:[{key, value, source}]}`.
- `work-set`: `om agent work set <key> <value>` prints `<key>  <value>  owner` (or `server <name>`, `repo <name>`). `default` clears the value. A bad value exits 1 with `<value> is not a value for <key>.` and `Use pr, branch, local or default.` (for `work.delivery`). The grant keys change only on a card or at the terminal (source).
- `coding-list`: `om agent coding list` prints `<name>  <state>  [version]  [added by you]`. States: `ready`, `not installed`, `signed out`, `installed, account cannot run it`, `installed, status unknown`. Profiles: Claude Code, Codex, Gemini CLI, Cursor CLI, plus any you add. JSON rows are `{id, name, origin, transport, executable, version, state}`.
- `coding-add`: `om agent coding add <id> -- <command...>` prints `Added <id>`; `list` then shows the row with `added by you`.
- `settings-door`: `GET /rpc/v1/roster/work/settings[?spaceId=|projectId=]` answers `{ok, result:{spaceId, projectId, settings}}`. `POST` needs an `Idempotency-Key` header, else 400 `missing_header`, `Idempotency-Key header is required.`
- `mcp`: `agent_work_show`, `agent_work_set` and `work_report` are on MCP stdio. `work_report` is how a running coding agent reports back (source).

## How to get to it (user POV)

- In a terminal: `om agent work show`, then `om agent work set work.delivery branch` to stop at a pushed branch with no PR.
- `om agent coding list` to see whether Claude Code or Codex is ready before mentioning `feature`.
- The first reply of a coding run names the settings it used and ends `change: om agent work set` (source).

## Driving it with control-om

Use a bare lane (`control-om up --port <p>` with `--env OM_API_KEY=om_dummy_proto` and dead service URLs, see [coding-project-link.md](coding-project-link.md)). Export `OM_LANE_PORT`.

1. `control-om om -- agent work show --format text`: seven rows, all `default`.
2. `control-om om -- agent work set work.delivery carrier-pigeon`: exit 1, `carrier-pigeon is not a value for work.delivery.` / `Use pr, branch, local or default.`
3. `agent work set work.delivery branch` prints `work.delivery  branch  owner`; `agent work show` reads `work.delivery  branch  owner`. `agent work set work.delivery default` clears it.
4. `control-om om -- agent coding list --format text`. Seen 2026-11-12 on the mini: `Claude Code  ready  2.1.322`, `Codex  installed, account cannot run it  0.160.1`, `Gemini CLI  not installed`, `Cursor CLI  not installed`. The rows read the host's search path, so they differ per machine.
5. `agent coding add vomfake -- /usr/bin/true` prints `{"id":"vomfake"}` (JSON off a terminal); `list` adds `vomfake  ready  added by you`.
6. `curl -s http://127.0.0.1:$OM_LANE_PORT/rpc/v1/roster/work/settings` and `?spaceId=s1`: 200 with the seven rows. `curl -X POST` with a body and no `Idempotency-Key`: 400 `missing_header`.

## Gotchas

- Without `--format`, a non-terminal stdout gets JSON. Pass `--format text` to capture rows.
- `work.delivery` takes `pr`, `branch`, `local` or `default`. `branch-only` is the old project delivery word and is refused.
- `GET /rpc/v1/roster/work/settings` with neither `spaceId` nor `projectId` answered 200 with the owner view on this tree.
- `coding list` reflects the host's real installs. Never treat `ready` as proof that a run will work: a run still needs a linked project and a relay to deliver the mention.
- `coding add` writes the lane home's registry only; a lane home is disposable.
