# A chat agent stops loudly at its budget

*Verified: 2026-11-03, branch `daryl/agent-budgets-loud` tree `2e933a0cf` (on main `c4428a3d7`, not yet merged), lane on 18154, bare lane with a fake model on 18155. Driven: 51 task-door submissions to `explain` with distinct asks, and the inbox read. Not driven: the 40,000-token per-run stop (the fake model reports no usage; pinned by `roster-chat-budget.test.ts` and `roster-harness-om.test.ts`) and the @mention path (needs rooms; pinned by `roster-reply-watcher.test.ts`). Evidence: `~/Documents/dev-notes/om-agent-creation/run-artifacts/budget-lane-18154/`, gallery `http://127.0.0.1:8098/agent-budgets-20261103/r1/`.*

Every chat agent has one budget: 40,000 tokens a run, 50 runs a day, 400,000 tokens a day (`CHAT_AGENT_BUDGET`, `packages/roster/src/chat-budget.ts`). Hitting it refuses the run with a reason and raises one inbox item; nothing fails silently.

## Sub-features

- Usage is recorded per run and attempt in `roster_chat_budget_usage`.
- The task door answers 429 `budget_exhausted` with `text`, `fix` and `resumeAt`.
- One `budget_exhausted` inbox item per stop, rows `Budget stop: <agent>`, `Cap: …`, `Resets: <ISO time>`.
- The reply watcher's @mention path raises the same inbox item instead of dropping the run silently; it posts nothing in the room.

## How to get to it (user POV)

Use an agent heavily. When it hits a cap, the run is refused with the cap and the reset time, and the inbox shows one budget stop.

## Driving it with control-om

Bare-lane recipe as in [agent-create.md](agent-create.md). The door merges identical asks into one run, so give every submission a distinct ask.

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
- The inbox reset time is a raw ISO timestamp.
