#!/usr/bin/env python3
r"""sync_personas.py — sync persona files into your agent runtime's config.

WHY:
    Agent personalities live in config.yaml under `agent.personalities:`.
    This script reads Markdown persona files from a source directory and
    regenerates that config block so new/changed personas appear with
    NO manual config edits.

WHAT IT WATCHES:
    Set PERSONA_DIR env var to point at your persona folder.
    PERSONA_DIR defaults to the `personas/` directory in this repo.

FILE FORMAT (each persona file):
    ---
    name: persona-key
    title: Display Name
    role: brief description
    ---
    <full system prompt here>

    Or: no frontmatter — name is derived from filename stem.
    A file is treated as a persona if it has frontmatter `name:` OR contains
    an em-dash " — " in the stem (excludes README.md, etc.).

USAGE:
    python sync/sync_personas.py                    # sync into config.yaml
    PERSONA_DIR=path python sync/sync_personas.py   # override source folder

HIERARCHY ENFORCEMENT:
    After syncing, validate_hierarchy() checks that your agent.hierarchy
    (L0-L4 + TEAM) still matches the live persona set.
"""
from __future__ import annotations
import os
import re
import sys
import json
import pathlib
import datetime
import argparse

# ── 2. identity token resolution ───────────────────────────────────────
DEFAULT_IDENTITIES = pathlib.Path(__file__).resolve().parent.parent / "config" / "identities.yaml"

# ── 1. locate the canonical persona folder ──────────────────────────────
DEFAULT_DIR = pathlib.Path(__file__).resolve().parent.parent / "personas"
FOLDER = pathlib.Path(os.environ.get("PERSONA_DIR", DEFAULT_DIR))


def load_identities(path: pathlib.Path | None = None) -> dict[str, str]:
    """Load identity tokens from identities.yaml. Returns {TOKEN: value}."""
    p = path or pathlib.Path(os.environ.get("IDENTITIES_FILE", DEFAULT_IDENTITIES))
    if not p.exists():
        return {}
    try:
        import yaml
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except ImportError:
        print("WARN: PyYAML unavailable, skipping identity resolution.", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"WARN: cannot parse identities.yaml ({e!r})", file=sys.stderr)
        return {}

    tokens: dict[str, str] = {}
    for section, values in (data or {}).items():
        if isinstance(values, dict):
            for k, v in values.items():
                tokens[f"<{k.upper()}>"] = str(v) if v is not None else ""
    return tokens


def resolve_tokens(prompt: str, tokens: dict[str, str]) -> str:
    """Replace tokens like <USER> with configured values."""
    if not tokens:
        return prompt
    for token, value in tokens.items():
        prompt = prompt.replace(token, value)
    return prompt

# config path (override via env)
HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
CONFIG_PATH = pathlib.Path(HERMES_HOME) / "config.yaml"

# anchor markers (idempotent replace between these)
START = "# >>> PERSONALITY SYNC (auto-managed) >>>"
END = "# <<< PERSONALITY SYNC <<<"

EM_DASH = "\u2014"  # —


