### Authoring or modifying a skill

**You own the skill's voice.** Agent-facing prose has a higher bar than human
prose: an unhelpful sentence becomes an instruction some future agent follows.

1. Use **superpowers:writing-skills** for the authoring loop.
2. **Declare the layer** in `registry.toml`. `mode` and `playbook-host` are
   Claude-only; `principle` installs on both runtimes and must carry
   `disable-model-invocation`.
3. **Commit the Codex gate with the skill.** A gated skill that installs to
   Codex needs `agents/openai.yaml` carrying
   `policy.allow_implicit_invocation: false`, because Claude reads the
   frontmatter flag and Codex reads that file. It is generated, mechanical, and
   marked so in `.gitattributes`, which hides it in review but never from git.
   Add it in the same change. Never ignore it. A clone without it fails
   `bin/doctor`, and `untracked-gate` fails the moment one is written but not
   added.
4. **Keep it short.** If a skill is long or repeats itself, it decomposes:
   routing in `SKILL.md`, detail in `references/`, steps in `playbooks/`.
5. **Cite, never restate.** A rule that exists as a principle gets referenced by
   name. Restating it is how the two copies drift apart.
6. **Keep the description tight.** No hard limit, but it loads into every
   session on every machine and Codex is already truncating. A description that
   will not come down usually means the skill has more than one job.
7. Run `bin/doctor`. It checks the flag, the citations, the roles, and the
   description budget.
8. Run `playbooks/opening-a-review.md`.

When in doubt, delete. Prose earns its keep by changing a decision.

**Reply:** the skill, its layer and why, validation notes.
