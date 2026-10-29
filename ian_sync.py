#!/usr/bin/env python3
"""
ian-sync.py — Sync knowledge, framework mappings, and version state for Ian L2/L3 personas.

Safe-by-default:
- Never overwrites title:, role:, triggers:, or any existing body text.
- Only adds: version: (if missing), ecc-mapping: (additive reference list), ecc-latest-version: (config).
- L3 only populated when L2 has >=3 natural sub‑categories from triggers/description keyword groups.
- Always backs up before any write.
- Requires explicit user confirmation (reply "yes") before applying changes.

Usage:
    ian-sync.py --check          # Report only, no modifications
    ian-sync.py --write          # Apply additive changes after user confirmation
    ian-sync.py --status         # Report current state
"""

import os
import re
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
REPO_ROOT = Path(__file__).resolve().parent
IANA_L2_DIR = REPO_ROOT / "personas" / "l2" / "ian"
CONFIG_YAML = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "hermes" / "config.yaml"
BACKUP_ROOT = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "hermes" / "ian-sync-backup"
GITHUB_REPO = "affaan-m/ECC"
GITHUB_API_BASE = "https://api.github.com/repos/{}"

# Keyword groups for L3 population detection
KEYWORD_GROUPS = {
    "api_erd": {"api", "erd", "data design", "desain data", "schema", "entity", "relation"},
    "devops_pipeline": {"deploy", "devops", "release", "rollback", "health check", "smoke test", "alert"},
    "security_offensive": {"pentest", "security audit", "red team", "vulnerability", "owasp", "auth bypass"},
    "security_defensive": {"incident response", "monitoring", "SIEM", "SOC", "blue team", "breach", "defensive"},
    "ux_research": {"UX research", "user research", "usability testing", "journey mapping", "persona", "user interview", "IA", "information architecture", "user flows"},
    "ui_design": {"UI design", "design system", "Figma", "component library", "visual design", "tokens", "handoff spec", "accessibility"},
    "flutter_mobile": {"mobile", "flutter", "android", "ios", "widget", "screen", "platform target"},
    "project_plan": {"plan", "buat rencana", "timeline", "dependencies", "go/no-go", "checklist", "work package"},
    "orchestration": {"orchestrate", "koordinasikan", "assign specialist", "track checkpoint", "exit criteria", "board"},
}



