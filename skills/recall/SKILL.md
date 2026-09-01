---
name: recall
description: "Rebuild your context on a topic from prior sessions and the shared record, handed back as a current-state brief. Use when resuming work after a gap."
disable-model-invocation: true
---

# Recall

Rebuild what you knew about a topic, from the record rather than from memory.

## Sources

- **Prior sessions.** `~/.claude/projects/<slug>/` on Claude,
  `~/.codex/sessions` and `history.jsonl` on Codex. Both, since work crosses
  runtimes.
- **The task's dev-notes folder**, by absolute path. Specs and plans live there,
  outside any repo, so they survive the branch.
- **The repository.** Branches matching the topic, their diffs against
  `origin/main`, open review requests, and whether anything is still running on
  an owned port.
- **The shared record.** Announcements and discussion in the rooms.

## Rules

- **Scope to the topic.** Do not sweep every session; find the ones about this.
- **Reality outranks intent.** A note saying a thing was done and a repository
  showing it was not means it was not. Report the discrepancy rather than
  averaging them.
- **Date everything.** "Recently" is useless on return. Absolute dates only.
- **Separate settled from open.** The value is knowing which decisions are
  closed, so they are not relitigated.

**Reply:** a current-state brief — what the goal was, what is done and proven,
what is in flight and where, what is decided, what is open, and the paths worth
reading first.
