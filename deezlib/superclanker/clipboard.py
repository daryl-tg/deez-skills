import shlex
import subprocess
import time
from pathlib import Path

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".tiff", ".tif", ".bmp"}
OSASCRIPT_TIMEOUT_S = 5


def _osascript(run, lines):
    argv = ["osascript"]
    for line in lines:
        argv += ["-e", line]
    try:
        return run(argv, capture_output=True, text=True, timeout=OSASCRIPT_TIMEOUT_S)
    except (OSError, subprocess.SubprocessError):
        return None


def _is_image(path):
    return path.suffix.lower() in IMAGE_SUFFIXES and path.is_file()


def _copied_file(run):
    done = _osascript(run, ["POSIX path of (the clipboard as «class furl»)"])
    if done is None or done.returncode != 0:
        return None
    path = Path((done.stdout or "").strip())
    return path.resolve() if str(path) != "." and _is_image(path) else None


def _image_data(run, dest_dir, clock):
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / f"img-{int(clock() * 1000)}.png"
    done = _osascript(run, [
        "set png to (the clipboard as «class PNGf»)",
        f'set f to open for access POSIX file "{path}" with write permission',
        "set eof f to 0",
        "write png to f",
        "close access f",
    ])
    if done is None or done.returncode != 0 or not path.is_file() or path.stat().st_size == 0:
        path.unlink(missing_ok=True)
        return None
    return path


def grab_image(dest_dir, run=subprocess.run, clock=time.time):
    return _copied_file(run) or _image_data(run, dest_dir, clock)


def image_paths(pasted):
    try:
        tokens = shlex.split(pasted.strip())
    except ValueError:
        return []
    paths = [Path(token.removeprefix("file://")).expanduser() for token in tokens]
    if not paths or not all(_is_image(path) for path in paths):
        return []
    return [path.resolve() for path in paths]