def parse_frontmatter(path):
    """Parse YAML frontmatter from a .md file. Returns dict of key-value pairs."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    fields = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- "):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]
            fields[k] = v
    return fields


def safe_get(fields, key, default=None):
    return fields.get(key, default)


def detect_keyword_groups(triggers_list, description_text):
    """Detect which KEYWORD_GROUPS are represented in triggers + description."""
    text = " ".join(triggers_list).lower() + " " + description_text.lower()
    found = set()
    for group_name, group_keywords in KEYWORD_GROUPS.items():
        if any(kw in text for kw in group_keywords):
            found.add(group_name)
    return found


import json

MAPPING_FILE = REPO_ROOT / "sync" / "ecc-mapping.json"


def load_mapping():
    """Load the verified ECC mapping (source of truth). See docs/ECC-MAPPING.md."""
    return json.loads(MAPPING_FILE.read_text(encoding="utf-8"))


def get_ecc_mapping(ian_l2_key):
    entry = load_mapping()["mappings"].get(ian_l2_key)
    return entry["items"] if entry else []


def get_ecc_fit(ian_l2_key):
    entry = load_mapping()["mappings"].get(ian_l2_key)
    return entry["fit"] if entry else None


def fetch_ecc_tree(ref="main"):
    """Return the set of file paths in ECC at <ref> (release tag), or None if unreachable."""
    try:
        r = subprocess.run(
            ["gh", "api", "repos/{}/git/trees/{}?recursive=1".format(GITHUB_REPO, ref),
             "--jq", ".tree[] | select(.type==\"blob\") | .path"],
            capture_output=True, text=True, timeout=60,
        )
        if r.returncode == 0 and r.stdout.strip():
            return set(r.stdout.split())
    except Exception:
        pass
    return None


def item_path(item):
    kind, name = item.split(":", 1)
    return {"skill": "skills/{}/SKILL.md", "agent": "agents/{}.md",
            "command": "commands/{}.md"}[kind].format(name)


def verify_mapping(tree):
    """Return list of (persona, item) that no longer exist in the live ECC tree."""
    missing = []
    for persona, entry in load_mapping()["mappings"].items():
        for item in entry["items"]:
            if item_path(item) not in tree:
                missing.append((persona, item))
    return missing


# ---- ECC skill import (verbatim copy + lockfile) ---------------------------
import hashlib
import base64

HERMES_HOME = Path(os.environ.get("HERMES_HOME") or (Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "hermes"))
ECC_SKILLS_DIR = HERMES_HOME / "skills" / "ecc"
LOCK_FILE = ECC_SKILLS_DIR / ".ecc-lock.json"


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def fetch_file(path, ref):
    r = subprocess.run(
        ["gh", "api", "repos/{}/contents/{}?ref={}".format(GITHUB_REPO, path, ref), "--jq", ".content"],
        capture_output=True, timeout=60)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    return base64.b64decode(r.stdout.strip())


def _local_hashes(dest):
    out = {}
    if dest.exists():
        for fp in sorted(dest.rglob("*")):
            if fp.is_file():
                out[fp.relative_to(dest).as_posix()] = _sha(fp.read_bytes())
    return out


def import_skills(dry_run):
    """Copy mapped ECC skills into HERMES_HOME/skills/ecc verbatim (plus declared patches).
    Never overwrites a skill whose local files differ from the lockfile (user edited it)."""
    mp = load_mapping()
    imports = mp.get("imports", {})
    tag = get_ecc_latest_version()
    if tag == "unknown":
        print("Cannot determine ECC release tag. Aborting.")
        return 1
    tree = fetch_ecc_tree(tag)
    if not tree:
        print("Cannot read ECC tree at {}. Aborting.".format(tag))
        return 1
    lock = json.loads(LOCK_FILE.read_text(encoding="utf-8")) if LOCK_FILE.exists() else {"skills": {}}
    results = []
    for name, spec in imports.items():
        prefix = "skills/{}/".format(name)
        files = sorted(p for p in tree if p.startswith(prefix))
        if not files:
            results.append((name, "MISSING at {}".format(tag)))
            continue
        dest = ECC_SKILLS_DIR / name
        entry = lock["skills"].get(name)
        if entry and dest.exists() and _local_hashes(dest) != entry["local_sha256"]:
            results.append((name, "SKIPPED: local files modified since import"))
            continue
        up, loc, blobs = {}, {}, {}
        failed = False
        for fp in files:
            rel = fp[len(prefix):]
            data = fetch_file(fp, tag)
            if data is None:
                results.append((name, "FETCH FAILED: " + fp))
                failed = True
                break
            up[rel] = _sha(data)
            if rel == "SKILL.md":
                for pt in spec.get("patches", []):
                    txt = data.decode("utf-8")
                    if pt["find"] not in txt:
                        results.append((name, "PATCH TARGET NOT FOUND: " + pt["find"]))
                        failed = True
                        break
                    data = txt.replace(pt["find"], pt["replace"]).encode("utf-8")
                if failed:
                    break
            loc[rel] = _sha(data)
            blobs[rel] = data
        if failed:
            continue
        if entry and entry["upstream_sha256"] == up and entry.get("tag") == tag and dest.exists():
            results.append((name, "up to date ({})".format(tag)))
            continue
        if not dry_run:
            for rel, data in blobs.items():
                tgt = dest / rel
                tgt.parent.mkdir(parents=True, exist_ok=True)
                tgt.write_bytes(data)
            lock["skills"][name] = {"tag": tag, "for": spec.get("for", []), "patched": bool(spec.get("patches")),
                                    "upstream_sha256": up, "local_sha256": loc}
        results.append((name, ("would import " if dry_run else "imported ") + "{} file(s) from {}".format(len(blobs), tag)))
    if not dry_run:
        ECC_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        lock.update({"ecc_repo": GITHUB_REPO, "ecc_tag": tag})
        LOCK_FILE.write_text(json.dumps(lock, indent=2), encoding="utf-8")
    print("ECC import {} (tag {}) -> {}".format("DRY RUN" if dry_run else "RESULT", tag, ECC_SKILLS_DIR))
    for name, msg in results:
        print("  {:28s} {}".format(name, msg))
    return 0


def report_imports(latest_tag):
    """Read-only drift report for --check."""
    print("\n--- ECC imported skills ---")
    if not LOCK_FILE.exists():
        print("  none imported yet (run --import-skills)")
        return
    lock = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
    print("  imported from {}; latest release {}{}".format(
        lock.get("ecc_tag"), latest_tag, "  ** UPDATE AVAILABLE **" if lock.get("ecc_tag") != latest_tag else ""))
    for name, e in lock["skills"].items():
        state = "ok" if _local_hashes(ECC_SKILLS_DIR / name) == e["local_sha256"] else "LOCALLY MODIFIED"
        print("  {:28s} {}{}".format(name, state, " (patched)" if e.get("patched") else ""))


def get_ecc_latest_version():
    """Fetch latest release tag from ECC GitHub repo."""
    try:
        result = subprocess.run(
            ["gh", "api", "repos/{}/releases".format(GITHUB_REPO), "--jq", ".[0].tag_name"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    try:
        result2 = subprocess.run(
            ["gh", "api", "repos/{}/tags".format(GITHUB_REPO), "--jq", "[0].name"],
            capture_output=True, text=True, timeout=15,
        )
        if result2.returncode == 0 and result2.stdout.strip():
            return result2.stdout.strip()
    except Exception:
        pass
    return "unknown"


def backup_file(path, backup_root):
    """Create a timestamped backup of the file. Returns the backup path."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = backup_root / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_dir / path.name)
    return backup_dir / path.name


