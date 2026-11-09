"""Turn one camera of a set.json into a scene file for the foyege-cinematic-direction previs script.

    python to_previs.py --set set.json --camera C1 --out previs_C1.json [--frames 121] [--fps 24] [--res 1280x704]

The previs room then has the same walls, door leaves and furniture as the blockout (all as boxes, ceiling left out
so the previs light reaches the floor; the camera's wild wall is left out too). Actors from set.json are copied
as standing figures at their marks, and the camera is copied as a still shot. Edit the keys in the output to block
the movement, then run build_previs.py from the foyege skill on it.

Limits of that previs script: actors are always standing, 1.6 m tall; boxes have no rotation (fine here, since
set.json yaw is a multiple of 90 and the parts are already turned).
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True  # keep __pycache__ out of the skill folder
_spec = importlib.util.spec_from_file_location("plan_check", HERE / "plan_check.py")
pc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pc)

COLORS = [(0.85, 0.35, 0.3), (0.3, 0.5, 0.85), (0.35, 0.7, 0.4), (0.85, 0.7, 0.3)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", type=Path, required=True)
    ap.add_argument("--camera", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--frames", type=int, default=121)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--res", default="1280x704")
    args = ap.parse_args()
    data = json.loads(args.set.read_text(encoding="utf-8-sig"))
    pc.validate(data)
    cams = {c["id"]: c for c in data.get("cameras", [])}
    if args.camera not in cams:
        raise SystemExit(f"camera {args.camera} not in {sorted(cams)}")
    if args.out.exists():
        raise SystemExit(f"{args.out} already exists")
    cam = cams[args.camera]
    wild = cam.get("wild_wall")

    boxes = []

    def add_box(name, b):
        x0, y0, z0, x1, y1, z1 = b
        boxes.append({"id": name, "location": [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2],
                      "size": [x1 - x0, y1 - y0, z1 - z0]})

    for name, wall, b in pc.wall_pieces(data) + pc.door_leaves(data):
        if wall != wild:
            add_box(name, b)
    for it in data.get("items", []):
        for name, c, s in pc.item_parts(it):
            boxes.append({"id": name, "location": list(c), "size": list(s)})

    notes = []
    if any(it.get('shape') in pc.fg.SHAPES for it in data.get('items', [])):
        notes.append('detailed furniture curves are approximated by component bounding boxes; ring holes use segmented bounds, not one solid box')
    if cam.get("level"):
        notes.append("level camera shift is not supported by the previs camera; framing is not identical to the blockout")
    actors = []
    for i, a in enumerate(data.get("actors", [])):
        if "actors" in cam and a["id"] not in cam["actors"]:
            continue
        loc = [a["center"][0], a["center"][1], a.get("base", 0.0)]
        actors.append({"id": a["id"], "color": list(COLORS[i % len(COLORS)]), "yaw_deg": a.get("yaw", 0),
                       "keys": [{"frame": 1, "location": loc}, {"frame": args.frames, "location": loc}]})
        if a.get("pose", "stand") != "stand" or abs(a.get("height", 1.6) - 1.6) > 0.05:
            notes.append(f"{a['id']}: previs shows a standing 1.6 m figure; set.json says {a.get('pose', 'stand')}, "
                         f"{a.get('height', 1.6)} m")
            if a.get("on"):
                # a standing figure would collide with the seat; keep the seat, move the figure out of it is the user's call
                notes.append(f"{a['id']}: overlaps {a['on']} in previs because the figure cannot sit")

    room = data["room"]
    res = [int(v) for v in args.res.lower().split("x")]
    scene = {
        "frames": args.frames, "fps": args.fps, "resolution": res,
        "actors": actors, "boxes": boxes,
        "camera": {"lens_mm": cam["lens"], "keys": [
            {"frame": 1, "location": cam["location"], "look_at": cam["look_at"]},
            {"frame": args.frames, "location": cam["location"], "look_at": cam["look_at"]}]},
        "topview": {"center": [room["width"] / 2, room["depth"] / 2, 0.0], "height": room["height"] + 5,
                    "ortho_scale": max(room["width"], room["depth"]) + 1.0},
        "source": {"set": data["id"], "version": data.get("version"), "camera": cam["id"], "wild_wall": wild,
                   "notes": notes},
    }
    args.out.write_text(json.dumps(scene, ensure_ascii=False, indent=1), encoding="utf-8")
    sys.stdout.write(json.dumps({"boxes": len(boxes), "actors": len(actors), "notes": len(notes)}) + "\n")


if __name__ == "__main__":
    main()
