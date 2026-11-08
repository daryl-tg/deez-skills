# Agent files, scopes and trust

*Re-driven 2026-11-09 (nightly), tree `5bfa0ccf6` (origin/main, v0.492.0), guest lane on 18143, booted with no guest 429. on a guest lane plus a scripted fake model: `agent init vomuser`, `agent list --lock`, `agent try` (`no-bare-ack` pass). Not re-driven: tamper restore, scopes, trust, install. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261109/r1/` (`cli/95-97`).*

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0), guest lane on 18141, booted with no guest 429. `agent init vomuser --dir <scratch>/vomuser --format json` wrote `plugin.json` and `agents/vomuser/AGENT.md`; `agent list --lock --format json` read the lane's `library/agents.lock.json`. Not re-driven: trust, scopes, `--preflight`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/133-134`).*

*Re-driven 2026-11-06 (nightly), lock only, tree `50fcc594b` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted at 19:18Z with no guest 429, host load average 10 falling to about 3.3: `agent list --lock` lists each installed agent with its version, a `sha256:` digest and `plugin`. Not re-driven: init, try, eval, install, scopes, trust, tune. Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/agent-lock.txt`).*

*Verified: 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0; #2306, #2318). Guest lane on 18163, booted in 2 s with no 429: `agent list --lock` (8 rows, `origin: plugin`), the installed `explain` files at `0444`, a `chmod u+w` plus appended line restored byte for byte within 3 s, `agent init` into the lane root, the user scope (an `AGENT.md` under `<home>/agents/<name>/` installed as `scope: user`, a same-named folder shadowing the plugin `argue`, deleting it un-shadowing), the project scope (`list --here` untrusted, `trust` installing `vomproj`, `--forget` disabling it), `install <dir> --preflight` and `--yes`. Bare lane on 18165 with a fake model on 18164: `agent try` (text and JSON), `agent eval explain` (`runs 9  correct 6  score 0.67`), and over MCP stdio `agent_tune` (empty refusal, a description diff) then `agent_tune_apply`. Not driven: an install with pins, a `pin_failed`, a registry install, tune from the TUI page. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/agent-*`, `cli/install-*`, `cli/mcp-tune*`).*

An agent is a folder. `om agent init` writes one you can edit, `om agent try` runs an ask against it, and `om install <dir>` installs it as an agent plugin. Installed files are read-only copies, a lock file records each agent's version, digest and origin, and your own edits go in a separate local file. Agents can also come from two folders the daemon watches: your user scope, and a project's `.om/agents/` once you trust that directory. A user or project agent with a plugin agent's name shadows it.

## Sub-features

- `init`: `om agent init <name> [--dir <dir>]` writes `plugin.json`, `om-package.json` (`kind: agent-plugin`, `name: @local/<name>`, `version: 0.1.0`), `agents/<name>/AGENT.md`, `evals/asks.md` and `knowledge/README.md`; JSON `{agent, dir, paths}`. With no `--dir` it writes `./<name>` in the current directory.
- `try`: `om agent try <dir_or_name> "<ask>"` stages the folder and prints the reply, then each check (`no-bare-ack  pass`); JSON `{package_id, reply, checks:[{name, verdict}]}`. It needs a model.
- `eval`: `om agent eval <name>` grades the trigger rate over the agent's sample asks: `runs 9  correct 6  score 0.67`. The agent page then reads `Trigger rate  0.67 (3 asks, today)`. Always on (no `OM_DEV`).
- `install`: `om install <dir> --preflight` prints the plan and a card (`Agent`, `Reach`, `Publisher`, `Shadow`, `Version`) and installs nothing; `--yes` installs (`package.kind: agent-plugin`, `agents:[{id,name,version,shadow}]`, a receipt). A name already held by a user-scope agent is refused `installation_conflict` (`The installer refused this plugin.`, hint `Plan the install again.`). Pinned dependencies install first and a failed one is `pin_failed:<name>` (source only).
- `read-only`: installed files live under `<home>/library/agents/<name>/` at mode `0444` (`AGENT.md`, `README.md`; `evals/`, `knowledge/`, `skills/`). A changed file is restored from the release. Your edits go in `AGENT.local.md` beside it.
- `lock`: `om agent list --lock` prints `<home>/library/agents.lock.json`: `{path, agents:[{name, version, digest, origin: plugin|user|project, source_path, pins, disabled}]}`. A shadowed plugin agent keeps its row next to the scope's row; a forgotten project agent reads `disabled: true`.
- `user-scope`: a folder `<home>/agents/<name>/AGENT.md` installs within seconds as `scope: user`, `origin: local`, `packageId: user.<name>` (lane log `[roster-scope] {"installed":["<name>"],…}`). Deleting the folder removes it (`"removed":["<name>"]`). `<home>` is the account home (`OM_HOME/accounts/<name>/`), never `~/.claude`.
- `shadow`: a user or project agent named like a plugin agent pauses the plugin one: `agent list` reads `argue  plugin  shadowed by user`, JSON `paused: true`, `shadowedBy: "user"`. Precedence is project, then user, then plugin (source; user over plugin is driven).
- `project-scope`: `om agent list --here` adds the current directory's `.om/agents/`: JSON `cwd {dir, trusted, untrustedAgents:[{name, scope, trust: "untrusted", path, tools}], projectAgents}`. `om agent trust <dir>` returns `{dir, trusted: true, agents}` and installs them as `project` agents; `--forget` returns `trusted: false`, and the agent reads `removed` on `agent list` and `disabled: true` in the lock.
- `tune`: `agent_tune {agent, description|when_to_use|sections}` returns `{approval_id, diff, summary}` and writes nothing; an empty ask is `bad_request` `Name what to change: description, when_to_use or sections. Tools, brain and kind stay as the plugin set them.` `agent_tune_apply {approval_id}` answers `{applied: true, applies_to: "next run"}` and writes `AGENT.local.md` (`description: "…"`); the `0444` `AGENT.md` is untouched and `agent show` marks the field `(you)`. There is no `om agent tune` verb; the TUI agent page has a tune prompt (not driven).