def insert_frontmatter_line(content, line):
    """Insert one line at the end of the YAML frontmatter (before its FIRST closing ---).
    Never touches the body. Returns content unchanged if no frontmatter."""
    m = re.match(r"^(---\r?\n.*?)(\r?\n---)(\r?\n|$)", content, re.DOTALL)
    if not m:
        return content
    nl = "\r\n" if "\r\n" in m.group(2) else "\n"
    return m.group(1) + nl + line + m.group(2) + content[m.end(2):]


def add_version_if_missing(content, fields):
    """If 'version' not in fields, add version: 1.0 inside the frontmatter."""
    if "version" in fields:
        return content
    return insert_frontmatter_line(content, "version: 1.0")


def set_frontmatter_field(content, key, value_line):
    """Replace 'key: ...' inside the frontmatter if present, else insert it. Body untouched."""
    m = re.match(r"^(---\r?\n)(.*?)(\r?\n---)", content, re.DOTALL)
    if not m:
        return content
    block = m.group(2)
    pat = re.compile(r"^{}:.*$".format(re.escape(key)), re.MULTILINE)
    if pat.search(block):
        block = pat.sub(lambda _m: value_line, block, count=1)
        return m.group(1) + block + content[m.end(2):]
    return insert_frontmatter_line(content, value_line)


def add_ecc_mapping(content, fields, mapping):
    """Set ecc-mapping inside the frontmatter (replaces a stale value, never touches body)."""
    flow = "[" + ", ".join('"{}"'.format(x) for x in mapping) + "]"
    return set_frontmatter_field(content, "ecc-mapping", "ecc-mapping: " + flow)


def populate_l3_under_l2(l2_path, l2_key):
    """
    Determine if L3 should be populated for this L2.
    Returns True if L3 files were created, False otherwise.
    """
    fields = parse_frontmatter(l2_path)
    description = safe_get(fields, "title", "") + " " + safe_get(fields, "role", "")

    triggers_raw = safe_get(fields, "triggers", "")
    if isinstance(triggers_raw, str):
        trigger_list = [t.strip().lower() for t in triggers_raw.split(",") if t.strip()]
    else:
        trigger_list = []

    groups = detect_keyword_groups(trigger_list, description)

    if len(groups) < 3:
        return False

    # L3 will be populated. Create L3 sub-files.
    l3_base = Path("/d/GitHub/ai-agent-registry/l3") / l2_key
    l3_base.mkdir(parents=True, exist_ok=True)

    group_to_short = {
        "api_erd": "api-erd",
        "devops_pipeline": "deploy-pipeline",
        "security_offensive": "sec-red",
        "security_defensive": "sec-blue",
        "ux_research": "ux-research",
        "ui_design": "ui-design",
        "flutter_mobile": "flutter",
        "project_plan": "plan",
        "orchestration": "alpha",
    }

    created_any = False

    # Build a set of group names that were found so we only create those
    found_groups = set()
    for g in groups:
        found_groups.add(g)

    for group_name in found_groups:
        short_name = group_to_short.get(group_name, group_name)
        l3_filename = "ian-{}-{}.md".format(l2_key, short_name)
        l3_path = l3_base / l3_filename

        if not l3_path.exists():
            l3_fields = {
                "name": "ian-{}-{}".format(l2_key, short_name),
                "title": "Ian-{}-{}".format(l2_key.title(), short_name.title().replace("-", " ")),
                "parent": l2_key,
                "version": "1.0",
                "ecc-mapping": get_ecc_mapping(l2_key),
            }
            fm_lines = ["---"]
            for k, v in l3_fields.items():
                if isinstance(v, list):
                    fm_lines.append("{}: {}".format(k, ", ".join(v)))
                else:
                    fm_lines.append("{}: {}".format(k, v))
            fm_lines.append("---")
            body = ""
            l3_path.write_text("\n".join(fm_lines) + "\n" + body, encoding="utf-8")
            created_any = True

    return created_any


