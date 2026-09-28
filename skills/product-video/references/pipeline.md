# Pipeline

Stage detail for `SKILL.md`. Paths are relative to the skill directory unless
absolute. `$RUN` is `~/.local/state/product-video/runs/<run-id>/`.

## 1. References

Pick 3 to 5 launch films from products with a similar audience. Sources:
whatships.com, product launch posts on X, and competitors' launch pages. For
each film:

```bash
ffmpeg -i ref.mp4 -vf "fps=2,scale=270:-1,tile=6x6" -frames:v 1 "$RUN/refs/<name>-contact.png"
```

Read the contact sheets, then write `style_guide.md` in dev-notes. It covers:
- palette in hex
- type: family, weight, tracking
- median shot length
- transition types
- camera moves
- how text enters and exits
- texture and grain

Take the grammar of a reference, never its content, logos or characters. The
project's own tokens and fonts override a reference's palette and type.

## 2. Brief and storyboard

The brief is one page in dev-notes. It covers:
- the film in one line
- audience
- duration
- formats
- BPM
- the beat list

Each beat names:
- its time range, 2 to 4 seconds
- the fixture and query string it mounts
- the triggers that run inside it
- the on-screen text
- the transition out

The first two seconds carry the hook.

Render one still per beat by running `scene.ts` with `duration` set to one
frame. Assemble them with `sheets.ts`, and ask the operator to approve the
storyboard with that sheet attached. Scenes, music and composition wait for the
answer.

## 3. Music

See `music.md` for providers and licensing.

```bash
PY=~/.local/state/product-video/toolchain/audio-venv/bin/python
$PY helpers/music.py generate --prompt "<mood>" --bpm <bpm> --seconds <s> --takes 3 --out-dir "$RUN/music"
$PY helpers/beats.py "$RUN/music/<take>.wav" --bpm <bpm> --json > "$RUN/music/<take>.beats.json"   # exit 1 = wrong tempo, try the next take
$PY helpers/music.py finish "$RUN/music/<take>.wav" --bpm <bpm> --seconds <s> --out "$RUN/music/bed.wav"
$PY helpers/beats.py "$RUN/music/bed.wav" --bpm <bpm> --json > "$RUN/music/beats.json"
```

Pass `--seconds` as the bed length the brief needs. `generate` oversizes each
take on its own (`ceil(seconds / 0.8) + 4`), and `finish` cuts it back.

`beats.json` `grid` drives every cut and trigger time. Snap beat boundaries to
the grid, never to round seconds.

## 4. Scenes

Build the fixture once per run:

```bash
bun helpers/fixture-build.ts --repo <project repo> --fixture <name> --out "$RUN/build/<name>"
```

Then write one `scene.json` per beat. The shape is in `bun helpers/scene.ts --help`,
and the project file gives the entry, query strings, routes and
`removeClasses`.

```bash
bun helpers/scene.ts "$RUN/scenes/03-reactions.json" --out "$RUN/clips/03-reactions.mp4"
```

`scene.ts` reports any finite animation that started with no trigger. That is a
timer-driven component. Fix it in the scene with a query string or route stub
that holds it still, or move the trigger so the animation lands on a beat. Never
fix it by editing product source.

After rendering each clip, open its first and last frames with
`ffmpeg -i clip.mp4 -vf "select=eq(n\,0)" -frames:v 1 first.png` and the same
for the last frame index. Confirm the beat shows the state the storyboard
promised, not an error or empty state. Stubs measured on one query string do not
prove another.

Clip rules:
- One clip per beat, trimmed on the grid.
- UI state changes land on beats, big moments on downbeats.
- A clip with no state change longer than one beat fails `dead-beats.ts`.

## 5. Compose

A HyperFrames project in `$RUN/compose/`. Pin the version the skill was proven
on, `npx hyperframes@0.8.82`, because the plugin updates daily.

- **Clips.** Each clip is `<video class="clip" muted playsinline>` on its own
  track, with no `crossorigin` and no timed wrapper around it. Composition frame
  n shows clip frame n minus the clip's start frame, frame-exact.
- **Titles and overlays** follow `/hyperframes-animation` and `style_guide.md`.
  Copy `gsap.min.js` into `assets/`, because a CDN script is a network fetch at
  render time. Give every named font an `@font-face` pointing at a local woff2
  copied from the project repo. Without one, lint reports
  `font_family_without_font_face` and the render falls back to a system face.
