"""Bind explicit take inputs/stage files without loading or accepting them. Stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def contained(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError("artifact paths must be relative to root")
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f"missing or out-of-root artifact: {relative}")
    return path


def records(root, job):
    if job.get("schema_version") != 1 or not isinstance(job.get("take_id"), str) or not job["take_id"].strip():
        raise ValueError("require schema_version 1 and nonempty take_id")
    timing = job.get("timing", {})
    for name in ("fps_num", "fps_den", "frame_count"):
        if type(timing.get(name)) is not int or timing[name] < 1:
            raise ValueError(f"timing.{name} must be a positive integer")
    items = job.get("artifacts")
    if not isinstance(items, list) or not items:
        raise ValueError("artifacts must be a nonempty list")
    seen, roles, result = set(), set(), []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("artifact must be an object")
        label, role = item.get("id"), item.get("role")
        if not isinstance(label, str) or not label or label in seen:
            raise ValueError("artifact ids must be nonempty and unique")
        if role not in {"source", "settings", "stage", "reference", "audio", "mask"}:
            raise ValueError("unknown artifact role")
        seen.add(label)
        roles.add(role)
        path = contained(root, item.get("path"))
        before = path.stat()
        if before.st_size == 0:
            raise ValueError(f"empty artifact: {label}")
        sha = digest(path)
        after = path.stat()
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise ValueError(f"artifact changed while hashing: {label}")
        result.append({"id": label, "role": role, "path": item["path"],
                       "bytes": after.st_size, "sha256": sha})
    if not {"source", "settings", "stage"}.issubset(roles):
        raise ValueError("require source, settings and completed stage artifacts")
    return result


def freeze(root, spec, output):
    root = Path(root).resolve()
    spec, output = Path(spec).resolve(), Path(output).resolve()
    raw = spec.read_bytes()
    job = json.loads(raw.decode("utf-8-sig"))
    artifacts = records(root, job)
    if spec.read_bytes() != raw:
        raise ValueError("job specification changed while hashing")
    receipt = {"schema_version": 1, "take_id": job["take_id"],
               "job_sha256": hashlib.sha256(raw).hexdigest(), "artifacts": artifacts,
               "scope": "file identity only; native stage validity and content acceptance unmeasured"}
    # Exclusive creation also rejects an existing receipt or a source path.
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return receipt


def verify(root, spec, receipt_path):
    raw = Path(spec).read_bytes()
    job = json.loads(raw.decode("utf-8-sig"))
    receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8-sig"))
    if receipt.get("schema_version") != 1 or receipt.get("job_sha256") != hashlib.sha256(raw).hexdigest():
        raise ValueError("job changed: create a new take/receipt")
    current = records(Path(root).resolve(), job)
    if Path(spec).read_bytes() != raw:
        raise ValueError("job specification changed while verifying")
    if receipt.get("take_id") != job["take_id"] or receipt.get("artifacts") != current:
        raise ValueError("artifact changed or receipt mismatch: do not reuse stage")
    return {"take_id": job["take_id"], "files_verified": len(current),
            "result": "identity_match", "content_acceptance": "unmeasured"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["freeze", "verify"])
    parser.add_argument("--root", required=True)
    parser.add_argument("--job", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    try:
        function = freeze if args.action == "freeze" else verify
        result = function(args.root, args.job, args.receipt)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, AttributeError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    main()
