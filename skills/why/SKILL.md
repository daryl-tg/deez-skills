---
name: why
description: "Recover why something was built the way it is, from git history, review threads, tickets, chat, and incident records. Use for 'why is this like this', 'why was Y chosen', or regression archaeology."
---

# Why

Answer from the record, not the code. Code shows what happens, never why.
**explore** answers how a thing works.

Read the commits and review threads that introduced the target and each later
change. `git log -S` finds when a behavior appeared and `git log -- <path>`
gives the file's arc. Rejected alternatives in review discussion are the answer
more often than the merged diff. When that trail is thin, look further, at the
ticket, the rooms around the merge date where the operator has read access, and
the incident records. A guard that looks arbitrary is often a postmortem action
item.

Cite what the authors wrote. Mark each claim as stated by the record, inferred,
or unknown, and never fill a gap with a plausible story. "The commit message
says X" is not "the author intended X". When sources disagree, surface both.
The operator's guess is a lead to check, not a conclusion to confirm.

Say what the record does not answer, and name the sources you could not reach.
An answer from git alone looks complete unless you say which doors were shut.

**Reply:** the answer, its citations with inferences marked, and what the
record does not answer.
