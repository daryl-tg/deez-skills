# Adding a skill

```bash
bin/new my-skill --category workflow --runtimes claude,codex
```

That creates `skills/my-skill/SKILL.md` from the template, appends the registry
entry, and regenerates the README index.

To bring in a skill that already exists somewhere on disk:

```bash
bin/adopt ~/some/path/my-skill --category workflow
```

`adopt` copies, registers, and leaves the original untouched. It does not link
anything — see `docs/migration.md`.

## Rules the doctor enforces

- The frontmatter `name:` must equal the install name. Codex resolves its
  catalogue by that field, so a mismatch makes a skill invisible even when the
  symlink is perfect.
- Keep the `description` tight, but there is **no character limit**. A
  well-decomposed skill needs a short description anyway; a long one is usually
  a symptom of a skill doing too much, which the structure catches better than a
  number would. What matters is the aggregate: `bin/doctor` reports the metadata
  cost per runtime, because that is what a runtime truncates on.
- Every folder under `skills/` needs a registry entry, and every entry needs a
  folder.
- The README index must be current. Run `bin/index` after any registry change.

## Categories and profiles

A category is a coarse grouping; a profile is the set of categories one machine
installs.

```toml
[profiles]
full = ["*"]
lean = ["core", "workflow", "writing"]
```

```bash
bin/link --profile lean          # preview
bin/link --profile lean --apply  # commit to it
```

## Per-runtime differences

Same skill, different install name:

```toml
[skills.my-skill-stub]
category   = "workflow"
runtimes   = ["codex"]
install_as = { codex = "my-skill" }
```

Genuinely different content per runtime:

```toml
[skills.graphify]
category = "workflow"
runtimes = ["claude", "codex"]
variant  = { codex = "skills/graphify-codex" }
```

Claude supports skills, commands, and subagents. Codex supports skills only;
the registry rejects a command or agent targeted at Codex.
