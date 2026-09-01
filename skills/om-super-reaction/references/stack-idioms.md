# Stack Idioms

Pinned technical contracts for implementing a super reaction: the anime.js v4
API, the effect definition model, the bake and capture CLIs, DOM-backend
rules, and the Claude Design generator flow. Training-data familiarity with
anime.js skews toward v3 — treat every idiom below as load-bearing, not a
stylistic preference.

## anime.js v4

```ts
import { createTimeline, stagger } from "animejs";
```

- Timelines conduct; they never own the visual look themselves. A timeline
  drives property values on layers — DOM/CSS transforms and opacity for the
  DOM backend, uniforms for a future GLSL backend — the layers execute what
  the timeline schedules.
- **Determinism is `seek()`-driven, never wall-clock.** In fixture/capture
  mode, build the timeline with `autoplay: false` and drive it entirely via
  `timeline.seek(ms)` against a seeded RNG, so the same seed renders
  identical frames every time. Live mode uses `autoplay: true` (rAF-backed)
  with the seed varied per fire.
- `stagger(...)` is the mechanism for the 80–150ms follow-through spacing the
  motion bible requires (`motion-bible.md` rule 2) — use it rather than
  hand-rolling per-layer delays.
- The harness (`src/lib/super-reactions/harness.ts` in the target repo, name
  indicative) owns timeline lifecycle, exclusivity, and reduced-motion
  switching. Effects code against the harness's `CeremonyContext` (which
  hands them a `timeline: Timeline`), never against `animejs` imports or
  DOM lifecycle directly outside that contract.

## Effect definition contract

One typed registry entry per effect, matching `SuperReactionEffect` in the
target repo's `src/lib/super-reactions/types.ts` (read that file for the
exact current shape before writing a catalog file — this is the shape at
spec time):

```
id: string                     // kebab-case, stable forever once shipped
name: string
tuple: { material, motionCharacter, shapeVerb }   // provenance; rubric grades against it
silhouette: string             // one sentence; the readability contract
backend: "dom" | "webgl"       // "dom" unless a storyboard genuinely demands "webgl"
envelope: { anticipationMs, peakMs, settleMs }    // sum must be <= 3000
ceremony(ctx: CeremonyContext): void   // builds layers into ctx.stage, drives ctx.timeline
calm(ctx: CeremonyContext): void       // designed reduced-motion variant — required, never omitted
hover?(host: HTMLElement): () => void  // pill-hover preview; return a cleanup fn
sound?(audio: AudioContext, timeline: Timeline): void   // optional, opt-in gated by the harness
```

The metadata is load-bearing, not decoration: the fixture reads `envelope` to
know which frames to capture, the rubric grades against `tuple` and
`silhouette`, and the registry enforces `id` stability (message history holds
these strings forever).

## Bake tool

```
bun tools/super-reactions/bake.ts <frames-module> <out-dir>
```

Bakes a procedural frame sequence into a flipbook atlas: `<out-dir>/<name>.atlas.png`
(a grid of frames) plus `<out-dir>/<name>.atlas.json` describing
`{ frame: { w, h }, count, fps, columns }`. The frames module default-exports:

```ts
{ name, frame: { w, h }, count, fps, draw(ctx: CanvasRenderingContext2D, frameIndex: number, seed: number): void }
```

Pass a fixed seed on the CLI (default `1`) so bakes are reproducible. Import
the resulting atlas as a Vite asset inside the effect's catalog file (lazy
chunk) — it lands in `dist/assets/` as an extra.

*Per plan Task 7, this tool is built in the same implementation loop as this
skill and may not exist yet when this skill is authored. Verify the exact CLI
flags and output shape against the real script in `tools/super-reactions/bake.ts`
before relying on this description — it documents the contract at spec time,
not a guarantee the shipped tool matches byte-for-byte.*

## Fixture and capture

```
bun tools/visual/super-reaction-capture.ts <effect-id> [--seed 1]
```

Drives the deterministic fixture (`tools/visual/super-reaction-fixture.tsx`)
via Playwright and writes screenshots to:

```
~/Documents/dev-notes/om-chat-super-reactions/run-artifacts/<effect-id>/{anticipation,peak,settle,calm,pill-idle,pill-hover}-{desktop,phone}.png
```

