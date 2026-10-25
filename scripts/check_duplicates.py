#!/usr/bin/env python3
"""Check for duplicate persona keys across all .md files."""
import pathlib, yaml, sys

persona_dir = pathlib.Path(__file__).resolve().parent.parent / "personas"
seen = {}
dups = False

for f in sorted(persona_dir.rglob("*.md")):
    content = f.read_text(encoding="utf-8")
    parts = content.split("---\n", 2)
    if len(parts) >= 3:
        fm = yaml.safe_load(parts[1])
        name = fm.get("name")
        if name:
            if name in seen:
                print(f"DUPLICATE key: {name} in {f} and {seen[name]}")
                dups = True
            seen[name] = str(f)

if not dups:
    print(f"No duplicate keys ({len(seen)} personas)")
else:
    sys.exit(1)
