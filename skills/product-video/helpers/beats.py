"""beats.py <wav> --bpm <n> [--json]

Detects beats and downbeats with beat_this and accepts the track only if its
tempo is within 3% of the requested one. The gate exists to reject misreads
(half or double time, a garbled detection), not to police tempo: music.py
finish stretches an accepted take onto the requested tempo. beat_this snaps beats to 20ms
frames, so a median interval reads 118 BPM as 120 (0.50/0.52s gaps). The tempo
is instead the slope of a least-squares line through beat time against beat
index, which is precise below a frame. On acceptance it also emits `grid`: beat
times at that detected tempo, phased onto the detected downbeats, free of the
tracker's frame jitter.

Exit 0 accepted, 1 tempo mismatch or no tempo found, 2 usage or environment.
Run with the toolchain venv python (setup-audio.sh).
"""
import argparse
import json
import math
import os
import sys

TOLERANCE_PCT = 3.0
TOOLCHAIN = os.environ.get(
    "PRODUCT_VIDEO_TOOLCHAIN",
    os.path.expanduser("~/.local/state/product-video/toolchain"),
)
# Keep the beat_this checkpoint in the toolchain, where setup-audio prefetched it.
os.environ.setdefault("TORCH_HOME", os.path.join(TOOLCHAIN, "torch-home"))


def load_mono(path):
    import numpy as np
    import soundfile as sf

    signal, sr = sf.read(path, dtype="float64", always_2d=True)
    return np.ascontiguousarray(signal.mean(axis=1)), sr


def detect(path):
    """Returns (beats, downbeats, duration) in seconds."""
    import warnings

    warnings.filterwarnings("ignore")
    from beat_this.inference import Audio2Beats

    signal, sr = load_mono(path)
    beats, downbeats = Audio2Beats(checkpoint_path="final0", device="cpu", dbn=False)(signal, sr)
    return [float(b) for b in beats], [float(d) for d in downbeats], len(signal) / sr


def regression_bpm(beats):
    """60 / slope of beat time against beat index.

    Indices come from rounding each gap to whole periods, so a missed beat
    counts as two; the period estimate is refined once from the first fit.
    """
    if len(beats) < 3:
        return None
    gaps = sorted(b - a for a, b in zip(beats, beats[1:]))
    period = gaps[len(gaps) // 2]
    for _ in range(2):
        idx = [0]
        for a, b in zip(beats, beats[1:]):
            idx.append(idx[-1] + max(1, round((b - a) / period)))
        n = len(beats)
        mx, my = sum(idx) / n, sum(beats) / n
        sxx = sum((i - mx) ** 2 for i in idx)
        period = sum((i - mx) * (t - my) for i, t in zip(idx, beats)) / sxx
    return 60.0 / period


def first_downbeat(downbeats, beats, bpm):
    """Phase of the bar at `bpm` (the detected tempo), fitted as a circular mean so one late detection
    cannot drag it; returned as the earliest grid downbeat at or after ~0."""
    period = 60.0 / bpm
    marks, cycle = (downbeats, 4 * period) if downbeats else (beats, period)
    c = sum(math.cos(2 * math.pi * t / cycle) for t in marks)
    s = sum(math.sin(2 * math.pi * t / cycle) for t in marks)
    phase = (math.atan2(s, c) / (2 * math.pi)) * cycle % cycle
    # A phase just short of a full cycle is a downbeat at ~0, not one bar in.
    if phase > cycle - 0.03:
        phase -= cycle
    return phase


def grid_times(phase, bpm, duration):
    period = 60.0 / bpm
    n = math.ceil((-0.03 - phase) / period)
    out = []
    while True:
        t = phase + n * period
        if t > duration:
            return out
        out.append(round(max(t, 0.0), 4))
        n += 1


def analyze(path, bpm):
    beats, downbeats, duration = detect(path)
    detected = regression_bpm(beats)
    result = {
        "bpm_requested": bpm,
        "bpm_detected": round(detected, 3) if detected else None,
        "beats": [round(b, 3) for b in beats],
        "downbeats": [round(d, 3) for d in downbeats],
    }
    ok = detected is not None and abs(detected - bpm) <= bpm * TOLERANCE_PCT / 100
    if ok:
        phase = first_downbeat(downbeats, beats, detected)
        result["grid"] = grid_times(phase, detected, duration)
        result["first_downbeat"] = round(max(phase, 0.0), 4)
    return ok, result, duration


def main(argv):
    ap = argparse.ArgumentParser(prog="beats.py", description=__doc__.split("\n\n")[1])
    ap.add_argument("wav")
    ap.add_argument("--bpm", type=float, required=True)
    ap.add_argument("--json", action="store_true")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    bpm = int(args.bpm) if args.bpm.is_integer() else args.bpm
    if not os.path.isfile(args.wav):
        print(f"beats: no such file: {args.wav}", file=sys.stderr)
        return 2
    try:
        ok, result, _ = analyze(args.wav, bpm)
    except ImportError as e:
        print(f"beats: toolchain missing ({e}); run helpers/setup-audio.sh", file=sys.stderr)
        return 2
    except Exception as e:  # unreadable audio is an input problem, not a finding
        print(f"beats: could not analyze {args.wav}: {e}", file=sys.stderr)
        return 2
    if not ok:
        result.pop("beats")
        result.pop("downbeats")
    if args.json:
        print(json.dumps({k: v for k, v in result.items() if k != "first_downbeat"}))
    else:
        verdict = "PASS" if ok else f"FAIL (outside ±{TOLERANCE_PCT:g}%)"
        print(f"beats: detected {result['bpm_detected']} BPM, requested {bpm}: {verdict}")
        if ok:
            print(f"  {len(result['downbeats'])} downbeats, grid of {len(result['grid'])} beats "
                  f"from {result['first_downbeat']}s")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