Fixture URL params: `?effect=<id>&mode=ceremony|calm|pill|hover&t=<ms>&seed=<n>&w=<px>`.
The capture script reads the effect's `envelope` off the registry (exposed on
`window` in fixture builds) to compute capture timestamps — roughly
`anticipationMs/2`, `anticipationMs + peakMs/2`, and `total - settleMs/4` —
plus the calm and pill-idle/pill-hover modes, at 1280×800 (desktop) and
390×844 (phone).

**Known repo gotcha:** the fixture imports its own CSS
(`import "../../src/shared/super-reactions.css";` plus the app base sheet) —
`main.tsx`'s imports do not reach fixtures. Confirm the fixture does this
before trusting a capture; an unstyled capture is a false pass, not a
failure the capture script will flag for you.

*Per plan Task 8, this tool is built in the same implementation loop as this
skill and may not exist yet when this skill is authored. Verify the exact CLI
flags, URL params, and output paths against the real script before relying on
this description.*

## DOM-backend rules (v1 foundation)

- **Additive layering via `mix-blend-mode: plus-lighter`.** This is how
  overlapping glow/light layers combine without muddying into grey — use it
  for any layer meant to read as light, not standard alpha compositing.
- **≤120 DOM garnish nodes per ceremony.** Bounded particle/garnish node
  count is a hard Performance-axis budget (`rubric.md`), not a soft target.
- **Compositor-only motion.** Animate `transform` and `opacity` only — never
  `top`/`left`/`width`/`height` or anything that forces layout. This is what
  keeps a ceremony off the main thread's layout/paint work.
- **Baked sprite flipbook atlases for hero elements.** Pre-render the
  hero visual (with any glow/blur/grading baked into the pixels) via the
  bake tool rather than live-rendering it; anime.js steps the flipbook's
  `background-position` through the atlas grid on the timeline.
- **`backend: "dom"` for every v1 effect** in the original plan, escalating
  only when a storyboard genuinely demanded it. That default flipped after
  the M1 operator batch review: pills and the picker passed, all three
  ceremonies failed the bar — the DOM backend hit its ceiling. Per the
  spec's own escalation path, every ceremony now targets `backend: "webgl"`;
  the DOM-backend rules above stay accurate for the pill/hover material and
  for any future effect where a storyboard doesn't need per-frame physics.

## OGL backend (webgl)

