"""music.py: turn generated takes into a loopable, loudness-normalized bed.

  music.py generate --prompt <p> --bpm <n> --seconds <s> [--takes 3] --out-dir <dir> [--seed <n>] [--json]
  music.py finish <wav> --bpm <n> --seconds <s> --out <wav> [--crossfade-ms 15] [--json]

generate runs ACE-Step 1.5 in its own venv (setup-audio.sh --music) and writes
take-<i>.wav plus take-<i>.wav.provenance.json. It only fills in missing takes,
so a rerun converges on --takes takes instead of replacing ones already heard.
ACE-Step is not deterministic for a fixed seed, so a chosen bed is an asset to
keep, never something to regenerate at render time.

finish accepts a take detected within 3% of the requested tempo (beats.py's
gate), stretches it onto that tempo with ffmpeg atempo when it is more than
0.1 BPM off, keeps only whole bars from the first downbeat (a take is ~80%
music and then goes silent), loops them with a crossfade at the bar line, and
applies two-pass loudnorm to -14 LUFS / -1.5 dBTP.

Exit 0 done, 1 the take is unusable (tempo check failed, under one bar of music,
or generation failed), 2 usage or environment.
"""
import argparse
import hashlib
import json
import math
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import time

# The skill dir is symlinked into the runtimes; keep bytecode out of it.
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLCHAIN = os.environ.get(
    "PRODUCT_VIDEO_TOOLCHAIN",
    os.path.expanduser("~/.local/state/product-video/toolchain"),
)
ACE_ROOT = os.path.join(TOOLCHAIN, "ACE-Step-1.5")
ACE_COMMIT = "ca1e85fe9430179831e6bc6be790c332190a3866"
# The model card that grants commercial use of outputs, pinned because it can change.
ACE_MODEL_CARD = "ACE-Step/Ace-Step1.5@19671f406d603126926c1b7e2adc169acbcade22"
TARGET_I, TARGET_TP, TARGET_LRA = -14.0, -1.5, 11.0
STRETCH_THRESHOLD_BPM = 0.1


class Unusable(Exception):
    """The input is valid but cannot become a bed: exit 1."""


class EnvError(Exception):
    """Missing tools, files or toolchain: exit 2."""


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def plain_bpm(bpm):
    return int(bpm) if float(bpm).is_integer() else bpm


# finish

