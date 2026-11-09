"""CPU-only package integrity checks; does not evaluate model quality."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import ast
import json
import re
import sys
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
from install_suite import load_suite

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
COUNTS = {"skills": 0, "links": 0, "json": 0, "python": 0, "text": 0}


def problem(path, message):
    ERRORS.append(f"{path.relative_to(ROOT)}: {message}")


def anchors(text):
    result = set()
    counts = {}
    for line in text.splitlines():
        if re.match(r"^#{1,6} ", line):
            heading = re.sub(r"^#{1,6} +", "", line).strip().lower()
            heading = re.sub(r"[^\w\s-]", "", heading, flags=re.UNICODE)
            base = re.sub(r"\s", "-", heading)
            duplicate = counts.get(base, 0)
            counts[base] = duplicate + 1
            result.add(base if not duplicate else f"{base}-{duplicate}")
    return result


def main():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(p in {".git", ".venv", "__pycache__"} for p in path.relative_to(ROOT).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (UnicodeError, OSError) as exc:
            problem(path, f"cannot read UTF-8 text: {exc}")
            continue
        COUNTS["text"] += 1
        # These patterns catch accidental host-specific data, not all secrets.
        patterns = {
            "absolute Windows path": r"(?i)\b[A-Z]:[/\\]",
            "private IPv4": r"\b(?:192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)\b",
            "credential URL": r"https?://[^/\s@]+:[^/\s@]+@",
        }
        for label, pattern in patterns.items():
            if re.search(pattern, text):
                problem(path, label)
        try:
            if path.name == "SKILL.md":
                if not text.startswith("---\n"):
                    raise ValueError("missing YAML frontmatter")
                front = yaml.safe_load(text.split("---", 2)[1])
                if front.get("name") != path.parent.name:
                    raise ValueError("skill name differs from directory")
                if not isinstance(front.get("description"), str) or not front["description"].strip():
                    raise ValueError("missing description")
                COUNTS["skills"] += 1
            elif path.suffix in {".yaml", ".yml"}:
                yaml.safe_load(text)
            elif path.suffix == ".json":
                json.loads(text)
                COUNTS["json"] += 1
            elif path.suffix == ".py":
                ast.parse(text, filename=str(path))
                COUNTS["python"] += 1
        except (ValueError, SyntaxError, yaml.YAMLError, AttributeError) as exc:
            problem(path, str(exc))
        if path.suffix == ".md":
            for href in re.findall(r"\]\(([^\s)]+)\)", text):
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc:
                    continue
                target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
                if not target.is_relative_to(ROOT) or not target.is_file():
                    problem(path, f"missing/internal link outside package: {href}")
                    continue
                COUNTS["links"] += 1
                if parsed.fragment and target.suffix == ".md":
                    if unquote(parsed.fragment) not in anchors(target.read_text(encoding="utf-8-sig")):
                        problem(path, f"missing heading: {href}")
    try:
        _, roster = load_suite(ROOT)
        if COUNTS["skills"] != len(roster):
            ERRORS.append("skill count differs from suite manifest")
    except (ValueError, KeyError, OSError) as exc:
        ERRORS.append(f"skill-suite.json: {exc}")
    print(json.dumps({"counts": COUNTS, "errors": ERRORS}, ensure_ascii=False, indent=2))
    return bool(ERRORS)


if __name__ == "__main__":
    sys.exit(main())
