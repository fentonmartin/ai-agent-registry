import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_personas as vp  # noqa: E402


class ValidateFileTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self._tmp.name)
        self.l1_keys = {"ian", "ran", "lan", "pan"}

    def tearDown(self):
        self._tmp.cleanup()

    def check(self, rel, frontmatter, body="Prompt.\n"):
        path = self.dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\n{frontmatter}---\n{body}", encoding="utf-8")
        return vp.validate_file(path, self.dir, self.l1_keys, sensitive=["SECRET"])

    def test_valid_l1(self):
        self.assertEqual(self.check("l1/pan.md", "name: pan\ntitle: Pan\nrole: product\n"),
                         ("L1", []))

    def test_valid_l2(self):
        layer, errors = self.check(
            "l2/ian/ian-api.md",
            "name: ian-api\ntitle: Ian-API\nrole: api\nparent: ian\ntriggers: [api]\n")
        self.assertEqual((layer, errors), ("L2", []))

    def assertError(self, result, fragment):
        _, errors = result
        self.assertTrue(any(fragment in e for e in errors), errors)

    def test_missing_frontmatter(self):
        path = self.dir / "l1" / "pan.md"
        path.parent.mkdir(parents=True)
        path.write_text("no frontmatter", encoding="utf-8")
        self.assertError(vp.validate_file(path, self.dir, self.l1_keys), "missing YAML frontmatter")

    def test_missing_required_fields(self):
        self.assertError(self.check("l1/pan.md", "name: pan\n"), "missing required field 'title'")

    def test_uppercase_name(self):
        self.assertError(self.check("l1/Pan.md", "name: Pan\ntitle: P\nrole: r\n"), "lowercase-kebab")

    def test_file_name_mismatch(self):
        self.assertError(self.check("l1/pan.md", "name: pam\ntitle: P\nrole: r\n"), "must match name")

    def test_wrong_folder(self):
        self.assertError(self.check("misc/pan.md", "name: pan\ntitle: P\nrole: r\n"), "must live in")

    def test_l1_with_parent(self):
        self.assertError(self.check("l1/pan.md", "name: pan\ntitle: P\nrole: r\nparent: ian\n"),
                         "must not declare a parent")

    def test_l2_without_parent(self):
        self.assertError(self.check("l2/ian/ian-x.md", "name: ian-x\ntitle: X\nrole: r\n"),
                         "must declare 'parent: ian'")

    def test_l2_parent_folder_mismatch(self):
        self.assertError(self.check("l2/ian/ian-x.md", "name: ian-x\ntitle: X\nrole: r\nparent: ran\n"),
                         "does not match folder")

    def test_l2_parent_not_allowed_children(self):
        self.assertError(self.check("l2/pan/pan-x.md", "name: pan-x\ntitle: X\nrole: r\nparent: pan\n"),
                         "may not have children")

    def test_l2_unknown_parent(self):
        self.assertError(self.check("l2/zzz/zzz-x.md", "name: zzz-x\ntitle: X\nrole: r\nparent: zzz\n"),
                         "not in L1 keys")

    def test_l2_key_prefix(self):
        self.assertError(self.check("l2/ian/api.md", "name: api\ntitle: X\nrole: r\nparent: ian\n"),
                         "must start with 'ian-'")

    def test_triggers_must_be_list(self):
        self.assertError(self.check("l1/pan.md", "name: pan\ntitle: P\nrole: r\ntriggers: x\n"),
                         "must be a list")

    def test_sensitive_pattern(self):
        self.assertError(self.check("l1/pan.md", "name: pan\ntitle: P\nrole: r\n", "a SECRET\n"),
                         "sensitive pattern")

    def test_email_and_api_key(self):
        fm = "name: pan\ntitle: P\nrole: r\n"
        self.assertError(self.check("l1/pan.md", fm, "mail a@b.co\n"), "email or API key")
        self.assertError(self.check("l1/pan.md", fm, "key sk-abcdefghijklmnopqrstuvwxyz\n"),
                         "email or API key")

    def test_tokens_are_not_flagged(self):
        fm = "name: pan\ntitle: P\nrole: r\n"
        self.assertEqual(self.check("l1/pan.md", fm, "mail <EMAIL>\n")[1], [])


class ValidateCountsTest(unittest.TestCase):
    def test_detects_stale_counts(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            (root / "README.md").write_text(
                "badge/personas-3-orange\n| **L1** | experts | 2 |\nWe have 3 personas.\n",
                encoding="utf-8")
            errors = vp.validate_counts(root, {"L0": 1, "L1": 1, "L2": 2})
        self.assertEqual(len(errors), 3, errors)

    def test_repo_docs_match_repo_personas(self):
        self.assertEqual(vp.main(), 0)


if __name__ == "__main__":
    unittest.main()
