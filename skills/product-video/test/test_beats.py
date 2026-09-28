import json
import os
import subprocess
import sys
import tempfile
import unittest

# The skill dir is symlinked into the runtimes; keep bytecode out of it.
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
BEATS = os.path.join(HERE, "..", "helpers", "beats.py")
sys.path.insert(0, os.path.join(HERE, "fixtures"))
from make_groove120 import make_groove120  # noqa: E402


def run_beats(wav, bpm):
    return subprocess.run(
        [sys.executable, BEATS, wav, "--bpm", str(bpm), "--json"],
        capture_output=True, text=True, timeout=300,
    )


class BeatsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.wav = make_groove120(os.path.join(cls.tmp.name, "groove120.wav"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_groove120_downbeats_every_two_seconds_from_zero(self):
        proc = run_beats(self.wav, 120)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)

        self.assertEqual(out["bpm_requested"], 120)
        self.assertAlmostEqual(out["bpm_detected"], 120, delta=2)
        downbeats = out["downbeats"]
        self.assertGreaterEqual(len(downbeats), 9)
        self.assertAlmostEqual(downbeats[0], 0.0, delta=0.020)
        for a, b in zip(downbeats, downbeats[1:]):
            self.assertAlmostEqual(b - a, 2.0, delta=0.030)

        # The grid sits at exactly the requested tempo, phased onto the downbeats.
        grid = out["grid"]
        self.assertAlmostEqual(grid[0], 0.0, delta=0.020)
        self.assertGreaterEqual(len(grid), 39)
        for a, b in zip(grid, grid[1:]):
            self.assertAlmostEqual(b - a, 0.5, delta=0.0015)
        self.assertGreaterEqual(len(out["beats"]), 39)

    def test_wrong_requested_tempo_is_a_finding(self):
        proc = run_beats(self.wav, 100)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["bpm_requested"], 100)
        self.assertAlmostEqual(out["bpm_detected"], 120, delta=2)

    def test_off_tempo_take_reports_its_real_tempo_and_grid(self):
        # beat_this quantizes beats to 20ms frames, so a median interval reads
        # a 118 BPM take as 120. The grid must follow the real beats.
        wav = make_groove120(os.path.join(self.tmp.name, "groove118.wav"), bpm=118)
        proc = run_beats(wav, 120)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["bpm_requested"], 120)
        self.assertAlmostEqual(out["bpm_detected"], 118, delta=0.1)
        self.assertGreaterEqual(len(out["beats"]), 36)
        for beat in out["beats"]:
            self.assertLessEqual(min(abs(g - beat) for g in out["grid"]), 0.030, beat)

    def test_gate_is_relative_to_the_requested_tempo(self):
        # finish stretches onto the grid, so the gate only rejects misreads:
        # within 3% of the requested tempo passes, beyond it does not.
        for bpm, code in ((117, 0), (116, 1)):
            with self.subTest(bpm=bpm):
                wav = make_groove120(os.path.join(self.tmp.name, f"groove{bpm}.wav"), bpm=bpm)
                proc = run_beats(wav, 120)
                self.assertNotIn("Traceback", proc.stderr)
                self.assertEqual(proc.returncode, code, proc.stdout)
                self.assertAlmostEqual(json.loads(proc.stdout)["bpm_detected"], bpm, delta=0.1)

    def test_half_and_double_time_readings_are_findings(self):
        for requested in (60, 240):
            with self.subTest(requested=requested):
                proc = run_beats(self.wav, requested)
                self.assertNotIn("Traceback", proc.stderr)
                self.assertEqual(proc.returncode, 1, proc.stdout)
                self.assertAlmostEqual(json.loads(proc.stdout)["bpm_detected"], 120, delta=2)


if __name__ == "__main__":
    unittest.main()
