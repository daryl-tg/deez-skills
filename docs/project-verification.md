# Project verification in the skills hub

Verification skills and feature maps belong to their product repository, stored
in `~/github/deez-skills` under that repository's name:

```text
projects/<repository>/skills/verify-<app>/
  SKILL.md
  bin/control-<app>
  features/README.md
  features/<feature>.md
```

## Resolve and register

Read the verification skill's `project` field in `registry.toml` first. For a
new project, take the basename of the product's origin remote, remove `.git`,
and lowercase it. A worktree or feature branch does not create a new project.
Use a distinct installed skill name if another project already owns that name.

Create or adopt the canonical skill from the hub root:

```sh
bin/new verify-<app> --project <repository> --category <existing-category>
bin/adopt <existing-skill-folder> --project <repository> --category <existing-category>
bin/link --apply
```

The registry entry retains its skill name and adds `project = "<repository>"`.
Installed runtime symlinks keep that name. `bin/deez skill-path <skill>` resolves
the canonical source. Old `skills/verify-*` paths are compatibility symlinks for
the four migrated skills; edit their project folders and create no second copy.
The generated README index links every registered project's skill and map.

New control wrappers live in the canonical skill's `bin/` and resolve the product
checkout from the caller's working directory, with an explicit override when
needed. Invoke the absolute wrapper path or link it onto PATH. Existing
operator-only wrappers, such as OpenFloor's untracked wrapper, keep their
documented exception. Do not reconstruct them.

## Capture verified surfaces

Before driving an app, read its project map's `features/README.md`. After proving
a surface absent from the map, add its feature file and index link before
handing off. Updating existing behavior also updates its recipe and provenance.
Use the map's four-H2 contract. New and re-verified entries record the verification
date, product commit or tree, what was driven, and what remains unverified.
Legacy entries retain their existing provenance; missing provenance stays unknown
until a live pass supplies it. Moving a file is not verification. Keep raw evidence and run state in their existing
artifact locations, outside the tracked map.

Clanker calls `create-verification-skill` when the project has no verification
skill and cannot yet prove its requested behavior. Maintenance finds the same
canonical project directory through the registry or installed symlink, never
by copying it into a product worktree.

## Publish only feature maps automatically

The operator authorizes automatic commits and pushes of verified feature-map
Markdown files to the deez-skills remote. At the end of Clanker feature/bug work,
creation, or maintenance, re-read the files changed by that run and publish them
from the hub root:

```sh
bin/deez sync-feature-maps <repository> <verify-skill> <feature>.md README.md
```

Arguments name only changed direct children of that skill's `features/` folder.
Include `README.md` when its index changed, and pass deleted entries when
removing drift. No changed map files means no automatic commit or push.

The publisher requires the canonical skill and its project registry entry to
exist on `origin/main` first. New skills and the initial layout migration use
ordinary source delivery before their maps can be automatically published.
It verifies project ownership and accepts only map `.md` files. It
preserves unrelated staged and unstaged changes, checks outgoing commits for
non-map files, and pushes only the hub's `main` to `origin/main`. A push refusal
leaves the local map commit safe; report the failure and retry after recovery.
`.sync-hold` pauses publishing and must be reported as unsynced work.

If the hub is behind its remote or has unrelated unpushed commits, preserve
that checkout and use a separate detached hub worktree based on fetched `origin/main`.
Copy only this run's reviewed map changes to their canonical project paths,
reconcile against any newer remote map, and publish using the original hub's
`bin/deez sync-feature-maps ... --repo <isolated-worktree>`.
The remote registry must already recognize the project skill. Local uncommitted
registry entries and skill files are insufficient. If that baseline has not
landed, finish ordinary source delivery first and report the maps as pending.
Do not force-push or erase local work.

This authorization covers map Markdown only. `SKILL.md`, control wrappers,
helpers, registry/config files, the hub's generated README, raw evidence, and
product changes retain their ordinary review and delivery path. Never call
`bin/sync` for map persistence because it stages the entire hub. Report the
project path, map commit, push result, and any remaining non-map changes.