- **Music.** `bed.wav` goes in as `<audio id="bed">`. Fade it in over at least
  50ms and out at the end, both through its `data-automation` volume lane, for
  example `{"t":0,"v":0},{"t":0.05,"v":1}`. Never fade with a GSAP volume tween.
  A bed that starts at full amplitude leaves an AAC peak at about 13ms. HF's
  true-peak guard then turns the whole mix down by about 6 dB. Mix with
  `/hyperframes-audio`. Never source music through `/media-use`.
- **Assets live inside the project.** Lint rejects `../` asset paths
  (`invalid_parent_traversal_in_asset_path`). Symlink clips and the bed into
  `compose/assets/`, for example `assets/clips` pointing at `$RUN/clips/final`.
  HF's frame cache keys on path, mtime and size, so a re-rendered clip is picked
  up with no edit.
- **Give full-frame cards an explicit size.** A root-level `.clip` is pinned
  top-left and shrink-wrapped, so a title card clips off the top unless it is
  sized to the whole frame.
- **Push held shots.** A slow linear push of at most 2 to 3% across a held shot
  keeps every half-second window above the `dead-beats.ts` threshold without
  reading as a camera move. That includes a closing title's hold.
- Put `data-no-timeline` on the composition root. It only skips a 45-second
  wait for timeline registration, and is harmless beside a registered timeline.

Render deterministically:

```bash
HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 \
  npx hyperframes@0.8.82 render "$RUN/compose" -o "$RUN/out/r<N>-mix.mp4" --fps 30 -w 1 --no-browser-gpu
```

A 24-second 1080×1920 composition renders in about 45 seconds, lint included.

HF warns about sparse keyframes on long `scene.ts` clips, because they are encoded
with a long GOP. Frame placement stays exact (SSIM 1.000 against the source),
so the warning is safe to ignore.

HF also writes outside the project: `~/.hyperframes/`,
`~/.cache/hyperframes/`, and a frame cache in
`$TMPDIR/hyperframes-extract-cache-<uid>`. Leave them unless the operator asks
for cleanup.

**The composition must pass `determinism.ts` on two renders before the run
relies on it.** HF 0.8.82 passed with clip inputs, a title card and a bed
(every stream identical, clip frames at SSIM 0.9985 against the source). If a
later version fails, compose with ffmpeg instead: concatenate clips with hard
cuts on grid times, burn titles in from `scene.ts`-rendered HTML title cards,
and mux `bed.wav`.

**Master.** HF's AAC mix does not land on the loudness target. It measured
-14.9 LUFS on a raw bed, and -14.19 LUFS / -1.23 dBTP on a bed that `finish`
had already mastered, because AAC overshoots true peak. Extract the audio,
normalize it with a true-peak target of -2.0 so the final AAC encode lands at or
under -1.5, and remux, copying the video untouched:

```bash
ffmpeg -v error -i "$RUN/out/r<N>-mix.mp4" -vn -c:a pcm_s16le "$RUN/out/r<N>-mix.wav"
bun helpers/loudness.ts "$RUN/out/r<N>-mix.wav" "$RUN/out/r<N>-master.wav" --tp -2.0
ffmpeg -v error -i "$RUN/out/r<N>-mix.mp4" -i "$RUN/out/r<N>-master.wav" \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest "$RUN/out/r<N>.mp4"
```

Then measure the final file's audio. The loudness check in `review.md` applies
to `r<N>.mp4`, not to the intermediate WAV.

`r<N>.mp4` is the revision the checks and the judge see. Run the determinism
check on two full passes, render plus master.

**Formats.** Render 9:16 first. For 16:9, re-render the scenes at 960×540 DPR 2
with the same `scene.json` beats. Never crop a 9:16 render.

## Revisions

A revision is one full render of the composition, named `r1`, `r2` and so on
within a run. Every judge round produces the next revision. Only the revision
the judge passes is published, under its own name. Render outputs are
`$RUN/out/r<N>.mp4`.

## 6 and 7. Checks and judge

See `review.md`.

## 8. Approval

See `review.md`, "Publish".

## Project file template

`references/projects/<project>.md`:

```markdown
# <project>

- Repo: <absolute path to the canonical checkout>
- Fixtures: <dir and naming, e.g. tools/visual/<name>-fixture.html>
- Build: fixture-build.ts works | needs <what>
- removeClasses: [<classes the fixtures force>]
- Routes to stub: <path, status, body>
- Query strings: <the states worth filming and how to reach them>
- Tokens and fonts: <where the brand lives in source>
- Evidence renderer: <how a revision is published and where the operator opens it>
- Never: <project-specific prohibitions>
```
