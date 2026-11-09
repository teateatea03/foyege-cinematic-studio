"""Audit complete RGB8/L8 PNG sequences after native visible-face composition."""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path

import numpy as np
from PIL import Image


def read_png(path, mode):
    raw = path.read_bytes()
    with Image.open(BytesIO(raw)) as image:
        if image.format != "PNG" or image.mode != mode:
            raise ValueError(f"{path.name}: require PNG mode {mode}, no implicit conversion")
        array = np.asarray(image).copy()
    return array, hashlib.sha256(raw).hexdigest()


def audit(source, candidate, mask, result, frame_count):
    if type(frame_count) is not int or frame_count < 1:
        raise ValueError("frame_count must be positive")
    roots = [Path(p) for p in (source, candidate, mask, result)]
    names = [f"{i:06d}.png" for i in range(frame_count)]
    for root in roots:
        if not root.is_dir() or {p.name for p in root.iterdir() if p.is_file()} != set(names):
            raise ValueError("each sequence must contain exactly 000000.png through frame_count-1")
    rows, geometry = [], None
    totals = {"protected_pixels": 0, "protected_changed": 0, "white_changed": 0,
              "formula_mismatch": 0, "candidate_changed_pixels": 0}
    for name in names:
        loaded = [read_png(root / name, mode) for root, mode in zip(roots, ["RGB", "RGB", "L", "RGB"])]
        (b, _), (c, _), (v, _), (r, _) = loaded
        if b.shape != c.shape or b.shape != r.shape or b.shape[:2] != v.shape:
            raise ValueError(f"{name}: geometry mismatch")
        if geometry is not None and geometry != b.shape:
            raise ValueError(f"{name}: sequence geometry changed")
        geometry = b.shape
        # C is already blended. Do not multiply by its earlier alpha a second time.
        expected = np.rint(b.astype(np.float32) + (c.astype(np.float32) - b) * (v[..., None] / np.float32(255)))
        delta = np.max(np.abs(r.astype(np.float32) - expected), axis=2)
        protected = v == 0
        white = v == 255
        counts = {
            "protected_pixels": int(protected.sum()),
            "protected_changed": int((protected & np.any(r != b, axis=2)).sum()),
            "white_changed": int((white & np.any(r != c, axis=2)).sum()),
            "formula_mismatch": int((delta > 1).sum()),
            "candidate_changed_pixels": int(np.any(c != b, axis=2).sum()),
        }
        for key, count in counts.items():
            totals[key] += count
        rows.append({"frame": name, **counts, "max_code_value_error": float(delta.max()),
                     "sha256": dict(zip(["source", "candidate", "mask", "result"], [sha for _, sha in loaded]))})
    passed = not any(totals[key] for key in ["protected_changed", "white_changed", "formula_mismatch"])
    return {"schema_version": 1, "result": "pixel_pass" if passed else "pixel_fail",
            "frame_count": frame_count, "width": geometry[1], "height": geometry[0],
            "totals": totals, "frames": rows, "fractional_mask_tolerance_code_values": 1,
            "scope": "RGB8 encoded values; no color conversion, PTS, audio, tracking or acting acceptance",
            "content_acceptance": "unmeasured"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ["source", "candidate", "mask", "result"]:
        parser.add_argument("--" + option, required=True)
    parser.add_argument("--frame-count", required=True, type=int)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    try:
        if Path(args.report).exists():
            raise ValueError("report exists; choose a new path")
        report = audit(args.source, args.candidate, args.mask, args.result, args.frame_count)
        with Path(args.report).open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        print(json.dumps({key: value for key, value in report.items() if key != "frames"}, ensure_ascii=False, indent=2))
        return 0 if report["result"] == "pixel_pass" else 2
    except (OSError, ValueError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
