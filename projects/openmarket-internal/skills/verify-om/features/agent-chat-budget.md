# A chat agent stops loudly at its budget

*Re-driven on main 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0; #2304), bare lane on 18165 with a scripted fake model on 18164. Driven: a run whose fake reply reported 45,100 tokens failed `budget_exhausted` `explain spent 45,100 tokens: past 40,000 tokens a run` (`usage.tokens 45100`) with one inbox item `Budget stop: explain` / `Cap: 40,000 tokens a run` / `Resets: next run`; paced task-door submissions to `explain` with distinct asks answered 200 until the 51st run of the UTC day, which answered 429 `{"code":"budget_exhausted","text":"explain is out of budget: 50 runs a day.","fix":"Try again at 2026-11-05T00:00:00.000Z","resumeAt":…}` and raised one more item (`Cap: 50 runs a day`, `Resets: 2026-11-05T00:00:00.000Z`); unpaced submissions first met the door's queue cap (429 `agent_busy` `explain is busy, 16 waiting`). Not driven: the 400,000-tokens-a-day stop, the hourly `maxTurnsPerHour` stop, the @mention path. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/bare-task-big.json`, `cli/bare-budget-*`, `cli/bare-inbox-*`).*

*Verified: 2026-11-03, branch `daryl/agent-budgets-loud` tree `2e933a0cf` (on main `c4428a3d7`, not yet merged), lane on 18154, bare lane with a fake model on 18155. Driven: 51 task-door submissions to `explain` with distinct asks, and the inbox read. Not driven: the 40,000-token per-run stop (the fake model reports no usage; pinned by `roster-chat-budget.test.ts` and `roster-harness-om.test.ts`) and the @mention path (needs rooms; pinned by `roster-reply-watcher.test.ts`). Evidence: `~/Documents/dev-notes/om-agent-creation/run-artifacts/budget-lane-18154/`, gallery `http://127.0.0.1:8098/agent-budgets-20261103/r1/`.*

Every chat agent has one budget: 40,000 tokens a run, 50 runs a day, 400,000 tokens a day (`CHAT_AGENT_BUDGET`, `packages/roster/src/chat-budget.ts`). Hitting it refuses the run with a reason and raises one inbox item; nothing fails silently.

## Sub-features

- Usage is recorded per run and attempt in `roster_chat_budget_usage`.
- The task door answers 429 `budget_exhausted` with `text`, `fix` and `resumeAt`.
- One `budget_exhausted` inbox item per agent, cap and UTC day (id `inbox_budget_<instance>_<cap>_<day>`, cap `run_tokens` or `daily_runs`), rows `Budget stop: <agent>`, `Cap: …`, `Resets: <ISO time>` (`Resets: next run` for the per-run stop).
- The per-run stop fails the run (`state: failed`, `error.code: budget_exhausted`, `explain spent 45,100 tokens: past 40,000 tokens a run`) after the turn that crossed it; the reply is not posted.
- Only chat agents are capped; coding (work) agents are exempt, and a per-credential `budgets.maxTurnsPerHour` refuses `budget_exhausted` `<agent> is out of turns this hour.` with no `resumeAt` (source).
- The reply watcher's @mention path raises the same inbox item instead of dropping the run silently; it posts nothing in the room.

## How to get to it (user POV)

Use an agent heavily. When it hits a cap, the run is refused with the cap and the reset time, and the inbox shows one budget stop.

## Driving it with control-om

Bare-lane recipe as in [agent-create.md](agent-create.md). The door merges identical asks into one run, so give every submission a distinct ask. It also queues at most 16 runs per agent and answers 429 `agent_busy` beyond that, so wait for each run (`GET /rpc/v1/roster/tasks/<id>?wait=25000`; the door refuses more with `malformed_body` `wait must be 0 to 25000 ms.`, proved 2026-11-09) before the next. For the per-run stop, have the fake model's final SSE chunk carry `usage` of more than 40,000 tokens for one ask.

```sh
for i in $(seq 1 51); do
  curl -sS -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:$OM_LANE_PORT/rpc/v1/roster/tasks \
    -H 'content-type: application/json' \
    -d "{\"id\":\"b-$i\",\"agent\":\"explain\",\"ask\":\"explain item $i\",\"requestedBy\":{\"surface\":\"direct\",\"userId\":\"local\"}}"
done
# 200 for runs 1-50 of the UTC day, then 429:
# {"code":"budget_exhausted","text":"explain is out of budget: 50 runs a day.","fix":"Try again at <next UTC midnight>","resumeAt":…}
curl -sS http://127.0.0.1:$OM_LANE_PORT/rpc/v1/roster/inbox
# exactly one budget_exhausted item
```

## Gotchas

- The count is per UTC day, so a lane that already ran tasks today reaches the cap sooner.
- The inbox reset time is a raw ISO timestamp for a daily stop and `next run` for a per-run stop.
- `agent_busy` is also a 429; read `code` before calling a refusal a budget stop.
- A fake model that sends no `usage` makes every run cost 0 tokens, so the token caps never fire.
