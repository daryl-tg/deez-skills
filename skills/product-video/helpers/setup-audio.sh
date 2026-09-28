#!/bin/bash
# Idempotently builds the audio toolchain outside the skill directory, which is
# symlinked into the runtime skill roots and must stay free of venvs and caches.
#
#   setup-audio.sh           Python 3.11 venv with beat_this, numpy, soundfile
#   setup-audio.sh --music   also ACE-Step 1.5 at the pinned commit
#
# Every step checks the end state before acting, so a rerun, or a rerun after a
# crash halfway, converges on the same toolchain. A second run is a fast no-op.
#
# ACE-Step weights (~10 GB) download on the first `music.py generate`, into
# $T/ACE-Step-1.5/checkpoints. To reuse an existing install at the pinned commit
# instead of cloning and downloading again, point PRODUCT_VIDEO_ACESTEP_REUSE at
# it; it is symlinked in, never copied or modified:
#   PRODUCT_VIDEO_ACESTEP_REUSE=~/.local/state/product-video/spikes/unit2/ACE-Step-1.5 \
#     setup-audio.sh --music
#
# Bash 3.2 compatible (macOS /bin/bash): no arrays, no ${x,,}, no mapfile.
set -eu

ACESTEP_REPO="https://github.com/ace-step/ACE-Step-1.5.git"
ACESTEP_COMMIT="ca1e85fe9430179831e6bc6be790c332190a3866"
# The commit the spike verified beat_this at.
BEAT_THIS_REF="git+https://github.com/CPJKU/beat_this@b95c8ab0c58c2d9fcfd40508ae8dffbc05ac4f5c"

T="${PRODUCT_VIDEO_TOOLCHAIN:-$HOME/.local/state/product-video/toolchain}"
MUSIC=0
for arg in "$@"; do
  case "$arg" in
    --music) MUSIC=1 ;;
    -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
    *) echo "setup-audio: unknown argument: $arg" >&2; exit 2 ;;
  esac
done

for tool in /usr/bin/python3 git; do
  command -v "$tool" >/dev/null 2>&1 || { echo "setup-audio: missing $tool" >&2; exit 2; }
done

mkdir -p "$T"
export UV_CACHE_DIR="$T/uv-cache"
export UV_PYTHON_INSTALL_DIR="$T/uv-python"
export TORCH_HOME="$T/torch-home"
UV="$T/uv-bootstrap/bin/uv"
PY="$T/audio-venv/bin/python"

has_modules() { # <python> <module>...
  py="$1"; shift
  [ -x "$py" ] || return 1
  "$py" - "$@" <<'EOF' 2>/dev/null
import importlib.util, sys
sys.exit(0 if all(importlib.util.find_spec(m) for m in sys.argv[1:]) else 1)
EOF
}

# uv is not on this machine; bootstrap it into a venv of the system python.
if ! "$UV" --version >/dev/null 2>&1; then
  echo "setup-audio: bootstrapping uv"
  rm -rf "$T/uv-bootstrap"
  /usr/bin/python3 -m venv "$T/uv-bootstrap"
  "$T/uv-bootstrap/bin/pip" install --quiet --upgrade pip uv
fi

if ! "$PY" -c 'import sys; sys.exit(sys.version_info[:2] != (3, 11))' 2>/dev/null; then
  echo "setup-audio: creating Python 3.11 venv"
  rm -rf "$T/audio-venv"
  "$UV" venv --quiet -p 3.11 "$T/audio-venv"
fi

if ! has_modules "$PY" beat_this numpy soundfile; then
  echo "setup-audio: installing beat_this, numpy, soundfile"
  "$UV" pip install --quiet -p "$PY" "$BEAT_THIS_REF" numpy soundfile
fi

# Prefetch the beat_this checkpoint so beats.py never needs the network.
if [ ! -f "$TORCH_HOME/hub/checkpoints/beat_this-final0.ckpt" ]; then
  echo "setup-audio: fetching beat_this checkpoint"
  "$PY" - <<'EOF'
import functools, torch.hub
torch.hub.load_state_dict_from_url = functools.partial(torch.hub.load_state_dict_from_url, progress=False)
from beat_this.inference import load_checkpoint
load_checkpoint("final0")
EOF
fi

if [ "$MUSIC" = 1 ]; then
  ACE="$T/ACE-Step-1.5"
  REUSE="${PRODUCT_VIDEO_ACESTEP_REUSE:-}"
  if [ ! -e "$ACE" ] && [ -n "$REUSE" ]; then
    if [ "$(git -C "$REUSE" rev-parse HEAD 2>/dev/null)" != "$ACESTEP_COMMIT" ]; then
      echo "setup-audio: $REUSE is not ACE-Step at $ACESTEP_COMMIT" >&2
      exit 2
    fi
    echo "setup-audio: reusing ACE-Step install at $REUSE"
    ln -s "$REUSE" "$ACE"
  fi
  if [ "$(git -C "$ACE" rev-parse HEAD 2>/dev/null)" != "$ACESTEP_COMMIT" ]; then
    echo "setup-audio: fetching ACE-Step 1.5 at $ACESTEP_COMMIT"
    if [ ! -d "$ACE/.git" ]; then
      rm -rf "$ACE"
      git init --quiet "$ACE"
      git -C "$ACE" remote add origin "$ACESTEP_REPO"
    fi
    git -C "$ACE" fetch --quiet --depth 1 origin "$ACESTEP_COMMIT"
    git -C "$ACE" checkout --quiet --detach FETCH_HEAD
  fi
  if ! has_modules "$ACE/.venv/bin/python" torch mlx diffusers transformers; then
    echo "setup-audio: syncing ACE-Step environment (several minutes)"
    (cd "$ACE" && "$UV" sync)
  fi
  echo "setup-audio: music ready at $ACE"
fi

echo "setup-audio: ready, python at $PY"
