"""Install complete skill directories without replacing existing installations."""
import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", ".venv", "__pycache__"}


def load_suite(root):
    root = Path(root).resolve()
    data = json.loads((root / "skill-suite.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("unsupported suite schema")
    roster = {}
    for skill in data["skills"]:
        name = skill["name"]
        if not isinstance(name, str) or not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in name):
            raise ValueError(f"invalid skill name: {name!r}")
        if name in roster or skill["path"] != f"skills/{name}":
            raise ValueError(f"duplicate name or unexpected skill path: {name}")
        source = root / skill["path"]
        if source.is_symlink() or not source.resolve().is_relative_to(root) or not (source / "SKILL.md").is_file():
            raise ValueError(f"unsafe or missing skill: {name}")
        for entry in source.rglob("*"):
            if entry.is_symlink() or not entry.resolve().is_relative_to(source.resolve()):
                raise ValueError(f"unsafe source entry: {entry}")
        roster[name] = skill
    actual = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    if actual != set(roster):
        raise ValueError(f"manifest/skill roster mismatch: {actual ^ set(roster)}")
    for skill in roster.values():
        deps = skill.get("requires", [])
        if not isinstance(deps, list) or any(dep not in roster for dep in deps):
            raise ValueError(f"unknown dependencies: {skill['name']}")
    profiles = data["profiles"]
    if not profiles or any(not isinstance(v, list) or not v or any(n not in roster for n in v) for v in profiles.values()):
        raise ValueError("invalid profiles")
    return data, roster


def selected_skills(roster, names):
    selected = set()
    pending = list(names)
    while pending:
        name = pending.pop()
        if name not in roster:
            raise ValueError(f"unknown skill: {name}")
        if name not in selected:
            selected.add(name)
            pending.extend(roster[name].get("requires", []))
    return sorted(selected)


def install(root, destination, names):
    root = Path(root).resolve()
    _, roster = load_suite(root)
    selected = selected_skills(roster, names)
    destination = Path(destination).expanduser().resolve()
    if destination == root or destination.is_relative_to(root):
        raise ValueError("destination must be outside the source checkout")
    if destination.exists() and not destination.is_dir():
        raise ValueError("destination is not a directory")
    # Preflight the whole selection before copying any skill.
    collisions = [name for name in selected if (destination / name).exists() or (destination / name).is_symlink()]
    if collisions:
        raise ValueError("existing skills; compare/back up separately: " + ", ".join(collisions))
    destination.mkdir(parents=True, exist_ok=True)
    for name in selected:
        shutil.copytree(root / roster[name]["path"], destination / name,
                        ignore=shutil.ignore_patterns(*IGNORED, "*.pyc"))
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, required=True, help="Codex/Claude skill root or a fresh test directory")
    parser.add_argument("--profile", default="crew", help="crew (default) or director")
    parser.add_argument("--skills", nargs="+", help="explicit selection; adds all packaging dependencies")
    args = parser.parse_args()
    try:
        data, _ = load_suite(ROOT)
        names = args.skills if args.skills else data["profiles"][args.profile]
        result = install(ROOT, args.destination, names)
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(1, f"Install failed: {exc}\n")
    print(json.dumps({"destination": str(args.destination.resolve()), "installed": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
