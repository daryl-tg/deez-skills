### OM Chat feature

**Repos:** `openmarket-chat`, `openmarket-chat-cloud`, `packages/rooms-client`.
**This family stops at `ready_for_review`.** It never merges, locally or
otherwise.

1. **Diagnose.** Route to the **explore** role. Load the
   **om-chat-design-system** skill before any UI decision.
2. **Desktop first**, per **principle-desktop-before-cloud**. The cloud twin
   does not start until desktop is proven.
3. **Failing check first**, then delegate implementation to the **executor**
   role, dispatched to Codex by default. Review the diff yourself.
4. **Inner loop while implementing:** `control-omchat doctor`, then replay the
   feature map recipe for what you changed. Deterministic, cheap, run after
   every meaningful edit. No exploration, no publishing.
5. **Terminal gate, once.** Drive the finished feature through `agent-browser`
   as a user would. Replay every scripted recipe first, then explore beyond
   them. Capture the accessibility snapshot and screenshot pair, publish the
   revision, and hand back the review URL.
6. **Wait for approval.** Per **principle-visual-approval-gates-delivery**.
   Silence is not approval.
7. **Port to cloud** and prove it separately on its own surface. A desktop
   screenshot is not cloud evidence.
8. Run `playbooks/om-chat-completion.md`.

**Reply:** what changed on each surface, the evidence URL, what is open.
