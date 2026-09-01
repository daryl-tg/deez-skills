### OM Mobile feature

**Repo:** `openmarket-chat-app`, the Expo iOS and Android client. **This family
lands**, by squash-merge through the MR.

1. **Diagnose.** Route to the **explore** role. When the feature already exists
   on web, port the **logic contract**, never the web design. Judge whether the
   web flow suits mobile at all, then build mobile-native UI.
2. **Failing check first**, then delegate implementation to the **executor**
   role. Review the diff.
3. **Inner loop:** `control-openfloor doctor`, then replay the feature map
   recipe for what you changed.
4. **Terminal gate, once, on iOS**, in the queued permanent `openfloor-lane`
   simulator. One lane, queued: never a second simulator, per
   **principle-separate-before-serializing-shared-state**. Replay the scripted
   recipes, then explore. Capture the pair, publish, hand back the URL.
5. **Android goes to the verification delta**, named explicitly in the reply. It
   is not verified by this run, and saying so is required rather than optional.
6. **Wait for approval.**
7. Run `playbooks/om-mobile-completion.md`.

**Reply:** what changed, the iOS evidence URL, the Android delta stated plainly,
what is open.
