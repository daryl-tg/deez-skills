# Mobile shell navigation

The phone-width information architecture: five labelled roots, one pane at a
time, one Back to the owning root. Mobile is the **same bundle rendered
responsively**, not a separate app — so every mobile claim is a claim about the
web bundle at a narrow viewport.

## Sub-features

- The five-root tab bar: Home, Chats, Spaces, Library, om.
- One-pane contract: a root shows a list; opening an item replaces it with a
  detail pane. No tab bar beside conversation detail.
- One **Back** control per detail, returning to the owning root.
- Session-owned restoration: reopening a detail restores its tape position and
  its draft.
- Touch-target floor (44px) and control reachability inside scroll clips.
- Keyboard-inset behavior when the on-screen keyboard is up.

## How to get to it (user POV)

On a phone you get a tab bar along the bottom with five destinations. Tapping
**Chats** lists your conversations. Tapping one opens it full-screen with a
**Back to Chats** control at the top — the tab bar gets out of the way. Going
back returns you to the list where you left it.

## Driving it with control-om-chat

```bash
export AGENT_BROWSER_SESSION=verify-mobile
agent-browser set viewport 390 844
agent-browser open "$(./control-om-chat url \
  'tools/visual/shell-fixture.html?view=home&alerts=quiet')"
```

The widths the navigation suite gates at are **320, 360, 390, 430, 768**. Drive
the matrix, not just 390 — 320 is where controls overflow their clips. Other
mobile suites in the repo use a shorter list (320, 360, 390, 430, no 768), so
match the suite you are defending rather than assuming one canonical matrix.

Handles that resolve today:

```bash
agent-browser find role button click --name "Chats"   --exact
agent-browser find role button click --name "Spaces"  --exact
agent-browser find role button click --name "Library" --exact
agent-browser find role button click --name "om"      --exact
agent-browser find role treeitem click --name "Direct message with ana, 2 unread"
agent-browser find role button click --name "Back to Chats"
```

The tab bar itself is `navigation` named **"Mobile navigation"**; scope to it
when a label is ambiguous.

The one-pane contract is checkable directly, and this is the assertion worth
capturing:

```bash
# On a root: exactly one root marker, zero detail markers, no Back control.
agent-browser eval 'document.querySelector("[data-mobile-root]")?.getAttribute("data-mobile-root")'
agent-browser eval 'document.querySelectorAll("[data-mobile-detail]").length'   # 0 on a root, 1 in a detail

# In a detail: exactly one Back, and the tab bar is gone.
agent-browser snapshot -c | grep -iE 'Back|Mobile navigation'
```

Useful modifiers: `?keyboard=<px>` raises a simulated keyboard inset,
`?text=200` doubles the root font size, `?bulk=120` loads a long tape,
`?draft=<text>` seeds a composer draft so restoration is observable.

## Gotchas

- Viewport is `agent-browser set viewport <w> <h>`. There is no bare
  `viewport` command; it fails with "Unknown command" and leaves you at
  1280×633, which is not a phone.
- The root marker is `[data-mobile-root="<root>"]` and detail is
  `[data-mobile-detail]` — attribute selectors, not roles. Quote them carefully
  through the shell.
- **`[data-mobile-detail]` does not cover every detail.** It is set only for
  `room`, `dm`, and `world`. Library notes and settings open through a
  different full-screen path marked `[data-mobile-takeover]` — set by
  `Panel.tsx` and `MobileSurface.tsx`, used by `DocPane.tsx` and
  `SettingsShell.tsx`. Asserting `[data-mobile-detail].length === 1` there
  reads 0 while the UI is correctly in a one-pane detail — check the takeover
  marker instead.
- **The om root is not a takeover.** `agent` and `agents` both classify to the
  `om` root tab, and that surface renders inside the root card with the tab bar
  still mounted — no Back control, no `[data-mobile-takeover]` anywhere in
  `AgentPane` or `AgentCenterPane`. The per-agent detail panel went away in
  Agent Center v6, so there is no om thread left to take the screen; an
  individual agent DM is an ordinary `dm` detail.
- The Open World tab is **not** a sixth root. It classifies under **Spaces**,
  so the tab bar stays five.
- Switching roots does **not** always change the URL hash meaningfully
  (`Chats` lands on `#/`). Assert the DOM marker, not the route, for root
  switches — the route *is* reliable for detail opens.
- A "one Back" assertion must allow three spellings: `Back`, `Back to X`, and
  `Back to conversation`. The third comes from `#653`: opening OM settings,
  schedules or alerts from inside Your om renders a `Back to conversation`
  control, and it is not gated on `useIsMobile()`, so it appears at phone width
  too — without a takeover or a detail marker, still inside the om root card
  with the tab bar mounted. You will not meet it in the fixture, because Your om
  there is stuck on its not-running empty state
  ([om-and-agents.md](om-and-agents.md)); it needs a running daemon.
- Chromium at a narrow viewport is not iOS WKWebView or Android WebView. A
  green matrix here is a `web-bundle` claim only; native certification is
  still open (`docs/mobile-native-release-checklist.md`).
