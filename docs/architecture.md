# How the hub is put together

Four layers, strictly separated. The `layer` field in `registry.toml` declares
which one an entry belongs to, and `bin/doctor` enforces the consequences.

| Layer | What it is | Runtimes | Flag |
|---|---|---|---|
| `mode` | The router. Classifies a request, copies a playbook's steps in verbatim | Claude only | required |
| `principle` | One rule. Cited by playbooks, never restated in them | **both** | required |
| `playbook-host` | A skill owning a `playbooks/` directory | Claude only | required |
| `workflow` | Everything else | either | optional |

## Why the router is Claude-only

`disable-model-invocation` works on Claude and is a **no-op on Codex** — tested
2026-09-01 with two identical probe skills differing only in the flag; Codex
listed both. A mode skill installed there would fire on description matches
instead of waiting to be routed to.

Claude can also dispatch to Codex, and Codex has no clean path back. So Claude
hosts the router and Codex is an executor lane.

## Why principles install on both

A handoff to Codex cites principles by name. Those citations only resolve if the
leaf exists on that runtime. A principle missing from Codex is a silently
truncated instruction, so the registry rejects one that is not on both.

## Why playbooks are not skills

They are plain `.md` files inside the mode skill. Twelve of them cost zero
registry entries and zero session tokens, and they are readable by absolute path
from either runtime without being installed anywhere. A Codex handoff cites the
path directly.

## Session cost

Skill metadata loads into every session before you type. That is the budget the
layers exist to protect.

| | pstack | This hub | Pre-existing setup |
|---|---|---|---|
| Skills | 45 | 33 | 69 |
| Visible on Claude | 6 | **3** | 69 |
| Metadata paid | ~290 tok | **~128 tok** | ~4,900 tok |

Codex ignores the flag, so it sees every skill. Still well under the ~4,100 it
currently pays, and it was **already truncating descriptions** at that level,
which is a correctness problem rather than a cost one.

There is no per-skill description limit. `bin/doctor` reports the aggregate per
runtime, since that is what a runtime truncates on, and the layers plus ordinary
decomposition are what keep it down.

## Delegation

Playbook steps name a **role**, never a model or a runtime, and the router
resolves it at dispatch. The five roles are defined for both runtimes in
`agent-matrix.tsv`.

Implementation dispatches to Codex through
`Agent(subagent_type: "codex:codex-rescue")` — the official OpenAI plugin's
subagent, which is what a router can call, unlike its slash commands. Raw
`codex exec` is the escape hatch when a structured return (`--output-schema`),
an explicit sandbox, or an ephemeral run is needed. The Codex MCP server is not
used: it exposes two tools and carries a conversation-tracking bug that breaks
multi-turn.

Planning, review, verification, and git mutations never dispatch.

## Verification

Two lanes, different frequencies.

- **Inner loop**, constantly during implementation: `control-<app> doctor` then
  replay the feature map recipe. Deterministic, cheap, no publishing.
- **Terminal gate**, once per feature: an agent drives `agent-browser` as a user
  would, replays every scripted recipe first, then explores beyond them,
  captures the accessibility-snapshot and screenshot pair, and publishes a
  revision to the review renderer.

`agent-browser` is the harness in both. `control-<app>` is a thin per-repo
wrapper that adds what `agent-browser` has no opinion about: a `doctor` check,
the app's own CLI, bound preconditions, and evidence publishing.
