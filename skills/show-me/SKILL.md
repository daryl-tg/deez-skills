---
name: show-me
description: "Explain the current topic visually, picking the smallest view that makes the point: pseudocode, a call tree, a component or file tree, a Mermaid diagram, a shaped diff, or one focused HTML page. Use for 'show me', 'draw this', 'what does this look like'. Not the decision trail, which is show-me-your-work."
---

Help the user understand the current topic of conversation visually. Skip the preamble and keep prose brief. Pick the smallest view that makes the key point clear.

- Show logic or an algorithm as pseudocode:

```text
on(save)
  if content is unchanged
    return cached result
  write new content
  return fresh result
```

- Show runtime control flow as a call tree:

```text
submitForm
  createSession
    persistPrompt
    launchAgent
  navigateToSession
```

- Show UI structure as a component tree, including state and module boundaries that matter:

```tsx
<SessionPage> (apps/example/src/routes/session.tsx)
  useSessionEvents()
  <SessionToolbar>
    <RunSkillButton> (packages/ui)
```

- Show file responsibility or a broad refactor as a shallow file tree:

```text
src/
├── commands/       # parses user actions
├── sessions/       # owns session state
└── transport/      # sends API requests
```

- Show component interaction, control flow, or data flow with Mermaid:

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant Daemon
    User->>UI: choose command
    UI->>Daemon: send expanded prompt
    Daemon-->>UI: stream result
```

- Use `diff` when the point is what changes and the surrounding shape already exists. Match the diff shape to the topic.

For a component change:

```diff
 <SessionPage>
   useSessionEvents()
   <SessionToolbar>
+    <RunSkillButton />
   <SessionTimeline>
+    <SkillResultCard />
```

For a file-layout change:

```diff
 src/
 ├── commands/
+│   └── show-me.ts       # expands the slash command
 ├── sessions/
-└── transport.ts
+└── transport/
+    ├── client.ts
+    └── stream.ts
```

For a call-tree or call-stack change:

```diff
 submitForm
   createSession
     persistPrompt
+    expandSkillMention
     launchAgent
-  navigateToSession
+  navigateToSession
+    subscribeToEvents
```

For a state or control-flow change:

```diff
 on(save)
-  write content
+  if content is unchanged
+    return cached result
+  write new content
+  invalidate cache
```

- Show the whole block when most of it is new, when omitted context would hide ownership or order, or when the user needs a copyable target shape:

```ts
function expandSkill(command: string): string {
  const skillName = command.slice(1)
  return `use the ${skillName} skill`
}
```

- For a visual UI, layout, state comparison, or concept too dense for Mermaid,
  write one focused HTML page. A diagram, an infographic, or a short slide deck,
  whichever fits the point. Match the product's colors, type, spacing, and
  components, use real labels and data, and make it read on both desktop and
  mobile. **om-chat-design-system** holds those tokens for OM Chat work.

  Then get it in front of the operator. Never run `open`. The browser it opens
  is on the mini and the operator is on the MacBook, so that command shows the
  page to nobody. On Claude, publish it as an Artifact and hand back the link.
  On Codex, serve it from an assigned port in the `18097`-`18197` band and say
  which `-L` line the operator needs, per **principle-bind-assigned-ports**.
  When the sketch is evidence for a review rather than an explanation, it
  belongs in that run's evidence gallery instead.

### guidance

**teach** owns the pacing, which is one diagram at a time, each adding a part.
This skill owns the form, which is which representation answers the question.
Reach for both together and neither restates the other.

Place each visual next to the short text it supports. Keep only the calls, files, props, states, and boundaries needed to answer the user's current question or the options to resolve the current discussion point.

You may use one of these, you may use several, it is unlikely you will use all of them. Use your judgement and don't overwhelm the user.
