---
description: Build the newest origin/main of openmarket-internal and openmarket-chat and install it as the live om.
argument-hint: "[--force]"
---

Run `~/.claude/skills/om-build/scripts/latest.sh $ARGUMENTS` with the Bash tool and a 600000 ms timeout. Do nothing before it: no fetch, no git status, no reading the om-build skill. The script does all of that.

Reply with its stdout rows unchanged in a code block. Add one line only when a row needs action:

- `FAIL:`: read the log it names, then give the cause and the fix in one line each.
- `mcp       WARN`: the MCP singleton can take a few minutes to launch a new binary. Check `pgrep -f 'om mcp serve --http'` once and say whether it is up.
- `daemon was down before the build`: say so.

Nothing else: no recap of what the script did, no next steps.
