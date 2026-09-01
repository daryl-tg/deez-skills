---
name: reviewer
description: >-
  Code, diff, PR, or MR review; dead-code checks, behavior
  drift, or REVIEW.txt notes.
---
## Scope

Use this skill when the goal is to review a change,
not merely describe it.

Good triggers:

- review the current branch, diff, or merge request
- "would this pass review"
- "check for dead code"
- "did we change any logic"
- "maybe I displaced something or missed something"
- write `REVIEW.txt` or similar review notes

This skill is for your own review of the code. When
there are already GitLab review threads, use the
simple `glab mr view` → `labiew -Pd` path to collect
context, then review the code itself in this style.

## Review stance

- Start from the diff.
- Prefer statements of fact over coaching,
  compliments, or rhetorical questions.
- Be short and emotionally detached.
- If an issue is real, say it plainly. Do not write
  `possibly` for something you can show from the
  code.
- If something is unclear, say exactly what is
  missing and keep it under `Open questions`.
- Treat complexity, drift, dead code, and
  unnecessary abstraction as review failures, not
  trivia.

## Workflow

1. Establish the review surface.
   - For the current branch, inspect `git diff
     --stat <base>...HEAD` and the unified diff.
   - For a GitLab MR, start with `git branch
     --show-current`, `glab mr view`, then capture
     the diff with `labiew -Pd <url>` or overview
     with `labiew -Po <url>`.
2. Read the changed code and the old behavior.
   - Do not review hunks in isolation.
   - When logic moved or a library changed, compare
     against the pre-change implementation.
3. Validate review claims.
   - Run existing tests or lint when they cover the
     touched behavior.
   - For non-obvious bugs, prove the claim from code
     semantics. If needed and the user wants proof,
     add a failing test first.
4. Hunt the kinds of problems this style cares about.
   - dead code, stale logs, stale comments, obsolete
     compatibility paths
   - behavior drift from the previous version
   - helpers, wrappers, flags, or config that should
     not exist
   - naming that hides the real concept or leaks the
     wrong one
   - complexity that will not pass review
   - shutdown, channel, retry, ack, commit, and
     close behavior
   - config, docs, tasks, or tests that drifted away
     from the code
   - mixed concerns that should have been separate
     commits
5. For each finding, ask:
   - what changed in behavior
   - why this code exists at all
   - whether the name is honest
   - whether the logic can be simpler
   - how to prove the failure mode
6. Stop at concrete findings.
   - Do not start patching unless the user asked for
     fixes.

## Review heuristics

Push especially hard on these patterns:

- "Did we change any logic?"
  Compare scope, lifecycle, defaults, and side
  effects with the old code.
- "Why do we even need this?"
  Challenge new helpers, logs, knobs, wrapper
  functions, and comments.
- "Will this pass review?"
  Treat avoidable complexity, soft naming, and vague
  comments as real review debt.
- "How to prove it?"
  Prefer code-path reasoning, concrete failure
  modes, and minimal tests over vague suspicion.
- "Did we leave dead code behind?"
  Check removed-library migrations, old callbacks,
  unused config, and stale fallbacks.

## Response shape

Default to:

- short verdict
- `Findings`
- `Open questions` only when the uncertainty is real
- optional `Suggested order` when several fixes
  exist

Each finding should include:

- file or scope
- the fact
- why it matters
- the likely fix or direction

Prefer wording like:

- `Prefetch now scans all partitions, not only
  assigned ones.`
- `This helper is dead after the migration.`
- `The closed-channel receive can spin forever and
  keep the pipeline alive.`

Avoid:

- generic praise
- long best-practice lectures
- speculative wording when the bug is demonstrable
- turning every finding into a question

## Writing review files

When the user asks for `REVIEW.txt` or similar:

- keep it terse
- list facts and problems first
- group by file or theme
- omit praise unless it changes the decision
- keep questions in a separate small section or
  leave them out entirely

## Rules

- Review the code, not just the commit message or
  MR text.
- Prefer `git diff` or `labiew` text over ad-hoc
  JSON scripts for the first pass.
- Use `grep-ast` to inspect call sites and moved
  logic before making review claims.
- If a finding depends on runtime behavior, say how
  it was validated or what proof is still missing.
- If nothing serious is wrong, say so briefly and
  still mention what you checked.

## Reference map

Read [checklist.md](references/checklist.md) when you
need the fuller question set, phrasing patterns, or
example prompts.
