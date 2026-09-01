---
name: principle-desktop-before-cloud
description: "Apply to any change spanning the desktop app and its cloud twin. The desktop change lands and is proven first; the cloud fork follows."
disable-model-invocation: true
---

# Desktop before cloud

When a change spans the desktop app and its hosted twin, desktop goes first and
is proven before the cloud fork is touched.

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