## How to get to it (user POV)

- Terminal: `om agent init <name>`, `om agent try <dir> "<ask>"`, `om agent eval <name>`, `om install <dir> --preflight`, `om agent list --lock`, `om agent list --here`, `om agent trust <dir> [--forget]`.
- Files: drop an `AGENT.md` folder into `<home>/agents/` or a trusted project's `.om/agents/`.
- MCP or om chat: `agent_tune` then `agent_tune_apply`.

## Driving it with control-om

Preconditions: a lane the run started, `OM_LANE_PORT` exported, and `om-skills defaults installed 8 package(s)` in the lane log. `try`, `eval` and `tune` need a model: use the bare lane (dummy `OM_API_KEY`, every service URL on `127.0.0.1:9`, `OPENMARKET_LLM_*` pointed at a fake OpenAI-compatible model) from [om creates an agent](./agent-create.md). Let `H=.control-om/home-<port>/accounts/guest`.

1. `control-om om -- agent list --lock --format json`; assert `path` ends `library/agents.lock.json` and eight `plugin` rows. `ls -l $H/library/agents/explain/` shows `-r--r--r--`.
2. Tamper: `cp` the `AGENT.md` aside, `chmod u+w`, append a line, run `agent list`, wait 3 s, `cmp` against the copy: identical, mode `0444` again.
3. `control-om om -- agent init vomuser --dir $PWD/$H/scratch/vomuser --format json`. Always pass `--dir` under the lane root: `control-om om --` runs from the repo root, so the default writes into the checkout.
4. User scope: copy that `AGENT.md` to `$H/agents/vomuser/AGENT.md` **with its `tools:` line deleted** (and `"tools"` dropped from `locked:`), wait 5 s, `agent list` shows `vomuser  user`. A same-named `argue` folder shadows the plugin `argue`; `rm -r` it and the plugin row is back.
5. Project scope: from the repo root of a disposable worktree, `mkdir -p .om/agents/vomproj` with an `AGENT.md`; `agent list --here --format json` shows it under `untrustedAgents`; `agent trust $PWD --format json` then `agent list` reads `vomproj  project`; `agent trust $PWD --forget` turns it to `removed`. Delete `.om/` afterwards.
6. Install: `agent init vomplug --dir $PWD/$H/scratch/vomplug`, then `control-om om -- install $PWD/$H/scratch/vomplug --preflight` (card rows, nothing installed) and `--yes` (`Installed`, a `plugin` row, `0444` files).
7. Bare lane: `agent try $H/scratch/vomtry "what is vomtry?"`, `agent eval explain`; over `om mcp serve --stdio`, `tools/call` `agent_tune {"agent":"explain"}` (refused), `agent_tune {"agent":"explain","description":"…"}`, then `agent_tune_apply {"approval_id":"…"}` in the same or a later session; `cat $H/library/agents/explain/AGENT.local.md`.

## Gotchas

- `agent init` writes `tools: ["room_read","library_read"]`, and the scope loader refuses exactly that: the lane log reads `[roster-scope] <name>: A draft names tools, never a bundle: room_read, library_read` and nothing installs. The same folder installs through `om install <dir>`. Delete the `tools:` line for a user or project scope (README gaps).
- A hand-copied plugin `AGENT.md` (for example `explain`'s, with `tools: [room_read, library_read]`) fails the same way; an `AGENT.md` with no `description` fails `AGENT.md needs description`.
- `agent trust <dir>` asks nothing on the CLI, even with stdin closed and no `--yes`. Over MCP `agent_trust` is not listed; in om chat it raises a card.
- A just-installed local agent reads `1 today` on `agent list` before any run of yours.
- `om roster list` (needs `OM_DEV=1`) keeps a removed user-scope agent's row (`argue  local  0.1.0`).
- `untrustedAgents[].tools` shows the bundles (`room_read`, `library_read`) for a folder with no `tools:` line.
