---
name: automate-me
description: "Draft or refresh the operator's personal mode skill from real transcript history rather than from description. Use for 'automate me', 'capture how I work', or refreshing a stale voice profile."
disable-model-invocation: true
---

# Automate me

Turn how the operator actually works into a skill agents follow. You read it out
of their history rather than asking them to describe it, because stated
preferences and revealed ones differ.

## 0. Check for an existing mode

Look for a `*-mode` skill in the hub. If one exists, default to updating it:
mine only history since its last edit (`git log -1 --format=%cI <path>`),
preserve sections nothing contradicts, revise those with new evidence, and add
sections only for genuinely new patterns.

## 1. Mine the history

Read prior sessions across **both** runtimes — `~/.claude/projects/<slug>/` and
`~/.codex/sessions` — since the operator's work crosses them and a Claude-only
sample misrepresents how they delegate.

Fan out across slices of time, one **explore** subagent per slice, each
returning patterns with evidence pointers. Signals worth hunting: reply
preferences, delegation habits, what "done" means to them, code and prose
discipline, process conventions, and how they respond to being asked versus
being shown.

**Cross-check before elevating.** A pattern in two or more slices is real. A
lone signal is noise, and a preference stated once and contradicted later is
noise twice over.

## 2. Ask what mining cannot see

Use `AskUserQuestion` with concrete options rather than open prompts. Two
structured rounds and one free-form question is enough. Intent that has not come
up yet will not be in the transcripts.

## 3. Draft

Follow **superpowers:writing-skills**. Frontmatter triggers on the operator's
name and the slash command, never on generic keywords. `disable-model-invocation:
true`, because a mode skill is heavy and opinionated and should apply when
invoked, not when matched.

Sparse is fine. Only add a section where there is a specific non-default rule.
"Communicate clearly" is not a section.

## 4. The voice profile

A mode skill that claims to match the operator's voice needs **their** samples.
Collect real writing from the record — messages, review comments, doc prose —
per register. **When a profile and a raw sample disagree, the sample wins.**

**Never ship a voice profile belonging to someone else.** An inherited profile
produces confident output in the wrong register, which is worse than none. If
you cannot build a real one yet, say so and leave the layer out.

## 5. Land it

Show the draft, take feedback, expect iterations. Cut ruthlessly: a mode skill
is not a manual. Then `playbooks/opening-a-review.md`.

**Reply:** the skill, the patterns it captures with their evidence, and what you
deliberately left out.
