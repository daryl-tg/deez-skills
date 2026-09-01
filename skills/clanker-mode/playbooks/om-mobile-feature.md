### OM Mobile feature

**Repo:** `openmarket-chat-app`, the Expo iOS and Android client. The native app
is OpenFloor; the company, services, and protocol references stay OpenMarket.
**This family lands**, by squash-merge through the MR.

This playbook never edits `openmarket-chat` or `openmarket-chat-cloud`. A
desktop or web change is `playbooks/om-chat-feature.md`.

1. **Resolve the candidate.** Read the repo's `CLAUDE.md` and `AGENTS.md`, plus
   the doc owning the touched surface: `docs/NAVIGATION.md` for `src/app/` or
   `src/navigation/`, `docs/ROOMS_CACHE.md` for persistence,
   `docs/PUSH_NOTIFICATIONS.md` for push. **Query the graphify graph before
   grep** for any where-is or what-calls question.
2. **With a web reference**, treat `openmarket-chat` as read-only. Port the
   **logic contract**, never the web design. Judge whether the web flow suits
   mobile at all, then build mobile-native UI.
3. **Failing check first**, then **dispatch implementation to Codex**. Wire
   types and domain models come
   from `@openmarket/rooms-client` subpath imports. Load **animate-expo** for
   motion work.
4. **Static gates carry the whole loop**, since they need no device:
   `pnpm run lint`, `pnpm run typecheck`, `pnpm test`, `pnpm run export:smoke`.
   Isolate baseline failures against the branch point; never call a partially
   failing invocation green.
5. **Device verification is one shot, at the end.** Do not open a lane
   mid-implementation to spot-check. A booted simulator is the scarcest resource
   on the machine, and every extra session lengthens the queue for other
   features. Implement until the static gates pass and the candidate is
   complete, **then** take a lane once and drive every changed journey in a
   single session. See `references/openfloor-lane.md`.
6. **Android goes to the verification delta**, named explicitly in the reply.
   Not verified by this run, and saying so is required.
7. **Publish and wait for approval.**
8. Run `playbooks/om-mobile-completion.md`.

**Reply:** what changed, the gate results, the iOS evidence URL, the Android
delta stated plainly, what is open.
