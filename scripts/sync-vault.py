"""
Sync the AI Security repo READMEs into an Obsidian vault.

Reads each category README.md, extracts sections and links,
and writes corresponding Obsidian notes with frontmatter and wiki-links.

Usage: python3 scripts/sync-vault.py
"""

import json
import re
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VAULT_DIR = REPO_ROOT / "vault"

# Top-level groups and their display names
GROUPS = {
    "foundations": "Foundations",
    "attacks": "Attacks",
    "defense": "Defense",
    "agents": "Agents",
    "coding": "Coding",
    "research": "Research",
    "practice": "Practice",
    "general": "General",
}

# Known cross-references: note name -> list of related note names
CROSS_LINKS = {
    "Guardrails and Firewalls": ["Prompt Injection", "Jailbreaking"],
    "Prompt Injection": ["Guardrails and Firewalls", "Secure Coding"],
    "Jailbreaking": ["Prompt Injection", "Red Teaming"],
    "Agent Security": ["Agent Identity", "MCP"],
    "Agent Identity": ["Agent Security", "MCP", "Secrets Management"],
    "MCP": ["Agent Security", "Agent Identity"],
    "Sandboxing and Isolation": ["Coding Tools"],
    "Secrets Management": ["Agent Identity", "Secure Coding"],
    "Red Teaming": ["Jailbreaking", "Prompt Injection"],
    "Secure Coding": ["Code Analysis", "Coding Tools"],
    "Code Analysis": ["Secure Coding", "Detection and Monitoring"],
    "Detection and Monitoring": ["Code Analysis", "Guardrails and Firewalls"],
    "Model Attacks": ["Supply Chain", "Safety and Alignment"],
    "Supply Chain": ["Model Attacks"],
    "Safety and Alignment": ["Model Attacks", "Agent Security"],
    "Incidents": ["Prompt Injection", "Agent Security", "MCP"],
    "Frameworks and Standards": ["Governance and Policy", "Threat Modeling"],
    "Governance and Policy": ["Frameworks and Standards"],
    "Threat Modeling": ["Architecture", "Frameworks and Standards"],
    "Architecture": ["Threat Modeling"],
    "Engineering Patterns": ["Secure Coding"],
    "Privacy": ["Safety and Alignment", "Secrets Management"],
}

# Tag mappings for frontmatter
GROUP_TAGS = {
    "foundations": "foundations",
    "attacks": "attacks",
    "defense": "defense",
    "agents": "agents",
    "coding": "coding",
    "research": "research",
    "practice": "practice",
    "general": "general",
}


def parse_readme(readme_path: Path) -> dict:
    """Parse a README.md into title, description, and sections."""
    text = readme_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = ""
    description = ""
    sections = []
    current_section = None

    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif not description and title and line.strip() and not line.startswith("#"):
            description = line.strip()
        elif line.startswith("## "):
            current_section = {"name": line[3:].strip(), "items": []}
            sections.append(current_section)
        elif current_section is not None and line.strip().startswith("- "):
            current_section["items"].append(line.strip())

    return {
        "title": title,
        "description": description,
        "sections": sections,
    }


def slugify(name: str) -> str:
    """Convert a note name to a filename-safe slug."""
    return name


def build_note(parsed: dict, group: str, note_name: str) -> str:
    """Build an Obsidian note from parsed README data."""
    tags = [GROUP_TAGS.get(group, group)]
    # Add a tag from the note name
    slug_tag = note_name.lower().replace(" ", "-").replace("&", "and")
    tags.append(slug_tag)

    lines = []
    lines.append("---")
    lines.append(f"tags: [{', '.join(tags)}]")
    lines.append(f"group: {GROUPS.get(group, group)}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {parsed['title']}")
    lines.append("")
    if parsed["description"]:
        lines.append(f"*{parsed['description']}*")
        lines.append("")

    # Cross-references
    related = CROSS_LINKS.get(note_name, [])
    if related:
        links = " | ".join(f"[[{r}]]" for r in related)
        lines.append(f"**Related:** {links}")
        lines.append("")

    # Sections
    for section in parsed["sections"]:
        lines.append(f"## {section['name']}")
        lines.append("")
        for item in section["items"]:
            lines.append(item)
        lines.append("")

    # Resource count
    total = sum(len(s["items"]) for s in parsed["sections"])
    lines.append("---")
    lines.append(f"*{total} resources*")
    lines.append("")

    return "\n".join(lines)


def build_moc(categories: list[dict]) -> str:
    """Build the Map of Content root note."""
    lines = []
    lines.append("---")
    lines.append("tags: [moc, index]")
    lines.append("---")
    lines.append("")
    lines.append("# AI Security")
    lines.append("")
    lines.append("*A curated collection of resources covering AI security, LLM safety, prompt injection, agent security, secure coding practices, and related topics.*")
    lines.append("")

    current_group = None
    for cat in categories:
        if cat["group_display"] != current_group:
            current_group = cat["group_display"]
            lines.append(f"## {current_group}")
            lines.append("")
        count = sum(len(s["items"]) for s in cat["parsed"]["sections"])
        desc = cat["parsed"]["description"] or ""
        lines.append(f"- [[{cat['note_name']}]] -- {desc} ({count})")
    lines.append("")

    total = sum(
        sum(len(s["items"]) for s in cat["parsed"]["sections"]) for cat in categories
    )
    lines.append("---")
    lines.append(f"*{total} total resources across {len(categories)} categories*")
    lines.append("")

    return "\n".join(lines)


