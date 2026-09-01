---
name: why
description: "Recover why something was built the way it is, from git history, review threads, tickets, chat, and incident records. Use for 'why is this like this', 'why was Y chosen', or regression archaeology."
---

# Why

Recover intent. **explore** answers how a thing works; this answers why it is
that way, and the evidence lives outside the code.

## Sources, in parallel

Query every category available, concurrently, and record which ones you could
not reach.

- **Source control.** `git log -S` for when a behavior appeared, `git log --
  <path>` for the file's arc, blame for the specific line. The commit message
  matters less than the surrounding commits.
- **Review threads.** The PR or MR that introduced it. Review discussion is
  where rejected alternatives are recorded, and rejected alternatives are the
  answer more often than the merged diff.
- **Issue tracker.** The ticket, and what it linked to.
- **Chat.** The room, around the merge date. Use the rooms tools where the
  operator has read access.
- **Incidents and monitoring.** A guard that looks arbitrary is often a
  postmortem action item.

## Reporting

**Confidence language is a finding, not style.** Keep it exactly as you write
it. "The commit message says X" is not "the author intended X".

- **Established** — a primary artifact states it. Cite it.
- **Likely** — several sources point the same way without saying it outright.
- **Unknown** — say so. Do not fill the gap with a plausible story.

**Name the categories you could not search.** An answer built from git alone
looks identical to a complete one unless you say which doors were shut.

**Reply:** the answer, its confidence, the citations, and the unsearched
categories.
