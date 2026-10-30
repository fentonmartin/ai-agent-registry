import io
import pathlib
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "sync"))

import yaml  # noqa: E402

import sync_personas as sp  # noqa: E402


def personas(*keys):
    return {k: (f"prompt for {k}", k.title(), "") for k in keys}


class SlugTest(unittest.TestCase):
    def test_lowercases_and_kebabs(self):
        self.assertEqual(sp.slug("Ian-API"), "ian-api")
        self.assertEqual(sp.slug("Jan — Default Tone"), "jan-default-tone")
        self.assertEqual(sp.slug("  ran__brand!! "), "ran-brand")

    def test_empty_becomes_unnamed(self):
        self.assertEqual(sp.slug("!!!"), "unnamed")


class FrontmatterTest(unittest.TestCase):
    def test_parses_scalars_and_body(self):
        fm, body = sp.parse_frontmatter("---\nname: zan\ntitle: \"Zan\"\n---\n\nHello\n")
        self.assertEqual(fm, {"name": "zan", "title": "Zan"})
        self.assertEqual(body, "Hello")

    def test_crlf(self):
        fm, body = sp.parse_frontmatter("---\r\nname: zan\r\n---\r\nHello\r\n")
        self.assertEqual(fm["name"], "zan")
        self.assertEqual(body, "Hello")

    def test_no_frontmatter(self):
        self.assertEqual(sp.parse_frontmatter("Hello"), (None, "Hello"))


