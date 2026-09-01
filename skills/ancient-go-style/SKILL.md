---
name: ancient-go-style
description: >-
  Go work where package documentation, dependency source, vendoring, or module
  setup matters.
---

## Scope

Use this skill for Go tasks when you need package or API documentation,
third-party dependency source, or module dependency setup.

## Rules

- Prefer `go doc` for Go package, symbol, and API documentation.
- Use go mod vendor to keep vendor/ up-to-date, then inspect dependency source under vendor/.
