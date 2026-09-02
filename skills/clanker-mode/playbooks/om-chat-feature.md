### OM Chat feature

**Repos:** `openmarket-chat` (desktop/daemon source), `@openmarket/rooms-client`
(browser-safe shared protocol), and `openmarket-chat-cloud` only when the
operator names it. **This family stops at `ready_for_review`.** It never merges.

Read `references/om-chat-boundaries.md` before editing. The short version:
cloud parity is retired, the repo's own fences still have to be green, and a
synced file is never edited independently in both copies.

1. **Resolve the candidate.** Read each affected repo's `AGENTS.md`. Route to
   the **explore** role. Load **om-chat-design-system** before any user-visible
   UI decision, and **om-chat** only when task context is an OM Chat link.
2. **Failing check first**, then delegate implementation to the **executor**
   role with a specific scope. Review the diff yourself.
3. **Static gates**, per repo, against the final candidate. For
   `openmarket-chat`: lint, typecheck, build, `bun tools/check-dist.ts`, tests.
   For `openmarket-chat-cloud`: frozen install in the owned worktree only when
   needed, then lint, typecheck, build, dist check, tests. **Isolate baseline
   failures against the branch point; never call a partially failing suite
   green.**
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
   product, fresh session per run, repo, and revision. Prove every changed
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


**No cloud port.** Parity with `openmarket-chat-cloud` is retired: a desktop
change is done without it. Port only when the operator names that change.

**Reply:** what changed per surface, the gate results, the evidence URL, what is
open.
