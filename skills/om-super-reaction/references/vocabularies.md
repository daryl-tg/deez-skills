# Tuple Vocabularies

Every super reaction concept starts from a constraint tuple committed BEFORE
any generation happens:

> **(material) × (motion character) × (shape verb)**

This is the single biggest anti-slop lever: an agent translating a specific,
concrete combination instead of "make a cool celebration" cannot converge on
the statistically-average output a default prompt produces. Never generate a
color script or storyboard without a committed tuple.

Each vocabulary entry below carries an extracted rule: a checkable behavior
the effect must honor to actually read as that material, motion character, or
shape, rather than as a generic burst wearing its label. Grade candidates
against these rules the same way you grade against `motion-bible.md`.

## Materials

| Material | Extracted rule |
|---|---|
| Gold leaf | Catches light at an angle; never glows uniformly. Expect anisotropic specular flecks that flash and die as the implied light angle sweeps past them, not a steady glow. |
| Holographic foil | Hue shifts with viewing angle or motion, as a coordinated sweep tied to rotation/parallax — never per-pixel rainbow noise (that's the banned anti-pattern, not this material). |
| Enamel pin | Hard-edged, flat color fields separated by a metal gutter line. No gradient inside a field. The "shine" is one specular pass across the surface, not a glow. |
| Stained glass | Reads by transmission, not reflection — light passes through it. Leaded seams are the primary silhouette; a backlit glow, not a surface sheen. |
| Ferrofluid | Spikes form and collapse along an implied magnetic field. Motion is viscous, never bouncy. Silhouette is one dark mass with sharp peaks, not scattered droplets. |
| Ember | A heat-based value ramp (dark red → orange → pale yellow at the hottest point), not a hue-based one. Edges cool and grey as they die. Embers pulse from an internal light source, never an external one. |
| Paper confetti | Irregular tumble with air-resistance flutter — rotation decorrelated from translation, not an orbital arc. Each piece keeps a flat matte fill; no gradient. |
| Mercury glass | A mirrored surface with a soft antique haze; reflections are distorted, never crisp. One dominant cool-silver value range, not multiple hues. |
| Neon tube | A constant-width glowing line: one saturated hue with a desaturated outer halo. Any flicker is a deliberate two-state cycle, never random noise. |
| Ink in water | A diffusion silhouette — edges soften and bloom outward over time, never a hard boundary. Motion accelerates then decelerates as it disperses; never a constant velocity. |
| Retro chrome | A hard mirrored value range in cool grey-silver; the specular is one sliding highlight band across the surface. Any color comes from a single external accent light (a beam, a glow), never from the chrome itself. |
| Hologram | Reads by emission with visible scanline banding; the image is translucent. Flicker happens only as deliberate authored jumps; chromatic-split fringes appear only during displacement, never at rest. |

## Motion characters

| Motion character | Extracted rule |
|---|---|
| Bioluminescent pulse | A slow build, sourced glow that breathes — eases in and out, never a hard flash. Amplitude decays geometrically across repeats. |
| Aurora drift | Continuous, non-repeating drift along a loose sine-like path. Color desaturates toward the edges of the drift. Never snaps to a stop. |
| Arena flash-and-roar | Anticipation is compressed into a single sharp beat (never zero — rule 1 of the structural rules still applies), then an overdriven peak flash, then a long roaring decay tail. |
| Hanabi contemplative bloom | One unhurried upward launch; a bloom that opens once and lingers, with a willow-style trailing decay. The "one primary element" rule is most load-bearing here — resist adding a second burst. |
| Confetti-cannon chaos | Many small independent elements launched from one point, but hierarchy still holds through one larger or brighter hero piece among them. Stagger is what keeps this from reading as simultaneous noise. |
| Magnetic snap | Elements approach along curved, not straight, paths and snap into a settled arrangement with a small overshoot-and-correct. The "snap" beat is the peak, not the anticipation. |
| Liquid settle | Motion decelerates through viscosity, not a spring bounce. The settle phase dominates the timing budget — a short peak, a long settle — with a brief surface wobble before stilling. |
| Dogfight strafe | Elements cross the frame on opposed curved flight paths with banked rotation; exchanges are short authored beats, never continuous fire. Hierarchy holds through one hero craft — everything else reads as escort. |
| Glitch stutter | Displacement happens in exactly 2–3 authored jumps (position/slice offsets with chromatic split), each landing back at rest. Never continuous random jitter — that is the noise anti-pattern, not this character. |

## Shape verbs

Sourced from the fireworks-shell taxonomy (named silhouettes, not just
particle counts).

| Shape verb | Extracted rule |
|---|---|
| Peony | A clean expanding sphere, no trails. Reads as a single dot that becomes a disc. |
| Chrysanthemum | A sphere with trailing sparks on each spoke. Trails must decay during the settle phase, never persist statically. |
| Willow | A cascading weep — spokes arc downward under an implied gravity and taper as they fall. The settle phase IS the willow's fall, not an afterthought tacked onto it. |
| Palm / diadem | A small number of thick comet tendrils rise and arc, each individually readable. Fewer, bigger elements than chrysanthemum, to keep hierarchy legible. |
| Ring | Expands as a flattened torus/halo silhouette, not a sphere. Must read instantly as a ring under the one-clause silhouette test, never as a blob. |
| Fountain | A sustained upward source with continuous fall-back; asymmetric timing, with a longer sustain than a burst shape needs. The least burst-like verb — closest in feel to the liquid-settle motion character. |
| Crown | Radiating spokes that stay attached to a shared base or anchor point (the pill, or the message row). Never fully detaches — it is visually worn by its anchor. |
| Spiral | A rotating expansion where angular velocity and radius both change over the timeline — a true spiral, not a rotating ring. Must decelerate its rotation into the settle phase or it reads as spinning forever. |
| Beam | A vertical cone or column locked to its anchor from above; reads instantly as a spotlight. Soft edges, and the footprint matches the anchor's width — a beam that outgrows its anchor reads as a wash, not a beam. |
| Scan | A single sweep line crosses the anchor once per beat, revealing or altering what it passes. The sweep has one direction and never ping-pongs more than once. |

## Mining sessions: how the vocabulary grows

New vocabulary entries come from a deliberate mining session, never from
inventing a material or motion character ad hoc while designing an effect.
Procedure:

1. **Collect inspiration sources**, not effect ideas. In scope: games (Riot
   VFX guide, gacha summon animations, fighting-game supers, Balatro's foil
   treatment, Hollow Knight, Persona 5), physical materials and phenomena,
   and craft showcases (motion-design reels, VFX breakdowns) — mined for
   *technique*, not copied wholesale. Competitor chat products (Discord,
   Telegram, Slack, iMessage) are in scope only as the floor to beat, never
   as inspiration to imitate.
2. **Extract a rule, not a description.** For each source, write the same
   shape of entry as the tables above: a material, motion character, or
   shape verb, plus one checkable behavioral rule an agent can grade a
   candidate against. "Looks cool" is not a rule; "catches light at an angle,
   never glows uniformly" is.
3. **Add the entry to this file** (the correct table above) before it is
   used in a tuple. A mining session produces vocabulary; it does not skip
   straight to a color script or storyboard for a specific effect.
4. **Never mine competitor chat products for concepts.** They set the bar to
   clear, not a well to draw from — this is the same distinction as the
   overall motion bible's stance against untuned library defaults: cliché in
   equals cliché out.

## The inspiration inbox

The operator drops raw links (game clips, material photos, VFX breakdowns,
whatever prompted the idea) into
`~/Documents/dev-notes/om-chat-super-reactions/inspiration-inbox.md` between
mining sessions. Before stage 1 (Tuple) of the pipeline, check this file for
unprocessed entries — run a mining session over them per the procedure above,
adding new vocabulary entries here, before picking a tuple. Mark processed
entries in the inbox file so a later session doesn't re-mine them (the exact
marking convention is whatever that file already uses; match it, don't
reinvent it if entries already exist).