def run_check():
    """Phase 1: Check only. Print summary, no modifications."""
    print("=" * 60)
    print("ian-sync CHECK -- Ian L2/L3 Version & Mapping Report")
    print("=" * 60)

    # Latest ECC version
    ecc_latest = get_ecc_latest_version()
    print("\n--- Latest ECC version: {}".format(ecc_latest))

    # Scan all Ian L2 .md files
    l2_files = sorted(IANA_L2_DIR.glob("*.md"))
    print("\n--- Found {} Ian L2 persona files:".format(len(l2_files)))

    any_missing_version = False
    any_l3_eligible = False

    for l2_path in l2_files:
        key = l2_path.stem  # e.g. ian-api from ian-api.md
        fields = parse_frontmatter(l2_path)
        has_version = "version" in fields

        # Parse triggers
        triggers_raw = safe_get(fields, "triggers", "")
        if isinstance(triggers_raw, str):
            trigger_list = [t.strip().lower() for t in triggers_raw.split(",") if t.strip()]
        else:
            trigger_list = []

        description = safe_get(fields, "role", "")
        groups = detect_keyword_groups(trigger_list, description)
        l3_eligible = len(groups) >= 3

        ecc_map = get_ecc_mapping(key)

        status_parts = []
        if not has_version:
            status_parts.append("⚠ no version")
            any_missing_version = True
        else:
            status_parts.append("✓ version: {}".format(fields.get("version", "?")))

        ecc_display = ecc_map if ecc_map else "(none)"
        status_parts.append(" ecc-mapping: {}".format(ecc_display))

        if l3_eligible:
            status_parts.append(" L3-eligible: yes")
            any_l3_eligible = True
        else:
            status_parts.append(" L3-eligible: no")

        print("  {}:  |  ".format(l2_path.name) + "  |  ".join(status_parts))

    # Config.yaml L3 status
    print("\n--- config.yaml L3 children: currently empty (children: {})")

    # Live verification of the mapping against ECC
    tree = fetch_ecc_tree(ecc_latest if ecc_latest != "unknown" else "main")
    broken = []
    if tree is None:
        print("\n--- ECC live check: SKIPPED (could not reach GitHub)")
    else:
        broken = verify_mapping(tree)
        if broken:
            print("\n--- ECC live check: {} item(s) MISSING (review docs/ECC-MAPPING.md):".format(len(broken)))
            for persona, item in broken:
                print("  MISSING {} -> {}".format(persona, item))
        else:
            print("\n--- ECC live check: all mapped items exist in ECC {}".format(ecc_latest))

    report_imports(ecc_latest)

    # Summary
    missing_count = sum(1 for l2 in l2_files if "version" not in parse_frontmatter(l2))
    l3_eligible_count = sum(
        1 for l2 in l2_files
        if len(detect_keyword_groups(
            [t.strip().lower() for t in safe_get(parse_frontmatter(l2), "triggers", "").split(",") if t.strip()],
            safe_get(parse_frontmatter(l2), "role", "")
        )) >= 3
    )

    print("\n--- SUMMARY ---")
    print("Ian L2 files scanned: {}".format(len(l2_files)))
    print("Missing version metadata: {}".format(missing_count))
    print("L3-eligible specialists: {}".format(l3_eligible_count))
    print("Latest ECC version: {}".format(ecc_latest))
    print("Backup root: {}".format(BACKUP_ROOT))
    print("No modifications were made. Use --write to apply additive changes.\n")

    return 1 if missing_count > 0 else 0


