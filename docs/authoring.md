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
- `description` must be under 300 characters, and under 200 is better. Every
  description is loaded into every session on every machine — at ~70 skills
  that is already ~5,000 tokens before you type anything.
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
