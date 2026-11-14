# The approval ledger from the CLI

*Re-driven 2026-11-15 (nightly), tree `5a4cb146d4` (origin/main, v0.495.0+internal), guest lane on 18185 started through `bootstrap.internal.ts`, booted with no guest 429. Read-only: `approvals list` `No pending approvals.`, `approvals ls --format json` `[]`, `--kind bogus` exit 2 now naming six kinds (`repo` is new since #2450), `--kind repo --format json` `[]`, `approvals show nope`, `approve nope` and `deny apr_doesnotexist` each exit 2, `GET /rpc/v1/approvals/inbox` with six `byKind` zeros and `GET /rpc/v1/approvals` `{"approvals":[]}`. Not re-driven: seeded rows, `deny` on a real row, the stream frames. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261115/r1/` (`cli/06-approvals.txt`).*

*Re-driven 2026-11-11 (nightly), tree `0ad4768f66` (origin/main, v0.494.0), guest lane on 18181, booted with no guest 429. `approvals list --format json` on an empty home is `[]`; a badge's room knock over MCP listed as `apr_…  grant  <expiry>  <badge> asks: read #vom-room` under `1 pending: 1 grant`; `om agent grants deny <id>` resolved it (`resolvedBy: cli`) and the list read `No pending approvals.` Not re-driven: `om approve` and `om deny`, the stream frames, tool and order cards. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261111/r1/`.*

*Re-driven 2026-11-10 (nightly), tree `c9bc93a355` (origin/main, v0.493.1), guest lane on 18143, booted with no guest 429. `approvals list` on a fresh home (`No pending approvals.`). Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261110/r1/` (`cli/approvals.txt`).*

*Re-driven 2026-11-09 (scheduled maintenance), tree `0d3d29cd27` (origin/main, v0.493.0), bare lane on 18145 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18144. `approvals list` `No pending approvals.`, `--kind bogus` exit 2, `approve nope` exit 2. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261109/r1/`.*

*Re-driven 2026-11-09 (nightly), tree `5bfa0ccf6` (origin/main, v0.492.0), guest lane on 18143, booted with no guest 429. `approvals list` `[]` only. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261109/r1/` (`cli/45`).*

*Re-driven 2026-11-08 (nightly), tree `5590b4d1c` (origin/main, v0.492.0), guest lane on 18141, booted in 2 s with no guest 429. `approvals list --format json` `[]` on a fresh lane. Not re-driven: the seeded rows, `approve`/`deny` and the stream frames. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261108/r1/` (`cli/65`).*

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0), guest lane on 18141, booted with no guest 429, refusals only: `approvals list --format json` `[]`, `--kind bogus` exit 2 naming the five kinds, `approve nope` and `deny nope` exit 2 `nope is not an approval id`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/30-33`).*

*Verified: 2026-11-06 (nightly), tree `50fcc594b` (origin/main, v0.492.0; #2253, #2255, #2274, #2316, #2321, #2329, #2334, #2337, #2338, #2340, #2344), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted at 19:18Z with no guest 429. Driven: `approvals list` empty, `--kind bogus`, `approve nope`, `approve`/`deny apr_doesnotexist`, `GET /rpc/v1/approvals/inbox`; two rows seeded into the lane's ledger (an MCP `room_delete` card and a carded `order_place` `tool_call`), listed, `om approve` refused on both from this auto-approve session, `om deny` on both, the list empty again, and `approval_changed`/`approval_resolved` on `/events/v1`. Not driven: a successful `om approve`, `answer_on_card`, `approval_typed_mismatch`, chain requests, the messenger fan-out, om chat's cards. Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/appr-*`, `approvals.sse`).*

