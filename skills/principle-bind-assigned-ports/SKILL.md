---
name: principle-bind-assigned-ports
description: "Apply whenever starting a server, choosing a port, or handing back a URL. Ports are assigned, never chosen. Bind 127.0.0.1 explicitly. Anything the operator opens must be forwarded."
disable-model-invocation: true
---

# Bind assigned ports

Ports are assigned by the reserved-ports table, never picked because they were
free.

**Why:** neither failure mode has a local symptom. A rig on an unforwarded port
is invisible from the operator's laptop; a rig squatting a reserved port breaks
the workflow that owns it. `curl` on the host passes either way.

**Two invariants.**

1. **Bind `127.0.0.1` explicitly.** The forwards dial IPv4 loopback, so a server
   on `[::1]` answers on the host and is dead from the laptop. Pass the flag;
   do not trust a framework default.
2. **Anything the operator opens sits on a forwarded port.** If the work needs a
   new one, say so and give the `-L` line. Never silently pick a free port and
   hand back a URL that cannot be reached.

**Owned ports, and the rule each carries.**

- `8097` local dev server. Never bind, target, reuse, or stop it. Preflight; if
  busy, ask rather than kill.
- `8098` device-owned review renderer. Hands off. Never start, restart, track,
  stop, or replace it. Publish through it; never author a revision file.
- `31337` the `om` daemon. `om service restart` is the only handle.
- `31338` singleton HTTP MCP. Never start a second.
- `4178`, `13137` forwarded general-purpose slots. Run-owned: stop what you
  started.
- `4848` agent-browser dashboard. Agent-owned, not tunnelled. Never handed over.
- `18097`–`18197` agent test servers. Allocate and preflight one per lane, stop
  only what the run started. Deliberately not tunnelled, so never a review URL.
