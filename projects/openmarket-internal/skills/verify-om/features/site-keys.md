# Site keys: a watch reads a site with your key

*Source-checked 2026-11-25 (nightly) against origin/main `d5ff40419` (v0.497.0+internal): the page kit's handoff over MCP (#2693, driven live in [mcp-stdio.md](mcp-stdio.md)); doctor's repair of a pre-merge `site_keys` table is in [daemon-lifecycle-and-health.md](daemon-lifecycle-and-health.md) (`doctor-schema`). No site key was driven.*

*Re-checked 2026-11-24 (nightly), tree `26d502c689` (origin/main), source only. #2664 fixes chat's kept-key report (below). Not driven: no key was saved or kept tonight.*

*Re-checked 2026-11-22 (nightly), tree `01482928a5` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. `setup key x --site http://example.com` exits 2 with `om: A site key is sent only over https; give the site as https://host.` before any prompt. The `no-escalation` line is corrected from source: only a keyed 401 or 403 answers `page_site_key_refused`. Not re-driven: the hidden prompt, the six ways of sending, a keyed read. (`cli/40-setup-key-http.*`.) Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261122/r1/`*

*Verified: 2026-11-20, merged main `2d01b6b5d4` (#2610, landed as `07c285b9e3`). Keyless lane on 18131 through `control-om`, every OpenMarket origin dead, a scripted model stand-in on 18136. Driven, 9 of 9 claims: the hidden prompt in a tmux pty and the chat box, six ways of sending a key read back from `httpbin.org`, redirects through `postman-echo.com`, a byte scan of the lane for 16 made-up values, export, share, package and MCP refusals, a way change and a site move, and the plain REPL's paste guard. Third-party reads only: `httpbin.org` and `postman-echo.com` with made-up keys. Not driven: a lane with Firecrawl set up (claim 6 rests on a probe of the merged code with a positive control), the TUI's key box, `/setup`. One defect on the chat decline path is recorded under [chart-number-from-address.md](chart-number-from-address.md). Evidence root `~/Documents/dev-notes/om-2026-11-20-e2e-verify/run-artifacts/s2/` (`phaseA/`, `harness/`). Gallery `http://127.0.0.1:8098/om-1120-e2e/s2/`.*

A person stores a key for one site under a name. A page watch that names the key sends it to that site only, over https, in the way the person chose. The key is typed at a hidden prompt and lives only in the vault. Everything om stores or shows a model carries `[site key <name>]` in its place. A watch that reads with a key cannot be exported, shared or packed, and cannot be authored over MCP.

## Sub-features

- `store`: `om setup key <name> --site <https url>`. It prints `Key:`, `Site:` (the origin only) and `Sent as:`, then asks `Paste the key (hidden):`. Typed characters show as squares. It ends `Saved: <name>`.
- `ways`: the default is `Authorization: Bearer`.
  - `--header <Name>` sends the key as that header.
  - `--scheme <Word>` sends `Authorization: <Word> <key>`.
  - `--query <param>` sends `?<param>=<key>` on the address.
  - `--basic-user <user>` sends Basic with that user and the key as password.
  - `--basic` sends Basic with the key as user.
