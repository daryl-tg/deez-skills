---
name: writing-docs
description: "Pick the document's audience and mode first, then apply the matching standard: STE for agent-facing docs, developer style for human-facing ones. Use for docs, RFCs, readmes, PR bodies, and commit messages."
disable-model-invocation: true
---

# Writing docs

One entry point, two engines. Step 1 decides which.

## 1. Audience and mode

**Audience.** Agent-facing (SKILL.md, AGENTS.md, CLAUDE.md, subagent
definitions, handoff prompts) or human-facing (docs, RFCs, readmes, PR bodies,
commit messages).

**Mode**, per Diátaxis. Pick one and commit to it; most bad documents are two
modes fighting.

| Mode | Answers | Fails when |
|---|---|---|
| Tutorial | "Take me through it once" | It explains instead of walking |
| How-to | "I need to do X" | It teaches concepts mid-task |
| Reference | "What are the exact parameters" | It has opinions |
| Explanation | "Why is it like this" | It turns into a how-to |

## 2a. Agent-facing → **writing-simplified-technical-english**

That skill is the engine. Its rule holds absolutely: **the rewrite keeps every
requirement and changes only the words and the layout.** A shorter document that
dropped or weakened an obligation is a failure, not an improvement.

Extract and restore unchanged: code fences, commands, paths, identifiers,
frontmatter `name`, tool and skill names, quoted strings, numbers and
thresholds.

For instruction shape, **writing-instructions**: state the principle, not all its
instances; examples only where they define a boundary the reader would not infer.

## 2b. Human-facing → developer style

- **One idea per sentence.** Split when the reader has to backtrack.
- **Active voice, named actor.** "The loader parses the file", not "the file is
  parsed".
- **Second person for instructions.** "Run the migration", not "the migration
  should be run".
- **Say what it does, not how it feels.** Name the mechanism or the number.
- **Global English.** No idioms, no cultural references, no humour that depends
  on a shared frame.
- **Front-load.** The reader stops early; put the outcome first.

Then run **unslop**. For anything going out in the operator's name, **humanize**
after that.

## Commit messages and PR bodies

The PR title and body **become main's commit message** under squash-merge, per
**principle-one-commit-lands**. Write them for someone reading `git log` a year
out: what changed, why, and what it means for the next person. Not a changelog
of the branch.

**Reply:** the document, plus the audience and mode you chose and why.
