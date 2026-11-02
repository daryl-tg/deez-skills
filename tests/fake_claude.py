#!/usr/bin/env python3
import json
import os
import subprocess
import sys


def flag_value(argv, flag):
    return argv[argv.index(flag) + 1] if flag in argv else None


def main(argv):
    with open(os.environ["FAKE_CLAUDE_LOG"], "a", encoding="utf-8") as log:
        log.write(json.dumps(argv) + "\n")
    script = os.environ.get("FAKE_CLAUDE_SCRIPT")
    if script:
        subprocess.run(script, shell=True, stdout=sys.stderr, check=False)
    exit_code = int(os.environ.get("FAKE_CLAUDE_EXIT", "0"))
    if exit_code:
        print(f"fake claude failed with {exit_code}", file=sys.stderr)
    session = flag_value(argv, "--session-id") or flag_value(argv, "--resume")
    result = os.environ.get("FAKE_CLAUDE_RESULT", "ok")
    print(json.dumps({"result": result, "session_id": session, "total_cost_usd": 0.001}))
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
