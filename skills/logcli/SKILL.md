---
name: logcli
description: >-
  Live Loki log exports, per-pod splits, and saved Kubernetes
  or service log captures; not logs already on disk.
---
## Scope

Use this workflow when logs must be collected from
Loki with `logcli`.

Not for logs already on disk. Use log analysis
skills after collection.

## Workflow

1. Create `logcli-work/<slug>/` for the
   investigation.
2. Resolve the Loki address, LogQL query, time range,
   and whether logs should stay combined or split by
   pod.
3. Convert human time input to RFC 3339 with
   `date -u -d ...`.
4. Collect to files with `logcli query` and
   `--part-path-prefix`.
5. If exact pod names matter, use `logcli series`
   first, then run one query per pod.
6. Report saved file paths and sizes to the user.

## Rules

- Never dump large log streams into the conversation.
- Use `--forward` for chronological output.
- Prefer `-o raw --no-labels` unless the task needs a
  different format.
- Keep outputs in the working directory, not `/tmp`.
- Derive pod regexes from deployment names when that
  saves time.

## Reference map

Read [reference.md](references/reference.md) for time
conversion examples, full collection commands,
defaults, and the per-pod flow.