Every card om raises (an MCP tool call that needs a yes, a chat card that parked,
a Firecrawl offer, an agent's room-access knock, an MCP chain request) is one row
in a single approval ledger in the home's database. `om approvals list` shows
the pending rows of six kinds, and `om approve <id>` or `om deny <id>` answers
one from the terminal. The first answer wins on every surface, and the stream
announces each change. A card that can move money is answered only on its own
card, and a chain request only at an interactive terminal.

## Sub-features

- `inbox-read`: `om approvals list [--kind chain|mcp|grant|draft|proposal|repo]
  [--format json]` (alias `om approvals ls`), `om approvals show <id>` for one
  card, `GET /rpc/v1/approvals/inbox` with `{items, counts}` per kind, and
  `GET /rpc/v1/approvals` with the raw ledger list `{approvals}`. The `repo`
  kind (#2450, `runner/approvals/inbox.ts:20`) lists a coding agent's repo
  grants, which only a plug-in supplies; it is always empty on a fresh lane.
- `answer`: `om approve <id>` and `om deny <id>` resolve a ledger row by its
  `apr_…` id. An unknown id is refused with exit 2.
- `harness-refusal`: `om approve` refuses when its process ancestry is an
  auto-approve harness (`assertApprovalCliHasHuman`, `cmd/approvals.ts`). `om
  deny` has no such door.
- `money-card` (#2344, source only): `om approve` on a `tool_call` row that
  reaches capital is `answer_on_card`; a card with a typed size is
  `approval_typed_mismatch` (`refuseCapitalYesOffCard`,
  `runner/approvals/wire.ts:107-125`).
- `chain-request` (#2340, source only): a `chain_arm` row's card reads
  `Answer in your terminal: om approve <id>`; `om approve` is
  `terminal_required` off a TTY or with `--format json`.
- `stream`: `/events/v1` carries `approval_changed` and `approval_resolved` as
  rows open and close.
- `fan-out` (#2321, #2329, #2334, source only): a card shows on every paired DM
  and every om chat window of its conversation and closes everywhere on one
  answer.

## How to get to it (user POV)

From a terminal, run `om approvals list` to see what waits for you, then
`om approve <id>` or `om deny <id>`. In om chat, `/approvals` brings back a card
you set aside. A card raised in a messenger DM shows the same id.

## Driving it with control-om

Preconditions: a lane the run started. The ledger is empty on a fresh lane, so
seed rows the way the product's own test does.

1. **The empty reads.** `control-om om -- approvals list` prints `No pending
   approvals.`; `--format json` prints `[]`; `--kind bogus` exits 2 with
   `--kind must be one of: chain | mcp | grant | draft | proposal | repo`.
   `curl -s "$(control-om url /rpc/v1/approvals/inbox)"` returns
   `{"ok":true,"data":{"items":[],"counts":{"total":0,"byKind":{"chain":0,"mcp":0,"grant":0,"draft":0,"proposal":0,"repo":0}}}}`;
   `curl -s "$(control-om url /rpc/v1/approvals)"` returns
   `{"ok":true,"data":{"approvals":[]}}`.
2. **Unknown ids.** `approvals show nope`, `approve nope`, `approve apr_doesnotexist` and
   `deny apr_doesnotexist` each exit 2 with `<id> is not an approval id` and
   ``Run `om approvals list` to see pending ids.``
3. **Open the stream first.** `curl -sN --max-time 25 "$(control-om url
   /events/v1)" > approvals.sse &`.
4. **Seed rows.** A scratch Bun script outside the repo imports the worktree's
   `runner/db` (`openDb({home})`), `runner/approvals/ledger` (`ApprovalLedger`),
   `mcp/approval-gate` (`mcpApprovalRequest`) and `agent/consent-strip`
   (`consentStrippedArgs`), with `home` set to
   `.control-om/home-<port>/accounts/guest`. Open one
   `mcpApprovalRequest("room_delete", {room: "ops"}, "<run-id> delete #ops")`
   and one `kind: "tool_call"` row for `order_place` (the shape is
   `createChatCard` in `packages/cli/test/approvals-cli.test.ts`). Each `open`
   returns an `apr_…` id.
5. **List.** `approvals list` shows both rows with id, kind, expiry, tool and
   summary, then `2 pending: 2 mcp`. The MCP card expires 15 minutes out, the
   tool card 24 hours out.
6. **Approve from an agent session.** `approve <id>` exits 2 with `refusing to
   approve from an auto-approve harness (--permission-mode bypassPermissions)`
   and ``Run `om approve <id>` from a separate operator-controlled shell.`` on
   either row. That refusal is the expected result from any agent-launched run.
7. **Deny.** `deny <order id> --format json` returns the approval with
   `state: "denied"`, `resolvedBy: "cli"`, `kind: "tool_call"`; `deny <mcp id>`
   prints `denied <id> via cli`. `approvals list` is empty again.
8. **Stream.** `approvals.sse` holds two `approval_changed` and two
   `approval_resolved` events.

## Gotchas

- **`om approve` cannot succeed from an agent session.** The harness check runs
  before any store read, so `answer_on_card` and `approval_typed_mismatch` are
  unreachable from a run like this one. Proving them needs an operator shell.
- `approvals list` files a carded `tool_call` row under kind `mcp`; `deny
  --format json` on the same row says `tool_call` (README, known product gaps).
- A row seeded by a separate process lands in the database directly; the
  daemon announces it through its change feed, not at the moment of insert.
- Never seed a row through the operator's home. The script's `home` must be the
  lane's account directory.
