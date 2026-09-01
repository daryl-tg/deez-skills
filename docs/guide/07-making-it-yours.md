# 7. Making it yours

## Add a skill

```bash
bin/new my-skill --category workflow --runtimes claude,codex
```

Scaffolds the folder, registers it, regenerates the index. Then decide the
layer, which is the only decision that matters:

- **`principle`** if it is one rule other things will cite. Must be on both
  runtimes, must carry the flag.
- **`playbook-host`** if it owns a `playbooks/` directory. Claude only.
- **`workflow`** for everything else. This is almost always the answer.

`bin/doctor` fails if a layer and its frontmatter disagree.

## Keep it short

The convention, measured:

| | Skills | Median | Max |
|---|---|---|---|
| pstack | 45 | 31 lines | 229 |
| This hub | 33 | 36 | 135 |
| The old collection | 69 | 103 | 1,294 |

If a skill is long or repeats itself, it decomposes: routing in `SKILL.md`,
detail in `references/`, steps in `playbooks/`. `om-chat-feature` was 214 lines
and became a 30-line playbook plus a reference file, because its phases were
always playbook content and only its boundaries were skill content.

**Descriptions are the expensive part.** They load into every session on every
machine, before you type anything.

There is deliberately **no per-skill limit**. A single long description is not
the problem; a runtime truncating the whole catalogue is. `bin/doctor` reports
the aggregate per runtime instead, which is the number that predicts truncation.

Structure is what keeps it down. A routed layer costs nothing on Claude, and a
skill decomposed properly needs a short description because it does one thing.
When a description will not come down, that is usually the skill telling you it
has more than one job.

## Cite, never restate

If a rule exists as a principle, reference it. Restating it is exactly how two
copies drift apart, and `bin/doctor` cannot catch a rule that has quietly
diverged in wording — only one that is cited and missing.

## Merge rather than skip

When something you want overlaps something you have, the useful move is almost
never to pick one. Each side usually owns a different half.

`design` exists because brainstorming owned the approval gate and architect
owned the technical artifact and the scrap phase. `test-first` exists because
one side owned the Iron Law and the other owned what to do when a unit test is
impractical. Skipping either would have thrown away the better half.

Two things to watch for when merging: a **direct contradiction** needs
adjudicating rather than blending — when architect said "no human checkpoint"
and the standing rule says the planning gate is mandatory, the standing rule
wins and the exception is written down. And a **near-duplicate is not a
duplicate**: `unslop` and `humanize` stayed separate because one is universal
and one is personal, and merging them would tie a general cleanup pass to one
person's register.

## Retire deliberately

Retiring is harvest-then-delete. `clanker-agent-polish` was retired, but it owned the
evidence publishing contract, so that moved to the terminal gate and the control
wrapper first. Deleting it outright would have lost the only statement of how
proof gets published.

Check what references a skill before removing it. Two things referenced
`clanker-agent-polish`, and both needed editing in the same change.

## Capture what a session taught

```
reflect
```

Three reviewers with different lenses read the transcript, findings sort into
Accepted / Rejected / Backlog, and **nothing is applied without approval**. A
finding is accepted only if it would change a future decision, and only if it is
a pattern rather than a one-off.

Anything better served by a check than by more instruction text goes to Backlog
as a build request. More prose is the weakest way to enforce anything.

```
automate-me
```

Mines real transcript history across both runtimes to draft a personal mode
skill. It reads how you work rather than asking you to describe it, because
stated and revealed preferences differ.

Next: [Recipes](./08-recipes.md).
