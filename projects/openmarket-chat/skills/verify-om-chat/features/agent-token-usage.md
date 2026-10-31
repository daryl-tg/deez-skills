# Agent token usage

## Sub-features

- Answer footer and tool activity summary show reported usage in tokens.
- Counts use lowercase `k` and uppercase `M`, with at most one decimal.
- Hover titles preserve the exact total. Missing usage omits the count.
- Expanding tool activity preserves the usage summary.
- The `failed` state of `agent-presentation-fixture.html` reads **Tool activity
  1 failed** above the tool rows (`room_list`, `watch_list`, `market_resolve`);
  the failed call shows `ok:false` on its row.

## How to get to it (user POV)

Open an om conversation with a completed answer. Read usage beside the answer's
elapsed time or in the tool activity header. Expand tool activity to see its
calls.

## Driving it with control-om-chat

The standalone fixture mounts the real AgentPane with a completed turn. The markup lives in `AgentPresentation.tsx`, not `AgentPane.tsx`: `formatTokenUsage` (`:241-269`), `.agent-answer-meta` (`:392`) and `.agent-activity-summary-detail` (`:654`). The away remote-control pane renders the same presentation (`packages/chat-ui/test/ui/remote-agent-presentation-parity.test.tsx`), so `remote-home-fixture.html?state=live` is the second place to look. At `f8b68bf7` the default fixture's `.agent-answer-meta` reads `12:00 PM · 1 tool · 2.0s · 12.3k tokens`.

```bash
agent-browser open "$(control-om-chat url 'tools/visual/agent-usage-fixture.html')"
agent-browser snapshot
agent-browser find role button click --name 'Expand tool activity'
agent-browser snapshot
agent-browser find role button click --name 'Collapse tool activity'
```

Default usage is `12.3k tokens`. Use `?tokens=1250000` for `1.3M tokens`,
`?tokens=0` for reported zero, and `?tokens=missing` for omitted usage. Each
turn also carries a price to detect accidental price rendering. Test desktop
and 375px phone widths. `?theme=light` selects light mode.

Check `.agent-answer-meta` and `.agent-activity-summary-detail` for both the
visible count and their exact-count `title` attributes. Save an accessibility
snapshot and screenshot for each layout.

## Gotchas

This fixture proves rendering with seeded usage. It cannot prove provider
metering, daemon transport, or history persistence. Copy, retry, file-to-doc,
and prompt editing are outside its wired journey. The full shell's default
agent fixture shows the daemon-off state instead of this transcript.

### Verification record

**Last verified:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) `agent-usage-fixture.html`: **12:00 PM · 1 tool · 2.0s · 12.3k tokens**, **Expand tool activity** → **Collapse tool activity**; `?tokens=1250000` → **1.3M tokens**. **Limitations:** the `failed` presentation state was load-smoked (`agent-presentation-fixture.html?state=failed`) but its text was not re-read; input+output fallback and daemon accounting stay pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`usage-01`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135) `agent-usage-fixture`: **Expand tool activity** → **Collapse tool activity**, `.agent-answer-meta` **12:00 PM · 1 tool · 2.0s · 12.3k tokens**; `?tokens=1250000` → **1.3M tokens**; `agent-presentation-fixture?state=failed` → **Tool activity 1 failed**. **Limitations:** Daemon accounting; the input+output fallback; the hover title was not read. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` `agent-usage-fixture`: `12.3k tokens`, `?tokens=1250000` → `1.3M tokens`, `?tokens=missing` → no count; **Expand tool activity** → **Collapse tool activity**; `agent-presentation-fixture?state=collapsed` toggled the same way. **Limitations:** Daemon accounting. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/`.

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `agent-usage-fixture` `.agent-answer-meta` title `12,345 tokens`; `agent-presentation-fixture?state=expanded` showed **Collapse tool activity**. **Limitations:** Daemon accounting and the input+output fallback not seedable. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 03, 38–39).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `agent-usage-fixture` `.agent-answer-meta` title `12,345 tokens`; `agent-presentation-fixture?state=expanded` showed **Collapse tool activity**. **Limitations:** The other `tokens=` seeds, the input+output fallback and daemon accounting were not driven. Evidence: none captured for this row.

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `agent-usage-fixture` `.agent-answer-meta` title `12,345 tokens`, and `agent-presentation-fixture?state=expanded` showed **Collapse tool activity**. **Limitations:** `tokens=1250000`, `tokens=1`, `tokens=missing`, the input+output fallback and daemon accounting were not re-driven. Previous record: 2026-10-26 at `5820fbea`.
