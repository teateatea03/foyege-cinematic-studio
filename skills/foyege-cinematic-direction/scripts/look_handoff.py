"""Check declared look handoffs; no pixel measurement, LUT application or color conversion."""
import argparse
import hashlib
import json
from pathlib import Path
import re

COMMON = ("working_space", "view_transform", "display", "world_light_id", "color_config_sha256")
COLOR = ("primaries", "transfer", "matrix", "range")


def text_or_unknown(value, field):
    if value is not None and (not isinstance(value, str) or not value.strip()):
        raise ValueError(f"{field} must be null or a nonempty string")
    if field.endswith("sha256") and value is not None and not re.fullmatch("[0-9a-f]{64}", value):
        raise ValueError(f"{field} must be lowercase SHA256")
    return value


def fields(obj, keys):
    if not isinstance(obj, dict) or any(key not in obj for key in keys):
        raise ValueError("missing declared fields; use explicit null for unknown values")
    return {key: text_or_unknown(obj[key], key) for key in keys}


def build(data):
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("require schema_version 1")
    if not isinstance(data.get("look_group"), str) or not data["look_group"].strip():
        raise ValueError("require look_group")
    light_note = text_or_unknown(data.get("world_light_note"), "world_light_note")
    baseline = fields(data["baseline"], COMMON)
    output = fields(data["baseline"].get("output_color"), COLOR)
    if not isinstance(data.get("shots"), list) or not data["shots"]:
        raise ValueError("require nonempty shots")
    issues, unknowns, rows, shot_ids = [], [], [], set()
    for key, value in {**baseline, **{"output_color." + k: v for k, v in output.items()}}.items():
        if value is None:
            unknowns.append({"shot_id": None, "field": "baseline." + key})
    for shot in data["shots"]:
        shot_id = shot.get("shot_id")
        if not isinstance(shot_id, str) or not shot_id.strip() or shot_id in shot_ids:
            raise ValueError("shot IDs must be nonempty and unique")
        shot_ids.add(shot_id)
        common = fields(shot, COMMON)
        source_color = fields(shot.get("input_color"), COLOR)
        target_color = fields(shot.get("output_color"), COLOR)
        input_transform = text_or_unknown(shot.get("input_transform"), "input_transform")
        reasons = shot.get("intentional_changes", {})
        if not isinstance(reasons, dict) or any(not isinstance(v, str) or not v.strip() for v in reasons.values()):
            raise ValueError("intentional_changes must map field names to nonempty reasons")
        for key, value in {**common, "input_transform": input_transform,
                           **{"input_color." + k: v for k, v in source_color.items()},
                           **{"output_color." + k: v for k, v in target_color.items()}}.items():
            if value is None:
                unknowns.append({"shot_id": shot_id, "field": key})
        for key, expected in {**baseline, **{"output_color." + k: v for k, v in output.items()}}.items():
            actual = target_color[key.split(".", 1)[1]] if key.startswith("output_color.") else common[key]
            if actual is not None and expected is not None and actual != expected:
                issues.append({"shot_id": shot_id, "kind": "baseline_difference", "field": key,
                               "expected": expected, "declared": actual,
                               "intentional_reason": reasons.get(key)})
        hashes, ids, look_rows = {}, {}, []
        for stage in ("baked_looks", "planned_looks"):
            looks = shot.get(stage)
            if not isinstance(looks, list):
                raise ValueError(f"{stage} must be a list")
            for look in looks:
                name = text_or_unknown(look.get("id"), "look.id")
                if name is None:
                    raise ValueError("look requires id")
                sha = text_or_unknown(look.get("sha256"), "look.sha256")
                if sha is None:
                    unknowns.append({"shot_id": shot_id, "field": stage + "." + name + ".sha256"})
                if sha is not None and sha in hashes:
                    issues.append({"shot_id": shot_id, "kind": "repeated_look_bytes",
                                   "look_id": name, "first_stage": hashes[sha], "stage": stage})
                if name in ids:
                    old_sha = ids[name]
                    kind = ("look_id_reused_with_different_bytes" if old_sha and sha and old_sha != sha
                            else "repeated_look_id")
                    issues.append({"shot_id": shot_id, "kind": kind, "look_id": name})
                ids[name] = sha
                if sha is not None:
                    hashes[sha] = stage
                look_rows.append({"id": name, "sha256": sha, "stage": stage})
        rows.append({"shot_id": shot_id, **common, "input_color": source_color,
                     "input_transform": input_transform, "output_color": target_color,
                     "looks": look_rows, "intentional_changes": reasons})
    return {"schema_version": 1, "look_group": data["look_group"], "world_light_note": light_note,
            "status": "needs_review" if issues else ("needs_binding" if unknowns else "handoff_consistent"),
            "baseline": data["baseline"], "shots": rows, "issues": issues, "unknowns": unknowns,
            "scope": "declared metadata only; no measured tags, OCIO validation, lighting or pixel matching",
            "content_acceptance": "unmeasured"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        raw = Path(args.input).read_bytes()
        report = build(json.loads(raw.decode("utf-8-sig")))
        report["spec_sha256"] = hashlib.sha256(raw).hexdigest()
        with Path(args.output).open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        print(json.dumps({"status": report["status"], "issues": report["issues"],
                          "unknown_fields": len(report["unknowns"])}, ensure_ascii=False))
        return 1 if report["issues"] else 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