class TokenTest(unittest.TestCase):
    def test_resolve(self):
        self.assertEqual(sp.resolve_tokens("Hi <USER> at <COMPANY>", {"<USER>": "Ann"}),
                         "Hi Ann at <COMPANY>")

    def test_load_identities_flattens_sections_and_warns_on_collision(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "identities.yaml"
            p.write_text("identity:\n  user: Ann\ninfra:\n  user: Bob\n  model: m1\n",
                         encoding="utf-8")
            err = io.StringIO()
            with redirect_stderr(err):
                tokens = sp.load_identities(p)
        self.assertEqual(tokens, {"<USER>": "Bob", "<MODEL>": "m1"})
        self.assertIn("<USER>", err.getvalue())

    def test_example_config_defines_every_token_used_by_personas(self):
        import re
        tokens = sp.load_identities(ROOT / "config" / "identities.example.yaml")
        used = set()
        for f in (ROOT / "personas").rglob("*.md"):
            used.update(re.findall(r"<[A-Z_]+>", f.read_text(encoding="utf-8")))
        self.assertEqual(used - set(tokens), set())


class BuildPersonalitiesTest(unittest.TestCase):
    def test_builds_from_folder(self):
        with tempfile.TemporaryDirectory() as d:
            folder = pathlib.Path(d)
            (folder / "zan.md").write_text("---\nname: zan\ntitle: Zan\n---\nHi <USER>\n",
                                           encoding="utf-8")
            (folder / "README.md").write_text("not a persona", encoding="utf-8")
            old = sp.FOLDER
            sp.FOLDER = folder
            try:
                out = sp.build_personalities({"<USER>": "Ann"})
            finally:
                sp.FOLDER = old
        self.assertEqual(list(out), ["zan"])
        self.assertEqual(out["zan"][0], "Hi Ann")

    def test_repo_personas_have_unique_keys(self):
        out = sp.build_personalities()
        files = [p for p in (ROOT / "personas").rglob("*.md")
                 if "references" not in p.parts and "assets" not in p.parts]
        self.assertEqual(len(out), len(files))


class MergeBlockTest(unittest.TestCase):
    def load(self, text):
        return sp.strict_yaml_load(text)

    def test_creates_agent_after_config_version(self):
        out = sp.merge_block("_config_version: 3\nmodel: x\n", personas("zan"))
        self.assertTrue(out.startswith("_config_version: 3\nagent:\n"))
        self.assertEqual(self.load(out)["agent"]["personalities"]["zan"], "prompt for zan")

    def test_nests_under_existing_agent_with_its_indent(self):
        cfg = "agent:\n    hierarchy:\n        L0: {members: [zan]}\ndisplay:\n  personality: zan\n"
        out = sp.merge_block(cfg, personas("zan", "jan"))
        data = self.load(out)
        self.assertEqual(sorted(data["agent"]), ["hierarchy", "personalities"])
        self.assertEqual(data["display"]["personality"], "zan")
        self.assertIn("\n    personalities:\n", out)

    def test_migrates_legacy_top_level_block(self):
        legacy = (f"{sp.START}\nagent:\n  personalities:\n    old: \"x\"\n{sp.END}\n"
                  "agent:\n  hierarchy: {}\n")
        data = self.load(sp.merge_block(legacy, personas("zan")))
        self.assertEqual(list(data["agent"]["personalities"]), ["zan"])
        self.assertIn("hierarchy", data["agent"])

    def test_idempotent(self):
        once = sp.merge_block("agent:\n  hierarchy: {}\n", personas("zan"))
        self.assertEqual(sp.merge_block(once, personas("zan")), once)

    def test_agent_on_last_line_without_newline(self):
        data = self.load(sp.merge_block("model: x\nagent:", personas("zan")))
        self.assertEqual(list(data["agent"]["personalities"]), ["zan"])

    def test_prompts_with_special_characters_round_trip(self):
        p = {"zan": ("line1\n\"quoted\": yes # not a comment\n—", "Zan", "")}
        data = self.load(sp.merge_block("", p))
        self.assertEqual(data["agent"]["personalities"]["zan"], p["zan"][0])


class StrictLoadTest(unittest.TestCase):
    def test_rejects_duplicate_keys(self):
        with self.assertRaises(yaml.YAMLError):
            sp.strict_yaml_load("agent: 1\nagent: 2\n")


class InjectTest(unittest.TestCase):
    def run_inject(self, text):
        with tempfile.TemporaryDirectory() as d:
            cfg = pathlib.Path(d) / "config.yaml"
            cfg.write_text(text, encoding="utf-8")
            old = sp.CONFIG_PATH
            sp.CONFIG_PATH = cfg
            try:
                with redirect_stderr(io.StringIO()):
                    changed = sp.inject_into_config(personas("zan"))
            finally:
                sp.CONFIG_PATH = old
            return changed, cfg.read_text(encoding="utf-8")

    def test_writes_and_reports_change(self):
        changed, text = self.run_inject("agent:\n  hierarchy: {}\n")
        self.assertTrue(changed)
        self.assertIn("personalities", text)

    def test_refuses_when_hand_written_personalities_would_duplicate(self):
        cfg = "agent:\n  personalities:\n    zan: manual\n"
        changed, text = self.run_inject(cfg)
        self.assertFalse(changed)
        self.assertEqual(text, cfg)


class HierarchyTest(unittest.TestCase):
    def documented_config(self):
        doc = (ROOT / "docs" / "HIERARCHY.md").read_text(encoding="utf-8")
        section = doc.split("## Hierarchy Config Format", 1)[1]
        return section.split("```yaml\n", 1)[1].split("```", 1)[0]

    def warnings_for(self, cfg_text, persona_set):
        with tempfile.TemporaryDirectory() as d:
            cfg = pathlib.Path(d) / "config.yaml"
            cfg.write_text(cfg_text, encoding="utf-8")
            old = sp.CONFIG_PATH
            sp.CONFIG_PATH = cfg
            try:
                with redirect_stderr(io.StringIO()):
                    return sp.validate_hierarchy(persona_set)
            finally:
                sp.CONFIG_PATH = old

    def test_documented_config_has_no_warnings(self):
        self.assertEqual(self.warnings_for(self.documented_config(), sp.build_personalities()), 0)

    def test_missing_layer_and_orphan_warn(self):
        cfg = "agent:\n  hierarchy:\n    L0: {members: [zan]}\n"
        # 5 missing layers + orphan 'pan'
        self.assertEqual(self.warnings_for(cfg, personas("zan", "pan")), 6)


if __name__ == "__main__":
    unittest.main()
