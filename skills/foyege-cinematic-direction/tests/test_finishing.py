"""Synthetic guard/PNG tests; not H3 generation, tracking or acting acceptance."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image, ImageFont

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import take_guard
import audit_visible_face
import render_system_cards


class TakeGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.spec = self.root / "job.json"
        self.receipt = self.root / "receipt.json"
        self.job = {"schema_version": 1, "take_id": "C1-take-1",
                    "timing": {"fps_num": 24, "fps_den": 1, "frame_count": 2},
                    "artifacts": [{"id": name, "role": name, "path": name + ".bin"}
                                  for name in ["source", "settings", "stage", "reference"]]}
        for item in self.job["artifacts"]:
            (self.root / item["path"]).write_bytes(item["id"].encode())
        self.save()

    def save(self):
        self.spec.write_text(json.dumps(self.job), encoding="utf-8")

    def freeze(self):
        return take_guard.freeze(self.root, self.spec, self.receipt)

    def test_unchanged_and_changed_artifacts(self):
        self.freeze()
        self.assertEqual(take_guard.verify(self.root, self.spec, self.receipt)["result"], "identity_match")
        for name in ["source", "settings", "stage", "reference"]:
            with self.subTest(role=name):
                path = self.root / (name + ".bin")
                original = path.read_bytes()
                path.write_bytes(b"changed")
                with self.assertRaisesRegex(ValueError, "artifact changed"):
                    take_guard.verify(self.root, self.spec, self.receipt)
                path.write_bytes(original)

    def test_changed_timing_and_no_overwrite(self):
        self.freeze()
        with self.assertRaises(FileExistsError):
            self.freeze()
        self.job["timing"]["frame_count"] = 3
        self.save()
        with self.assertRaisesRegex(ValueError, "job changed"):
            take_guard.verify(self.root, self.spec, self.receipt)

    def test_path_escape_and_duplicate_role_id(self):
        self.job["artifacts"][0]["path"] = "../outside.bin"
        self.save()
        with self.assertRaisesRegex(ValueError, "out-of-root"):
            self.freeze()
        self.job["artifacts"][0]["path"] = "source.bin"
        self.job["artifacts"][1]["id"] = "source"
        self.save()
        with self.assertRaisesRegex(ValueError, "unique"):
            self.freeze()

    def test_cli_real_process_rejects_changed_stage(self):
        args = [sys.executable, "-X", "utf8", str(SCRIPTS / "take_guard.py")]
        options = ["--root", str(self.root), "--job", str(self.spec), "--receipt", str(self.receipt)]
        run = subprocess.run(args + ["freeze"] + options, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        (self.root / "stage.bin").write_bytes(b"replaced")
        run = subprocess.run(args + ["verify"] + options, capture_output=True)
        self.assertEqual(run.returncode, 2)
        self.assertIn(b"artifact changed", run.stderr)


class MaskAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.roots = [Path(self.temp.name) / p for p in ["source", "candidate", "mask", "result"]]
        for root in self.roots:
            root.mkdir()
        self.b = np.full((2, 3, 3), 40, dtype=np.uint8)
        self.c = np.full((2, 3, 3), 100, dtype=np.uint8)  # already blended candidate
        self.v = np.array([[0, 128, 255], [0, 128, 255]], dtype=np.uint8)
        self.result = np.rint(self.b + (self.c.astype(np.float32) - self.b) * self.v[..., None] / 255).astype(np.uint8)
        self.write()

    def write(self):
        for root, array in zip(self.roots, [self.b, self.c, self.v, self.result]):
            Image.fromarray(array).save(root / "000000.png")

    def audit(self):
        return audit_visible_face.audit(*self.roots, 1)

    def test_full_mask_endpoints_and_fraction(self):
        report = self.audit()
        self.assertEqual(report["result"], "pixel_pass")
        self.assertEqual(report["totals"]["protected_pixels"], 2)
        self.assertEqual(report["totals"]["candidate_changed_pixels"], 6)

    def test_outside_mask_change_rejected(self):
        self.result[0, 0, 0] += 1
        self.write()
        report = self.audit()
        self.assertEqual(report["result"], "pixel_fail")
        self.assertEqual(report["totals"]["protected_changed"], 1)

    def test_double_alpha_rejected(self):
        self.result[:, 1, :] = 55
        self.write()
        self.assertEqual(self.audit()["totals"]["formula_mismatch"], 2)

    def test_missing_frame_and_implicit_mask_conversion_rejected(self):
        with self.assertRaisesRegex(ValueError, "exactly"):
            audit_visible_face.audit(*self.roots, 2)
        Image.fromarray(np.repeat(self.v[..., None], 3, axis=2)).save(self.roots[2] / "000000.png")
        with self.assertRaisesRegex(ValueError, "mode L"):
            self.audit()

    def test_geometry_mismatch_rejected(self):
        Image.new("RGB", (4, 2)).save(self.roots[1] / "000000.png")
        with self.assertRaisesRegex(ValueError, "geometry mismatch"):
            self.audit()


class SystemCardTests(unittest.TestCase):
    def setUp(self):
        config_path = SCRIPTS.parent / "assets/finishing/system_cards.example.json"
        self.config = render_system_cards.load_config(config_path)
        # Portable layout tests use ASCII. The actual CJK font is checked in the local CLI run.
        for cue in self.config["cues"]:
            cue["title"], cue["detail"] = "SYSTEM", "DRAFT"
        self.typefaces = {size: ImageFont.load_default() for size in (18, 22, 30, 52)}

    def frame_hash(self, index):
        return hashlib.sha256(render_system_cards.render_frame(self.config, self.typefaces, index).tobytes()).hexdigest()

    def test_random_access_reproducible_and_hold_preserved(self):
        expected = self.frame_hash(60)
        self.frame_hash(0)
        self.frame_hash(143)
        self.assertEqual(self.frame_hash(60), expected)
        self.assertEqual(self.frame_hash(72), self.frame_hash(119))
        self.assertNotEqual(self.frame_hash(0), self.frame_hash(47))

    def test_boundaries_and_missing_interval(self):
        for frame in [-1, 144]:
            with self.assertRaises(ValueError):
                self.frame_hash(frame)
        bad = copy.deepcopy(self.config)
        bad["cues"][1]["start"] += 1
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "contiguous"):
                render_system_cards.load_config(path)


if __name__ == "__main__":
    unittest.main()