def loop_bars(x, sr, first_downbeat, last_beat, bpm, seconds, crossfade_ms):
    """Returns (bed, bars, start_sample, loop_samples).

    The first pass is the take as recorded. Each repeat starts with the audio
    that followed the loop fading out under the loop's own start, so the sample
    after every seam continues the sample before it and the splice is spread
    over the crossfade instead of landing on one sample.
    """
    import numpy as np

    bar = 240.0 / bpm
    xf = int(round(crossfade_ms / 1000.0 * sr))
    start = int(round(first_downbeat * sr))
    # The tracker can place a beat in a take's silent tail, so the music also
    # ends at the last audible 10ms (above -50 dBFS, as silencedetect reads it).
    hop = max(1, sr // 100)
    power = (x[: len(x) // hop * hop] ** 2).mean(axis=1).reshape(-1, hop).mean(axis=1)
    loud = np.flatnonzero(power > 10 ** (-50 / 10))
    audible_end = (int(loud[-1]) + 1) * hop if len(loud) else 0
    music_end = min(len(x), audible_end, int(round((last_beat + 60.0 / bpm) * sr)))
    bars = int(math.floor((music_end - start - xf) / (bar * sr) + 1e-9))
    if bars < 1:
        raise Unusable(f"under one whole bar of music after the first downbeat at {first_downbeat:.3f}s")
    n = int(round(bars * bar * sr))
    seg = x[start:start + n + xf]
    body = seg[:n].copy()
    if xf:
        fade_in = (np.arange(xf) / xf)[:, None]
        body[:xf] = seg[:xf] * fade_in + seg[n:n + xf] * (1.0 - fade_in)
    total = int(round(seconds * sr))
    repeats = max(0, math.ceil((total - n) / n))
    bed = np.concatenate([seg[:n]] + [body] * repeats)[:total]
    return bed, bars, start, n


def ffmpeg(*args):
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise EnvError(f"ffmpeg failed: {proc.stderr.strip().splitlines()[-1:]}")
    return proc.stderr


def loudnorm_stats(log):
    return json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", log)[-1])


def measure(path, target):
    return loudnorm_stats(ffmpeg("-i", path, "-af", f"loudnorm={target}:print_format=json", "-f", "null", "-"))


def linear_fits(m):
    return float(m["input_tp"]) + TARGET_I - float(m["input_i"]) <= TARGET_TP


def loudnorm(src, out, sr, total):
    """Two-pass linear loudnorm, preceded by a peak limiter when needed.

    Generated beds sit at -15 to -20 LUFS with peaks near 0 dBTP, so the gain
    to -14 would break -1.5 dBTP. loudnorm then drops to its dynamic mode, which
    undershoots the target by more than a LU. Limiting first, oversampled 4x to
    approximate true peak, leaves headroom for a plain linear gain.
    """
    target = f"I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}"
    first = m = measure(src, target)
    gain = 0.0
    ceiling = 10 ** ((TARGET_TP - 1.0) / 20)
    for _ in range(4):
        if linear_fits(m):
            break
        gain += TARGET_I - float(m["input_i"])
        limited = src + ".limited.wav"
        ffmpeg("-y", "-i", src, "-af",
               f"aresample={4 * sr},volume={gain:.3f}dB,"
               f"alimiter=limit={ceiling:.5f}:attack=1:release=60:level=false:latency=true,aresample={sr}",
               "-c:a", "pcm_f32le", limited)
        m = measure(limited, target)
    else:
        if not linear_fits(m):
            raise EnvError("could not bring peaks under the true-peak target")
    if gain:
        src = limited
    # Resample back from loudnorm's internal 192k and pin the length exactly.
    chain = (
        f"loudnorm={target}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
        f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
        f":offset={m['target_offset']}:linear=true:print_format=json,"
        f"aresample={sr},apad=whole_len={total},atrim=end_sample={total}"
    )
    applied = loudnorm_stats(ffmpeg("-y", "-i", src, "-af", chain, "-ar", str(sr), "-c:a", "pcm_s24le", out))
    applied["limiter_gain_db"] = round(gain, 2)
    return first, applied


def finish(args):
    import numpy as np
    import soundfile as sf

    sys.path.insert(0, HERE)
    import beats

    src = os.path.abspath(args.wav)
    if not os.path.isfile(src):
        raise EnvError(f"no such file: {args.wav}")
    bpm = plain_bpm(args.bpm)
    ok, found, _ = beats.analyze(src, bpm)
    if not ok:
        raise Unusable(f"tempo check failed: detected {found['bpm_detected']} BPM, requested {bpm}")
    pre = post = found["bpm_detected"]
    ratio = 1.0

    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    work = tempfile.mkdtemp(prefix="product-video-music-")
    try:
        take = src
        # Bars are cut at the requested length, so a take even slightly off
        # tempo would put every loop seam off the beat. Stretch it onto the
        # requested tempo first, then trust only a fresh detection.
        if abs(pre - bpm) > STRETCH_THRESHOLD_BPM:
            ratio = bpm / pre
            take = os.path.join(work, "stretched.wav")
            ffmpeg("-y", "-i", src, "-af", f"atempo={ratio:.6f}", "-c:a", "pcm_f32le", take)
            ok, found, _ = beats.analyze(take, bpm)
            if not ok:
                raise Unusable(f"tempo check failed after stretching x{ratio:.4f}: {found['bpm_detected']} BPM")
            post = found["bpm_detected"]
        x, sr = sf.read(take, dtype="float64", always_2d=True)
        bed, bars, start, n = loop_bars(
            x, sr, found["first_downbeat"], found["beats"][-1], bpm, args.seconds, args.crossfade_ms,
        )
        raw = os.path.join(work, "looped.wav")
        sf.write(raw, bed.astype(np.float32), sr, subtype="FLOAT")
        staged = os.path.join(work, "bed.wav")
        measured, applied = loudnorm(raw, staged, sr, len(bed))
        shutil.move(staged, out)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    prov = {
        "tool": "product-video music.py finish",
        "source": src,
        "sha256": sha256(src),
        "bpm": bpm,
        "bpm_detected": post,
        "bpm_detected_pre": pre,
        "bpm_detected_post": post,
        "stretch_ratio": round(ratio, 6),
        "bars": bars,
        "bar_seconds": 240.0 / bpm,
        # Trim points are on the stretched timeline; source time is that times stretch_ratio.
        "trim": {
            "start_s": round(start / sr, 6), "end_s": round((start + n) / sr, 6),
            "start_sample": start, "end_sample": start + n,
            "source_start_s": round(start / sr * ratio, 6), "source_end_s": round((start + n) / sr * ratio, 6),
        },
        "crossfade_ms": args.crossfade_ms,
        "seconds": args.seconds,
        "sample_rate": sr,
        "output_sha256": sha256(out),
        "loudness": {
            "target_i": TARGET_I, "target_tp": TARGET_TP,
            "input_i": float(measured["input_i"]), "input_tp": float(measured["input_tp"]),
            "output_i": float(applied["output_i"]), "output_tp": float(applied["output_tp"]),
            "normalization_type": applied.get("normalization_type"),
            "limiter_gain_db": applied["limiter_gain_db"],
        },
    }
    take_prov = src + ".provenance.json"
    if os.path.isfile(take_prov):
        with open(take_prov) as f:
            prov["source_provenance"] = json.load(f)
    write_json(out + ".provenance.json", prov)
    return prov, (
        f"finish: {out}\n  {bars} bars from {start / sr:.3f}s looped to {args.seconds}s, "
        f"{float(applied['output_i']):.1f} LUFS / {float(applied['output_tp']):.1f} dBTP, "
        f"stretch x{ratio:.4f} ({pre} -> {post} BPM) "
        f"({applied.get('normalization_type')})"
    )


# generate

def generate(args):
    py = os.path.join(ACE_ROOT, ".venv", "bin", "python")
    if not os.access(py, os.X_OK):
        raise EnvError(f"ACE-Step not installed at {ACE_ROOT}; run helpers/setup-audio.sh --music")
    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    missing = [
        i for i in range(1, args.takes + 1)
        if not os.path.isfile(os.path.join(out_dir, f"take-{i}.wav.provenance.json"))
    ]
    base = args.seed if args.seed is not None else secrets.randbelow(2**31 - args.takes)
    job = {
        "root": ACE_ROOT,
        "out_dir": out_dir,
        "prompt": args.prompt,
        "bpm": plain_bpm(args.bpm),
        "seconds": args.seconds,
        "duration": math.ceil(args.seconds / 0.8) + 4,
        "takes": [{"index": i, "seed": base + i} for i in missing],
    }
    work = tempfile.mkdtemp(prefix="product-video-ace-")
    try:
        job_path = os.path.join(work, "job.json")
        job["result"] = os.path.join(work, "result.json")
        write_json(job_path, job)
        if missing:
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
                       HF_HOME=os.environ.get("HF_HOME", os.path.join(TOOLCHAIN, "hf-home")),
                       TORCH_HOME=os.environ.get("TORCH_HOME", os.path.join(TOOLCHAIN, "torch-home")))
            # ACE-Step logs heavily to stdout; keep ours clean for --json.
            subprocess.run([py, "-B", os.path.abspath(__file__), "_ace-worker", job_path],
                           cwd=ACE_ROOT, env=env, stdout=sys.stderr, check=False)
        done = []
        if os.path.isfile(job["result"]):
            with open(job["result"]) as f:
                done = json.load(f)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    takes = sorted(
        os.path.join(out_dir, f"take-{i}.wav") for i in range(1, args.takes + 1)
        if os.path.isfile(os.path.join(out_dir, f"take-{i}.wav.provenance.json"))
    )
    summary = {"out_dir": out_dir, "takes": takes, "generated": done, "requested": args.takes}
    if len(takes) < args.takes:
        raise Unusable(f"only {len(takes)} of {args.takes} takes exist in {out_dir}: {json.dumps(summary)}")
    return summary, "generate: " + ", ".join(takes)


def ace_worker(job_path):
    """Runs inside ACE-Step's venv. Loads the models once for all takes."""
    with open(job_path) as f:
        job = json.load(f)
    root = job["root"]
    os.chdir(root)
    sys.path.insert(0, root)
    from acestep.handler import AceStepHandler
    from acestep.inference import GenerationConfig, GenerationParams, generate_music
    from acestep.llm_inference import LLMHandler

    commit = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    t0 = time.time()
    dit = AceStepHandler()
    msg, ok = dit.initialize_service(project_root=root, config_path="acestep-v15-turbo", device="mps")
    if not ok:
        raise SystemExit(f"ACE-Step DiT init failed: {msg[:300]}")
    llm = LLMHandler()
    msg, ok = llm.initialize(checkpoint_dir=os.path.join(root, "checkpoints"),
                             lm_model_path="acestep-5Hz-lm-1.7B", backend="mlx", device="mps")
    if not ok:
        raise SystemExit(f"ACE-Step LM init failed: {msg[:300]}")
    init_s = time.time() - t0

    done = []
    for take in job["takes"]:
        stage = os.path.join(job["out_dir"], f".take-{take['index']}.staging")
        shutil.rmtree(stage, ignore_errors=True)
        os.makedirs(stage)
        t1 = time.time()
        params = GenerationParams(
            caption=job["prompt"], lyrics="[Instrumental]", instrumental=True, bpm=job["bpm"],
            timesignature="4", duration=job["duration"], seed=take["seed"], thinking=True,
        )
        config = GenerationConfig(batch_size=1, use_random_seed=False, seeds=[take["seed"]], audio_format="wav")
        res = generate_music(dit, llm, params, config, save_dir=stage)
        paths = [a.get("path") for a in res.audios if a.get("path")]
        if not res.success or not paths:
            print(f"take {take['index']} failed: {res.error}", file=sys.stderr)
            shutil.rmtree(stage, ignore_errors=True)
            continue
        dest = os.path.join(job["out_dir"], f"take-{take['index']}.wav")
        shutil.move(paths[0], dest)
        shutil.rmtree(stage, ignore_errors=True)
        lm = res.extra_outputs.get("lm_metadata") if isinstance(res.extra_outputs, dict) else None
        prov = {
            "provider": "ACE-Step 1.5",
            "commit": commit,
            "model_card": ACE_MODEL_CARD,
            "license": "MIT; model card permits commercial use of outputs. Disclose AI involvement.",
            "seed": take["seed"],
            "prompt": job["prompt"],
            "bpm": job["bpm"],
            "timesignature": "4",
            "duration_requested": job["duration"],
            "seconds_needed": job["seconds"],
            "sha256": sha256(dest),
            "lm_metadata": json.loads(json.dumps(lm, default=str)) if lm else None,
            "generate_s": round(time.time() - t1, 1),
            "init_s": round(init_s, 1),
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }
        # Provenance last: its presence is what marks a take complete.
        write_json(dest + ".provenance.json", prov)
        done.append({"take": dest, "seed": take["seed"], "generate_s": prov["generate_s"]})
    write_json(job["result"], done)


def main(argv):
    if argv[:1] == ["_ace-worker"]:
        ace_worker(argv[1])
        return 0
    ap = argparse.ArgumentParser(prog="music.py", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("finish")
    f.add_argument("wav")
    f.add_argument("--bpm", type=float, required=True)
    f.add_argument("--seconds", type=float, required=True)
    f.add_argument("--out", required=True)
    f.add_argument("--crossfade-ms", type=float, default=15.0)
    f.add_argument("--json", action="store_true")
    g = sub.add_parser("generate")
    g.add_argument("--prompt", required=True)
    g.add_argument("--bpm", type=float, required=True)
    g.add_argument("--seconds", type=float, required=True)
    g.add_argument("--takes", type=int, default=3)
    g.add_argument("--out-dir", required=True)
    g.add_argument("--seed", type=int)
    g.add_argument("--json", action="store_true")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    try:
        result, report = (finish if args.cmd == "finish" else generate)(args)
    except Unusable as e:
        print(f"music {args.cmd}: {e}", file=sys.stderr)
        if args.json:
            print(json.dumps({"ok": False, "error": str(e)}))
        return 1
    except (EnvError, ImportError) as e:
        print(f"music {args.cmd}: {e}", file=sys.stderr)
        return 2
    print(json.dumps(result) if args.json else report)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
