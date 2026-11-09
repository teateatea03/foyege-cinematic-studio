"""Packaging checks; no tools/models are installed or run."""
import json
from pathlib import Path
import tempfile
import unittest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from install_suite import ROOT, install, load_suite, selected_skills


class InstallSuiteTests(unittest.TestCase):
    def test_full_clean_install(self):
        data, roster = load_suite(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "skills"
            installed = install(ROOT, destination, data["profiles"]["crew"])
            self.assertEqual(set(installed), set(roster))
            for name in installed:
                source = ROOT / roster[name]["path"]
                files = [p for p in source.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]
                for file in files:
                    self.assertEqual(file.read_bytes(), (destination / name / file.relative_to(source)).read_bytes())

    def test_dependency_closure_and_cycles(self):
        _, roster = load_suite(ROOT)
        self.assertEqual(selected_skills(roster, ["cinematic-screenwriting"]),
                         ["cinematic-screenwriting", "foyege-cinematic-direction"])
        self.assertIn("set-design", selected_skills(roster, ["openmontage"]))
        with self.assertRaises(ValueError):
            selected_skills(roster, ["unknown"])

    def test_each_selection_has_all_linked_files(self):
        import re
        from urllib.parse import urlsplit, unquote
        _, roster = load_suite(ROOT)
        for name in roster:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                destination = Path(tmp).resolve()
                install(ROOT, destination, [name])
                for file in destination.rglob("*.md"):
                    for href in re.findall(r"\]\(([^\s)]+)\)", file.read_text(encoding="utf-8")):
                        url = urlsplit(href)
                        if url.scheme or url.netloc:
                            continue
                        target = (file.parent / unquote(url.path)).resolve() if url.path else file
                        self.assertTrue(target.is_relative_to(destination) and target.is_file(), (name, file, href))

    def test_collision_has_no_partial_install(self):
        data, _ = load_suite(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            existing = destination / "set-design"
            existing.mkdir()
            marker = existing / "KEEP"
            marker.write_text("unchanged", encoding="utf-8")
            with self.assertRaises(ValueError):
                install(ROOT, destination, data["profiles"]["crew"])
            self.assertEqual(marker.read_text(encoding="utf-8"), "unchanged")
            self.assertEqual([p.name for p in destination.iterdir()], ["set-design"])

    def test_manifest_rejects_unbundled_dependency(self):
        data, _ = load_suite(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for item in data["skills"]:
                folder = root / item["path"]
                folder.mkdir(parents=True)
                (folder / "SKILL.md").write_text("stub", encoding="utf-8")
            data["skills"][0]["requires"].append("private-only")
            (root / "skill-suite.json").write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown dependencies"):
                load_suite(root)


if __name__ == "__main__":
    unittest.main()
