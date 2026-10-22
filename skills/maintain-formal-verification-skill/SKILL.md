---
name: maintain-formal-verification-skill
description: "Bring a project's formal verification back in line with changed code: read the commits that touched verified code, update the model or harness, rerun, and say whether each failure is drift or a bug. Use for /maintain-formal-verification-skill or after merges that skipped the check."
disable-model-invocation: true
---

# Maintain a formal verification skill

A formal check proves a property of what it describes. When the code changes and
the verification does not, the check can keep passing while it describes code
that no longer exists. That pass is the dangerous case, because it looks like a
proof.

This is the upkeep loop for a skill that **create-formal-verification-skill**
generated, or any project skill that runs a model checker, prover, or code-level
verifier against named code. The project skill handles a change an agent makes
while using it. This handles the changes that skipped it: merges, edits made
without the skill, drift across many commits. It is the formal sibling of
**maintain-verification-skill**.

## Outcomes

Give each check one outcome, and say which.

- **in sync.** Nothing since the last sync alters what the check describes, and
  it passes.
- **updated.** The code changed, the verification now describes the new code,
  and the check passes.
- **bug.** The verification describes the current code, and the code breaks the
  property. A finding about the code, not drift.
- **blocked.** The check could not be brought back in line or could not run. Say
  exactly why.

A check can be both updated and bug: the update makes it describe the code
again, then the property fails on it.

## Edit scope

Only the verification: models, harnesses, property files, and the skill itself,
in its canonical hub directory per
[the project verification contract](../../docs/project-verification.md). Never
product code unless the operator asks. When a property fails on the current
code, report it. Never weaken the property or the model to make it pass.

## Pass

1. **Find the checks.** Look in the registry for skills carrying the project's
   `project` field, under `projects/<repository>/skills/`, and read each for a
   verifier it runs against named code. Several, read them all or the one the
   operator named. None, stop and point at **create-formal-verification-skill**.
   For each check, collect the property, the covered code, the bounds and
   assumptions, the command, and the sync commit. With no sync commit recorded,
   use the last commit that changed the verification files, and say so.

2. **Run it as it is.** Run each check once before changing anything, and record
   the result. A pass says the old description still holds, not that the code is
   correct. A failure can be drift or a bug. Do not decide which until step 5.

3. **Read every change to covered code.** Diff the covered files from the sync
   commit to now, and read each commit message. Follow code that moved: a covered
   function renamed, split, or moved is still covered. Look for new code that
   touches the guarded state, such as a new writer of the same fields. Classify
   each change, checking against the model, not the commit message.
   - **No effect.** Formatting, comments, or paths the verification does not
     cover.
   - **The model no longer describes the code.** One step became two, a branch
     came or went, a check moved, a new path reaches the guarded state, a range
     changed. The model or harness must change.
   - **The promise changed on purpose**, with evidence in the change: the doc
     comment, the tests, the changelog, the commit message. The property must
     change, and you cite that evidence.
   - **The promise may be broken.** The code changed and nothing says the promise
     did. A failure that follows is a bug candidate.

4. **Update from the code, not from the result.** Each changed part points again
   to code a reviewer can open, and one indivisible step stays one step. Write
   the update before you rerun, never shaped by what makes it pass. Change a
   property only for a promise that changed on purpose, and record the old
   wording, the new wording, and the evidence. Keep the bounds unless the change
   makes them wrong. A reduced bound goes in the report.

5. **Rerun and judge each result.**
   - **Pass.** Break the new code the way the property guards against, confirm
     the check catches it, then drop the break. An update can lose the ability
     to fail.
   - **Fail.** Replay the counterexample against the real code step by step. A
     step that cannot happen means the verification is wrong: fix it and say
     what was wrong. If every step can happen, it is a bug. Name the commit that
     introduced it, tell the counterexample in the code's words, and state the
     harm in one sentence. A cheap reproduction against the real code goes in the
     report as evidence, never into product code.

6. **Update the skill.** Covered code, commands, bounds, assumptions, and the
   sync commit, set to the commit you checked. Never move the sync commit for a
   blocked check, and say so. Then follow the skill once as the next agent would,
   so you know its steps still run.

## Report

For each check:

- The outcome, and the commits you read.
- What changed in the verification and why: the code changed shape, or the
  promise changed on purpose, with the evidence.
- The rerun result, and the break that showed the updated check can still fail.
- Each bug in plain words: the counterexample as steps, the harm, the commit
  that introduced it.
- What the verification still does not cover, including new code it should.

Say outright which failures were drift and which were bugs. A check that passed
before the update and fails after means the old pass was on a stale description.

Put the verification updates in a change of their own, separate from any
product fix. They use ordinary source delivery, never
`bin/deez sync-feature-maps`.