Built as its own goal (target repo's G8) once M1's DOM backend hit its
ceiling. Two new files own it: `src/lib/super-reactions/webgl.ts` (the
renderer/canvas/bloom pipeline) and `CeremonyContext.gl` (harness.ts wires
it in). Read `webgl.ts` directly before writing a webgl-backend effect —
this section documents the landed contract, not a guarantee of exact
current line numbers.

- **`bun add ogl`, pinned in `package.json` and `tools/parity-manifest.json`
  dependencies** — same mechanism as animejs. Lands ONLY in the lazy
  `super-reactions` chunk; verify a build the same way as animejs
  (`grep -c "createTimeline" dist/assets/rooms.js` for animejs,
  `grep -c "WEBGL_lose_context"` or any OGL/GLSL-specific string for OGL —
  both must be `0`).
- **One shared OGL `Renderer`/canvas, acquired and released, never
  constructed per-effect.** `webgl.ts` exports `acquireGlLayer(bloomKnobs)`
  (called by the harness right before a webgl effect's `ceremony()`/`calm()`)
  and `releaseGlLayer()` (called at ceremony teardown, alongside the DOM
  stage's own removal). The canvas itself is a persistent element appended
  to `document.body` once, NOT parented inside the per-ceremony `stage` div
  (that div is destroyed every fire; the canvas must outlive it to be
  reusable). Idle-disposed (GL context genuinely released via
  `WEBGL_lose_context`) after a silence timeout, not on every teardown —
  reuse across ceremonies fired back to back is the point.
- **Additive light via `mix-blend-mode: plus-lighter` on the CANVAS
  element itself**, not per-object alpha compositing in GLSL. The renderer
  is opaque (`alpha: false`), cleared to black every frame; black contributes
  nothing under additive blending, so the "empty" canvas reads as fully
  transparent over the DOM behind it. This sidesteps WebGL premultiplied-
  alpha compositing entirely and is the same technique every DOM-backend
  glow layer already uses — one additive idiom for both backends.
  `preserveDrawingBuffer: true` is required on the Renderer for Playwright
  screenshots to capture GL content reliably; verified empirically (a
  fixture capture of a throwaway proof effect showed real rendered pixels,
  not a blank frame — don't assume, test it for any new webgl effect too).
- **DPR capped at 2.** `Math.min(window.devicePixelRatio || 1, 2)`.
- **`webglcontextlost` is NOT automatic (OGL's own TODO on Renderer.js) —
  handle it yourself.** Listen on the canvas, `event.preventDefault()`, then
  tear the shared state down to nothing (don't attempt in-place restoration)
  — the next fire's `acquireGlLayer()` rebuilds fresh.
- **In-house bloom: threshold -> separable Gaussian ping-pong at half
  resolution -> additive composite.** No post-processing library (OGL's own
  `Post` extra assumes uniform resolution through its whole pass chain,
  which doesn't fit a half-res blur step cleanly) — `webgl.ts`'s
  `BloomPipeline` hand-rolls four `RenderTarget`s (full-res scene, half-res
  bright-pass, two half-res blur ping-pong) and three fullscreen-triangle
  shader passes.
- **`bloom: { threshold, strength, radius }` is REQUIRED on a
  `"webgl"`-backend effect, enforced at `registerEffect()` time
  (registry.ts), not just by the type.** An untuned shared bloom preset
  across every webgl effect is a blacklist item — each effect tunes its own
  three knobs; the pipeline's render targets are never rebuilt for a knob
  change, only the uniform values swap in.
- **anime.js stays the conductor for webgl too — no separate rAF loop.**
  An effect adds a driver tween to `ctx.timeline` (autoplay in live mode,
  seek()-driven in deterministic mode, identical to the DOM backend's own
  per-frame sprite steppers like close-encounter's `driveSaucerSpecular`)
  whose `onUpdate` sets uniforms/attributes for the current progress and
  calls `ctx.gl.render()`. `timeline.seek(ms)` fires `onUpdate` synchronously
  — this is what makes `runCeremonyDeterministic` work unchanged for a
  webgl effect: same seed in, same rendered pixels out, verified
  byte-identical across two independent capture runs of a throwaway proof
  effect.
- **Seeded RNG for every particle attribute, computed once at build time,
  never re-rolled per frame.** Call `ctx.rng()` for each particle's
  angle/speed/size/etc. when the effect's `ceremony()`/`calm()` builds its
  `Geometry`, upload as vertex attributes, then compute each particle's
  actual position/size/alpha as a pure function of those attributes and the
  driver's `uProgress` uniform in the vertex shader — never simulate
  iteratively frame-to-frame (that would make determinism dependent on
  having stepped every intermediate frame, not just seek()'d to one).
- **Meshes belong to `ctx.gl.scene` (a `Transform`), added via
  `mesh.setParent(ctx.gl.scene)`.** The harness clears every child (and
  disposes its geometry/program GPU buffers via their own `.remove()`
  methods) both defensively on acquire and normally on release — an effect
  never has to clean up its own meshes.
- **`≤120` DOM garnish node budget doesn't apply here** (a webgl effect's
  garnish lives in GPU buffers, not the DOM) — but keep particle counts and
  draw calls sane for the same reason the DOM budget exists: a ceremony is a
  celebratory beat, not a stress test. No pinned numeric budget yet; if G9's
  per-effect direction needs one, it belongs in `rubric.md`'s Performance
  axis, not here.

## Claude Design generator flow (generator, never driver)

A dedicated claude.ai/design project, "OM Super Reactions," is the working
surface for pipeline stages 2 (color script) and 3 (storyboard), synced via
DesignSync (`list` → `finalize_plan` → `write`). Guardrails, followed in
spirit on every use:

- **Every generation prompt carries the tuple, the motion bible's rules, and
  the anti-pattern blacklist.** There is no unconstrained "make something
  cool" generation path — a prompt missing the tuple or the constraints is
  malformed, not a shortcut.
- **Cards advance only by passing the framework's gates**, never by being
  liked. The color-script gate (palette rules alone) and the storyboard cull
  (the operator's stage-3 pick) are the only ways a candidate moves forward.
- **The design project is disposable working state.** The repo's registry
  entry and `super-reactions-spec.md` are the source of truth. Delete a
  rejected candidate's cards rather than archiving them — nothing there
  needs to survive past sign-off.
- **Never paste repo source into the design project.** This repo's source is
  proprietary (see the target repo's `AGENTS.md`). Build cards from specs —
  palettes, frames, storyboard text — only, never from `.ts`/`.tsx` file
  contents.
- **Frame-by-frame motion tuning happens in the repo fixture, not the design
  project.** The design project produces static color-script and storyboard
  artifacts; once implementation starts (stage 4), iteration moves to the
  self-grade loop against live fixture captures.
