---
name: pi-development
description: >-
  Pi asset development: extensions, skills, prompts, themes,
  packages, providers, models, TUI, or SDK integrations.
---
## Scope

Use this workflow when creating or revising pi extensions,
skills, prompt templates, themes, packages, SDK integrations,
providers, models, or TUI components.

Also use it when the user asks about pi itself or pi's own
documentation.

Not for everyday use of pi as a coding agent.

## Pi documentation

Read pi documentation only when the user asks about pi itself,
its SDK, extensions, themes, skills, prompt templates, TUI,
keybindings, providers, models, or packages.

Resolve the installed pi package with npm. Do not hard-code the
global npm directory, and do not resolve these paths relative to
the current working directory.

```bash
pi_root="$(npm root -g)/@earendil-works/pi-coding-agent"
readme_path="$pi_root/README.md"
docs_path="$pi_root/docs"
examples_path="$pi_root/examples"
```

- Main documentation: `$readme_path`
- Additional docs: `$docs_path`
- Examples: `$examples_path`

When an instruction names `docs/foo.md`, read
`$docs_path/foo.md`. When it names `examples/foo/`, inspect
`$examples_path/foo/`. Read relevant pi `.md` files completely;
if a read is truncated, continue until the file is complete.
Follow `.md` cross-references before implementing.

Topic map:

- Extensions: `docs/extensions.md`, `examples/extensions/`
- Custom tools: `docs/extensions.md`,
  `examples/extensions/tools.ts`,
  `examples/extensions/dynamic-tools.ts`
- Themes: `docs/themes.md`
- Skills: `docs/skills.md`
- Prompt templates: `docs/prompt-templates.md`
- TUI components: `docs/tui.md`, `examples/extensions/`
- Keybindings: `docs/keybindings.md`,
  `examples/extensions/commands.ts`
- SDK integrations: `docs/sdk.md`, `examples/sdk/`
- Custom providers: `docs/custom-provider.md`,
  `examples/extensions/custom-provider-anthropic/`,
  `examples/extensions/custom-provider-gitlab-duo/`
- Adding models: `docs/models.md`
- Pi packages: `docs/packages.md`

## Default target locations

When the user says they want to build, create, add, or revise a
pi asset and does not name a destination, assume a user-level
home asset, not a project asset:

- Skills: `~/.pi/agent/skills/<name>/`
- Extensions: `~/.pi/agent/extensions/<name>.ts` or
  `~/.pi/agent/extensions/<name>/`
- Prompt templates: `~/.pi/agent/prompts/<name>.md`

Use a project, package, or other directory only when the user
explicitly asks for that location.

## Workflow

1. Identify the pi topic and choose the smallest mechanism
   that solves the problem:
   - prompt template for static prompt expansion
   - skill for repeatable workflows, references, scripts, and
     light structure
   - extension for tools, hooks, UI, or runtime behavior
   - theme for TUI colors only
   - package for sharing or bundling assets
2. Read the matching official docs and examples from the
   installed package. Prefer installed examples over invented
   APIs.
3. Keep the top-level asset easy to scan. Move deep material
   into `references/`, repeated deterministic work into
   `scripts/`, and starter files into `assets/`.
4. Test in fresh pi sessions. Compare against a baseline when
   you need to prove the asset changed behavior instead of
   merely existing.
5. Before finishing, verify discovery rules, install paths,
   local links, and any referenced script paths.

## Rules

- Read the installed pi docs instead of copying large API
  references into a skill.
- Do not bundle local pi documentation unless the installed docs
  are missing the workflow-specific guidance.
- Use npm-resolved documentation and example paths. Do not
  hard-code the global npm installation directory.
- For skills, make `description` trigger-oriented and slightly
  aggressive.
- For extensions, prefer patterns from the installed examples
  over invented APIs.
- Wrap prose at 80 columns.