def build_canvas(categories: list[dict]) -> str:
    """Build an Obsidian canvas JSON file with the category layout."""
    nodes = []
    edges = []

    # Color palette for groups
    colors = {
        "Foundations": "1",  # red
        "Attacks": "2",     # orange
        "Defense": "3",     # yellow
        "Agents": "4",      # green
        "Coding": "5",      # cyan
        "Research": "6",    # purple
        "Practice": "0",    # default
        "General": "0",
    }

    # Layout: arrange groups in columns
    group_x = {}
    x_pos = 0
    for group_key, group_display in GROUPS.items():
        group_x[group_display] = x_pos
        x_pos += 400

    # Track y position per group
    group_y = {g: 0 for g in GROUPS.values()}

    # Add MOC node at center-top
    moc_id = "moc"
    nodes.append({
        "id": moc_id,
        "type": "file",
        "file": "AI Security.md",
        "x": 1400,
        "y": -200,
        "width": 300,
        "height": 80,
        "color": "1",
    })

    for cat in categories:
        group = cat["group_display"]
        x = group_x[group]
        y = group_y[group]

        node_id = cat["note_name"].lower().replace(" ", "-")
        file_path = f"{group}/{cat['note_name']}.md"

        nodes.append({
            "id": node_id,
            "type": "file",
            "file": file_path,
            "x": x,
            "y": y,
            "width": 350,
            "height": 60,
            "color": colors.get(group, "0"),
        })

        # Edge from MOC to each node
        edges.append({
            "id": f"edge-moc-{node_id}",
            "fromNode": moc_id,
            "toNode": node_id,
            "fromSide": "bottom",
            "toSide": "top",
        })

        group_y[group] += 100

    # Add cross-reference edges
    for note_name, related_list in CROSS_LINKS.items():
        from_id = note_name.lower().replace(" ", "-")
        for related in related_list:
            to_id = related.lower().replace(" ", "-")
            # Only add edge once (alphabetical order to dedupe)
            if from_id < to_id:
                edges.append({
                    "id": f"edge-{from_id}-{to_id}",
                    "fromNode": from_id,
                    "toNode": to_id,
                    "fromSide": "right",
                    "toSide": "left",
                    "color": "0",
                })

    return json.dumps({"nodes": nodes, "edges": edges}, indent=2)


def sync():
    """Main sync function."""
    categories = []

    for group_key, group_display in GROUPS.items():
        group_dir = REPO_ROOT / group_key
        if not group_dir.is_dir():
            continue

        # Check if the group itself has a README (e.g., general/)
        readme = group_dir / "README.md"
        if readme.exists() and not any(group_dir.iterdir().__class__(d) for d in group_dir.iterdir() if d.is_dir()):
            # Leaf directory (like general/)
            parsed = parse_readme(readme)
            note_name = parsed["title"] or group_display
            categories.append({
                "group": group_key,
                "group_display": group_display,
                "note_name": note_name,
                "parsed": parsed,
            })
            continue

        # Walk subdirectories
        for subdir in sorted(group_dir.iterdir()):
            if not subdir.is_dir():
                continue
            readme = subdir / "README.md"
            if not readme.exists():
                continue

            parsed = parse_readme(readme)
            note_name = parsed["title"] or subdir.name.replace("-", " ").title()
            categories.append({
                "group": group_key,
                "group_display": group_display,
                "note_name": note_name,
                "parsed": parsed,
            })

    # Write vault notes
    for cat in categories:
        group_dir = VAULT_DIR / cat["group_display"]
        group_dir.mkdir(parents=True, exist_ok=True)
        note_path = group_dir / f"{cat['note_name']}.md"
        content = build_note(cat["parsed"], cat["group"], cat["note_name"])
        note_path.write_text(content, encoding="utf-8")

    # Write MOC
    moc_path = VAULT_DIR / "AI Security.md"
    moc_path.write_text(build_moc(categories), encoding="utf-8")

    # Write canvas
    canvas_path = VAULT_DIR / "overview.canvas"
    canvas_path.write_text(build_canvas(categories), encoding="utf-8")

    # Summary
    total_resources = sum(
        sum(len(s["items"]) for s in cat["parsed"]["sections"]) for cat in categories
    )
    print(f"Synced {len(categories)} categories, {total_resources} resources")
    for cat in categories:
        count = sum(len(s["items"]) for s in cat["parsed"]["sections"])
        print(f"  {cat['group_display']}/{cat['note_name']}: {count} resources")


if __name__ == "__main__":
    sync()
