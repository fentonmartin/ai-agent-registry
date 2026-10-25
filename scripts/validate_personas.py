#!/usr/bin/env python3
"""Validate all persona files in the personas/ directory.
Checks: YAML frontmatter, lowercase keys, parent references, sensitive patterns.
"""
import pathlib
import sys

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

PERSONA_DIR = pathlib.Path(__file__).resolve().parent.parent / "personas"

SENSITIVE = ["FEN", "Fenton", "fentonmartin", "fentonxm",
             "Fayolex", "fayolex", "E3 Platform"]

errors = []

for f in sorted(PERSONA_DIR.rglob("*.md")):
    content = f.read_text(encoding="utf-8")

    if not content.startswith("---"):
        errors.append(f"{f.relative_to(PERSONA_DIR)}: missing YAML frontmatter (must start with ---)")
        continue

    parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE) \
        if False else content.split("---\n", 2)
    if len(parts) < 3:
        errors.append(f"{f.relative_to(PERSONA_DIR)}: malformed frontmatter")
        continue

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        errors.append(f"{f.relative_to(PERSONA_DIR)}: invalid YAML in frontmatter: {e}")
        continue

    if not isinstance(fm, dict):
        errors.append(f"{f.relative_to(PERSONA_DIR)}: frontmatter must be a YAML mapping")
        continue

    # name is required
    if "name" not in fm:
        errors.append(f"{f.relative_to(PERSONA_DIR)}: missing required field 'name'")
        continue

    # name must be lowercase-kebab
    name = fm.get("name", "")
    if name and name != name.lower():
        errors.append(f"{f.relative_to(PERSONA_DIR)}: name must be lowercase ('{name}')")

    # parent must reference a valid L1 key
    parent = fm.get("parent")
    if parent:
        l1_dir = PERSONA_DIR / "l1"
        if l1_dir.exists():
            l1_keys = [p.stem for p in l1_dir.glob("*.md")]
            if parent not in l1_keys:
                errors.append(f"{f.relative_to(PERSONA_DIR)}: parent '{parent}' not in L1 keys: {l1_keys}")

    # Check for sensitive patterns
    for s in SENSITIVE:
        if s in content:
            errors.append(f"{f.relative_to(PERSONA_DIR)}: contains sensitive pattern '{s}'")

if errors:
    for e in errors:
        print(f"  ERROR: {e}")
    sys.exit(1)
else:
    count = len(list(PERSONA_DIR.rglob("*.md")))
    print(f"All {count} persona files validated successfully.")
