"""Optional CPU calibration of an explicitly supplied T8 visible_face_mask module."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", required=True, help="reviewed T8 h3_t8/visible_face_mask.py")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    # This is synthetic arithmetic calibration, not inference or a GPU benchmark.
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    import numpy as np
    import torch
    from PIL import Image
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    from audit_visible_face import audit
    module_path = Path(args.module).resolve()
    module_sha = hashlib.sha256(module_path.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location("reviewed_t8_visible_mask", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=False)
    roots = [output / name for name in ["source", "candidate", "mask", "result"]]
    for root in roots:
        root.mkdir()
    base = np.full((12, 90, 160, 3), 40, dtype=np.uint8)
    candidate = base.copy()
    mask = np.zeros((12, 90, 160), dtype=np.uint8)
    alpha = np.zeros_like(mask, dtype=np.float32)
    for frame in range(12):
        x = 20 + frame
        candidate[frame, 20:70, x:x+50] = 100  # already blended result
        alpha[frame, 20:70, x:x+50] = .5
        mask[frame, 20:70, x+15:x+30] = 128
        mask[frame, 20:70, x+30:x+50] = 255
    b = torch.from_numpy(base.astype(np.float32) / 255)
    c = torch.from_numpy(candidate.astype(np.float32) / 255)
    v = torch.from_numpy(mask.astype(np.float32) / 255)
    binding = module.capture(b, v, fps=24, source_start_frame=0, broadcast_single_mask=False)
    sentinel = {"scope": "object identity only, not actual audio"}
    composed, audio, _, native_json = module.composite(binding, c, torch.from_numpy(alpha), sentinel)
    if audio is not sentinel or torch.cuda.is_initialized():
        raise RuntimeError("audio object changed or unexpected CUDA initialization")
    rendered = (composed * 255).round().to(torch.uint8).numpy()
    for frame in range(12):
        for root, array in zip(roots, [base, candidate, mask, rendered]):
            Image.fromarray(array[frame]).save(root / f"{frame:06d}.png")
    report = audit(*roots, 12)
    if hashlib.sha256(module_path.read_bytes()).hexdigest() != module_sha:
        raise RuntimeError("native implementation changed during calibration")
    report.update({"native_module_sha256": module_sha, "native_report": json.loads(native_json),
                   "cuda_initialized": torch.cuda.is_initialized(),
                   "scope": "12 synthetic CPU frames; no detector, H3 sampling, video PTS or acting validation"})
    (output / "audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": report["result"], "totals": report["totals"],
                      "cuda_initialized": report["cuda_initialized"]}, indent=2))
    return 0 if report["result"] == "pixel_pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
