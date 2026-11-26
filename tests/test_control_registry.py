import os
import socket
import subprocess
import tempfile
import time
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CONTROL = REPO / "projects/openmarket-registry/skills/verify-registry/bin/control-registry"
FAKE_SERVER = """\
import http.server, os, sys
class Health(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200 if self.path == "/v1/health" else 404)
        self.end_headers()
        self.wfile.write(b"ok")
    def log_message(self, *args):
        pass
http.server.HTTPServer(("127.0.0.1", int(os.environ["PORT"])), Health).serve_forever()
"""


def bindable(port):
    with socket.socket() as probe:
        try:
            probe.bind(("127.0.0.1", port))
        except OSError:
            return False
        return True


def free_port():
    for port in range(18196, 18150, -2):
        if bindable(port) and bindable(port + 1):
            return port
    raise RuntimeError("no free agent port pair for the test lane")


class ControlRegistryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.product = self.root / "openmarket-registry"
        (self.product / "src").mkdir(parents=True)
        (self.product / "package.json").write_text('{\n  "name": "@openmarket-xyz/registry"\n}\n')
        (self.product / "src/main.ts").write_text(FAKE_SERVER)
        subprocess.run(["git", "init", "-q", str(self.product)], check=True)
        self.fake_bin = self.root / "bin"
        self.fake_bin.mkdir()
        self.fake("agent-browser", 'printf "%s\\n" "$@"')
        self.fake("bun", 'exec python3 "$1"')
        self.port = free_port()
        self.addCleanup(lambda: self.run_control("down"))

    def fake(self, name, body):
        path = self.fake_bin / name
        path.write_text(f"#!/bin/sh\n{body}\n")
        path.chmod(0o755)

    def run_control(self, *args, cwd=None, extra_env=None):
        env = {
            **os.environ,
            "REGISTRY_LANE_PORT": str(self.port),
            "PATH": f"{self.fake_bin}:{os.environ['PATH']}",
        }
        env.pop("REGISTRY_REPO", None)
        env.update(extra_env or {})
        return subprocess.run([str(CONTROL), *args], capture_output=True, text=True,
                              env=env, cwd=cwd or self.product, timeout=90)

    def test_it_refuses_a_directory_that_is_not_a_registry_checkout(self):
        other = self.root / "elsewhere"
        other.mkdir()
        subprocess.run(["git", "init", "-q", str(other)], check=True)
        result = self.run_control("doctor", cwd=other)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not an openmarket-registry checkout", result.stderr)

    def test_registry_repo_names_the_checkout_from_anywhere(self):
        result = self.run_control("doctor", cwd=self.root, extra_env={"REGISTRY_REPO": str(self.product)})
        self.assertIn(f"origin      http://127.0.0.1:{self.port}", result.stdout)

    def test_doctor_fails_with_no_lane(self):
        result = self.run_control("doctor")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("health      UNREACHABLE", result.stdout)

    def test_up_starts_a_lane_doctor_passes_and_down_stops_it(self):
        up = self.run_control("up")
        self.assertEqual(up.returncode, 0, up.stderr)
        self.assertIn(f"registry lane ready at http://127.0.0.1:{self.port}", up.stdout)
        doctor = self.run_control("doctor")
        self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)
        self.assertIn("health      /v1/health answers", doctor.stdout)
        down = self.run_control("down")
        self.assertEqual(down.returncode, 0, down.stderr)
        self.assertIn("stopped registry lane", down.stdout)
        time.sleep(0.5)
        self.assertNotEqual(self.run_control("doctor").returncode, 0)

    def test_up_refuses_an_occupied_port(self):
        with socket.socket() as holder:
            holder.bind(("127.0.0.1", self.port))
            holder.listen()
            result = self.run_control("up")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("is occupied", result.stderr)

    def test_up_refuses_a_port_outside_the_agent_range(self):
        result = self.run_control("up", extra_env={"REGISTRY_LANE_PORT": "8097"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("18097-18197", result.stderr)

    def test_down_with_no_lane_says_so(self):
        result = self.run_control("down")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("already stopped", result.stdout)

    def test_browser_delegates_to_agent_browser(self):
        result = self.run_control("browser", "open", "about:blank")
        self.assertEqual(result.stdout.split(), ["open", "about:blank"])


if __name__ == "__main__":
    unittest.main()
