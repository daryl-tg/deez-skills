#!/bin/bash
# Installs the scene harness toolchain: playwright (pinned) and its headless
# chromium, outside the skill dir. Safe to rerun; a complete install is a no-op.
# Bash 3.2 compatible (macOS /bin/bash).
set -euo pipefail

VERSION=1.61.1
TC="${PRODUCT_VIDEO_TOOLCHAIN:-$HOME/.local/state/product-video/toolchain}"
PKG="$TC/node_modules/playwright/package.json"
export PLAYWRIGHT_BROWSERS_PATH="$TC/ms-playwright"

for bin in node npm; do
  command -v "$bin" >/dev/null 2>&1 || { echo "setup-scene: $bin not on PATH" >&2; exit 2; }
done

mkdir -p "$TC"
# A package.json of its own stops npm walking up into some parent project.
[ -f "$TC/package.json" ] || printf '{ "private": true }\n' > "$TC/package.json"

installed=""
if [ -f "$PKG" ]; then
  installed=$(node -p "require('$PKG').version" 2>/dev/null || true)
fi
if [ "$installed" != "$VERSION" ]; then
  echo "setup-scene: installing playwright@$VERSION into $TC"
  npm install --prefix "$TC" --no-audit --no-fund --save-exact "playwright@$VERSION" >&2 \
    || { echo "setup-scene: npm install failed" >&2; exit 2; }
else
  echo "setup-scene: playwright@$VERSION present"
fi

# playwright install skips a browser whose install marker already exists.
node "$TC/node_modules/playwright/cli.js" install --only-shell chromium >&2 \
  || { echo "setup-scene: chromium install failed" >&2; exit 2; }
echo "setup-scene: ready ($TC)"
