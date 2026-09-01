---
name: chrome-devtools
description: >-
  Browser automation through the Chrome DevTools Protocol with the bundled
  chrome-devtools script.
---

Use this skill to control an already-running Chromium with remote debugging
enabled. Prefer this for rendered-page state, forms, screenshots, console/log
checks, lightweight network diagnostics, and DOM interactions.

The skill is self-contained: run the bundled script directly, no installation
required (Python 3.10+ only, no third-party packages):

```sh
<directory-with-this-skill>/references/chrome-devtools <command> [options]
```

## Requirements

Chrome or Chromium must be running with remote debugging enabled:

```sh
chromium --remote-debugging-port=9222
# or:
google-chrome --remote-debugging-port=9222
```

## Workflow

1. If tab state is unclear, list tabs first.
2. Select a tab when multiple page tabs are open, or pass `--tab-id` on each command.
3. Navigate with `--new-tab` when no suitable page exists.
4. Read the page before interacting; use `--mode interactive` to get stable refs.
5. Prefer selectors or refs for clicks/types; use coordinates only for visual-only targets.
6. After actions, wait for a selector, text, or URL change before reading again.
7. Capture screenshots to a file when visual evidence matters.
8. Use `logs --duration-ms <ms>` for console/runtime log capture; add `--include-network` when resource timing and in-window network request summaries are useful.

## CLI examples

```sh
chrome-devtools help read-page
chrome-devtools list-tabs
chrome-devtools select-tab C87A0E7D8A
chrome-devtools navigate --new-tab --wait-until load https://example.com
chrome-devtools read-page --mode interactive --max-chars 20000
chrome-devtools click --selector 'button[type=submit]' --wait-after-ms 500
chrome-devtools type --selector 'input[name=q]' --clear --submit 'search text'
chrome-devtools wait --text 'Results' --timeout-ms 10000
chrome-devtools evaluate 'document.title'
chrome-devtools logs --duration-ms 1000 --include-network
chrome-devtools screenshot --full-page --output /tmp/page.png
```

## Notes

Set `CHROME_DEVTOOLS_URL` for a non-default endpoint (default
`http://127.0.0.1:9222`). The selected tab is stored under
`CHROME_DEVTOOLS_STATE_DIR` when set, otherwise in the user state directory.

`chrome-devtools help <command>` and `<command> --help` print detailed
subcommand help, including options, target-selection behavior, and examples.
Use this before less-familiar commands.

`logs` streams console/log/runtime-exception events only after the command
attaches. With `--include-network`, it also prints a safe network summary: CDP
request events observed during the capture window plus
`PerformanceResourceTiming` entries available from the page; it does not dump
request or response headers.
