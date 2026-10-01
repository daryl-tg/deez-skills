---
name: create-verification-skill
description: "Generate a project-owned verification skill, feature map, and control wrapper in the deez-skills hub so an agent can drive the real app and prove behavior. Use for /create-verification-skill, \"make a control skill for this repo\", or when a project has no scripted way to prove UI, CLI, or service behavior."
disable-model-invocation: true
---

# Create a verification skill

Every project needs a scripted way to drive the real app and prove behavior:
launch it, exercise a feature the way a user would, capture evidence. This
generates the canonical skill, feature map, and wrapper under
`~/github/deez-skills/projects/<repository>/skills/verify-<app>/`, while keeping
the installed name `verify-<app>` stable. Follow the layout, ownership, and
persistence contract in
[`../../docs/project-verification.md`](../../docs/project-verification.md).
Write for the next agent, not a human. It will be read cold, mid-task, by an
agent that has never seen the app.

## 0. Resolve the project owner

For a known installed skill, use its registry project ownership first. Otherwise
derive `<repository>` from the origin remote repository basename, stripping
`.git`. Never use a feature-worktree directory name. Choose an existing registry
category; do not create a category for this skill.

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

## 2. Scaffold in the hub

From the deez-skills root, run:

```sh
bin/new verify-<app> --category <existing-category> --project <repository>
```

Generate the skill and feature map in the created project directory. Keep the
registry key and installed symlink name as `verify-<app>`; the project namespace
is canonical storage, not part of the installed name.

## 3. Generate the control wrapper

Write `bin/control-<app>` inside the canonical verification skill directory and
make it executable. Model it on `references/control-wrapper.sh`. Four verbs:

- `doctor` — read-only. Is this instance worth driving? Right build, right port,
  serving the working tree, dependencies answering.
- `browser <verb>` — delegates to `agent-browser`. Never reimplements it.
- `cli -- <cmd>` — runs the app's own CLI, capturing stdout, stderr, exit code.
- `evidence publish <run-id> <revision>` — pushes the artifact pair to the
  review renderer. Never authors a revision `index.html`.

Existing product-specific wrappers may have documented ownership exceptions.
In particular, never reconstruct or replace OpenFloor's operator-only untracked
wrapper.

## 4. Generate the skill

Write `SKILL.md` in the canonical verification skill directory with frontmatter
(`name: verify-<app>`, and a description naming the app, the surface, and when
to reach for it) and these sections, each grounded in what the interview found.
No placeholders.

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

## 5. Seed the feature map

Create `features/README.md` inside the canonical verification skill plus one file
per user-facing feature, top three to five to start. Follow
[`references/feature-map-example/`](references/feature-map-example/). Four H2s
in order: `Sub-features`, `How to get to it (user POV)`,
`Driving it with control-<app>`, `Gotchas`.

Every feature entry records its last verified date, the product commit or tree
that was driven, the verification scope, and any limitations. Keep the README
index aligned with every sibling feature file, including entries Clanker adds.

The project-owned map in the hub is the maintained verification source. A proof
that drives one convenient entry point is incomplete when the map lists others.

## 6. Register, install, and prove it

Confirm the scaffold is registered, then run `bin/link --apply` from the hub so
the stable `verify-<app>` name resolves to the project-owned skill.

Run its own instructions end to end once: launch, doctor, drive one mapped
feature, capture evidence, clean up. Then confirm the evidence still exists at
its named location. A cleanup that eats the proof fails this step. Run the
generated cleanup after every failed iteration too, so broken attempts do not
strand processes and ports.

A generated skill that was never executed is a draft, not a deliverable.

Persist the canonical skill, feature map, wrapper, registry entry, and generated
index exactly as required by the shared project-verification contract. Once the
skill and registry entry have landed through ordinary source delivery, and the
map is proved with its index current, automatically publish only its changed
`features/*.md` files with:

```sh
bin/deez sync-feature-maps <project> <verify-skill> <map-file.md>...
```

Pass filenames relative to `features/`, including `README.md` when it changed.
If no map file changed, publish nothing. Never use bare `bin/sync`, and never
include `SKILL.md`, wrappers, registry/config files, raw evidence, or product
repository changes. Handle every non-map source edit through its ordinary
review and delivery path; standing authorization to publish feature maps does
not authorize a product push.

## 7. Point at the maintenance loop

Name `maintain-verification-skill` as the upkeep pass. Suggest a cadence only if
asked.
