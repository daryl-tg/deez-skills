# Agent token usage

## Sub-features

- Answer footer and tool activity summary show reported usage in tokens.
- Counts use lowercase `k` and uppercase `M`, with at most one decimal.
- Hover titles preserve the exact total. Missing usage omits the count.
- Expanding tool activity preserves the usage summary.

## How to get to it (user POV)

Open an om conversation with a completed answer. Read usage beside the answer's
elapsed time or in the tool activity header. Expand tool activity to see its
calls.

## Driving it with control-om-chat

The standalone fixture mounts the real AgentPane with a completed turn. The markup lives in `AgentPresentation.tsx`, not `AgentPane.tsx`: `formatTokenUsage` (`:241-269`), `.agent-answer-meta` (`:392`) and `.agent-activity-summary-detail` (`:654`). The away remote-control pane renders the same presentation (`test/remote-agent-presentation-parity.test.tsx`), so `remote-home-fixture.html?state=live` is the second place to look. At `f8b68bf7` the default fixture's `.agent-answer-meta` reads `12:00 PM · 1 tool · 2.0s · 12.3k tokens`.

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

**Last verified:** 2026-10-22. **Product commit:** `cd9f8c72a6522caccc3b6157a4990fb6c9d0b0cf` (origin/main). **Scope:** `.agent-answer-meta` read `12.3k tokens` (title `12,345 tokens`), `tokens=1250000` gave `1.3M tokens` (title `1,250,000 tokens`), `tokens=1` gave `1 token`, and `tokens=missing` gave no count and no price. **Expand tool activity** flipped to **Collapse tool activity**, and the detail kept the title `12,345 tokens`. `agent-presentation-fixture` states collapsed/expanded/failed/live rendered their toggles. **Limitations:** The input+output fallback (not seedable) and live daemon accounting were not exercised. Previous record: 2026-10-12 at `a0916a25` (a feature-branch commit).
