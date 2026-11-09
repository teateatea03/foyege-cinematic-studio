"""Translate timed SRT locally using an explicitly supplied Index Translate runtime.

No models, vendor source, package installation or automatic CPU fallback are bundled.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time


def validate_formatting(cues):
    """Support plain text or one whole-cue style; reject mixed spans before loading."""
    for cue in cues:
        if ("<" in cue.text or "{\\" in cue.text) and not re.fullmatch(
            r"<(i|b|u)>[^<>]+</\1>", cue.text, re.S
        ):
            raise ValueError("Mixed inline styles require manual review; use plain cues or whole-cue i/b/u")


def translate_cue(translator, text, source, target, budget, glossary):
    """Keep whole-cue format tokens outside the model; scope glossary to this cue."""
    wrapped = re.fullmatch(r"(%%IT_[A-Za-z0-9_]+%%)(.+?)(%%IT_[A-Za-z0-9_]+%%)", text, re.S)
    body = wrapped.group(2) if wrapped else text
    active_terms = {key: value for key, value in glossary.items() if key in body}
    result = translator.translate(body, source, target, budget, active_terms)
    if wrapped:
        result = {**result, "text": wrapped.group(1) + result["text"] + wrapped.group(3)}
    return result


def write_new(path, content):
    """Publish a complete file atomically without replacing an existing destination."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".subtitle-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--vendor", required=True, type=Path, help="Directory containing index_translate_core")
    parser.add_argument("--packages", required=True, type=Path, help="Isolated compatible Python packages")
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--cuda-device", required=True, help="Authorized GPU UUID or CUDA device selector")
    parser.add_argument("--source", default="zh")
    parser.add_argument("--target", default="en")
    parser.add_argument("--glossary", type=Path)
    parser.add_argument("--bilingual", action="store_true")
    parser.add_argument("--output-budget", type=int, default=256)
    args = parser.parse_args()
    receipt = args.output.with_suffix(args.output.suffix + ".receipt.json")
    if args.output.exists() or receipt.exists():
        raise FileExistsError("Choose new output and receipt paths; existing artifacts are retained")
    if not (args.vendor / "index_translate_core/__init__.py").is_file():
        raise ValueError("Missing Index Translate runtime source")
    if not args.packages.is_dir() or not args.model.is_dir():
        raise ValueError("Missing isolated packages or model directory")
    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda_device
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    sys.path.insert(0, str(args.packages.resolve()))
    sys.path.insert(0, str(args.vendor.resolve()))
    from index_translate_core.subtitles import decode_srt, parse_srt, translate_srt

    raw = args.input.read_bytes()
    text = decode_srt(raw)
    cues = parse_srt(text)
    validate_formatting(cues)
    glossary = json.loads(args.glossary.read_text(encoding="utf-8-sig")) if args.glossary else {}
    if not isinstance(glossary, dict) or len(glossary) > 100 or any(
        not isinstance(k, str) or not k or not isinstance(v, str) for k, v in glossary.items()
    ):
        raise ValueError("Glossary must contain at most 100 nonempty string keys and string values")
    import torch
    import transformers
    import tokenizers
    import safetensors
    from index_translate_core.inference import LocalTranslator

    if torch.cuda.device_count() != 1:
        raise RuntimeError("Select exactly one authorized CUDA device; no CPU fallback")
    started = time.monotonic()
    translator = None
    details = []
    try:
        translator = LocalTranslator(args.model, "cuda", "bf16", 4096)

        def translate(body):
            result = translate_cue(translator, body, args.source, args.target, args.output_budget, glossary)
            details.append(result)
            return result

        translated, metadata = translate_srt(
            text, translate, bilingual=args.bilingual,
            progress=lambda done, total: print(f"cue {done}/{total}", flush=True),
        )
        output_cues = parse_srt(translated)
        if [(c.number, c.timing) for c in cues] != [(c.number, c.timing) for c in output_cues]:
            raise ValueError("Cue numbers or timecodes changed")
        report = {
            "input_sha256": hashlib.sha256(raw).hexdigest(),
            "model_revision": translator.model_info["revision"],
            "device": torch.cuda.get_device_name(0), "precision": translator.precision,
            "transformers": transformers.__version__, "tokenizers": tokenizers.__version__,
            "safetensors": safetensors.__version__, "acceleration": translator.acceleration_info,
            "metadata": metadata, "results": details,
            "seconds": round(time.monotonic() - started, 3),
            "output_sha256": hashlib.sha256(translated.encode("utf-8-sig")).hexdigest(),
            "review_status": "requires_semantic_and_readability_review",
        }
    finally:
        if translator is not None:
            translator.release()
    write_new(args.output, translated.encode("utf-8-sig"))
    write_new(receipt, (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"output": str(args.output), "cues": len(cues), "device": report["device"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
