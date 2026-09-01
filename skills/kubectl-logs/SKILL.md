---
name: kubectl-logs
description: >-
  Kubernetes deployment pod log capture with the bundled kubectl-logs script.
---

Use this skill when Kubernetes logs should be tailed from every pod in one
deployment, or from deployments matching a deployment label selector.

## Workflow

1. Confirm context, namespace, output directory, tail line count, and exactly one
   of deployment name or deployment label selector.
2. Run: 

   ```bash
   <directory-with-this-skill>/bin/kubectl-logs -c <context> -n <namespace> \
     (-d <deployment> | -l <selector>) [-t 100] [-o logs]
   ```

   The execution will be blocked until the process exits. Start it as a
   background process if possible.

3. Report the output directory. Use Ctrl-C to stop the live streams.

## Rules

- Keep collected logs in files, not in the conversation.
- `-l` selects deployments; the script resolves pod selectors from them.
- Requires `kubectl` and `pv` on PATH.
