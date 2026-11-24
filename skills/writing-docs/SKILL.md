---
name: writing-docs
description: "Pick the document's audience and mode first, then apply the matching standard: STE for agent-facing docs, developer style for human-facing ones. Use for docs, RFCs, readmes, PR bodies, and commit messages."
disable-model-invocation: true
---

# Writing docs

Write so a tired engineer understands on the first read. Step 1 picks the
engine.

## 1. Audience and mode

**Audience.** Agent-facing (SKILL.md, AGENTS.md, CLAUDE.md, subagent
definitions, handoff prompts) or human-facing (docs, RFCs, readmes, PR bodies,
commit messages).

**Mode**, per Diátaxis. One document, one mode. Split and link instead of
mixing them.

| Mode | Answers | Fails when |
|---|---|---|
| Tutorial | "Take me through it once" | It explains instead of walking |
| How-to | "I need to do X" | It teaches concepts mid-task |
| Reference | "What are the exact parameters" | It has opinions |
| Explanation | "Why is it like this" | It turns into a how-to |

## 2a. Agent-facing docs use **writing-simplified-technical-english**

**The rewrite keeps every requirement and changes only the words and the
layout.** A shorter document that dropped or weakened an obligation is a
failure.

Extract and restore unchanged: code fences, commands, paths, identifiers,
frontmatter `name`, tool and skill names, quoted strings, numbers and
thresholds. Shape the instructions with **writing-instructions**.

## 2b. Human-facing docs use developer style

- One idea per sentence. Split the sentence the reader has to reread.
- Say who does what. Passive only when the actor is unknown or beside the
  point.
- Talk to the reader as "you". Write instructions as commands, condition first.
- Name the mechanism or the number, not how it feels.
- Write the real symbol, file, flag, or command name, not a synonym for it.
- Global English. No idioms, cultural references, or humour that depends on a
  shared frame.
- Front-load. Put the outcome first.

Then run **unslop**. For anything going out in the operator's name, run
**humanize** after that.

## Commit messages and PR bodies

The PR title and body **become main's commit message** under squash-merge, per
**principle-one-commit-lands**. Write them for someone reading `git log` a year
out. Say what changed, why, and what it means for the next person, not a
changelog of the branch. Link logs, SHA lists, and metric tables instead of
pasting them. The body's headings live in `playbooks/opening-a-review.md`.

**Reply:** the document, plus the audience and mode you chose and why.
