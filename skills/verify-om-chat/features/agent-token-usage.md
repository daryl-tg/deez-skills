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

The standalone fixture mounts the real AgentPane with a completed turn.

```bash
agent-browser open "$(./control-om-chat url 'tools/visual/agent-usage-fixture.html')"
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