def slug(text: str) -> str:
    """jan-default style slug from arbitrary text."""
    text = re.sub(rf"\s*{EM_DASH}\s*", " ", text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "unnamed"


def parse_frontmatter(src: str):
    """Return (frontmatter_dict_or_None, body_str)."""
    if not src.startswith("---"):
        return None, src
    parts = re.split(r"^---\s*$", src, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return None, src
    fm: dict = {}
    for line in parts[1].splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            val = val.strip('"').strip("'")
            fm[key] = val
    return fm, parts[2].strip()


def is_persona_file(path: pathlib.Path, fm) -> bool:
    """A file is a persona if it has a frontmatter name OR contains an em-dash
    in the stem (excludes README.md, _notes.md, etc.)."""
    if fm and fm.get("name"):
        return True
    if path.name.lower() in {"readme.md", "agent.md", "notes.md"} or path.name.startswith("_"):
        return False
    return EM_DASH in path.stem


def extract_prompt(fm, body: str) -> str:
    """Prefer an explicit system_prompt; fall back to the body text."""
    if fm and (fm.get("system_prompt") or fm.get("prompt")):
        return (fm.get("system_prompt") or fm.get("prompt")).strip()
    return body.strip()


def build_personalities(tokens: dict[str, str] | None = None) -> dict[str, tuple[str, str, str]]:
    """Return {key: (prompt, title, role)}."""
    out: dict[str, tuple[str, str, str]] = {}
    used: dict[str, int] = {}
    if not FOLDER.is_dir():
        print(f"WARN: persona folder not found: {FOLDER}", file=sys.stderr)
        return out

    for f in sorted(FOLDER.rglob("*.md")):
        src = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(src)
        if not is_persona_file(f, fm):
            continue
        base = slug(fm.get("name")) if (fm and fm.get("name")) else slug(f.stem.split(EM_DASH)[0].strip())
        key = base
        if key in out:
            used[key] = used.get(key, 0) + 1
            rest = f.stem.split(EM_DASH, 1)[1].strip() if EM_DASH in f.stem else ""
            key = f"{base}-{slug(rest)}" if rest else f"{base}-{used[key]}"
            while key in out:
                used[key] = used.get(key, 0) + 1
                key = f"{key}-{used[key]}"
        prompt = extract_prompt(fm, body)
        if tokens:
            prompt = resolve_tokens(prompt, tokens)
        title = (fm or {}).get("title") or f.name
        role = (fm or {}).get("role") or ""
        out[key] = (prompt, title, role)
    return out


def render_block(personalities: dict[str, tuple[str, str, str]], indent: str = "  ") -> str:
    """Render the personalities YAML block, indented to sit under `agent:`
    (JSON scalars => valid YAML)."""
    lines = [f"{indent}{START}", f"{indent}personalities:"]
    for key in sorted(personalities):
        prompt = personalities[key][0]
        lines.append(f"{indent}  {key}: {json.dumps(prompt, ensure_ascii=False)}")
    lines.append(f"{indent}{END}")
    return "\n".join(lines) + "\n"


# existing marker block, at any indentation (incl. the legacy top-level form)
BLOCK_RE = re.compile(
    rf"^[ \t]*{re.escape(START)}[ \t]*\n.*?^[ \t]*{re.escape(END)}[ \t]*(?:\n|\Z)",
    re.S | re.M,
)
AGENT_RE = re.compile(r"^agent:[ \t]*(?:#.*)?$", re.M)


def child_indent(text: str, pos: int) -> str:
    """Indentation of the first child line after `pos` (default two spaces)."""
    for ln in text[pos:].splitlines():
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        indent = ln[: len(ln) - len(ln.lstrip())]
        return indent or "  "
    return "  "


def merge_block(text: str, personalities: dict[str, tuple[str, str, str]]) -> str:
    """Return `text` with the personalities block placed under the top-level
    `agent:` key. A single `agent:` mapping is kept so a user-maintained
    `agent.hierarchy` and the synced `agent.personalities` never collide."""
    base = BLOCK_RE.sub("", text)
    m = AGENT_RE.search(base)
    if m:
        nl = base.find("\n", m.end())
        if nl == -1:
            base += "\n"
            nl = len(base) - 1
        pos = nl + 1
        return base[:pos] + render_block(personalities, child_indent(base, pos)) + base[pos:]
    lines = base.splitlines(keepends=True)
    anchor = 0
    for i, ln in enumerate(lines):
        if ln.startswith("_config_version:"):
            anchor = i + 1
            break
    head = "".join(lines[:anchor])
    if head and not head.endswith("\n"):
        head += "\n"
    return head + "agent:\n" + render_block(personalities) + "".join(lines[anchor:])


def strict_yaml_load(text: str):
    """yaml.safe_load that rejects duplicate mapping keys instead of
    silently keeping the last one."""
    import yaml

    class StrictLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node, deep=False):
        seen = set()
        for key_node, _ in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in seen:
                raise yaml.constructor.ConstructorError(
                    None, None, f"duplicate key {key!r}", key_node.start_mark)
            seen.add(key)
        return loader.construct_mapping(node, deep)

    StrictLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    return yaml.load(text, Loader=StrictLoader)


def inject_into_config(personalities: dict[str, tuple[str, str, str]]) -> bool:
    """Write the personalities block under `agent:` in config.yaml. Return True if changed."""
    if not CONFIG_PATH.exists():
        print(f"WARN: config.yaml not found at {CONFIG_PATH}", file=sys.stderr)
        print(f"Set HERMES_HOME env var to your runtime config directory.", file=sys.stderr)
        return False
    text = CONFIG_PATH.read_text(encoding="utf-8")
    new = merge_block(text, personalities)
    if new == text:
        return False
    # self-check: refuse to write invalid YAML (or YAML with duplicate keys)
    try:
        strict_yaml_load(new)
    except ImportError:
        pass
    except Exception as e:
        print(f"ERROR: sync would write INVALID YAML ({e!r}); config.yaml left untouched.",
              file=sys.stderr)
        return False
    CONFIG_PATH.write_text(new, encoding="utf-8")
    return True


def validate_hierarchy(personas: dict[str, tuple[str, str, str]]) -> int:
    """Check agent.hierarchy in config.yaml against the live persona set.

    Verifies:
      - L0..L4 + TEAM keys exist
      - every persona referenced in hierarchy members/children exists in personas
      - no persona in `personalities` is orphaned (absent from all layers)
      - display.personality points to a living persona

    Returns the number of warnings. Always advisory — never blocks sync.
    """
    try:
        import yaml
    except ImportError:
        print("WARN: PyYAML unavailable, skipping hierarchy validation.",
              file=sys.stderr)
        return 0

    warnings = 0
    if not CONFIG_PATH.exists():
        return 0

    try:
        cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"WARN: cannot parse config.yaml for hierarchy validation ({e!r})",
              file=sys.stderr)
        return 0

    hierarchy = cfg.get("agent", {}).get("hierarchy")
    if not hierarchy:
        print("WARN: agent.hierarchy block missing.",
              file=sys.stderr)
        return 1

    # 1. Required layers
    required_layers = ["L0", "L1", "L2", "L3", "L4", "TEAM"]
    for layer in required_layers:
        if layer not in hierarchy:
            print(f"WARN: hierarchy layer '{layer}' missing",
                  file=sys.stderr)
            warnings += 1

    # 2. Collect all persona keys referenced in the hierarchy
    referenced = set()
    for layer in ("L0", "L1"):
        members = hierarchy.get(layer, {}).get("members") or []
        if isinstance(members, str):
            members = [members]
        for m in members:
            referenced.add(m)

    l2 = hierarchy.get("L2", {})
    if isinstance(l2, dict):
        children = l2.get("children") or {}
        if isinstance(children, dict):
            for parent, child_list in children.items():
                referenced.add(parent)
                if isinstance(child_list, str):
                    child_list = [child_list]
                for c in child_list:
                    referenced.add(c)

    # 3. Check referenced keys exist as personas
    for ref in sorted(referenced):
        if ref not in personas:
            print(f"WARN: hierarchy references persona '{ref}' that is not in "
                  f"agent.personalities (stale reference)",
                  file=sys.stderr)
            warnings += 1

    # 4. Check for orphaned personas
    for key in sorted(personas.keys()):
        if key in referenced:
            continue
        if key == "jan":  # default voice, always OK outside hierarchy
            continue
        print(f"WARN: persona '{key}' exists in agent.personalities but is not "
              f"referenced in agent.hierarchy (orphaned)",
              file=sys.stderr)
        warnings += 1

    # 5. display.personality resolves
    display_p = cfg.get("display", {}).get("personality")
    if display_p and display_p not in personas:
        print(f"WARN: display.personality='{display_p}' does not match any living "
              f"personality.",
              file=sys.stderr)
        warnings += 1

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync persona files into agent runtime config.")
    parser.add_argument("--check", action="store_true",
                        help="Validate persona files without writing config.yaml")
    parser.add_argument("--identities", type=pathlib.Path, default=None,
                        help="Path to identities.yaml for token resolution")
    parser.add_argument("--dry-run", action="store_true",
                        help="Build personalities but don't write to config.yaml")
    args = parser.parse_args()

    if not FOLDER.is_dir():
        print(f"ERROR: persona folder missing: {FOLDER}", file=sys.stderr)
        return 2

    # Load identity tokens for <USER>, <COMPANY>, etc. resolution
    tokens = load_identities(args.identities)
    personas = build_personalities(tokens if tokens else None)

    if args.check:
        print(f"CHECK: {len(personas)} persona files validated.")
        unresolved = set()
        for key in sorted(personas):
            prompt = personas[key][0]
            matches = re.findall(r"<[A-Z_]+>", prompt)
            unresolved.update(matches)
        if unresolved:
            print(f"  Unresolved tokens: {', '.join(sorted(unresolved))}")
        else:
            print("  All tokens resolved.")
        validate_hierarchy(personas)
        return 0

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M")

    if args.dry_run:
        print(f"[{now}] DRY RUN: {len(personas)} personas would be synced.")
        for key in sorted(personas):
            print(f"  - /personality {key}")
        validate_hierarchy(personas)
        return 0

    changed = inject_into_config(personas)
    if not changed:
        validate_hierarchy(personas)
        return 0
    print(f"[{now}] Synced {len(personas)} personas -> config.yaml agent.personalities")
    for key in sorted(personas):
        print(f"  - /personality {key}")
    validate_hierarchy(personas)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
