# OM Chat boundaries

## Repository roles

- `openmarket-chat` — the desktop and daemon source. Changes land and are proven
  here first.
- `openmarket-chat-cloud` — the hosted sister. **Parity is no longer required.**
  A desktop change is complete without a cloud port; do not open one, do not
  gate delivery on one, and do not treat the twin lagging as a defect. Port only
  when the operator asks for that change by name.
- `@openmarket/rooms-client` — owns browser-safe shared protocol behavior. Wire
  types, request clients, and domain models come from here. Never re-derive
  protocol behavior in a consumer.

**Never independently edit both copies of a synced file.** This survives the
parity retirement: if a run does touch both forks, it changes the source and
ports, because two independent edits of the same synced file is drift that no
fence in either repo can see.

The repos still carry their own mechanical fences (the parity manifest, the
shared-style coverage ratchet). Keep them green in whichever repo you are
editing. Green there is not a claim about the other fork.

## Services and ports

Use the shared `openmarket` HTTP MCP at `http://127.0.0.1:31338/mcp`. Never
spawn an operator stdio server. `openmarket-chat` stays a session-local stdio
child and is run-owned cleanup input.

`8097` is the operator's local dev server: never bind, target, reuse, or stop
it. Agent-only test servers take an allocated `18097`–`18197` port, recorded in
the run ledger, and are stopped only when run-owned. See
**principle-bind-assigned-ports** for the full table.

For daemon behavior use the real daemon-served rig. Use Vite directly only for
layout-only work.

## Git boundaries

Do not fetch, pull, merge, push local `main`, close a todo, deploy, or alter the
local `main` branch. Completion pushes only the promoted feature branch, creates
or reuses its review request, and announces that linked request.

The final branch is **checked out in the primary worktree, not merged into
main**. See **principle-promote-to-the-main-worktree**.
