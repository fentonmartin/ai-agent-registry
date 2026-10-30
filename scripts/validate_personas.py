#!/usr/bin/env python3
"""Validate all persona files in the personas/ directory.

Checks:
  - YAML frontmatter is present, parses, and is a mapping
  - required fields: name, title, role
  - name is lowercase-kebab (^[a-z][a-z0-9-]*$) and matches the file name
  - layout: personas/l0/<key>.md, personas/l1/<key>.md,
    personas/l2/<parent>/<key>.md
  - L2 personas declare `parent` equal to their folder, the parent is an
    L1 persona allowed to have children, and the key starts with "<parent>-"
  - L0/L1 personas declare no parent
  - `triggers`, if present, is a list
  - no private sensitive patterns, email addresses or API keys
  - persona counts quoted in README.md, index.md and docs/HIERARCHY.md
    match the files on disk
"""
import os
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install -r requirements.txt")
    sys.exit(1)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PERSONA_DIR = REPO_ROOT / "personas"

# Only these L1 personas may have L2 children (see docs/HIERARCHY.md).
PARENTS_WITH_CHILDREN = {"ian", "ran", "lan", "ban"}
REQUIRED_FIELDS = ("name", "title", "role")
KEY_RE = re.compile(r"^[a-z][a-z0-9-]*$")

# Private names to keep out of persona files are NOT listed here (this file
# is public). They come from config/sensitive-patterns.txt (gitignored, one
# per line) and/or the SENSITIVE_PATTERNS env var (comma-separated, e.g. a
# CI secret).
SENSITIVE_FILE = REPO_ROOT / "config" / "sensitive-patterns.txt"

# Generic leaks: real email addresses and common API key formats.
SECRET_RE = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    r"|sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}"
)


def load_sensitive():
    patterns = [p.strip() for p in os.environ.get("SENSITIVE_PATTERNS", "").split(",")]
    if SENSITIVE_FILE.exists():
        for ln in SENSITIVE_FILE.read_text(encoding="utf-8").splitlines():
            if not ln.lstrip().startswith("#"):
                patterns.append(ln.strip())
    return [p for p in patterns if p]

# Docs that quote persona counts.
COUNT_DOCS = ("README.md", "index.md", "docs/HIERARCHY.md")


def parse_frontmatter(content):
    """Return (frontmatter_dict, error_message). One of them is None."""
    if not content.startswith("---"):
        return None, "missing YAML frontmatter (must start with ---)"
    parts = content.split("---\n", 2)
    if len(parts) < 3:
        return None, "malformed frontmatter"
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return None, f"invalid YAML in frontmatter: {e}"
    if not isinstance(fm, dict):
        return None, "frontmatter must be a YAML mapping"
    return fm, None


def layer_of(rel):
    """Return (layer, folder_parent) for a path relative to the persona dir."""
    parts = rel.parts
    if len(parts) == 2 and parts[0] in ("l0", "l1"):
        return parts[0].upper(), None
    if len(parts) == 3 and parts[0] == "l2":
        return "L2", parts[1]
    if len(parts) == 3 and parts[0] == "l3":
        return "L3", parts[1]
    return None, None


def validate_file(path, persona_dir, l1_keys, sensitive=()):
    """Return (layer, errors) for one persona file."""
    rel = path.relative_to(persona_dir)
    errors = []

    def err(msg):
        errors.append(f"{rel.as_posix()}: {msg}")

    content = path.read_text(encoding="utf-8")
    fm, problem = parse_frontmatter(content)
    if problem:
        err(problem)
        return None, errors

    for field in REQUIRED_FIELDS:
        if not fm.get(field):
            err(f"missing required field '{field}'")
    name = fm.get("name")
    if not name:
        return None, errors
    name = str(name)

    if not KEY_RE.match(name):
        err(f"name must be lowercase-kebab matching {KEY_RE.pattern} ('{name}')")
    if path.stem != name:
        err(f"file name '{path.name}' must match name '{name}'")

    layer, folder_parent = layer_of(rel)
    parent = fm.get("parent")
    if layer is None:
        err("must live in personas/l0/, personas/l1/ or personas/l2/<parent>/")
    elif layer in ("L0", "L1"):
        if parent:
            err(f"{layer} personas must not declare a parent (found '{parent}')")
    elif layer == "L2":
        if not parent:
            err(f"L2 persona must declare 'parent: {folder_parent}'")
        elif parent != folder_parent:
            err(f"parent '{parent}' does not match folder 'l2/{folder_parent}/'")
        if parent and parent not in l1_keys:
            err(f"parent '{parent}' not in L1 keys: {sorted(l1_keys)}")
        elif parent and parent not in PARENTS_WITH_CHILDREN:
            err(f"L1 '{parent}' may not have children (allowed: "
                f"{', '.join(sorted(PARENTS_WITH_CHILDREN))})")
        if parent and not name.startswith(f"{parent}-"):
            err(f"L2 key '{name}' must start with '{parent}-'")
    elif layer == "L3":
        if not parent:
            err(f"L3 persona must declare 'parent: {folder_parent}'")

    triggers = fm.get("triggers")
    if triggers is not None and not isinstance(triggers, list):
        err("'triggers' must be a list")

    for s in sensitive:
        if s in content:
            err(f"contains sensitive pattern '{s}'")
    for m in SECRET_RE.finditer(content):
        err(f"looks like an email or API key: '{m.group(0)[:12]}...'")

    return layer, errors


def validate_counts(repo_root, counts):
    """Check persona counts quoted in docs against `counts` ({layer: n})."""
    total = sum(counts.values())
    errors = []
    for doc in COUNT_DOCS:
        p = repo_root / doc
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for m in re.finditer(r"badge/personas-(\d+)-", text):
            if int(m.group(1)) != total:
                errors.append(f"{doc}: personas badge says {m.group(1)}, found {total}")
        for m in re.finditer(r"\b(\d+) personas\b", text):
            if int(m.group(1)) != total:
                errors.append(f"{doc}: says '{m.group(0)}', found {total}")
        # README table rows: | **L1** | ... | 11 |   HIERARCHY list: - L1: 11 (...)
        for m in re.finditer(r"^\| \*\*(L[012])\*\* \|.*\| (\d+) \|\s*$|^- (L[012]): (\d+)\b",
                             text, re.M):
            layer = m.group(1) or m.group(3)
            n = int(m.group(2) or m.group(4))
            if n != counts.get(layer, 0):
                errors.append(f"{doc}: says {layer} = {n}, found {counts.get(layer, 0)}")
    return errors


def main():
    l1_keys = {p.stem for p in (PERSONA_DIR / "l1").glob("*.md")}
    sensitive = load_sensitive()
    if not sensitive:
        print("NOTE: no private sensitive patterns configured "
              f"({SENSITIVE_FILE.relative_to(REPO_ROOT).as_posix()} or SENSITIVE_PATTERNS).")
    errors = []
    counts = {"L0": 0, "L1": 0, "L2": 0, "L3": 0}
    files = sorted(PERSONA_DIR.rglob("*.md"))
    for f in files:
        layer, errs = validate_file(f, PERSONA_DIR, l1_keys, sensitive)
        errors.extend(errs)
        if layer:
            counts[layer] += 1
    errors.extend(validate_counts(REPO_ROOT, counts))

    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        return 1
    print(f"All {len(files)} persona files validated successfully "
          f"(L0={counts['L0']}, L1={counts['L1']}, L2={counts['L2']}, L3={counts['L3']}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
