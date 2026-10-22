---
name: create-formal-verification-skill
description: "Generate a project-owned skill in the deez-skills hub that formally verifies the code where a bug costs most and tests reach least, with whichever tool fits. Use for /create-formal-verification-skill, \"model-check this race\", or \"prove this invariant\"."
disable-model-invocation: true
---

# Create a formal verification skill

A test checks the cases someone thought to write. Formal verification checks
every case in a stated scope: every order of steps in a model, every input up to
a bound, or every input. This finds the part of a repo where that matters most,
verifies one property of it, and leaves a project-owned skill that lets the next
agent check a change against that property. The operator must be able to trust
the result and act on it without learning the verification language.

This is the formal sibling of **create-verification-skill**, which proves
behavior by driving the running app. The two answer different questions and a
project can have both.

## Choose the target from the code

Answer from the codebase. Ask only what you cannot observe. If the operator named
an area or a bug, start there.

A good target is a promise the code makes, where a break harms users and tests
rarely reach the case that breaks it: concurrency, retries, state machines,
parsers, unsafe code. Choose the strongest such target, not the easiest to
verify.

## Let the question choose the tool

Pick the tool that answers the question at the lowest cost.

- Whether events can happen in a bad order suits a model checker over a small
  model of the design. TLA+ is the default for that, in any language.
- Whether the code itself behaves for every input (memory safety, overflow, a
  data-structure invariant) suits a verifier that runs on the code.
- If no verifier runs on this language, say so, and test the real code with
  generated inputs rather than a hand model of the function.
- A property that must hold at every size, where a bound is not enough, can
  need a proof assistant.

Prefer a tool the repo's developers can install and run, and say why you chose
it.

## What makes it good

- **True to the code.** Every part of the model points to code a reviewer can
  open. One indivisible step in the model is one indivisible step in the code.
  Names come from this repo.
- **Able to fail.** Show each property failing on a broken variant of the code
  it guards, such as a removed check or a reordered step. A check you never saw
  fail proves nothing, per **principle-failing-test-first**.
- **Findings stay findings.** When the current code breaks the property, report
  the counterexample in the code's terms. Never weaken the property or the model
  until it passes, and never change product code unless the operator asks.
- **Honest about scope.** Say what is verified, under which bounds and
  assumptions, and what is left out. A pass covers the model or the bound, not
  the system.
- **Readable without the tool.** State the property and the harm in one plain
  sentence each. Tell a counterexample as a short sequence of steps in the code's
  words.
- **Cheap to rerun.** One command, a pinned tool version, and a run short enough
  to use on every relevant change.
- **Kept in step.** Record which files and functions each check covers, and the
  commit at which you last confirmed the verification describes them.

## Generate the skill in the hub

It lives where every project verification skill lives, per
[the project verification contract](../../docs/project-verification.md). Resolve
`<repository>` the same way: registry `project` field first, else the origin
remote basename without `.git`, never a worktree name. From the hub root:

```sh
bin/new formal-<area> --project <repository> --category <existing-category>
```

That creates `projects/<repository>/skills/formal-<area>/`. An existing formal
check written elsewhere comes in with `bin/adopt <folder> --project <repository>
--category <existing-category>` instead.

Put the model, property files, and run script in that directory, resolving the
product checkout from the caller's working directory as control wrappers do. A
harness that must compile inside the product (a code-level verifier's proof
harness) goes in the product repo through its ordinary review, and the skill
records its path.

Write `SKILL.md` with frontmatter that names the area and says when to use it.
From the skill alone the next agent must be able to tell whether a change
touches the verified code, run the check, tell a real bug from a modeling error,
and update the verification when a change is intended. Put the coverage record
and the sync commit in it, and say to move the sync commit forward only after
confirming the verification describes the code at the new commit. Use real
commands, paths, and nouns. No placeholders.

Run `bin/link --apply` so the name resolves on both runtimes. The skill has no
feature map, so none of it rides `bin/deez sync-feature-maps`. Every file uses
ordinary source delivery.

## Prove it before you hand off

Follow the generated skill once, as the next agent would, on a scratch change
that breaks the property in the real code. It must catch the break. Drop the
scratch change and confirm the check is back where it started: passing, or
failing only on the findings you will report. If the skill misses the break or a
step does not run, fix the skill or the verification, never the scratch change.
A skill that was never run is a draft.

## Hand off

Tell the operator what you verified, the tool and why, the bounds, what the
check found in plain words, how to run it, and what it does not cover. Suggest a
second target only if you found a close one. Name
**maintain-formal-verification-skill** as the upkeep pass for changes that did
not recheck it.
