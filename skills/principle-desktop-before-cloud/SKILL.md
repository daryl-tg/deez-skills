---
name: principle-desktop-before-cloud
description: "Apply only when the operator asks for a change in both the desktop app and its cloud twin. Cloud parity is retired, so a desktop change no longer implies a cloud one; when both are asked for, desktop lands and is proven first."
disable-model-invocation: true
---

# Desktop before cloud

**Cloud parity is retired.** A desktop change is complete without a cloud port.
Do not open one, do not gate delivery on one, and do not report the twin lagging
as unfinished work. This principle applies only when the operator asks for the
cloud change by name.

When they do, desktop goes first and is proven before the cloud fork is touched.

**Why:** the two share a lineage but not a deployment. Doing them together means
a defect found later has two candidate sources and no known-good side. Doing
desktop first gives the cloud change a proven reference.

**The rule.**

- Land and prove desktop. Proof means the real surface, per
  **principle-prove-on-the-real-surface**, not that the code compiles in both.
- Only then port to cloud, and prove it separately on its own surface. A desktop
  screenshot is not evidence for cloud.
- Shared-primitive changes propagate to every consumer, and each consumer is
  verified. A fix ported to one and assumed for the rest is untested twice.
- Never a single review request spanning both when the surfaces are proven
  separately. Each side carries its own evidence.
