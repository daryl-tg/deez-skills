# The monthly model spend limit

*Re-driven on main 2026-11-13 (nightly), tree `298c469dd7` (v0.495.0+internal), bare lane on 18187 with an openai-compatible fake model on 18186 and one seeded priced row in `llm_rounds` ($5.00, this month; test scaffolding). `om config set spend.monthly_usd 1`, then `om chat --once` exited 1 with `Monthly model spend: $5.00 of $1.00 used.` and `Raise it: om config set spend.monthly_usd <n>`; the fake's request count stayed at 3. `om usage llm --format text` printed `Limit:    $5.00 of $1.00 this month (500%)` and `Unpriced: 3 rounds this month, counted as $0`; the JSON carries `month.spent_usd`, `limit_usd`, `percent` and `unpriced_rounds`. `config set spend.monthly_usd 0` from the run's own shell exited 2 (`Raising spend.monthly_usd needs a person at the terminal`): clearing the limit counts as raising it. Not re-driven: the watch hold, the agent limit, the notices. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261113/r1/` (`cli/11-spend-cap.txt`).*

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

- Bare lane as in [persona-chat-tools.md](persona-chat-tools.md). An `openai-compatible` model is never priced, so its rounds count as zero whatever usage it reports. To reach the limit, either dial a catalog model through a subscription lane's base-URL seam (`OM_PROVIDER_BASE_URL_ANTHROPIC`), or seed one priced row into the lane's `llm_rounds` table for this month and say so in the evidence.
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

- The `Model limit` row in plain `om usage` is unit-tested only. The `Unpriced` row in `om usage llm` is live (2026-11-13).
- Setting the limit to `0` clears it, so an auto-approve harness is refused it like a raise.
- A subscription sign-in's figure is what an API key would have paid, so the limit is notional there.
- Rounds in the files `round-door.test.ts` lists as not yet routed pass no limit.
- The daemon's budgets RPC on loopback is not behind the terminal check.
