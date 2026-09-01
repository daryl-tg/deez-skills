import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEEZ = REPO / "bin" / "deez"


class TrampolineTest(unittest.TestCase):
    def run_deez(self, *args, env=None):
        return subprocess.run(
            [str(DEEZ), *args],
            capture_output=True,
            text=True,
            env={**os.environ, **(env or {})},
        )

    def test_version_subcommand_succeeds(self):
        result = self.run_deez("version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("deez", result.stdout)

    def test_exits_3_and_names_a_remedy_when_no_tomllib_interpreter(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "python3"
            fake.write_text("#!/bin/sh\nexit 1\n")
            fake.chmod(0o755)
            # Keep /bin and /usr/bin so `env` and `bash` still resolve; the fake
            # python3 shadows the real one, and 3.11+ builds live outside both.
            result = self.run_deez(
                "version", env={"PATH": f"{tmp}:/bin:/usr/bin", "DEEZ_PYTHON": ""}
            )
            self.assertEqual(result.returncode, 3)
            self.assertIn("brew install", result.stderr)


if __name__ == "__main__":
    unittest.main()
