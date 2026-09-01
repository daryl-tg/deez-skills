---
name: om-chat-design-system
description: "Design and implement OM Chat React UI against the local components, tokens, layout, and interaction patterns. Load before any user-visible OM Chat UI decision: features, fixes, modals, panels, responsive and a11y work."
---

# OM Chat design system

Treat the existing OM Chat product as the design system. Make a new interface
feel inevitable beside its nearest established peer; do not invent a parallel
visual language for a routine product change.

This is a companion to `$om-chat-feature`, not a delivery workflow. Load it
before designing or implementing a user-visible OM Chat change, then return to
the feature workflow for testing, review, and delivery.

## Before writing React

This skill owns what OM Chat's UI should look like: its components, tokens,
layout, and interaction patterns. It does not own how React should be written.

- **Performance and structure** come from **vercel-react-best-practices**. Read
  it before any non-trivial component or data-fetching change, and follow its
  ordering: waterfalls and bundle size are critical, re-render tuning is medium.
  Reaching for `memo` before checking for a waterfall optimises the wrong thing.
- **Motion** comes from **animate**, held to the bar in **emil-design-eng**.
  Anything gesture-driven or material-like also reads **apple-design**.
- **The data shape comes first**, per **principle-model-the-domain**. A
  component tuned for re-renders around the wrong shape is still wrong.

Local patterns in this skill win over general guidance where they conflict: the
design system is the constraint, the vendored skills are the craft.

## Discover before coding

1. Read repository instructions, the affected route, and the closest existing
   components in the same surface.
2. Identify the owning layout, shared primitive, icon source, CSS token source,
   and visual test or fixture. Reuse them before creating an alternative.
3. Write a compact internal UI contract: user job, primary action, information
   hierarchy, reference peers, required states, responsive behavior, and any
   intentional exception to the existing pattern.

Use the real product content and state shape. Do not design around placeholder
copy, fabricated metrics, decorative labels, or a screenshot-sized happy path.

## Build with the product grammar

Use existing spacing, color, typography, radius, elevation, motion, and focus
tokens. Align new content to its parent grid and neighboring components. Match
the established density, control sizing, padding, truncation, and empty-state
language for that surface. Do not introduce one-off hex values, type scales,
radii, shadows, animations, or breakpoints without an explicit design-system
reason.

Prefer an existing component or local extension over a look-alike. Extract a
new shared primitive only when repeated use or a real semantic boundary makes it
more coherent. Use Lucide icons when available; otherwise extend the local
currentColor SVG grammar. Do not use emoji or text characters as replacement UI
icons.

Every control must communicate its action and state. Give icon-only controls an
accessible name, keep keyboard focus visible, preserve touch targets, and make
disabled, pending, error, empty, and success states actionable and specific.
Treat narrow layouts, long labels, localization expansion, overflow, and reduced
motion as normal product states rather than edge cases.

## Review the experience, not only the DOM

Before visual approval, compare the assembled candidate with its reference peer
at each affected viewport. Verify hierarchy, alignment, whitespace, scannability,
contrast, control affordance, focus order, and recovery paths. Exercise the
complete changed journey with the final data/state, including relevant loading,
empty, error, hover, focus, and modal states.

Use `$agent-browser` for the final interactive smoke and screenshots. A visual
check passes only when the controls are visible, enabled when appropriate,
on-screen, unobscured, keyboard-reachable, and produce their expected outcome.
Inspect console errors, failed requests, and relevant accessibility findings.
Repair material differences before requesting visual approval.

## New visual directions

When the user explicitly asks for a new standalone surface or visual direction,
apply the useful discipline from Anthropic's frontend-design guidance: state the
audience and page job, choose a clear hierarchy and one restrained focal point,
then critique the result for generic decoration. Still preserve OM Chat's
component, token, accessibility, and interaction contracts unless the request
explicitly changes the design system itself.
