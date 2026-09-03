# 6. Two runtimes

pstack does not have this problem: Cursor is one app that spawns mixed-model
subagents. Here the work spans two apps that cannot see each other's sessions.

## Claude hosts the router. Codex is an executor lane.

Three facts force it, all verified rather than assumed:

1. **`disable-model-invocation` works on Claude and is a no-op on Codex.**
   Tested with two identical probe skills differing only in the flag; Codex
   listed both. A router there would fire on description matches.
2. **Claude can dispatch to Codex; there is no clean path back.**
3. **Codex is already truncating skill descriptions.** The same test emitted
   *"Skill descriptions were shortened to fit the skills context budget"*. Every
   skill added there makes a live problem worse.

## What holds them together

**Principles install on both.** A handoff cites them by name, and the citation
resolves because the leaf exists locally on either side. The router speaks a
vocabulary both runtimes hold.

**Playbooks are files, cited by absolute path.** They need no installation to be
read. Codex follows the steps without the router existing there.

**Steps name a role, never a model.** The five roles are defined for both
runtimes as agent definitions, and the router resolves the role to a lane at
dispatch.

## How dispatch actually happens

Through the official OpenAI plugin, and specifically through its **subagent**,
not its slash commands. Slash commands are manual invocation by you; the
subagent is what a router can call:

```
Agent(subagent_type: "codex:codex-rescue")
```

Raw `codex exec` is the escape hatch when you need a structured return
(`--output-schema` takes a JSON Schema), an explicit sandbox, or an ephemeral
run. The Codex MCP server is **not** used: it exposes two tools and carries a
conversation-tracking bug that breaks multi-turn, which the resume semantics
depend on.

## Switching who implements

One line in `registry.toml`:

```toml
[routing]
default_lane = "codex"    # or "claude"
```

The four beneath it — planning, review, verification, git mutations — are not
preferences. They stay with Claude whatever `default_lane` says, and the
registry rejects any other value.

## The rule every handoff obeys

**Codex does not inherit your context**, and the risk grows with codebase size.
So every dispatch is self-contained: cite the playbook by absolute path, the
principles by name. Never assume the delegate knows what you know.

Next: [Making it yours](./07-making-it-yours.md).
