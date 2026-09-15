---
name: principle-prove-every-host
description: "Apply when a change touches shared UI consumed by more than one application host. The change reaches every host at once, so every host runs its own gate and carries its own evidence. One host's screenshot is never proof for another."
disable-model-invocation: true
---

# Prove every host

Shared code has more than one consumer. A change to it is not one change that
later gets ported — it is already live in every host the moment it lands. So
the question is never *which host goes first*; it is *which hosts did I just
change, and did I prove each one*.

**Why:** a shared edit makes every consumer a candidate source for any defect
found afterwards. Proving one host and inferring the rest leaves the others
untested while reading as finished. The inference is cheap and wrong: hosts
differ in boot, transport, auth, routing and asset base, which is exactly where
a shared component breaks differently in each.

**The rule.**

- **Name the hosts before you edit.** A change under a shared package touches
  all of them. A change under one host's own source touches only that one. Say
  which, in the plan, before the first edit.
- **Run every affected host's gate.** Both gates green, or the work is not
  done. A green gate in one host is not a claim about the other.
- **Capture evidence per host, on that host's own surface.** Different URL,
  different session, different screenshot. A `/rooms` capture is not evidence
  for `/chat/`, and neither is "it is the same component".
- **Never one review request spanning hosts proven separately.** Each side
  carries the evidence that proves it.
- **A host that cannot be proven is reported, not assumed.** Say which host is
  unproven and why, per **principle-finish-or-report**. Do not round it up.

Proof means the running product, per **principle-prove-on-the-real-surface** —
not that the shared code compiles against both tsconfigs.

## OM Chat, concretely

`openmarket-chat` is one workspace with two hosts. `packages/chat-ui` holds the
UI; the repo root hosts `/rooms` (desktop and daemon), `apps/cloud` hosts
`/chat/`. Editing `packages/chat-ui` changes both.

```bash
# rooms / desktop gate
bun run lint && bun run typecheck && bun run build
bun --tsconfig-override ./tsconfig.json tools/check-dist.ts
bun --tsconfig-override ./tsconfig.json tools/test-fast.ts
# cloud gate
bun run verify:cloud
```

`test/chat-ui-workspace.test.ts` is the fence that keeps a host from quietly
forking a screen instead of sharing it. Keep it green; extend a host adapter
rather than widening its app-local renderer exceptions.
