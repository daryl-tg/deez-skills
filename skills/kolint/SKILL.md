---
name: kolint
description: >-
  YAML config audits against Go structs: schema, defaults,
  required fields, and unknowns.
---
## Scope

Use this workflow to compare YAML config files against
Go config structs defined with ko tags and classify
`DEFAULT`, `REQUIRED`, `OPTIONAL`, `UNKNOWN`,
`UNUSED`, and `REDUNDANT` findings.

Not for generic schema validation or non-ko config
systems.

## Workflow

1. Identify the target config type, Go package, and
   optional YAML root before running the audit.
2. Run report mode first so you can see
   `DEFAULT`/`REQUIRED`/`OPTIONAL`/`UNKNOWN`/
   `UNUSED`/`REDUNDANT` findings together.
3. Fix `REQUIRED` and `UNKNOWN` findings first; they
   usually indicate broken config or typos.
4. For `DEFAULT` and `OPTIONAL`, decide which fields
   should stay implicit and which should be written
   into YAML for clarity.
5. Treat `UNUSED` as code-or-config drift. Confirm the
   field is truly unused before deleting or ignoring
   it.
6. Add or update `.kolint.yml` when the audit is a
   recurring project workflow, then re-run after
   config-struct changes.

## Rules

- Be explicit with `--type` and `--package` when the
  project is ambiguous.
- Use `--root` for Helm values or nested config
  subtrees.
- Use report mode when you need `UNUSED`; annotate
  mode does not run usage analysis.
- Use annotate mode for review artifacts, not as a
  substitute for understanding the report.
- Keep ignore patterns narrow.
- Document recurring audit usage in `AGENTS.md`.

## Reference map

Read [reference.md](references/reference.md) for:

- finding kinds and meanings, including `UNUSED`
- report and annotate modes, and why `UNUSED` is
  report-only
- flags, project config, and ignore patterns
- Helm, multiple-type, and AGENTS.md guidance
