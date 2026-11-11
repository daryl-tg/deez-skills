# Publish an agent you made (om agent publish, agent_publish)

*Verified: 2026-11-11, branch `daryl/agent-listing-publish` tree `c6944b91eb` (not yet on main; rebased since as `01438631ec`), bare lane on 18131 from the feature worktree with one stand-in on 18132 answering `/auth/validate-api-key` and the fake model, `OM_REGISTRY_URL` at an in-memory registry preview on 18120 built from registry branch `daryl/agents-category`. Driven: `agent create --file draft.json --yes` with a `listing`, the staged files, `agent list --format json`, two `agent publish --dry-run` runs, the TTY publish card (declined), `agent publish --yes` twice, then the registry's `/agents` and the agent's page. Not driven: MCP `agent_publish` (needs `om mcp arm`), `--cover`, `--artwork`, a coding agent, a real registry. Evidence: `http://127.0.0.1:8098/registry-agents-category/r2/`.*

`om agent publish <name>` puts an agent you created on the registry as `@<username>/<name>` in one step. It stages a copy of the agent's folder, writes `om-package.json` with the listing (display name, tagline, tags), and publishes behind one tier-3 card. The agent's own folder is never changed. The listing is set when the agent is created, through `listing` on the draft, and can be overridden at publish.

## Sub-features

- `agent_create` draft takes an optional `listing`: `displayName` (1 to 40, one line), `tagline` (1 to 200, one line), `tags` (1 to 8, each 1 to 32), `avatar` (one emoji, no letters or digits), `jobs` (1 to 5, each 1 to 120). Hidden characters are refused. The create card gains a `Name` row.
- The listing lands in the agent's folder: `plugin.json` `description` (tagline), `keywords` (tags), `catalog.jobs`, `catalog.displayName`, and `AGENT.md` `avatar`. With no listing the files are as before.
- `agent_publish` (tier 3): input `agent`, optional `listing`, `dry_run`, `yes`, `cover_words`, the artwork fields, `registry`. CLI flags `--dry-run`, `--yes`, `--cover`, `--artwork`, `--artwork-alt`, `--registry`, `--name`, `--tagline`, `--tag` (repeatable).
- Version: the plugin's own version on a first publish, a patch bump of the registry's latest after that.
- Card rows `Package`, `Version`, `Name`, `Tagline`, `Tags`; question `Publish agent <name> to the registry?`. A dry run raises no card.
- Refusals: `not_local` (the agent did not come from this home), `not_found` (no staged folder), `package_deleted` (the coordinate was deleted on the registry).

## How to get to it (user POV)

Create an agent with a listing (`om agent create --file draft.json`, or ask om chat to make one), then run `om agent publish <name>`. Add `--dry-run` to see the coordinate, version and listing first.

## Driving it with control-om

Use the bare-lane recipe from [agent-create.md](agent-create.md), with two changes. Point `OM_AUTH_BASE_URL` at a stand-in that answers `POST /auth/validate-api-key` with `{"userId":"<account>","username":"<name>","email":null}`, so the CLI can name the scope. Point `OM_REGISTRY_URL` at a registry you own for the run. Pass both on `control-om up --env` and export them for every `control-om om --` call. Set `OM_API_KEY` to a value that registry accepts as that account.

```sh
control-om om -- agent create --file draft.json --yes        # draft carries "listing"
control-om om -- agent list --format json                    # the row's avatar is the listing's emoji
cat .control-om/home-$OM_LANE_PORT/accounts/guest/roster/local/<name>/plugin.json
control-om om -- agent publish <name> --dry-run              # Would publish @<username>/<name> <version>, then Name, Tagline, Tags, Avatar, Does
control-om om -- agent publish <name> --dry-run --name "Other" --tag a --tag b
control-om om -- agent publish <name> --yes                  # Published @<username>/<name> <version>, Listing: <registry>/@<username>/<name>
control-om om -- agent publish <name> --yes                  # the next patch
```

The card needs a TTY. Drive it with `expect`, wait for `Publish agent`, and answer `n` to leave nothing published.

Prove the dry run posted nothing by reading `GET <registry>/v1/search?kind=agent-plugin&q=<name>` before and after. Prove the stage was removed by listing the temp directory for `om-agent-publish-*`.

## Gotchas

- The staged folder is under the account home, `.control-om/home-<port>/accounts/guest/roster/local/<name>`, not directly under the lane root.
- With every auth URL dead the publish stops at the username lookup. The stand-in is what lets a bare lane publish.
- An agent made by `agent_create` ships no `README.md`, so its registry page reads "No README in this version."
- `agent_configure` edits live in the instance overlay and are not published. The published agent is the package folder.
- `control-om down` takes the port from `OM_LANE_PORT`, not from a `--port` flag.
- Six pinned test files fail on main for reasons unrelated to this feature (`approval-carrier`, `surface-goldens`, `mcp-stdio-catalog`, `capital-parity`, `answer-vocabulary-ratchet`, `agent-tool-metadata`), measured on `0ad4768f66`.
