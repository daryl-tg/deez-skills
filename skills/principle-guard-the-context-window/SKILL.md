---
name: principle-guard-the-context-window
description: "Apply when context fills up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents and keep summaries in the main thread."
disable-model-invocation: true
---

# Guard the context window

The context window is finite and non-renewable within a session. Every token
entering it should earn its place.

**Why:** overflow degrades reasoning, creates compression artifacts, and halts
progress. Unlike compute or wall-clock, context spent inside a session cannot be
reclaimed.

- **Isolate large payloads.** Route verbose output, screenshots, and long
  documents to a subagent. The main thread gets the summary, not the raw data.
- **Do not read what you will not use.** Read selectively. Skip what the current
  task does not need.
- **Keep frequently used content inline.** Templates and references used on
  every invocation belong in the skill body, not in a separate file costing a
  read each time.
- **Size phases and cap scope.** Limit files per phase, set turn budgets,
  account for the mechanism's own cost.

This is why skill metadata matters: descriptions load before you type anything,
and a catalogue too large to fit gets truncated silently. The layers exist to
keep that bill down.

The reader-facing analogue is **principle-minimize-reader-load**.
