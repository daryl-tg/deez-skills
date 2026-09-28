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

A HyperFrames project in `$RUN/compose/`:
- Each clip is a `<video class="clip">` on its own track.
- Titles and overlays follow `/hyperframes-animation` and `style_guide.md`.
- `bed.wav` is placed as `<audio>`. Mix with `/hyperframes-audio`. Never source
  music through `/media-use`.

Render deterministically:

```bash
HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 \
  npx hyperframes render "$RUN/compose" -o "$RUN/out/r<N>.mp4" --fps 30 -w 1 --no-browser-gpu
```

Put `data-no-timeline` on the composition root. Without it the render waits
45 seconds per session and can fail with `Attempted to use detached Frame`.
Expect about 60 seconds of lint before each render.

**The composition must pass `determinism.ts` on two renders before the run
relies on it.** If HyperFrames cannot hold identical frames with clip inputs,
compose with ffmpeg instead: concatenate clips with `xfade` transitions on grid
times, burn titles in from `scene.ts`-rendered HTML title cards, and mux
`bed.wav`.

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
