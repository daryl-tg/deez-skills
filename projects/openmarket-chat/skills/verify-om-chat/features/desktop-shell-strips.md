# Desktop shell strips

The desktop app (Electron, `desktop/`) injects `window.omShell` before the
bundle runs. The shared Shell reads it and shows up to three status strips at
the top of the app (`packages/chat-ui/src/components/Shell.tsx:3355-3357`).
Neither browser host has the bridge, so a person sees these strips only in the
desktop app.

## Sub-features

- **App update strip** (`DesktopUpdateStrip.tsx`): a `role="status"` strip
  `.desktop-update-strip[data-update-phase]`. The message and one action button
  follow the phase. `available` shows **OM Chat <version> is verified and ready
  for your approval.** with **Install update**. `mandatory` shows **Install
  now**, `ready` shows **Restart now**, a retryable `failed` shows **Retry
  update**, and `channel-unhealthy` shows **Check again**. The button calls
  `omShell.requestUpdateAction(<value>)`, for example `accept`.
- **OpenMarket (daemon) update strip** (`DesktopDaemonUpdateStrip.tsx`):
  `[data-daemon-update-phase]`. `available` shows **OpenMarket <version> is
  ready to update inside OM Chat.** with **Update OpenMarket**. `updating` has no
  button. `failed` shows **Try again**. The button calls
  `omShell.requestDaemonUpdate({ action: "install" })`.
- **Background strip** (`DesktopBackgroundStrip.tsx`): `[data-background-phase]`.
  `app-only` shows **Background features run only while OM Chat is open.** with
  **Enable background**. If the reason is `repair-failed`, the button reads
  **Try again**. Each `attention` reason has its own sentence and a **Review**
  button. The phases `checking` and `background` render nothing. The button
  calls `omShell.requestBackgroundAction("enable" | "review")`.

## How to get to it (user POV)

Open the OM Chat desktop app. A strip appears above the chat when an app or
OpenMarket update is waiting, or when background features are off. Press the
strip's button to act on it.

## Driving it with control-om-chat

The fixture lane has no `window.omShell`. Each strip subscribes once at mount,
so an `eval` after load is too late. Register a bridge stub as an
**init script** before the first navigation:

```bash
cat > "$SCRATCH/omshell-init.js" <<'JS'
window.__omShellCalls = [];
window.omShell = {
  getUpdateStatus: () => ({ phase: "available", version: "9.9.9" }),
  onUpdateStatus: () => () => {},
  requestUpdateAction: (a) => { window.__omShellCalls.push("update:" + a); return Promise.resolve(true); },
  getDaemonUpdateStatus: () => ({ phase: "available", version: "1.2.3" }),
  onDaemonUpdateStatus: () => () => {},
  requestDaemonUpdate: (a) => { window.__omShellCalls.push("daemon:" + JSON.stringify(a)); return Promise.resolve(true); },
  getBackgroundStatus: () => ({ phase: "app-only", reason: "not-registered" }),
  onBackgroundStatus: () => () => {},
  requestBackgroundAction: (a) => { window.__omShellCalls.push("background:" + a); return Promise.resolve(true); },
};
JS
export AGENT_BROWSER_SESSION=verify-strips
agent-browser --init-script "$SCRATCH/omshell-init.js" open about:blank
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser eval '(()=>JSON.stringify([...document.querySelectorAll(".desktop-update-strip,[data-background-phase]")].map(s=>s.innerText)))()'
agent-browser find role button click --name "Install update"
agent-browser find role button click --name "Update OpenMarket"
agent-browser find role button click --name "Enable background"
agent-browser eval '(()=>JSON.stringify(window.__omShellCalls))()'
#   ["update:accept","daemon:{\"action\":\"install\"}","background:enable"]
```

To drive another phase, change the stub's return value and open the route in a
new session. A stub `on*Status` callback never fires, so the strip cannot change
phase after load.

## Gotchas

- **This proves the renderer, not the desktop.** The stub stands in for the
  Electron preload. Real update checks, a signed handoff, the daemon install and
  launchd registration need the shell itself (`cd desktop && bun run probe` /
  `smoke`; agents never launch a visible window).
- Defining `window.omShell` also turns on the Shell's other desktop-only paths
  (`Shell.tsx:1400`, `:2710`: desktop setup and daemon recovery). A minimal stub
  without `getAppSetupStatus` keeps them quiet. Add only the methods you mean to
  drive.
- The background strip needs all three of `getBackgroundStatus`,
  `onBackgroundStatus` and `requestBackgroundAction`; without any one of them
  it renders nothing (`DesktopBackgroundStrip.tsx:28-42`).
- `/chat/` was not driven. The strips are shared code, but the hosted app never
  has a bridge.

### Verification record

**Last verified:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160) through the `--init-script` `window.omShell` stub: **Install update** (OM Chat 9.9.9), **Update OpenMarket** (1.2.3) and **Enable background**; **Enable background** and **Update OpenMarket** recorded `background:enable` and `daemon:{"action":"install"}`. **Limitations:** unchanged; phase changes after load not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/` (`strips-01`).

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18143) `?view=room&alerts=quiet` with the init-script bridge above: three strips rendered, **available: OM Chat 9.9.9 is verified and ready for your approval. / Install update**, **available: OpenMarket 1.2.3 is ready to update inside OM Chat. / Update OpenMarket** and **app-only: Background features run only while OM Chat is open. / Enable background**. Pressing the three buttons recorded `update:accept`, `daemon:{"action":"install"}` and `background:enable`, and no error overlay appeared. **Limitations:** only the `available` and `app-only` phases were driven. The other phases are read from source. Real Electron delivery is unverified. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`strip-01-desktop`).