- `read`: `om watch page-add <url> --site-key <name>` adds a keyed page source. What the site echoes is stored with `[site key <name>]` in place of an exact match of the value.
- `origin-lock`: a page on another origin, or on `http://`, is refused before any read: `site_key_wrong_origin`, exit 2. A name nothing holds answers `site_key_unknown`.
- `redirects`: a redirect to another origin or to `http://` carries no key, in header, query or bearer form. A same-origin redirect keeps it.
- `no-leak`: the watch file, stream id, snapshot key and `final_url` hold the address without the key. Journal rows read `X-E2e-Alt added: "[site key <name>]"`. No request body to the model holds a value.
- `no-escalation`: a keyed read that answers 403 or 404 never goes to Firecrawl or om's browser (`packages/cli/src/runner/watch-engine/page-fetch.ts:350-352`, `packages/cli/src/shared/escalating-fetcher.ts:108`). A keyed 401 or 403 answers `page_site_key_refused` (`page-fetch.ts:408-419`). Source names only 401 and 403 for that code, so what a keyed 404 answers is not known (source, 2026-11-22; not driven).
- `no-export`: `om watch export` and every `om watch share --dry-run` form answer `watch_reads_site_key`, exit 2: `shares cannot carry keys`. `om package publish --dry-run` and `om package install` on a pack whose recipe names a site key answer `invalid_watch_pack`.
- `no-mcp`: `om mcp serve --stdio` answers `mcp_site_key_refused` for `watch_create`, `watch_source_add` and `watch_edit`, also when the source is a JSON string. `watch_export` answers `watch_reads_site_key`.
- `way-change`: the same name and site with a new way asks `Change how it is sent? Keeps the stored key. [y/N]:`. Yes changes the way with no paste. The ciphertext is unchanged.
- `site-move`: the same name with another site asks `Replace it? [y/N]:`, then the hidden paste. No prints `Kept <name> for <site>`. Esc at the paste leaves the row and ciphertext unchanged.
- `hostile-input`: names, sites, headers and users with shell characters are refused at setup. Printed commands quote hostile names and an IPv6 site.
- `paste-guard`: in the plain REPL a key-looking line, or a `!` line holding a Bearer token, is held with `This looks like a key. Save it as a site key? [s]ave, send [a]nyway, [c]ancel:`.
  - Cancel prints `Not sent.` and sends nothing to the model.
  - Save asks `Key name` and `Site (https://host):` and prints `Saved <name> for <origin>`.
  - Keeping the key on file at a replace prompt in chat now reports `Kept <name> for <site>. The key on file is unchanged; no new key was saved.` (the result carries `kept: true` and `said`, no `stored`); before #2664 it was reported as a save (source, 2026-11-24).
  - A held `!` command does not run.
- `chat-tools`: `site_key_add` and `site_key_list` are core chat tools. `site_key_add` opens the hidden box in chat.

## How to get to it (user POV)

- `om setup key nasa --site https://api.nasa.gov --query api_key`, paste the key at the hidden prompt.
- `om watch page-add 'https://api.nasa.gov/…' --site-key nasa`.
- In `om chat`, ask for a number from a site that needs a key. om opens the hidden box.
- Run the same `om setup key` again to change how the key is sent or to move it.

## Driving it with control-om

Preconditions: a lane the run started, `OM_LANE_PORT` exported. The lane env is `harness/env-a.sh` in the evidence root: a dummy `OM_API_KEY`, every OpenMarket origin at `http://127.0.0.1:9`, and the three `OPENMARKET_LLM_*` values at the stand-in. Keep made-up key values in a file outside the evidence folder.

### Store a key at the hidden prompt

1. The prompt needs a pty. Start a tmux session and run `harness/tmux-setup-key.sh <out-prefix> <value> <setup key args…>`. It types the command, waits for the prompt, types the value with `tmux send-keys -l`, and captures before, typed and after.
2. See the squares in the typed capture, and `Saved: <name>` after. The script prints how often the value shows on screen. Expect 0.
3. Read back `site_keys` in the lane's `accounts/guest/om.sqlite`: `name, origin, send_kind, send_name, added_at, last_used_at`.
4. Read `vault_secrets` for the row `sitekey:<name>`. The value is there as ciphertext only.
5. Quote the site. zsh globs a `?` in an unquoted URL.

### Read with each way, and the redirects

1. Store one key per way against `https://httpbin.org`. Add a page per key: `control-om om -- watch page-add 'https://httpbin.org/anything?probe=<id>' --site-key <name> --format json`.
2. Read `watch_page_snapshots.observed_text`. See `$.headers.Authorization "Bearer [site key <name>]"`, or the header, query or Basic form.
3. For redirects store keys against `https://postman-echo.com`, and add `https://postman-echo.com/redirect-to?url=<encoded https://httpbin.org/anything?…>`. The snapshot shows no `Authorization`, no key param and no key header.
4. Redirect to an `http://` address. No key.
5. Controls: a direct read and a same-origin redirect keep the key.
6. `watch page-add https://postman-echo.com/get --site-key <httpbin key>`. See `site_key_wrong_origin`.

### A journal row without waiting

Change the key's way on the same site (`--header x-other`, answer y), then `control-om om -- watch run now <slug>`. The echo differs, so a row is written. Read it in `watch_intake.event_json`.

