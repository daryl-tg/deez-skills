---
name: port-designer-ui
description: Use when porting a component, dialog, page, landing-page redesign, or other visual treatment from Kiyotaka_Mar25_V9 into a Kiyotaka Vue repository, especially for requests such as “match the new design,” “port the designer version,” or “bring over this UI.”
---

# Port Designer UI

Port the approved visual design into the existing target implementation. Treat the work as a restyle, not a rebuild.

## Local paths

- `DESIGNER_REPO=/Users/dboon/Github/Kiyotaka-v4-revamp/Kiyotaka_Mar25_V9`
- `NOTES_DIR=/Users/dboon/Documents/dev-notes`
- `TARGET_REPO` is the current repository unless the user names another one.
- Store durable artifacts in `NOTES_DIR/port-<component-or-page>/`, never inside either repository.

If a path is missing, search common development roots before asking the user.

## Non-negotiable boundaries

1. **UI only by default.** Change styling, layout, colors, typography, spacing, imagery, and icons.
2. Preserve existing target behavior: props, emits, stores, composables, handlers, data sources, routes, links, analytics, SEO metadata, accessibility semantics, and triggers.
3. A new/removed control, route, state transition, data field, component entry point, or interaction sequence is a **flow change**. List it and require an explicit keep/drop decision. Drop it by default.
4. Restyle existing target components. If no target counterpart exists, treat creation as a structural change and obtain explicit scope approval before implementation.
5. Do not add dependencies, commits, or unrelated cleanup unless explicitly requested.
6. Do not skip or reorder the pipeline below.

## Required tools

Use browser automation for live capture and verification. Load the appropriate available browser skill/tool (in-app Browser, Chrome DevTools, or the repository's headless probe). Code inspection alone is not a substitute for exercising the live UI.

For Vue targets, load and follow the `vue-best-practices` skill before editing.

## Pipeline

### 1. Locate

1. In `DESIGNER_REPO`, run `git log --oneline -30` first. Commit subjects often identify the current variant.
2. Search `src/components/` and inspect the app entry/router to identify the variant actually rendered. Do not assume the highest `V2`/`V3`/`V4` suffix is current. Ignore duplicate files such as `* 2.tsx` and archives.
3. Find the exact route or UI action that mounts the designer component/page.
4. Locate the existing target `.vue`, page, layout, styles, and assets in `TARGET_REPO`.
5. If still ambiguous, present the leading candidates with commit and render-path evidence. Never guess silently.

### 2. Capture the live designer UI

1. Start the designer dev server in the background from `DESIGNER_REPO`; record its PID, port, and log path.
2. Drive the live UI through every applicable state: clicks, hover, focus, keyboard, open/close transitions, selected states, empty/loading/error states, drag behavior, and motion.
3. For page/landing work, capture the supported desktop and mobile layouts and any meaningful intermediate breakpoint.
4. Record a flow inventory in `NOTES_DIR/port-<component-or-page>/flow-inventory.md` containing:
   - each visible element and state;
   - responsive behavior;
   - required assets and fonts;
   - pure visual differences;
   - flow/structural differences requiring keep/drop decisions.
5. Save reference screenshots only in the notes directory. Temporary screenshots belong in the session scratch directory.

### 3. Validation gate — stop before implementation

1. Show the exact designer states, not merely the app root. Use the available image-viewing surface and optionally provide the live designer URL.
2. Present the flow inventory, visual-change list, and flow-change decisions.
3. Ask for an explicit verdict that the selected source and captured states are correct.
4. If the user corrects anything, return to Locate or Capture.
5. Do not edit the target until the user explicitly approves the reference. Record each approved flow change.

### 4. Implement the approved port

Write `implementation-brief.md` in the port notes directory with:

- absolute source and target paths;
- approved inventory and decisions;
- reference screenshot paths;
- responsive states;
- target-specific translation contract;
- verification commands.

Then implement directly in the target repository, following its `AGENTS.md` and git workflow.

#### Shared translation contract

- Translate React/JSX patterns into idiomatic Vue SFCs without copying source behavior blindly.
- Reuse target components, icons, fonts, assets, utilities, and design tokens before adding anything.
- Keep script/business-logic edits at zero unless an approved flow change strictly requires them.
- Preserve target accessibility and semantic structure; visual fidelity does not justify removing labels, focus behavior, or keyboard access.
- Match source responsive behavior with the smallest target-native diff.

#### `kiyotaka-landing-page-v2` contract

- Use Nuxt 4, Vue 3 Composition API, and `<script setup>` conventions.
- Prefer existing Tailwind CSS 4, Quasar, and nearby CSS/component patterns; do not introduce a parallel styling system.
- Reuse existing landing components and styles under `app/components/landing/` and `app/assets/styles/` when they are the active implementation.
- Preserve routes, runtime configuration, outbound links, analytics, and SEO behavior.
- Use `@nuxt/content` for documentation/guide copy when the target content already belongs there; do not move landing-page copy into content files without a repository precedent.

#### `kiyotaka-frontend` contract

- Translate JSX + Tailwind into Vue SFC template + scoped SCSS using existing project conventions.
- Map colors to project tokens declared for both light and dark themes; do not add raw hex/rgb/hsl values where tokens are required.
- For scoped dark-mode CSS, wrap the full selector with `:global(body.body--dark ...)` according to the target convention.
- Put new user-facing strings in the existing i18n system and update all required locales (`en`, `cn`, `ja`, `ko`, `ru`, `hi`).

### 5. Verify and clean up

1. Review the diff. Any unapproved change to behavior, data, routing, stores, handlers, or dependencies is a finding and must be reverted or approved.
2. Run targeted tests first, then the target repository's lint/typecheck/build/static checks as applicable.
3. Start the target app and capture side-by-side designer/target screenshots for every inventoried state and responsive layout.
4. Verify light and dark mode when the target supports both.
5. Show the comparison to the user and obtain visual sign-off. Iterate on mismatches rather than declaring approximate success.
6. Stop the designer and target dev servers started for this port. Confirm their ports have no remaining listener.
7. Delete scratch screenshots. Keep only inventory-cited reference images in the notes directory.
8. Run `git status --porcelain` in both repositories and confirm no screenshots, logs, or port artifacts leaked into either repo.

## Screenshot hygiene

Screenshots may exist only in the disposable session scratch directory or `NOTES_DIR/port-<component-or-page>/`. Never write screenshots, browser downloads, or comparison artifacts under a git repository.

## Stop conditions

The port is complete only when the approved inventory is implemented, behavior remains intact except for explicitly approved flow changes, validation checks pass or gaps are stated, visual comparisons are signed off, servers are stopped, and both repositories are artifact-clean.
