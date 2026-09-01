# OM Chat boundaries

## Repository roles

- `openmarket-chat` — the desktop and daemon source. Changes land and are proven
  here first.
- `openmarket-chat-cloud` — the ordered hosted sister. Receives only approved,
  hosted-compatible behavior, after desktop is proven.
- `@openmarket/rooms-client` — owns browser-safe shared protocol behavior. Wire
  types, request clients, and domain models come from here. Never re-derive
  protocol behavior in a consumer.

**Never independently edit both copies of a synced file.** Change the source,
then port. Two independent edits of the same synced file is the drift this rule
exists to prevent.

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
