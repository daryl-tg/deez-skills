# <app> verification map

The maintained source for verifying user-facing behavior. Read this index before
driving, then use the matching feature file as the recipe.

## Baseline preconditions

- Launch <app> on its **assigned** port. Bind `127.0.0.1`. Never pick a free one.
- `control-<app> doctor` reports the expected origin, build, and working tree.
- Seed whatever fixture data the recipes name.
- Never drive an instance this verification run did not start.

## Driving conventions

- Start every recipe from the baseline unless its preconditions say otherwise.
- Prefer ARIA roles and accessible names over CSS selectors or DOM position.
- Browser actions run through `control-<app> browser`, terminal actions through
  `control-<app> cli -- <command>`.
- Treat every command as literal. Keep quoted names and flags unchanged.
- Restore seeded data after a mutation. Never remove proof artifacts.

## Proof and skip reporting

- Capture the user action and the resulting state, not only the final screen.
- UI proof is a **pair**: an accessibility snapshot and a screenshot, both
  showing app identity. The snapshot is diffable and survives a restyle; the
  screenshot is what a human reads.
- CLI proof includes the command, stdout, stderr, and exit code.
- Mutation proof includes a read-only second view of the stored value.
- Publish a revision with `control-<app> evidence publish <run-id> <revision>`
  and hand back the returned review URL. Never an `18097`–`18197` URL.
- Report an unreachable path with the attempted command and the unmet
  precondition. Never report a skipped entry point as verified via another path.

## Feature entry contract

An H1 title, one paragraph of user-visible behavior, then exactly four H2s in
order: `Sub-features`, `How to get to it (user POV)`,
`Driving it with control-<app>`, `Gotchas`.

Keep implementation detail out. Name only user paths, stable handles, required
state, commands, and observable proof.

## Features

- [Send a message](./send-message.md)