### The leak scan

`harness/leak-scan.py <values.json> <path>…` scans raw bytes for every value in raw, JSON-escaped, URL-encoded, form-encoded and Basic forms. It never prints a value.

1. Scan the lane home, the sqlite file and its wal, a `sqlite3 .dump`, the lane log, `agent.log` and the stand-in's request bodies.
2. Include a value holding `/ + = !` and one holding `"` and `\`.
3. Run it on a control file that holds the values. Expect hits there and 0 everywhere else.

### Export, share, pack and MCP

1. `control-om om -- watch export <keyed watch> --format json`. See `watch_reads_site_key`, exit 2.
2. `watch share <watch> --dry-run`, with `--with-recipe`, with `--recipe-only`, and `watch share --ref <a> --ref <b> --name <pack> --dry-run`. The same refusal.
3. Copy `examples/packages/macro-releases`, add `stream_ref.extra.site_key` to a feed source, and run `package publish <dir> --dry-run`. See `invalid_watch_pack`. The unedited copy passes.
4. `harness/mcp-drive.py` with `harness/mcp-calls-*.json` drives `om mcp serve --stdio`. The listener must be schema-valid (`{kind, stream_ref, user_goal}`), because the site-key refusal runs after schema validation.

### Chat without a real model

1. `harness/fake-model.ts` is an openai-compatible stand-in that emits scripted tool calls and logs every request body.
2. `watch_page_add` loads only through `watch_kit {request: "<the URL alone>"}` in chat. Over MCP the kit hands the page to the person instead (`door.handoff`: `Pages are not added over MCP. …`, live 2026-11-25, see [mcp-stdio.md](mcp-stdio.md)).
3. The plain REPL is `OM_PLAIN_CHAT=1 control-om om -- chat` in the tmux pane. Count the stand-in's requests before and after each held line.

### The Firecrawl half

A lane cannot set Firecrawl up without calling Firecrawl. `harness/c06-escalation-probe.ts` registers a recording transport on the merged tree and reads `httpbin.org` for real. Unkeyed 403 and 404 call `admits` then `fetch`. Keyed 403 and 404 make 0 calls, also when the caller names the transport.

## Gotchas

- **Known, not verified-good: a hint names a command that fails.** `om watch page-add http://httpbin.org/… --site-key <name>` hints `store one: om setup key <name> --site http://httpbin.org`. Setup refuses `http://` (`sent only over https`). `packages/cli/src/actions/watch/_page-leg.ts:716`. Evidence `phaseA/c03-origin-mismatch.txt`.
- **Known, not verified-good: a keyed refusal offers Firecrawl.** `page_site_key_refused` carries ``Run `om setup firecrawl` to retry public pages this machine cannot read``, though a keyed read never goes there. `packages/cli/src/actions/watch/_page-leg.ts:427`. Evidence `phaseA/c06-lane-observations.txt`.
- **Known, not verified-good: "send anyway" does not send an `sk-` key.** The runtime's older scrubber replaces it with `[REDACTED_API_KEY]` and prints ``Run `om init` to update the stored key``, which is about the OpenMarket key. Evidence `phaseA/c09-repl-paste-guard.txt`.
- The paste guard skips addresses. A key typed inside a URL in chat is not held. See [chart-number-from-address.md](chart-number-from-address.md).
- Never pipe the prompt. `om setup key … </dev/null` fails with `No more input is available`.
- `httpbin.org/redirect-to` refuses other hosts now. Use `postman-echo.com/redirect-to?url=…` for cross-origin and `http://` hops.
- `watch_share` and `package_publish` over MCP are refused `capital_not_armed` for every watch, keyed or not. They prove nothing about site keys there.
- The stdio servant lists `watch_create`, `watch_source_add`, `watch_edit`, `watch_export`, `watch_share` and `package_publish`. It does not list `watch_compose`, `watch_page_add` or `site_key_*`.
- Keystrokes sent to the pty while the REPL is open become chat turns.
- A lane writes no `runner.log`. The daemon's log is `.control-om/lane-<port>.log`.
- On a fresh home a diff-only keyed `watch_page_add` from chat ran `auto-approved`, with the card's rows printed (`KEY <name>, sent only to <site>`). Not checked against the intended default.
