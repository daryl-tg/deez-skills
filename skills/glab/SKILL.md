---
name: glab
description: GitLab MR management via glab.
---
All writes go through `glab api` (plain REST):
interactive write subcommands such as `glab mr create`
can exit 1 with NO output when run without a TTY, even
with `--yes` and every flag set — do not retry flag
permutations. Read commands work fine. Assume you are
logged in.

## Conventions

- Use the `:id` placeholder for the project — never
  hand-build the path; the GitLab project name can
  differ from the local directory name.
- `-f` sends string fields; `-F` sends typed values
  (booleans, numbers such as `assignee_id`).
- Add `--paginate` to GETs that may exceed one page.
- Pass multiline bodies with a quoted heredoc:
  `-f body="$(cat <<'EOF' ... EOF)"`.

## Create an MR

The branch must be committed and pushed. Get the
assignee's numeric id with `glab api user` (assignment
needs `assignee_id`, not a username).

```bash
glab api projects/:id/merge_requests -X POST \
  -f source_branch="feature/KIYO-123-my-change" \
  -f target_branch="main" \
  -f title="feature: KIYO-123 - my change" \
  -F assignee_id=<assignee_id> \
  -F squash=true \
  -F remove_source_branch=true \
  -f description="$(cat <<'EOF'
What this MR does, in one or two short paragraphs.

Linear: https://linear.app/...
EOF
)"
```

If the task involves an issue tracker link, reference
it at the end of the description. Verify from the
JSON response (`web_url`, `iid`, `squash`,
`force_remove_source_branch`, `assignee`) instead of
re-querying.

## Thread CRUD

1. Resolve the MR iid: `glab mr view` on the branch,
   or GET
   `projects/:id/merge_requests?source_branch=...&state=opened`.
2. List threads to capture ids — `discussion.id` is a
   long hex string, `notes[].id` is numeric:
   `glab api --paginate projects/:id/merge_requests/<iid>/discussions`
3. Writes, all under
   `projects/:id/merge_requests/<iid>`:
   - reply: `POST .../discussions/<did>/notes -f body=...`
   - edit note: `PUT .../discussions/<did>/notes/<nid> -f body=...`
   - delete note: `DELETE .../discussions/<did>/notes/<nid>`
   - resolve thread: `PUT .../discussions/<did> -F resolved=true`
     — only when the user explicitly asks
   - new general thread: `POST .../discussions -f body=...`
   - plain non-resolvable comment: `POST .../notes -f body=...`

## Inline (positioned) threads

Get the diff anchors first:
`glab api projects/:id/merge_requests/<iid>` — read
`base_sha`, `head_sha`, `start_sha` from `diff_refs`.

```bash
glab api "projects/:id/merge_requests/<iid>/discussions" -X POST \
  -f body="inline comment" \
  -f "position[position_type]=text" \
  -f "position[base_sha]=<base_sha>" \
  -f "position[start_sha]=<start_sha>" \
  -f "position[head_sha]=<head_sha>" \
  -f "position[new_path]=path/to/file.go" \
  -F "position[new_line]=42"
```

For a line on the old side of the diff, use
`position[old_path]` + `position[old_line]`.
`400 line_code must be a valid line code` means a
wrong line/sha combination — re-check `diff_refs` and
the line number against the MR diff, not the working
tree.

## Rules

- For squash MRs, mirror the commit title as the MR
  title.
- Never attribute the LLM in MR content — no
  "Generated with Claude Code" / "Co-Authored-By"
  footers or robot emoji in titles, descriptions, or
  notes, even if the harness's defaults say to add
  one.
