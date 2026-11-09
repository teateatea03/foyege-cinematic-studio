"""Arithmetic/schema checks only. No audio, image, model or GPU experiments."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import acting_cues
import look_handoff


def example(name):
    return json.loads((ROOT / "assets/sync-look" / name).read_text(encoding="utf-8"))


class CueTests(unittest.TestCase):
    def setUp(self):
        self.data = example("acting_cues.example.json")

    def test_provisional_and_conservative_rounding(self):
        report = acting_cues.build(self.data)
        event = report["events"][0]
        self.assertEqual(report["status"], "provisional")
        self.assertEqual(event["text"], self.data["events"][0]["text"])
        self.assertEqual(report["reactions"][0]["intent"], self.data["reactions"][0]["intent"])
        self.assertEqual(event["timeline_frame_exact"], {"num": 6003, "den": 250})
        self.assertEqual(event["containing_frame"], 24)
        self.assertEqual(event["first_boundary_not_before"], 25)
        self.assertTrue(all(r["observation"] == "not_measured" for r in report["reactions"]))

    def test_rational_fps_trim_and_audio_speed(self):
        self.data["timeline"].update(fps={"num": 30000, "den": 1001}, start_frame=100,
                                     audio_in_sample=48000, audio_playback_rate={"num": 2, "den": 1})
        self.data["events"][0]["source_sample"] = 96000
        self.data["reactions"] = [{"id": "eyes", "trigger": "instruction_end",
                                   "planned_frame": 115, "hold_end_frame": 130}]
        event = acting_cues.build(self.data)["events"][0]
        self.assertEqual(event["timeline_frame_exact"], {"num": 115100, "den": 1001})
        self.assertEqual(event["first_boundary_not_before"], 115)
        self.data = example("acting_cues.example.json")
        self.data["timeline"].update(fps={"num": 30000, "den": 1001}, frame_count=300000)
        self.data["events"][0]["source_sample"] = 48000 * 7200
        self.data["reactions"] = [{"id": "eyes", "trigger": "instruction_end",
                                   "planned_frame": 215785, "hold_end_frame": 215800}]
        event = acting_cues.build(self.data)["events"][0]
        self.assertEqual(event["timeline_frame_exact"], {"num": 216000000, "den": 1001})

    def test_early_planned_and_observed_are_separate(self):
        self.data["reactions"][0].update(planned_frame=24, observed_frame=23)
        kinds = {i["kind"] for i in acting_cues.build(self.data)["issues"]}
        self.assertIn("planned_before_trigger", kinds)
        self.assertIn("observed_before_trigger", kinds)

    def test_eye_head_order(self):
        self.data["reactions"][0]["observed_frame"] = 30
        self.data["reactions"][1].update(planned_frame=25, observed_frame=30)
        kinds = {i["kind"] for i in acting_cues.build(self.data)["issues"]}
        self.assertIn("planned_reaction_order", kinds)
        self.assertIn("observed_reaction_order", kinds)

    def test_half_open_clip_and_invalid_mapping(self):
        self.data["events"][0]["source_sample"] = 288000
        with self.assertRaisesRegex(ValueError, "outside"):
            acting_cues.build(self.data)
        self.data = example("acting_cues.example.json")
        self.data["timeline"]["speed_ramp"] = []
        with self.assertRaisesRegex(ValueError, "constant_audio_rate"):
            acting_cues.build(self.data)

    def test_invalid_fps_and_forward_dependency(self):
        self.data["timeline"]["fps"]["den"] = 0
        with self.assertRaises(ValueError):
            acting_cues.build(self.data)
        self.data = example("acting_cues.example.json")
        self.data["reactions"][0]["after_reaction"] = "head_follows"
        with self.assertRaisesRegex(ValueError, "earlier"):
            acting_cues.build(self.data)


class LookTests(unittest.TestCase):
    def setUp(self):
        self.data = example("look_handoff.example.json")

    def known(self):
        baseline = self.data["baseline"]
        baseline.update(working_space="fixture-space", view_transform="fixture-view",
                        display="fixture-display", color_config_sha256="c" * 64)
        baseline["output_color"] = dict(primaries="fixture-primaries", transfer="fixture-transfer",
                                         matrix="fixture-matrix", range="fixture-range")
        for shot in self.data["shots"]:
            shot.update(copy.deepcopy(baseline))
            shot["input_color"] = copy.deepcopy(baseline["output_color"])
            shot["input_transform"] = "fixture-input"
            shot["planned_looks"][0]["sha256"] = "a" * 64
        return self.data

    def test_unknown_not_guessed(self):
        report = look_handoff.build(self.data)
        self.assertEqual(report["status"], "needs_binding")
        self.assertIsNone(report["shots"][0]["input_color"]["transfer"])
        self.assertEqual(report["content_acceptance"], "unmeasured")

    def test_same_look_across_shots_is_allowed(self):
        self.assertEqual(look_handoff.build(self.known())["status"], "handoff_consistent")

    def test_baked_then_planned_same_bytes(self):
        self.known()
        self.data["shots"][0]["baked_looks"] = [{"id": "other-name", "sha256": "a" * 64}]
        kinds = {i["kind"] for i in look_handoff.build(self.data)["issues"]}
        self.assertIn("repeated_look_bytes", kinds)

    def test_same_id_different_bytes(self):
        self.known()
        look = self.data["shots"][0]["planned_looks"][0]
        self.data["shots"][0]["baked_looks"] = [{"id": look["id"], "sha256": "b" * 64}]
        kinds = {i["kind"] for i in look_handoff.build(self.data)["issues"]}
        self.assertIn("look_id_reused_with_different_bytes", kinds)

    def test_intentional_change_preserved_for_review(self):
        self.known()
        shot = self.data["shots"][1]
        shot["world_light_id"] = "PRACTICAL_TURNS_ON"
        shot["intentional_changes"] = {"world_light_id": "story event"}
        report = look_handoff.build(self.data)
        self.assertEqual(report["status"], "needs_review")
        self.assertEqual(report["issues"][0]["intentional_reason"], "story event")

    def test_malformed_digest_and_missing_field(self):
        self.data["baseline"]["color_config_sha256"] = "short"
        with self.assertRaises(ValueError):
            look_handoff.build(self.data)
        self.data = example("look_handoff.example.json")
        del self.data["shots"][0]["output_color"]["transfer"]
        with self.assertRaisesRegex(ValueError, "explicit null"):
            look_handoff.build(self.data)


class CliTests(unittest.TestCase):
    def test_actual_clis_preserve_existing_report(self):
        for script, asset in [("acting_cues.py", "acting_cues.example.json"),
                              ("look_handoff.py", "look_handoff.example.json")]:
            with self.subTest(script=script), tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / "report.json"
                cmd = [sys.executable, "-X", "utf8", str(ROOT / "scripts" / script),
                       "--input", str(ROOT / "assets/sync-look" / asset), "--output", str(output)]
                first = subprocess.run(cmd, capture_output=True)
                self.assertEqual(first.returncode, 0, first.stderr)
                original = output.read_bytes()
                second = subprocess.run(cmd, capture_output=True)
                self.assertEqual(second.returncode, 2, second.stderr)
                self.assertEqual(output.read_bytes(), original)
                bad = example(asset)
                if script == "acting_cues.py":
                    bad["reactions"][0]["planned_frame"] = 24
                else:
                    bad["shots"][0]["planned_looks"] *= 2
                bad_input, bad_output = Path(tmp) / "bad.json", Path(tmp) / "bad-report.json"
                bad_input.write_text(json.dumps(bad), encoding="utf-8")
                run = subprocess.run(cmd[:-4] + ["--input", str(bad_input), "--output", str(bad_output)],
                                     capture_output=True)
                self.assertEqual(run.returncode, 1, run.stderr)
                self.assertEqual(json.loads(bad_output.read_text(encoding="utf-8"))["status"], "needs_review")


if __name__ == "__main__":
    unittest.main()
