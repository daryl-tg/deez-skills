from pathlib import Path

from deezlib import frontmatter, registry

MARKER = "<!-- deez:index -->"


def _description(entry, repo_root):
    folder = Path(repo_root) / registry.source_dir(entry, entry.runtimes[0])
    try:
        return frontmatter.parse(folder / "SKILL.md")["description"]
    except frontmatter.FrontmatterError:
        return "—"


_LAYER_MARK = {
    "mode": "router",
    "principle": "principle",
    "playbook-host": "playbooks",
    "workflow": "",
}


def _row(entry, repo_root):
    runtimes = ", ".join(entry.runtimes)
    description = _description(entry, repo_root).replace("|", "\\|")
    if len(description) > 160:
        description = description[:159] + "…"
    layer = _LAYER_MARK.get(entry.layer, entry.layer)
    return f"| `{entry.name}` | {layer} | {runtimes} | {description} |"


def render(reg, repo_root):
    lines = [MARKER, "", "## Everything in the hub", ""]
    if not reg.entries:
        lines += [
            "No entries yet. The framework is in place; migration adds them.",
            "",
        ]
        return "\n".join(lines)

    by_category = {}
    for entry in reg.entries:
        by_category.setdefault(entry.category, []).append(entry)

    for category in sorted(by_category):
        lines.append(f"### {reg.categories[category]}")
        lines.append("")
        lines.append("| Name | Layer | Runtimes | Description |")
        lines.append("| --- | --- | --- | --- |")
        for entry in sorted(by_category[category], key=lambda e: e.name):
            lines.append(_row(entry, repo_root))
        lines.append("")
    return "\n".join(lines)


def _head(readme_path):
    text = Path(readme_path).read_text(encoding="utf-8")
    head, _, _ = text.partition(MARKER)
    return head


def write(reg, repo_root, readme_path):
    readme_path = Path(readme_path)
    updated = _head(readme_path) + render(reg, repo_root) + "\n"
    if readme_path.read_text(encoding="utf-8") == updated:
        return False
    readme_path.write_text(updated, encoding="utf-8")
    return True


def is_stale(reg, repo_root, readme_path):
    readme_path = Path(readme_path)
    expected = _head(readme_path) + render(reg, repo_root) + "\n"
    return readme_path.read_text(encoding="utf-8") != expected
