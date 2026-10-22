---
name: correct
description: "Find the mistakes agents keep repeating in a repo and make each one impossible: architecture first, then types, a lint whose error names the fix, a test, and docs last. Prove each check fails on a real past mistake. Use for /correct."
disable-model-invocation: true
---

# Correct

The operator keeps correcting agents in this repo for the same mistakes. Change
the repo so the next agent cannot make them. **reflect** captures one session's
lessons as skill edits, with approval. This makes a repeated class of mistake
impossible in the code itself.

Assume every contributor is an agent that sees only the files it opened, copies
the nearest example, and takes the shortest path that compiles. Design the repo
so a change that looks right from one file is right for the whole repo.

## Find the mistake classes

Read recent commits, reverts, review comments, `AGENTS.md` and `CLAUDE.md`, and
comments that explain workarounds. Group the mistakes into classes. A class
counts once it has happened twice.

## Fix each class at the highest level that works

The order comes from **principle-encode-lessons-in-structure**. Text is the
weakest guard because nothing fails when an agent skips it.

1. **Architecture.** Give each piece of state one owner and each task one
   supported way. Hide internals so the wrong import fails. Replace hand-synced
   lists with one source of truth. Delete the old ways and the dead code an agent
   would copy, per **principle-migrate-callers-then-delete-legacy-apis**.
2. **Types**, so the bad state cannot be written, per
   **principle-type-system-discipline**. If bad code still compiles, add a lint
   or CI check whose error names the file, type, or function to use instead. If
   the pattern is already common, fail only when a change adds more of it.
3. **A test of the behavior**, per
   **principle-test-behavior-not-implementation**. Fix or delete any test that
   passes when its behavior breaks, or fails when only the internals change.
4. **Docs or agent rules last**, only for judgment calls.

## Fix and prove

Fix the most frequent classes now, one commit each. Prove each new check fails
on a real past mistake: reapply it and watch the check go red. Run the same
command locally and in CI. An exception goes on the offending line with a
reason, an expiry date, and a human's approval.

## Keep the rule table

Keep a table in `AGENTS.md` (or `CLAUDE.md` where that is the repo's file) that
pairs each rule with what enforces it. When the operator corrects you, fix the
mistake and add the rule. If the rule was already there and nothing enforces
it, that is a repeat, so fix it at the highest level in the same change. Drop a
rule once its mistake cannot happen.

**Reply:** each class with its evidence, the level you picked, the past mistake
each new check failed on, and why a higher level did not work.
