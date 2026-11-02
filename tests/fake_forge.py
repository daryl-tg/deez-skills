#!/usr/bin/env python3
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from unittest import mock

KEPT_FLAG_VALUES = ("--repo", "-F")
FIXTURES = Path(__file__).with_name("fixtures") / "super"


def fixture_key(tool, argv):
    words, index = [], 0
    while index < len(argv):
        token = argv[index]
        if token.startswith("-"):
            if token in KEPT_FLAG_VALUES and index + 1 < len(argv):
                words.append(argv[index + 1])
            index += 2
            continue
        words.append(token)
        index += 1
    return "-".join(re.sub(r"[^A-Za-z0-9_.]", "-", word) for word in [tool, *words])


def is_write(tool, argv):
    if tool == "gh":
        return argv[:2] == ["pr", "comment"]
    return any(
        flag == "-f" and value.startswith("body=") for flag, value in zip(argv, argv[1:])
    )


def main(tool, argv):
    with open(os.environ["FAKE_FORGE_LOG"], "a", encoding="utf-8") as log:
        log.write(json.dumps([tool, *argv]) + "\n")
    key = fixture_key(tool, argv)
    fixtures = Path(os.environ["FAKE_FORGE_FIXTURES"])
    failure = fixtures / f"{key}.stderr"
    answer = fixtures / f"{key}.json"
    if failure.exists():
        sys.stderr.write(failure.read_text(encoding="utf-8"))
        return 1
    if answer.exists():
        sys.stdout.write(answer.read_text(encoding="utf-8"))
        return 0
    if is_write(tool, argv):
        sys.stdout.write("{}\n")
        return 0
    print(f"no fixture for {key}", file=sys.stderr)
    return 1


def install(case, fixtures=FIXTURES):
    tmp = Path(tempfile.mkdtemp())
    case.addCleanup(shutil.rmtree, tmp, True)
    bin_dir = tmp / "bin"
    bin_dir.mkdir()
    for tool in ("gh", "glab"):
        shutil.copy(__file__, bin_dir / tool)
        (bin_dir / tool).chmod(0o755)
    log = tmp / "forge.jsonl"
    patcher = mock.patch.dict(os.environ, {
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "FAKE_FORGE_FIXTURES": str(fixtures),
        "FAKE_FORGE_LOG": str(log),
    })
    patcher.start()
    case.addCleanup(patcher.stop)
    return log


def calls(log):
    try:
        return [json.loads(line) for line in Path(log).read_text(encoding="utf-8").splitlines()]
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[0]).name, sys.argv[1:]))
