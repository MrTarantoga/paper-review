#!/usr/bin/env python3
"""Validate SKILL.md frontmatter, plugin manifests and internal file references."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


# Plugin manifests
plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
for field in ("name", "version", "description"):
    check(plugin.get(field), f"plugin.json: missing '{field}'")
check(re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", "")), "plugin.json: version is not semver")
names = [p.get("name") for p in market.get("plugins", [])]
check(plugin.get("name") in names, "marketplace.json: does not list the plugin from plugin.json")

# Skills
skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
check(skills, "no skills/*/SKILL.md found")
for skill in skills:
    rel = skill.relative_to(ROOT)
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{rel}: missing YAML frontmatter")
        continue
    meta = dict(
        line.split(":", 1) for line in m.group(1).splitlines() if ":" in line and not line.startswith(" ")
    )
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    name, desc = meta.get("name", ""), meta.get("description", "")
    check(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and len(name) <= 64,
          f"{rel}: name must be lowercase-hyphenated, at most 64 chars")
    check(name == skill.parent.name, f"{rel}: name '{name}' does not match folder '{skill.parent.name}'")
    check(desc and len(desc) <= 1024, f"{rel}: description must be 1-1024 chars (is {len(desc)})")
    check(not re.search(r"<[a-z]", desc), f"{rel}: description must not contain XML tags")
    check("~/.claude/" not in text, f"{rel}: hardcoded ~/.claude/ path breaks plugin installs")
    # Every `references/...` or `scripts/...` path mentioned must exist
    for ref in sorted(set(re.findall(r"`((?:references|scripts)/[\w./-]+)`", text))):
        check((skill.parent / ref).exists(), f"{rel}: referenced file '{ref}' does not exist")

if errors:
    print("\n".join(f"ERROR: {e}" for e in errors))
    sys.exit(1)
print(f"OK: {len(skills)} skill(s), plugin '{plugin['name']}' v{plugin['version']}")
