"""groove120: 20s mono 44.1k test groove at 120 BPM, one bar every 2.0s.

Ported from the Unit 2 spike. A bare accented click fools beat trackers into a
downbeat one beat late; kick, snare and a bass root that changes every bar give
them the right phase. Seeded, so regeneration is byte-identical.

onbeat_hats=False drops the hat noise that starts on every beat, and pad_hz
adds sustained sines (pad_amp each). Together they make a variant whose bar lines are free of
noise, so its loop seam can be judged sample by sample. silent_from mutes
everything after that time, like a generated take that stops early. bpm moves
the tempo off 120, like a generated take that misses the requested tempo.
"""
import math
import random
import struct
import sys
import wave


def make_groove120(path, dur=20.0, onbeat_hats=True, pad_hz=None, silent_from=None, bpm=120.0, pad_amp=0.15):
    rng = random.Random(0)
    sr = 44100
    beat = 60.0 / bpm
    n = int(sr * dur)
    buf = [0.0] * n

    def add(t, fn, length):
        s = int(round(t * sr))
        for i in range(int(length * sr)):
            if s + i < n:
                buf[s + i] += fn(i / sr)

    kick = lambda x: 0.9 * math.sin(2 * math.pi * (50 + 80 * math.exp(-x * 30)) * x) * math.exp(-x * 9)
    snare = lambda x: 0.35 * rng.uniform(-1, 1) * math.exp(-x * 25) + 0.2 * math.sin(2 * math.pi * 190 * x) * math.exp(-x * 20)
    hat = lambda x: 0.12 * rng.uniform(-1, 1) * math.exp(-x * 80)
    roots = [55.0, 43.65, 49.0, 41.2]
    for k in range(int(dur / beat)):
        t = k * beat
        pos = k % 4
        if pos == 0:
            add(t, kick, 0.4)
        if pos == 2:
            add(t, kick, 0.3)
        if pos in (1, 3):
            add(t, snare, 0.25)
        if onbeat_hats:
            add(t, hat, 0.06)
        add(t + 0.25, hat, 0.06)
        if pos == 0:
            r = roots[(k // 4) % 4]
            add(t, lambda x, r=r: 0.3 * math.sin(2 * math.pi * r * 2 * x) * math.exp(-x * 0.8), 1.95)
            for m in (1, 1.26, 1.5):
                add(t, lambda x, r=r, m=m: 0.06 * math.sin(2 * math.pi * r * 8 * m * x) * min(1, x * 20) * math.exp(-x * 0.6), 1.95)
    if pad_hz:
        for hz in (pad_hz if isinstance(pad_hz, (list, tuple)) else [pad_hz]):
            buf = [v + pad_amp * math.sin(2 * math.pi * hz * i / sr) for i, v in enumerate(buf)]
    if silent_from is not None:
        cut = int(round(silent_from * sr))
        buf[cut:] = [0.0] * (n - cut)
    peak = max(abs(x) for x in buf)
    buf = [x / peak * 0.9 for x in buf]
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", int(x * 32767)) for x in buf))
    return path


if __name__ == "__main__":
    make_groove120(sys.argv[1] if len(sys.argv) > 1 else "groove120.wav")
