import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

import soundfile as sf

# The skill dir is symlinked into the runtimes; keep bytecode out of it.
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
MUSIC = os.path.join(HERE, "..", "helpers", "music.py")
BEATS = os.path.join(HERE, "..", "helpers", "beats.py")
sys.path.insert(0, os.path.join(HERE, "fixtures"))
from make_groove120 import make_groove120  # noqa: E402


def finish(src, out, seconds, *extra):
    return subprocess.run(
        [sys.executable, MUSIC, "finish", src, "--bpm", "120", "--seconds", str(seconds), "--out", out, *extra],
        capture_output=True, text=True, timeout=300,
    )


def detect_beats(path):
    proc = subprocess.run(
        [sys.executable, BEATS, path, "--bpm", "120", "--json"], capture_output=True, text=True, timeout=300,
    )
    return proc.returncode, json.loads(proc.stdout)


def measure(path):
    log = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "loudnorm=print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    ).stderr
    stats = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", log).group(0))
    return float(stats["input_i"]), float(stats["input_tp"])


class FinishTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.src = make_groove120(os.path.join(cls.tmp.name, "groove120.wav"))
        cls.out = os.path.join(cls.tmp.name, "bed.wav")
        cls.proc = finish(cls.src, cls.out, 30)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_bed_is_requested_length_at_streaming_loudness(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stderr)
        info = sf.info(self.out)
        self.assertEqual(info.samplerate, 44100)
        self.assertLessEqual(abs(info.frames - 30 * 44100), 1)
        integrated, true_peak = measure(self.out)
        self.assertAlmostEqual(integrated, -14.0, delta=0.5)
        self.assertLessEqual(true_peak, -1.4)

    def test_provenance_names_the_source_by_content(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stderr)
        with open(self.out + ".provenance.json") as f:
            prov = json.load(f)
        with open(self.src, "rb") as f:
            self.assertEqual(prov["sha256"], hashlib.sha256(f.read()).hexdigest())
        self.assertEqual(prov["source"], os.path.abspath(self.src))
        self.assertEqual(prov["bpm"], 120)
        # 20s of groove holds 9 whole bars plus the crossfade tail.
        self.assertEqual(prov["bars"], 9)

    def test_loop_seam_does_not_click(self):
        # groove120's hats put 0.03-0.10 sample jumps on every downbeat, and its
        # crest factor makes the limiter clamp both sides of a seam alike. So
        # the seam is judged on a variant with quiet bar lines and a loud
        # two-partial pad, whose phase a hard splice breaks.
        src = make_groove120(os.path.join(self.tmp.name, "pad120.wav"), onbeat_hats=False,
                             pad_hz=(110.3, 146.9), pad_amp=0.2)
        cases = {"crossfaded": ([], True), "hard splice": (["--crossfade-ms", "0"], False)}
        for name, (extra, clean) in cases.items():
            with self.subTest(name):
                out = os.path.join(self.tmp.name, f"pad-{len(extra)}.wav")
                proc = finish(src, out, 40, *extra)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                with open(out + ".provenance.json") as f:
                    bars = json.load(f)["bars"]
                x, sr = sf.read(out)
                seams = range(bars * 2 * sr, len(x), bars * 2 * sr)
                self.assertGreaterEqual(len(seams), 1)
                worst = max(abs(x[s] - x[s - 1]) for s in seams)
                if clean:
                    self.assertLessEqual(worst, 0.05)
                else:
                    self.assertGreater(worst, 0.05)

    def test_silence_after_the_music_is_not_looped(self):
        # A take that stops 5ms into a bar: the tracker still hears that
        # downbeat, but the bar after it is silence and must not be a source
        # for the loop or its crossfade.
        src = make_groove120(os.path.join(self.tmp.name, "early-stop.wav"), silent_from=18.005)
        out = os.path.join(self.tmp.name, "early-stop-bed.wav")
        proc = finish(src, out, 40)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        with open(out + ".provenance.json") as f:
            prov = json.load(f)
        self.assertLessEqual(prov["trim"]["end_s"] + 0.015, 18.005)
        x, sr = sf.read(out)
        window = int(0.015 * sr)
        rms = lambda a: float((a ** 2).mean() ** 0.5)
        first = rms(x[:window])
        for s in range(prov["bars"] * 2 * sr, len(x), prov["bars"] * 2 * sr):
            self.assertGreater(rms(x[s:s + window]) / first, 0.8)

    def test_off_tempo_take_is_stretched_so_the_loop_keeps_time(self):
        # A take at 118 cut into 2.0s bars would land every seam ~0.3s off the
        # beat, a hiccup no sample-jump check can hear.
        src = make_groove120(os.path.join(self.tmp.name, "groove118.wav"), bpm=118)
        out = os.path.join(self.tmp.name, "bed118.wav")
        proc = finish(src, out, 40)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        with open(out + ".provenance.json") as f:
            prov = json.load(f)

        code, found = detect_beats(out)
        self.assertEqual(code, 0, found)
        self.assertAlmostEqual(found["bpm_detected"], 120, delta=0.1)
        beats = found["beats"]
        gaps = [b - a for a, b in zip(beats, beats[1:])]
        mean = sum(gaps) / len(gaps)
        seams = [k * prov["bars"] * 2.0 for k in range(1, 40) if k * prov["bars"] * 2.0 < 39.5]
        self.assertGreaterEqual(len(seams), 1)
        for seam in seams:
            j = min(range(1, len(beats) - 1), key=lambda i: abs(beats[i] - seam))
            # beat_this reports beats on 20ms frames, so any gap, seam or not,
            # can read one frame off the mean; allow that frame plus 5ms.
            for gap in (beats[j] - beats[j - 1], beats[j + 1] - beats[j]):
                self.assertLessEqual(abs(gap - mean), 0.025, f"seam at {seam}s")

        self.assertAlmostEqual(prov["stretch_ratio"], 120 / 118, delta=0.002)
        self.assertAlmostEqual(prov["bpm_detected_pre"], 118, delta=0.1)
        self.assertAlmostEqual(prov["bpm_detected_post"], 120, delta=0.1)


if __name__ == "__main__":
    unittest.main()
