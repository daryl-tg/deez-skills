---
name: create-verification-skill
description: "Generate a project-local verification skill and its control wrapper so an agent can drive the real app and prove behavior. Use for /create-verification-skill, \"make a control skill for this repo\", or when a project has no scripted way to prove UI, CLI, or service behavior."
disable-model-invocation: true
---

# Create a verification skill

Every project needs a scripted way to drive the real app and prove behavior:
launch it, exercise a feature the way a user would, capture evidence. This
generates that as `skills/verify-<app>/` plus a `control-<app>` wrapper the repo
owns. Write for the next agent, not a human. It will be read cold, mid-task, by
an agent that has never seen the app.

## 1. Interview the repo, not the user

Answer from the codebase. Ask only what you cannot observe.

- **Surface.** What does a user touch? Web UI, CLI, desktop, API, mobile. Pick
  the primary one, note the rest.
- **Run.** How does it start locally? Prefer the repo's own documented dev
  command. Note env vars, seed data, auth.
- **Drive.** `agent-browser` is the harness for anything browser or Electron.
  Its SKILL.md is a discovery stub, so run `agent-browser skills get core` for
  real usage rather than writing commands from memory.
- **Observe.** What evidence can be captured? Accessibility snapshots,
  screenshots, response bodies, logs, exit codes.
- **Isolate.** Can two instances run side by side? If not, say so in the
  generated skill. Refusing to double-drive a shared instance beats corrupting
  the operator's session.

**Ports are assigned, never discovered.** Read the reserved-ports table before
choosing anything. Bind `127.0.0.1` explicitly. Agent test servers take
`18097`–`18197`, which are deliberately not tunnelled, so one may never be
handed back as a review URL. Never bind, target, or stop `8097`, `8098`, or
`31337`.

If the checkout does not build or start, fix that first or report it precisely.
A skill written against a broken base teaches wrong steps.

## 2. Generate the control wrapper

Write `control-<app>` into the repo it drives, not into this hub, so it versions
with the app. Model it on `references/control-wrapper.sh`. Four verbs:

- `doctor` — read-only. Is this instance worth driving? Right build, right port,
  serving the working tree, dependencies answering.
- `browser <verb>` — delegates to `agent-browser`. Never reimplements it.
- `cli -- <cmd>` — runs the app's own CLI, capturing stdout, stderr, exit code.
- `evidence publish <run-id> <revision>` — pushes the artifact pair to the
  review renderer. Never authors a revision `index.html`.

## 3. Generate the skill

Write `skills/verify-<app>/SKILL.md` with frontmatter (`name: verify-<app>`, and
a description naming the app, the surface, and when to reach for it) and these
sections, each grounded in what the interview found. No placeholders.

**Launch** the exact command plus how to tell it is ready, and teardown.
**Doctor** the one read-only check. **Drive** the `control-<app>` recipe with
real handles from this repo, ARIA roles and accessible names over coordinates.
**Evidence** what to capture and where it goes. **Cleanup** kill what you
started, never by process name; evidence survives teardown. **Helpers**
executable, with invocation shown.

Proof standards for the Evidence section: exercise the real user path, not
internal setters or test-only endpoints. Capture the action and the resulting
state, not just the final screen. Verify side effects alongside what is visible.
When the safe path is a dry run, verify what it actually skips by observing,
since some dry runs still touch the network.

## 4. Seed the feature map

Create `skills/verify-<app>/features/README.md` plus one file per user-facing
feature, top three to five to start. Follow
[`references/feature-map-example/`](references/feature-map-example/). Four H2s
in order: `Sub-features`, `How to get to it (user POV)`,
`Driving it with control-<app>`, `Gotchas`.

The map is the repo's maintained verification source. A proof that drives one
convenient entry point is incomplete when the map lists others.

## 5. Prove it before handing it over

Run its own instructions end to end once: launch, doctor, drive one mapped
feature, capture evidence, clean up. Then confirm the evidence still exists at
its named location. A cleanup that eats the proof fails this step. Run the
generated cleanup after every failed iteration too, so broken attempts do not
strand processes and ports.

A generated skill that was never executed is a draft, not a deliverable.

## 6. Point at the maintenance loop

Name `maintain-verification-skill` as the upkeep pass. Suggest a cadence only if
asked.
