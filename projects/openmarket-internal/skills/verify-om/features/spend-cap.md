# The monthly model spend limit

*On main since 2026-11-12: PR #2448 merged as `1d586e05b6`. Its roster test is now `packages/cli/test/private/roster/agent-spend-cap.test.ts`. Not yet re-driven on main.*

*Re-checked 2026-11-11 (nightly, source only) against origin/main `0ad4768f66` (v0.494.0): PR #2448 is still open and nothing of it is on main. Headings renamed to the map's four-H2 contract; no recipe changed.*

*Verified: 2026-11-10, branch `daryl/spend-cap` tree `e9762387e1` (PR #2448, on origin/main `0ad4768f66`), bare lane on 18166 with a scripted fake model on 18162 that reports usage under a priced model id. Gallery `http://127.0.0.1:8098/spend-cap/r2/` (6 screenshots). Not on main until the PR merges.*

`spend.monthly_usd` is one dollar limit per UTC month for every model round that passes the round door. An agent credential's `maxSpendUsd` is that agent's own limit per month. A round past either limit is refused before any provider is dialed.

## Sub-features

- Chat past the limit answers with one cause line and one fix line and sends nothing to the model.
- A watch's judge round past the limit is skipped, and its posts are held as `held: over this month's limit`.
- An agent past its own limit has its next turn declined with `agent_spend_cap_reached`. Other agents keep working.
- `om agent budgets set <name> --max-spend-usd <n|unlimited>` changes an agent's limit.
- Raising or clearing either limit from an auto-approve harness is refused with exit 2. Lowering one always works.
- `om usage llm` prints `Limit` and `Unpriced` rows, and `--by agent` groups spend by agent.
- One notice at 80 percent and one at the limit, each once per month.
- Unset or `0` is no limit and nothing changes.

## How to get to it (user POV)

1. `om config set spend.monthly_usd 20`
2. Use chat or let watches run.
3. `om usage llm` to see the limit row.

## Driving it with control-om

- Bare lane as in [persona-chat-tools.md](persona-chat-tools.md). The fake model must report `usage` and use a model id the price catalog knows, or every round is unpriced and counts as zero.
- Chat makes two start-up probe rounds that cost money on a priced fake. Make the fake bill only requests that carry tools, or set the limit above the probes' cost.
- Count the fake model's request log before and after a refused turn. No growth is the proof that nothing was dialed.
- The watch case: `om event push <watch> --text ... --kind filing` on a watch with a judge, then read the lane log for `judge skipped` and `om watch unjudged <watch> --days 1 --format json` for the held reason.
- The agent case uses the house agent or a roster agent as in [agent-create.md](agent-create.md). A bare lane may boot with no house credential.
- The harness refusal: run the raise from a parent process that carries an auto-approve flag.
- Plain `om usage` cannot run on a bare lane, because its gateway address is dead by design. Use `om usage llm`.

### What to check

- The refused turn's two lines, and the unchanged request count.
- The held reason says this month, not today.
- `credential_id` is set on a round the house agent ran.

## Gotchas

- The `Model limit` row in plain `om usage` and the `Unpriced` row are unit-tested only.
- A subscription sign-in's figure is what an API key would have paid, so the limit is notional there.
- Rounds in the files `round-door.test.ts` lists as not yet routed pass no limit.
- The daemon's budgets RPC on loopback is not behind the terminal check.
