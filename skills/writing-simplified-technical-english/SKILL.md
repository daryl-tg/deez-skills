---
name: writing-simplified-technical-english
description: "Rewrite an agent-facing document in ASD-STE100 when it is too long, gets truncated, or reads as dense prose: SKILL.md, AGENTS.md, CLAUDE.md, subagent definitions, handoff prompts. Every requirement survives the rewrite."
---

# Simplified Technical English for agent documents

ASD-STE100 (Issue 9, 2025-01-15) is a controlled language. It removes the two
causes of a misread instruction: a word with more than one meaning, and a
sentence with more than one structure. Apply it to documents that agents read.

**The rewrite keeps every requirement. It changes only the words and the
layout.** A rewrite that adds, removes, or weakens a requirement is a failure,
not a shorter document.

Rules: `references/ste-rules.md`. Substitutions: `references/word-list.md`.

## Do not change these

Extract these zones before you rewrite. Restore them unchanged after.

- Code fences, inline code, commands, paths, URLs, regexes, and identifiers.
- The frontmatter `name` field, and all tool, skill, agent, and file names.
- Quoted rationalizations, error strings, and report strings. Their exact
  words do the work.
- Numbers, thresholds, time limits, and version identifiers.

These rules apply to prose only. They never reach into an extracted zone.

## Procedure

1. Record the requirement list. Number every obligation, prohibition,
   precondition, exception, order constraint, and stop condition.
2. Rewrite each prose sentence with `references/ste-rules.md`. When a
   word-for-word replacement is not sufficient, write a different sentence
   (Rule 9.1).
3. Cut only from the cut list below.
4. Split the document only per `## Length` below. Do not cut a requirement,
   and do not split a document, to make it shorter.
5. Compare the requirement list against the new document. Each item must map
   to one item, and the new document must add none. Restore anything absent.
6. Rewrite the file in place under version control. If there is none, write
   the new text beside it and tell the operator.
7. Report the requirement count before and after, and each phrase that you
   kept longer. If you split the document, report which part moved and why an
   agent does not need it to start.

## What you can cut

- A sentence that gives motivation, praise, or history, and adds no rule.
- Text that repeats a rule that the document already gives.
- A second example of a rule that one example already shows.
- Prose that repeats a table or a list below it.
- A hedge that adds no condition: "generally", "as much as possible".

## What you must keep

- Every obligation, prohibition, exception, precondition, and order.
- Every number, path, name, command, and report string.
- Every hedge that shows uncertainty. "The job can fail" is not "the job
  fails". A shorter sentence that makes a hedge into a fact is a new claim.
- Every quoted rationalization and its counter.

## Length

A document has no word limit. Length is not a defect. Some documents are
correct only when they are long. A rewrite that makes a document shorter than
its requirements is a failure.

Do not split a document to make it shorter. Split a part into
`references/<topic>.md` only when the two conditions below are both true.

- An agent does not need the part to start the task correctly.
- The part is a self-contained procedure, table, or checklist that an agent
  reads at one identified step.

Keep these in the primary document, at any length: each prohibition, each
safety instruction, each stop condition, and the sequence of the work. An agent
that reads the primary document alone must not do damage. See Rule 7.2 in
`references/ste-rules.md`.

When you split a part, name its file at the step that needs it. Do not collect
the pointers in a list at the end. A pointer that an agent meets after the work
arrives too late.

The sentence, paragraph, and multi-word noun limits stay. They are in
`references/ste-rules.md`. They control one sentence. They do not control the
length of a document.

## Frontmatter

Keep the `description` field as trigger conditions only, below 1024
characters. Do not make it a summary of the procedure. An agent that reads such
a summary can obey it and not read the document.

## Stop and report

Stop and tell the operator when one of these is true.

- A requirement is ambiguous, and the two readings give different behavior.
- The source text has no content to keep. STE makes the form better, not the
  content.
