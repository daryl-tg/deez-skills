### OM Chat feature

**Repo:** `openmarket-chat` — one workspace holding both hosts (`/rooms` at
the root, `/chat/` in `apps/cloud`) over one shared `packages/chat-ui`. Protocol
comes from `@openmarket/rooms-client`. **This family stops at
`ready_for_review`.** It never merges.

Read `references/om-chat-boundaries.md` before editing. The short version: UI
lives in `packages/chat-ui` and a change there hits both hosts at once, host
`src/` is re-export facades, and the parity/sync tooling is deleted.

1. **Resolve the candidate.** Read the root `AGENTS.md` and, for cloud work,
   `apps/cloud/AGENTS.md`. **Name the hosts the change touches** — shared
   (`packages/chat-ui`, both hosts) or host-local — and say so before editing.
   Route to the **explore** role, pointing it at `packages/chat-ui/src/`, never
   the facades under `src/`. Load **om-chat-design-system** before any user-visible
   UI decision, and **om-chat** only when task context is an OM Chat link.
2. **Failing check first**, then delegate implementation to the **executor**
   role with a specific scope. Review the diff yourself.
3. **Static gates**, from the workspace root, against the final candidate.
   Rooms/desktop: `bun run lint && bun run typecheck && bun run build`, then
   `tools/check-dist.ts` and `tools/test-fast.ts`. Cloud:
   `bun run verify:cloud`. **Run both whenever `packages/chat-ui` changed** —
   per **principle-prove-every-host**, one green gate says nothing about the
   other host. Keep `test/chat-ui-workspace.test.ts` green rather than widening
   its exceptions. **Isolate baseline failures against the branch point; never
   call a partially failing suite green.**
4. **Inner loop while implementing:** `control-om-chat doctor`, then replay the
   feature map recipe for what changed. Cheap, deterministic, after every
   meaningful edit.
5. **Freeze and review.** Record the commit or tree hash and the exact diff
   range. Review that frozen diff against the acceptance criteria and
   non-goals. Fix substantive findings, rerun the gates those fixes touch,
   re-freeze. Store the review output with the run evidence.
   **Cross-model review is off by default here** — it cost more than it
   returned. Run one only when the operator asks by name.
6. **Terminal gate, once.** A headless `agent-browser` journey per affected
   **host**, fresh session per run, host, and revision. A `/rooms` capture is
   never evidence for `/chat/`. Prove every changed
   control is visible, enabled, on-screen, clickable, and reaches its outcome.
   Save the accessibility output, the screenshot, and any console or network
   errors. Never open a visible browser on the operator's desktop; CDP is for
   diagnosing a failed gate only.
7. **Publish and wait for approval**, per
   **principle-visual-approval-gates-delivery**.
8. Run `playbooks/om-chat-completion.md`.

**Before handing off: did you drive a surface the map does not cover?** If the
terminal gate exercised anything with no feature file, write one now, following
the four-H2 contract in `features/README.md`. You have the handles in front of
you and you know what proved it works. A maintenance pass can recover that later
from source, but it costs a full live sweep to learn what you already know right
now. Per **principle-encode-lessons-in-structure**: capture it where it is
cheap.


**There is no cloud port.** Shared UI is imported, not copied — a
`packages/chat-ui` change is already in both hosts the moment it lands. What
that buys you is one edit; what it costs you is two gates and two evidence
sets. Never look for a manifest to refresh or a twin to sync.

**Reply:** what changed per surface, the gate results, the evidence URL, what is
open.
