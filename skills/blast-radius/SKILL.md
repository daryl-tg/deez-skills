---
name: blast-radius
description: "Find what a small-looking change could break beyond its diff, proving each safety claim with running code rather than assertion. Use before shipping a change that touches shared code."
disable-model-invocation: true
---

# Blast radius

A change is only as small as its reach. This finds what else it touches, and
**proves** each "that is fine" rather than asserting it.

1. **Enumerate the callers.** Every use of the symbol, route, config key, event
   name, or column touched. Search by name, then by string, then by the shapes
   that would not match either. Route the sweep to the **explore** role.
2. **Cross the boundaries the diff does not show.** Shared packages and their
   consumers. Persisted data written by the old shape and read by the new.
   Serialized messages in flight. Cached values. Anything derived from a schema
   the change alters.
3. **Rank by blast radius, not by proximity.** A distant caller in a path that
   handles money or auth outranks a nearby one in a debug helper.
4. **Prove the safety claims.** For each "this one is fine", say how you know,
   and make it runnable: a test that fails without the change, a script that
   greps the real data, an exercised path. **A claim proven by reasoning is
   unproven.** This is where the principle **principle-build-the-lever** applies — the
   proof should be a thing a reviewer reruns.
5. **Name what you could not prove.** An honest unproven item is worth more than
   a confident wrong one.

**Reply:** the reach, ranked; the proof for each safe claim; the unproven
remainder stated plainly.
