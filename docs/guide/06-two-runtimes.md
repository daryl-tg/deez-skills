# 6. Two runtimes

pstack does not have this problem: Cursor is one app that spawns mixed-model
subagents. Here the hub installs to two apps that cannot see each other's
sessions, though only Claude Code is in use today.

## Claude hosts the router. Codex support is dormant.

The operator works in Claude Code only, so every delegate is a Claude subagent.
The hub still installs to `~/.codex`, so a resubscribe needs no rebuild. Three
facts, all verified rather than assumed, say why the router never lived there:

1. **`disable-model-invocation` works on Claude and is a no-op on Codex.**
   Tested with two identical probe skills differing only in the flag; Codex
   listed both. A router there would fire on description matches.
2. **Codex is already truncating skill descriptions.** The same test emitted
   *"Skill descriptions were shortened to fit the skills context budget"*. Every
   skill added there makes a live problem worse.

## What holds them together

**Principles install on both.** A handoff cites them by name, and the citation
resolves because the leaf exists locally on either side. The router speaks a
vocabulary both runtimes hold.

**Playbooks are files, cited by absolute path.** They need no installation to be
read. A delegate follows the steps without the router existing there.

**Steps name a role, never a model.** The five roles are defined for both
runtimes as agent definitions, and the router resolves the role to a lane at
dispatch.

## How dispatch actually happens

Through the Agent tool, one role per call:

```
Agent(subagent_type: "executor")
```

Review goes to `code-reviewer`, verification to `verifier`. Nothing routes to
Codex.

## The routing lane

One line in `registry.toml`:

```toml
[routing]
default_lane = "claude"
```

The four beneath it — planning, review, verification, git mutations — are not
preferences. They stay with the lead whatever `default_lane` says, and the
registry rejects any other value.

## The rule every handoff obeys

**A delegate does not inherit your context**, and the risk grows with codebase size.
So every dispatch is self-contained: cite the playbook by absolute path, the
principles by name. Never assume the delegate knows what you know.

Next: [Making it yours](./07-making-it-yours.md).