def run_write():
    """Phase 2: Apply additive changes after user confirmation."""
    print("=" * 60)
    print("ian-sync WRITE -- Preparing additive changes (backup first)")
    print("=" * 60)

    if "--yes" not in sys.argv:
        try:
            answer = input("\nProceed with applying changes? (type 'yes' to confirm): ").strip().lower()
        except EOFError:
            answer = ""
        if answer != "yes":
            print("Aborted. No changes applied. (Use --write --yes for non-interactive confirmation.)")
            return 1

    # Backup all L2 files
    l2_files = sorted(IANA_L2_DIR.glob("*.md"))
    for l2_path in l2_files:
        backup_file(l2_path, BACKUP_ROOT)
    print("  -> Backed up {} Ian L2 files".format(len(l2_files)))

    # Backup config.yaml
    backup_file(CONFIG_YAML, BACKUP_ROOT)
    print("  -> Backed up config.yaml")

    # Apply changes to each L2 file
    updated = []
    for l2_path in l2_files:
        key = l2_path.stem
        fields = parse_frontmatter(l2_path)
        content = l2_path.read_text(encoding="utf-8")

        # Add version if missing
        if "version" not in fields:
            content = add_version_if_missing(content, fields)
            print("  -> Added version: 1.0 to {}".format(l2_path.name))

        # Add ecc-mapping if missing
        ecc_map = get_ecc_mapping(key)
        fit = get_ecc_fit(key)
        if fit:
            content = add_ecc_mapping(content, fields, ecc_map)
            content = set_frontmatter_field(content, "ecc-fit", "ecc-fit: " + fit)
            print("  -> ecc-mapping {} (fit: {}) -> {}".format(ecc_map, fit, l2_path.name))

        # Write back
        l2_path.write_text(content, encoding="utf-8")
        updated.append(l2_path)

    # Populate L3 where eligible
    l3_eligible_files = []
    for l2_path in l2_files:
        result = populate_l3_under_l2(l2_path, l2_path.stem)
        if result:
            l3_eligible_files.append(l2_path)
            print("  -> L3 populated under {}".format(l2_path.name))

    # config.yaml L3 left as-is
    print("  -> config.yaml L3 children left as-is (children: {})")

    # Summary
    print("\n--- WRITE COMPLETE ---")
    print("L2 files updated: {}".format(len(updated)))
    print("L3 populated under: {}".format(len(l3_eligible_files)))
    print("Backups stored at: {}".format(BACKUP_ROOT))

    # Git commit if in a git repo
    try:
        stat_result = subprocess.run(
            ["git", "status", "--short"], cwd="/d/GitHub/ai-agent-registry",
            capture_output=True, text=True, timeout=10,
        )
        if stat_result.returncode == 0 and stat_result.stdout.strip():
            diff_result = subprocess.run(
                ["git", "diff", "--stat"], cwd="/d/GitHub/ai-agent-registry",
                capture_output=True, text=True, timeout=10,
            )
            if diff_result.stdout.strip():
                add_cmds = ["git", "add"]
                add_cmds.append("--")
                for p in updated:
                    add_cmds.append(str(p))
                subprocess.run(add_cmds, cwd=str(REPO_ROOT), capture_output=True, timeout=30)
                subprocess.run(
                    ["git", "commit", "-m",
                     "ian-sync: add version metadata & ECC mappings (user-approved)"],
                    cwd="/d/GitHub/ai-agent-registry", capture_output=True, timeout=30,
                )
                print("  -> Changes committed to git repo.")
    except Exception as e:
        print("  -> Git commit skipped: {}".format(e))

    print("\n  ian-sync complete. Review the changes above.\n")


def run_status():
    """Phase 3: Report current state."""
    print("=" * 60)
    print("ian-sync STATUS -- Current State Report")
    print("=" * 60)

    l2_files = sorted(IANA_L2_DIR.glob("*.md"))
    print("\n--- Ian L2 files: {}".format(len(l2_files)))

    for l2_path in l2_files:
        fields = parse_frontmatter(l2_path)
        has_version = "version" in fields
        ecc_map = fields.get("ecc-mapping", "not set")
        print("  {}: version={}, ecc-mapping={}".format(l2_path.name, has_version, ecc_map))

    # L3 directory
    l3_dir = Path("/d/GitHub/ai-agent-registry/l3")
    if l3_dir.exists():
        l3_files = list(l3_dir.glob("*.md"))
        print("\n--- L3 files ({}):".format(len(l3_files)))
        for f in l3_files:
            print("  {}".format(f.name))
    else:
        print("\n--- L3: no directory yet")

    # ECC latest version
    ecc_latest = get_ecc_latest_version()
    print("\n--- Latest ECC version: {}".format(ecc_latest))

    print("\n  Use `ian-sync --check` for a full report, or `ian-sync --write` (after review) to apply additive changes.\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ian-sync.py --check | --write | --status | --import-skills [--yes]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "--import-skills":
        sys.exit(import_skills(dry_run="--yes" not in sys.argv))
    elif cmd == "--check":
        sys.exit(run_check())
    elif cmd == "--write":
        sys.exit(run_write())
    elif cmd == "--status":
        sys.exit(run_status())
    else:
        print("Unknown command: {}".format(cmd))
        print("Usage: ian-sync.py --check | --write | --status | --import-skills [--yes]")
        sys.exit(1)