"""Check a set layout (set.json) and draw its floor plan.

Plain Python 3.10+ with Pillow. No Blender, no GPU.

    python plan_check.py --set set.json --out OUT_DIR

Writes OUT_DIR/plan.png (labelled floor plan) and OUT_DIR/plan_check.json
(every check with PASS / WARN / FAIL). OUT_DIR must not exist yet.
The schema is described in references/set-json.md.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
import os


WALLS = ("S", "N", "W", "E")
EPS = 0.01  # 1 cm tolerance
sys.dont_write_bytecode = True
_fg_spec = importlib.util.spec_from_file_location("furniture_geometry", Path(__file__).resolve().parent / "furniture_geometry.py")
fg = importlib.util.module_from_spec(_fg_spec)
_fg_spec.loader.exec_module(fg)


# ---------- geometry ----------

def rect_of(item):
    """Axis-aligned footprint (x0, y0, x1, y1) of an item; yaw must be 0/90/180/270."""
    w, d = item["size"][0], item["size"][1]
    if int(item.get("yaw", 0)) % 180 == 90:
        w, d = d, w
    cx, cy = item["center"]
    return (cx - w / 2, cy - d / 2, cx + w / 2, cy + d / 2)


def front_vec(yaw):
    """Unit vector the item's front faces. yaw 0 faces -Y, 90 faces +X (counterclockwise from above)."""
    a = math.radians(yaw)
    return (math.sin(a), -math.cos(a))


def front_zone(item):
    """Rectangle in front of an item that must stay free (front_clear metres deep)."""
    depth = item.get("front_clear", 0)
    if depth <= 0:
        return None
    x0, y0, x1, y1 = rect_of(item)
    fx, fy = front_vec(item.get("yaw", 0))
    if fy < -0.5:
        return (x0, y0 - depth, x1, y0)
    if fy > 0.5:
        return (x0, y1, x1, y1 + depth)
    if fx > 0.5:
        return (x1, y0, x1 + depth, y1)
    return (x0 - depth, y0, x0, y1)


def overlap(a, b, tol=EPS):
    return a[0] < b[2] - tol and b[0] < a[2] - tol and a[1] < b[3] - tol and b[1] < a[3] - tol


def point_rect_dist(px, py, r):
    dx = max(r[0] - px, 0, px - r[2])
    dy = max(r[1] - py, 0, py - r[3])
    return math.hypot(dx, dy)


def opening_span(op, room):
    """Return (x0, y0, x1, y1) of an opening on the inner wall line."""
    W, D = room["width"], room["depth"]
    a, b = op["offset"], op["offset"] + op["width"]
    return {"S": (a, 0, b, 0), "N": (a, D, b, D), "W": (0, a, 0, b), "E": (W, a, W, b)}[op["wall"]]


INWARD = {"S": (0, 1), "N": (0, -1), "W": (1, 0), "E": (-1, 0)}


def door_hinge(op, room):
    """Hinge point and far jamb. hinge left/right is seen from inside the room, facing the door."""
    x0, y0, x1, y1 = opening_span(op, room)
    nx, ny = INWARD[op["wall"]]
    left = (ny, -nx)  # left of the facing direction (-nx, -ny)
    ends = [(x0, y0), (x1, y1)]
    ends.sort(key=lambda p: p[0] * left[0] + p[1] * left[1], reverse=True)
    return (ends[0], ends[1]) if op.get("hinge", "left") == "left" else (ends[1], ends[0])


def door_swing_zone(op, room):
    """Square the door leaf sweeps (approximates the quarter circle) for an inward door."""
    x0, y0, x1, y1 = opening_span(op, room)
    w = op["width"]
    if op.get("swing", "in") != "in":
        return None
    return {"S": (x0, 0, x1, w), "N": (x0, room["depth"] - w, x1, room["depth"]),
            "W": (0, y0, w, y1), "E": (room["width"] - w, y0, room["width"], y1)}[op["wall"]]


# ---------- 3D parts (shared with build_set.py and to_previs.py; plain Python, no Blender) ----------

def opening_z(op):
    """(sill, head) heights of an opening."""
    sill = op.get("sill", 0.9 if op["type"] == "window" else 0.0)
    return sill, sill + op.get("height", 1.2 if op["type"] == "window" else 2.05)


def wall_pieces(data):
    """Wall boxes split around openings: list of (name, wall, (x0, y0, z0, x1, y1, z1))."""
    room = data["room"]
    W, D, H, T = room["width"], room["depth"], room["height"], room.get("wall", 0.12)
    out = []
    for wall in WALLS:
        length = W if wall in "SN" else D

        def piece(tag, a, b, z0, z1):
            if b - a < 1e-4 or z1 - z0 < 1e-4:
                return
            if wall in "SN":  # S and N walls run over the corners so the corners are closed
                a2 = -T if a <= 1e-6 else a
                b2 = W + T if b >= W - 1e-6 else b
                y0, y1 = (-T, 0) if wall == "S" else (D, D + T)
                out.append((f"wall_{wall}_{tag}", wall, (a2, y0, z0, b2, y1, z1)))
            else:
                x0, x1 = (-T, 0) if wall == "W" else (W, W + T)
                out.append((f"wall_{wall}_{tag}", wall, (x0, a, z0, x1, b, z1)))

        pos, n = 0.0, 0
        for op in sorted((o for o in data.get("openings", []) if o["wall"] == wall), key=lambda o: o["offset"]):
            sill, head = opening_z(op)
            piece(f"solid{n}", pos, op["offset"], 0, H)
            piece(f"{op['id']}_below", op["offset"], op["offset"] + op["width"], 0, sill)
            piece(f"{op['id']}_above", op["offset"], op["offset"] + op["width"], min(head, H), H)
            pos, n = op["offset"] + op["width"], n + 1
        piece(f"solid{n}", pos, length, 0, H)
    return out


def door_leaves(data):
    """Door leaf boxes: list of (name, wall, (x0, y0, z0, x1, y1, z1)). leaf: closed (default), open, none."""
    room = data["room"]
    T = room.get("wall", 0.12)
    out = []
    for op in data.get("openings", []):
        state = op.get("leaf", "closed")
        if op["type"] != "door" or state == "none":
            continue
        _sill, head = opening_z(op)
        hinge, far = door_hinge(op, room)
        nx, ny = INWARD[op["wall"]]
        w, t = op["width"], 0.04
        if state == "open":
            s = 1 if op.get("swing", "in") == "in" else -1
            cx, cy = hinge[0] + s * nx * w / 2, hinge[1] + s * ny * w / 2
            sx, sy = (t, w) if op["wall"] in "SN" else (w, t)
        else:
            cx, cy = (hinge[0] + far[0]) / 2 - nx * T / 2, (hinge[1] + far[1]) / 2 - ny * T / 2
            sx, sy = (w, t) if op["wall"] in "SN" else (t, w)
        out.append((f"door_{op['id']}", op["wall"], (cx - sx / 2, cy - sy / 2, 0, cx + sx / 2, cy + sy / 2, head)))
    return out


def rot90(yaw, x, y):
    c, s = round(math.cos(math.radians(yaw))), round(math.sin(math.radians(yaw)))
    return x * c - y * s, x * s + y * c


BOOTH_T = 0.05  # booth shell thickness


def booth_door(it, w, d, h, t, step):
    """Booth door in item coordinates (front faces -Y), with a window in it so the inside stays visible.
    door: closed (default), open (swung out 90 degrees), slide (slid back along the outside of the hinge-side panel),
    none; hinge left/right as seen standing in front of it."""
    state = it.get("door", "closed")
    if state == "none":
        return []
    lw, z0, z1 = w - 2 * t, step + 0.02, h - t - 0.02
    hs = 1 if it.get("hinge", "right") == "right" else -1
    hx = hs * (w / 2 - t)
    wz0, wz1, s = z0 + 0.9, z1 - 0.2, 0.1
    if state == "slide" or wz1 - wz0 < 0.3:
        bars = [(lw / 2, lw, z0, z1)]
    else:  # bottom rail, top rail, two stiles around the window
        bars = [(lw / 2, lw, z0, wz0), (lw / 2, lw, wz1, z1), (s / 2, s, wz0, wz1), (lw - s / 2, s, wz0, wz1)]
    out = []
    for i, (u, us, za, zb) in enumerate(bars):  # u runs from the hinge across the leaf
        if state == "open":
            out.append((f"__door{i}", (hx, -d / 2 - u, (za + zb) / 2), (t, us, zb - za)))
        elif state == "slide":
            out.append((f"__door{i}", (hs * (w / 2 + t / 2), -d / 2 + u, (za + zb) / 2), (t, us, zb - za)))
        else:
            out.append((f"__door{i}", (hx - hs * u, -d / 2 + t / 2, (za + zb) / 2), (us, t, zb - za)))
    return out


def part_box(c, s):
    return (c[0] - s[0] / 2, c[1] - s[1] / 2, c[2] - s[2] / 2, c[0] + s[0] / 2, c[1] + s[1] / 2, c[2] + s[2] / 2)


def item_parts(it):
    """World-axis boxes making up an item: list of (name, (cx, cy, cz), (sx, sy, sz)).
    shape: box (default), chair (seat plus backrest), table (top plus four legs), booth (open-front shell with a
    door, for a pod, closet or phone booth; seat is the height of its raised floor). The first part is named by the id."""
    w, d, h = it["size"]
    base, yaw = it.get("base", 0.0), int(it.get("yaw", 0)) % 360
    shape = it.get("shape", "box")
    parts = []  # item coordinates: front faces -Y
    if shape in fg.SHAPES:
        parts = [("__"+suffix,c,s) for p in fg.primitives(it) for suffix,c,s in fg.local_boxes(p)]
        mark_z, mark_h = h*0.6, 0.03
    elif shape == "booth":
        t, step = BOOTH_T, it.get("seat", 0.0)
        parts.append(("", (0, d / 2 - t / 2, h / 2), (w, t, h)))  # back panel
        for i, sx in enumerate((-1, 1)):
            parts.append((f"__side{i}", (sx * (w / 2 - t / 2), -t / 2, h / 2), (t, d - t, h)))
        parts.append(("__roof", (0, -t / 2, h - t / 2), (w - 2 * t, d - t, t)))
        if step > 0:
            parts.append(("__step", (0, -t / 2, step / 2), (w - 2 * t, d - t, step)))
        parts += booth_door(it, w, d, h, t, step)
        mark_z, mark_h = h - t / 2, t
    elif shape == "chair":
        seat = it.get("seat", 0.46)
        parts.append(("", (0, 0, seat / 2), (w, d, seat)))
        parts.append(("__back", (0, d / 2 - 0.03, (seat + h) / 2), (w, 0.06, h - seat)))
        mark_z, mark_h = seat * 0.6, max(0.03, seat * 0.2)
    elif shape == "table":
        top, leg = 0.04, 0.05
        parts.append(("", (0, 0, h - top / 2), (w, d, top)))
        for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (-1, 1), (1, 1))):
            parts.append((f"__leg{i}", (sx * (w / 2 - leg / 2), sy * (d / 2 - leg / 2), (h - top) / 2), (leg, leg, h - top)))
        mark_z, mark_h = h - top / 2, top
    else:
        parts.append(("", (0, 0, h / 2), (w, d, h)))
        mark_z, mark_h = h * 0.6, max(0.03, h * 0.2)
    if it.get("front_mark", True):
        parts.append(("__front", (0, -d / 2 - 0.006, mark_z), (w * 0.6, 0.012, mark_h)))
    out = []
    for suffix, (lx, ly, lz), (sw, sd, sh) in parts:
        wx, wy = rot90(yaw, lx, ly)
        if yaw % 180 == 90:
            sw, sd = sd, sw
        out.append((it["id"] + suffix, (it["center"][0] + wx, it["center"][1] + wy, base + lz), (sw, sd, sh)))
    return out


def actor_body(a):
    """Proxy body in the actor's own coordinates (front faces -Y, origin at the actor's floor, see base).
    Heights for sitting are estimates: head top about seat + 0.52 x height, eyes about seat + 0.45 x height.
    slump (asleep face down on a desk whose top is rest high) is a rough estimate too."""
    H, pose = a.get("height", 1.6), a.get("pose", "stand")
    s = a.get("seat", 0.46)
    legs = [("__thigh", (0, -0.22, s + 0.07), (0.34, 0.44, 0.14)), ("__shin", (0, -0.42, s / 2), (0.3, 0.12, s))]
    if pose == "sit":
        top, eye = s + 0.52 * H, s + 0.45 * H
        capsule, head = (0.16, s, top - 0.22), (0, 0, top - 0.11)
        boxes = legs
    elif pose == "slump":
        rest = a.get("rest", 0.75)
        top, eye = rest + 0.30, rest + 0.19
        capsule, head = (0.16, s, s + 0.34), (0.08, -0.56, rest + 0.19)
        boxes = legs + [("__chest", (0, -0.25, (s + rest) / 2 + 0.24), (0.40, 0.40, 0.24)),
                        ("__arms", (0, -0.58, rest + 0.04), (0.60, 0.20, 0.08))]
    else:
        top, eye = H, 0.93 * H
        capsule, head = (0.17, 0.0, H - 0.22), (0, 0, H - 0.11)
        boxes = []
    boxes.append(("__front", (head[0], head[1] - 0.12, head[2]), (0.05, 0.05, 0.04)))
    return {"capsule": capsule, "head": (head, 0.11), "boxes": boxes, "eye": eye, "top": top}


# ---------- validation ----------

def num(v, label, lo=None, hi=None):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(f"{label} must be a finite number")
    if lo is not None and v < lo or hi is not None and v > hi:
        raise ValueError(f"{label} must be within {lo}..{hi}")
    return v


def validate(data):
    room = data["room"]
    for k in ("width", "depth", "height"):
        num(room[k], f"room.{k}", 1.0, 60.0)
    num(room.get("wall", 0.12), "room.wall", 0.02, 1.0)
    ids = [x["id"] for x in data.get("openings", []) + data.get("items", []) + data.get("cameras", [])
           + data.get("paths", []) + data.get("actors", []) + data.get("lights", [])]
    if len(ids) != len(set(ids)) or not all(isinstance(i, str) and i.strip() for i in ids):
        raise ValueError("ids must be unique non-empty strings")
    bad = [i for i in ids if not all(c.isascii() and (c.isalnum() or c == "_") for c in i) or "__" in i]
    if bad:
        raise ValueError(f"ids may use only ASCII letters, digits and single underscores: {bad}")
    for a in data.get("actors", []):
        if len(a["center"]) != 2 or a.get("pose", "stand") not in ("stand", "sit", "slump"):
            raise ValueError(f"actor {a['id']}: center needs [x, y]; pose is stand, sit or slump")
        num(a.get("height", 1.6), f"{a['id']}.height", 0.5, 2.5)
        num(a.get("yaw", 0), f"{a['id']}.yaw")
        num(a.get("base", 0), f"{a['id']}.base", 0, 3)
    for op in data.get("openings", []):
        if op["type"] not in ("door", "window", "opening") or op["wall"] not in WALLS:
            raise ValueError(f"opening {op['id']}: bad type or wall")
        length = room["width"] if op["wall"] in "SN" else room["depth"]
        num(op["offset"], f"{op['id']}.offset", 0, length)
        num(op["width"], f"{op['id']}.width", 0.2, length - op["offset"])
    for it in data.get("items", []):
        if len(it["size"]) != 3 or len(it["center"]) != 2:
            raise ValueError(f"item {it['id']}: size needs 3 numbers, center needs 2")
        for i, v in enumerate(it["size"]):
            num(v, f"{it['id']}.size[{i}]", 0.005, 30)
        if int(it.get("yaw", 0)) % 90 != 0 or it.get("yaw", 0) != int(it.get("yaw", 0)):
            raise ValueError(f"item {it['id']}: yaw must be 0, 90, 180 or 270")
        if it.get("shape", "box") not in {"box", "chair", "table", "booth", "floor_cover"} | fg.SHAPES:
            raise ValueError(f"item {it['id']}: unsupported shape")
        if it.get("shape") in fg.SHAPES and min(it['size']) < 0.1:
            raise ValueError(f"item {it['id']}: detailed furniture dimensions must be at least 0.1 m")
        if it.get("shape") == "floor_cover" and (it.get("base", 0) != 0 or it["size"][2] > 0.02):
            raise ValueError(f"item {it['id']}: floor_cover must be on the floor and at most 2 cm thick")
        if it.get("shape") == "chair" and not 0.1 < it.get("seat", 0.46) < it["size"][2]:
            raise ValueError(f"item {it['id']}: seat must be between 0.1 m and the chair height")
        if it.get("shape") == "booth":
            if it.get("door", "closed") not in ("closed", "open", "slide", "none") or it.get("hinge", "right") not in ("left", "right"):
                raise ValueError(f"item {it['id']}: door is closed, open, slide or none; hinge is left or right")
            if min(it["size"][0], it["size"][1]) < 4 * BOOTH_T or not 0 <= it.get("seat", 0.0) < it["size"][2] - 0.5:
                raise ValueError(f"item {it['id']}: booth too small, or its seat (raised floor) too high")
    time_ids = {t["id"] for t in data.get("times", [])}
    light_ids = {lt["id"] for lt in data.get("lights", [])}
    for it in data.get("items", []):
        if "light" in it and it["light"] not in light_ids:
            raise ValueError(f"item {it['id']}: light must reference an existing light id")
        for color_key in ['color', 'color_off']:
            if color_key in it:
                if len(it[color_key]) != 3:
                    raise ValueError(f"item {it['id']}: {color_key} needs three RGB values")
                for value in it[color_key]:
                    num(value, f"{it['id']}.{color_key}", 0, 1)
    for path in data.get("paths", []):
        if len(path["points"]) < 2 or any(len(p) != 2 for p in path["points"]):
            raise ValueError(f"path {path['id']}: needs at least 2 points of [x, y]")
        num(path["width"], f"{path['id']}.width", 0.3, 5)
    for cam in data.get("cameras", []):
        num(cam["lens"], f"{cam['id']}.lens", 8, 300)
        if cam.get("wild_wall") and cam["wild_wall"] not in WALLS:
            raise ValueError(f"camera {cam['id']}: wild_wall must be one of {WALLS}")
        if len(cam["location"]) != 3 or len(cam["look_at"]) != 3:
            raise ValueError(f"camera {cam['id']}: location and look_at need 3 numbers")
        if set(cam.get("times", [])) - time_ids:
            raise ValueError(f"camera {cam['id']}: times {sorted(set(cam['times']) - time_ids)} are not in times")
        if set(cam.get("actors", [])) - {a["id"] for a in data.get("actors", [])}:
            raise ValueError(f"camera {cam['id']}: actors lists ids that are not in actors")


# ---------- checks ----------

def run_checks(data):
    room, items = data["room"], data.get("items", [])
    W, D = room["width"], room["depth"]
    floor = [it for it in items if it.get("base", 0) <= EPS and it.get("shape") != "floor_cover"]
    by_id = {it["id"]: it for it in items}
    results = []

    def add(check, status, detail, ids=()):
        results.append({"check": check, "status": status, "detail": detail, "ids": list(ids)})

    for it in items:
        r = rect_of(it)
        if r[0] < -EPS or r[1] < -EPS or r[2] > W + EPS or r[3] > D + EPS:
            add("inside_room", "FAIL", f"{it['id']} 超出房間 {tuple(round(v, 2) for v in r)}", [it["id"]])
        top = it.get("base", 0) + it["size"][2]
        if top > room["height"] + EPS:
            add("under_ceiling", "FAIL", f"{it['id']} 頂部 {top:.2f} m 高過天花板 {room['height']} m", [it["id"]])
        if it.get("on") and it["on"] not in by_id:
            add("support", "FAIL", f"{it['id']} 放在不存在的 {it['on']} 上", [it["id"]])
        if it.get("on") in by_id:
            base = by_id[it["on"]]
            want = base.get("base", 0) + base["size"][2]
            if abs(it.get("base", 0) - want) > 0.02:
                add("support", "WARN", f"{it['id']} 的 base {it.get('base', 0)} 和 {base['id']} 的頂面 {want:.2f} 不一致", [it["id"]])

    for i, a in enumerate(floor):
        for b in floor[i + 1:]:
            if overlap(rect_of(a), rect_of(b)):
                add("overlap", "FAIL", f"{a['id']} 和 {b['id']} 重疊", [a["id"], b["id"]])

    for it in items:
        zone = front_zone(it)
        if not zone:
            continue
        if zone[0] < -EPS or zone[1] < -EPS or zone[2] > W + EPS or zone[3] > D + EPS:
            add("front_clear", "FAIL", f"{it['id']} 前方 {it['front_clear']} m 的使用空間碰到牆", [it["id"]])
        allowed = set(it.get("allow_in_front", []))
        for other in floor:
            if other["id"] == it["id"] or other["id"] in allowed:
                continue
            if overlap(zone, rect_of(other)):
                add("front_clear", "FAIL", f"{other['id']} 擋住 {it['id']} 前方 {it['front_clear']} m 的使用空間", [it["id"], other["id"]])

    for op in data.get("openings", []):
        if op["type"] == "door":
            zone = door_swing_zone(op, room)
            if zone:
                for other in floor:
                    if overlap(zone, rect_of(other)):
                        add("door_swing", "FAIL", f"{other['id']} 在 {op['id']} 的開門範圍內", [op["id"], other["id"]])
            if op["width"] < 0.8 - EPS:
                add("door_width", "WARN", f"{op['id']} 寬 {op['width']} m，少於常用的 0.8 m", [op["id"]])
        if op["type"] == "window":
            span = opening_span(op, room)
            band = {"S": (span[0], 0, span[2], 0.6), "N": (span[0], D - 0.6, span[2], D),
                    "W": (0, span[1], 0.6, span[3]), "E": (W - 0.6, span[1], W, span[3])}[op["wall"]]
            for other in floor:
                if overlap(band, rect_of(other)) and other["size"][2] > op.get("sill", 0.9) + EPS:
                    add("window_blocked", "WARN", f"{other['id']}（高 {other['size'][2]} m）擋在 {op['id']} 前面，窗台 {op.get('sill', 0.9)} m", [op["id"], other["id"]])

    for path in data.get("paths", []):
        pts, half = path["points"], path["width"] / 2
        worst, worst_id, worst_pt = math.inf, None, None
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 0.05) + 1)
            for k in range(n):
                t = k / (n - 1)
                px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
                wall_gap = min(px, py, W - px, D - py)
                if wall_gap < worst and not path.get("ignore_walls"):
                    worst, worst_id, worst_pt = wall_gap, "牆", (px, py)
                for other in floor:
                    if other["id"] in path.get("ignore", []):
                        continue
                    dist = point_rect_dist(px, py, rect_of(other))
                    if dist < worst:
                        worst, worst_id, worst_pt = dist, other["id"], (px, py)
        clear = 2 * worst if worst < math.inf else None
        status = "PASS" if clear is None or clear >= path["width"] - EPS else ("WARN" if clear >= 0.6 else "FAIL")
        where = f"，最窄處在 ({worst_pt[0]:.2f}, {worst_pt[1]:.2f}) 靠近 {worst_id}" if worst_pt else ""
        add("path_width", status, f"{path['id']} 要 {path['width']} m 寬，實際約 {clear:.2f} m{where}" if clear is not None else f"{path['id']} 無障礙", [path["id"]])

    for cam in data.get("cameras", []):
        x, y, z = cam["location"]
        inside = 0 < x < W and 0 < y < D
        if not inside and not cam.get("wild_wall"):
            add("camera_inside", "FAIL", f"{cam['id']} 在房間外，要註明拆哪面牆（wild_wall）", [cam["id"]])
        elif not inside:
            add("camera_inside", "WARN", f"{cam['id']} 在房間外，拍攝時要拆 {cam['wild_wall']} 牆", [cam["id"]])
        if not 0.1 < z < room["height"] - 0.05:
            add("camera_height", "WARN", f"{cam['id']} 高 {z} m，貼近地板或天花板", [cam["id"]])
        for other in floor:
            if other.get("shape") == "booth" or other.get("shape") in fg.SHAPES:
                gaps = []
                for name, c, s in item_parts(other):
                    b = part_box(c, s)
                    if b[5] < z - 0.3 or b[2] > z + 0.3:
                        continue
                    g = point_rect_dist(x, y, (b[0], b[1], b[3], b[4]))
                    if inside and g == 0 and b[2] <= z <= b[5]:
                        add("camera_inside", "FAIL", f"{cam['id']} 在 {name} 裡面", [cam["id"], other["id"]])
                    gaps.append((g, name))
                if inside and gaps and 0 < min(gaps)[0] < 0.3:
                    add("camera_clearance", "WARN", f"{cam['id']} 離 {min(gaps)[1]} 只有 {min(gaps)[0]:.2f} m（少於 0.3 m）",
                        [cam["id"], other["id"]])
                continue
            r = rect_of(other)
            gap = point_rect_dist(x, y, r)
            if inside and gap == 0 and z <= other["size"][2]:
                add("camera_inside", "FAIL", f"{cam['id']} 在 {other['id']} 裡面", [cam["id"], other["id"]])
            elif inside and gap < 0.3 and z < other["size"][2] + 0.3:
                add("camera_clearance", "WARN", f"{cam['id']} 離 {other['id']} 只有 {gap:.2f} m（少於 0.3 m）", [cam["id"], other["id"]])

    for a in data.get("actors", []):
        x, y = a["center"]
        body = actor_body(a)
        if not (0.15 < x < W - 0.15 and 0.15 < y < D - 0.15):
            add("actor_inside", "FAIL", f"{a['id']} 站在牆裡或房間外", [a["id"]])
        z0, z1 = a.get("base", 0), a.get("base", 0) + body["top"]
        if z1 > room["height"] - 0.05:
            add("actor_headroom", "FAIL", f"{a['id']} 頭頂 {z1:.2f} m 碰到天花板", [a["id"]])
        support = by_id.get(a.get("on"))
        if a.get("on") and not support:
            add("actor_support", "FAIL", f"{a['id']} 坐或站在不存在的 {a['on']} 上", [a["id"]])
        if support and a.get("pose") in ("sit", "slump"):
            raised = support.get("seat", 0.46 if support.get("shape") == "chair" else 0.0)
            seat = support.get("base", 0) + (raised if support.get("shape") in ("chair", "booth") else support["size"][2])
            if abs(seat - a.get("seat", 0.46)) > 0.03:
                add("actor_support", "WARN", f"{a['id']} 的 seat {a.get('seat', 0.46)} m 和 {support['id']} 的座面 {seat:.2f} m 不一致", [a["id"], support["id"]])
        for other in floor:
            if other.get("shape") == "booth":  # check the shell, so a stand-in can stand inside or sit on the edge
                for name, c, s in item_parts(other):
                    b = part_box(c, s)
                    if b[5] <= z0 + EPS or b[2] >= z1 - EPS or (name.endswith("__step") and a.get("on") == other["id"]):
                        continue
                    if point_rect_dist(x, y, (b[0], b[1], b[3], b[4])) < 0.15:
                        add("actor_clearance", "FAIL", f"{a['id']} 和 {name} 撞在一起", [a["id"], other["id"]])
                continue
            if other["id"] == a.get("on") or other.get("shape") == "table":
                continue
            if point_rect_dist(x, y, rect_of(other)) < 0.15:
                add("actor_clearance", "FAIL", f"{a['id']} 和 {other['id']} 撞在一起", [a["id"], other["id"]])

    if not any(r["status"] != "PASS" for r in results):
        add("summary", "PASS", "沒有發現問題")
    return results


# ---------- drawing ----------

def load_font(size, path=None):
    from PIL import ImageFont  # lazy: Blender imports this module without Pillow
    for candidate in [path, str(Path(os.environ.get("WINDIR", "/nonexistent")) / "Fonts" / "msjh.ttc"), "/System/Library/Fonts/PingFang.ttc",
                      "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]:
        if candidate and Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                continue
    return ImageFont.load_default()


def draw_plan(data, results, out_png, font_path=None, ppm=120, cameras=True):
    from PIL import Image, ImageDraw
    room = data["room"]
    W, D, T = room["width"], room["depth"], room.get("wall", 0.12)
    margin, legend_w = 1.0, 5.0
    img_w = int((W + 2 * margin + legend_w) * ppm)
    img_h = int((D + 2 * margin) * ppm)
    img = Image.new("RGB", (img_w, img_h), "white")
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dr, do = ImageDraw.Draw(img), ImageDraw.Draw(over)
    f_s, f_m, f_l = load_font(15, font_path), load_font(19, font_path), load_font(26, font_path)

    def P(x, y):
        return (margin + x) * ppm, (margin + D - y) * ppm

    def R(r):
        (a, b), (c, d) = P(r[0], r[3]), P(r[2], r[1])
        return [a, b, c, d]

    flagged = {i for r in results if r["status"] != "PASS" and (cameras or not r["check"].startswith("camera_"))
               for i in r["ids"]}

    # grid
    g = 0.0
    while g <= W + 1e-6:
        dr.line([P(g, 0), P(g, D)], fill=(205, 205, 205) if abs(g - round(g)) < 1e-6 else (235, 235, 235), width=1)
        g += 0.5
    g = 0.0
    while g <= D + 1e-6:
        dr.line([P(0, g), P(W, g)], fill=(205, 205, 205) if abs(g - round(g)) < 1e-6 else (235, 235, 235), width=1)
        g += 0.5

    # walls
    for r in [(-T, -T, W + T, 0), (-T, D, W + T, D + T), (-T, 0, 0, D), (W, 0, W + T, D)]:
        dr.rectangle(R(r), fill=(40, 40, 40))

    # front-clear zones and door swings (under items)
    for it in data.get("items", []):
        z = front_zone(it)
        if z:
            do.rectangle(R(z), fill=(80, 160, 255, 40), outline=(80, 160, 255, 160))
    for op in data.get("openings", []):
        x0, y0, x1, y1 = opening_span(op, room)
        gap = {"S": (x0, -T, x1, 0), "N": (x0, D, x1, D + T), "W": (-T, y0, 0, y1), "E": (W, y0, W + T, y1)}[op["wall"]]
        dr.rectangle(R(gap), fill="white")
        if op["type"] == "window":
            for frac in (0.3, 0.7):
                if op["wall"] in "SN":
                    yy = gap[1] + (gap[3] - gap[1]) * frac
                    dr.line([P(x0, yy), P(x1, yy)], fill=(30, 110, 200), width=2)
                else:
                    xx = gap[0] + (gap[2] - gap[0]) * frac
                    dr.line([P(xx, y0), P(xx, y1)], fill=(30, 110, 200), width=2)
        if op["type"] == "door":
            w = op["width"]
            hinge, far = door_hinge(op, room)
            nx, ny = INWARD[op["wall"]]
            if op.get("swing", "in") != "in":
                nx, ny = -nx, -ny
            leaf = (hinge[0] + nx * w, hinge[1] + ny * w)
            dr.line([P(*hinge), P(*leaf)], fill=(150, 90, 30), width=3)
            cx, cy = P(*hinge)
            rr = w * ppm
            angles = [math.degrees(math.atan2(P(*q)[1] - cy, P(*q)[0] - cx)) % 360 for q in (far, leaf)]
            start = angles[0] if (angles[1] - angles[0]) % 360 == 90 else angles[1]
            dr.arc([cx - rr, cy - rr, cx + rr, cy + rr], start, start + 90, fill=(150, 90, 30), width=1)
        nx, ny = INWARD[op["wall"]]
        lx, ly = P((x0 + x1) / 2 + nx * 0.2, (y0 + y1) / 2 + ny * 0.2)
        dr.text((lx, ly), op.get("name_zh", op["id"]), fill=(30, 110, 200) if op["type"] == "window" else (150, 90, 30),
                font=f_s, anchor="mm")

    # paths
    for path in data.get("paths", []):
        pts = [P(*p) for p in path["points"]]
        do.line(pts, fill=(60, 190, 90, 70), width=int(path["width"] * ppm), joint="curve")
        dr.line(pts, fill=(40, 150, 70), width=2)
        dr.text((pts[0][0] + 6, pts[0][1] - 22), path.get("name_zh", path["id"]), fill=(40, 150, 70), font=f_s)

    img.paste(Image.alpha_composite(img.convert("RGBA"), over).convert("RGB"))
    dr = ImageDraw.Draw(img)

    # items
    for it in sorted(data.get("items", []), key=lambda i: i.get("base", 0)):
        r = rect_of(it)
        raised = it.get("base", 0) > EPS
        overhead = it.get("base", 0) >= 1.8  # ceiling and high wall items: outline only, so they don't hide the floor
        bad = it["id"] in flagged
        dr.rectangle(R(r), fill=None if overhead else ((250, 240, 215) if not raised else (235, 225, 250)),
                     outline=(210, 30, 30) if bad else ((120, 90, 160) if raised else (120, 100, 70)), width=3 if bad else 2)
        fx, fy = front_vec(it.get("yaw", 0))
        cx, cy = it["center"]
        hw = (r[2] - r[0]) / 2 if abs(fx) > 0.5 else (r[3] - r[1]) / 2
        tip = P(cx + fx * hw, cy + fy * hw)
        dr.ellipse([tip[0] - 4, tip[1] - 4, tip[0] + 4, tip[1] + 4], fill=(120, 100, 70))
        if it.get("shape") == "booth":  # shell and door leaf
            for name, c, s in item_parts(it):
                if "__side" in name or "__door" in name or name == it["id"]:
                    b = part_box(c, s)
                    dr.rectangle(R((b[0], b[1], b[3], b[4])), fill=(150, 90, 30) if "__door" in name else (120, 100, 70))
        label = it.get("name_zh", it["id"])
        mx, my = P(cx, cy)
        if overhead:
            label += f"（{it['base']:.1f} m 高）"
        dr.text((mx, my), label, fill=(120, 90, 160) if overhead else (20, 20, 20), font=f_s, anchor="mm")

    # actors (stand-in people)
    for a in data.get("actors", []):
        c = P(*a["center"])
        r = 0.2 * ppm
        col = (210, 30, 30) if a["id"] in flagged else (0, 140, 140)
        dr.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], outline=col, width=3, fill=(220, 245, 245))
        fx, fy = front_vec(a.get("yaw", 0))
        tip = P(a["center"][0] + fx * 0.32, a["center"][1] + fy * 0.32)
        dr.line([c, tip], fill=col, width=3)
        pose = {"sit": "坐", "slump": "趴桌"}.get(a.get("pose"), "站")
        dr.text((c[0], c[1]), f"{a['id']}", fill=col, font=f_s, anchor="mm")
        dr.text((c[0] + r + 4, c[1] + r - 6), f"{a.get('name_zh', '')}（{pose}，{a.get('height', 1.6)} m）", fill=col, font=f_s)

    # cameras
    for cam in (data.get("cameras", []) if cameras else []):
        x, y, _ = cam["location"]
        tx, ty, _ = cam["look_at"]
        c = P(x, y)
        ang = math.atan2(ty - y, tx - x)
        half = math.atan(18.0 / cam["lens"])  # 36 mm sensor width
        for s in (-1, 1):
            e = P(x + 1.2 * math.cos(ang + s * half), y + 1.2 * math.sin(ang + s * half))
            dr.line([c, e], fill=(200, 40, 140), width=1)
        e = P(x + 0.45 * math.cos(ang), y + 0.45 * math.sin(ang))
        dr.line([c, e], fill=(200, 40, 140), width=3)
        dr.ellipse([c[0] - 9, c[1] - 9, c[0] + 9, c[1] + 9], outline=(200, 40, 140), width=3, fill="white")
        dr.text((c[0] + 11, c[1] + 4), f"{cam['id']} {cam['lens']}mm", fill=(200, 40, 140), font=f_s)

    # north arrow
    if "north_deg" in data:
        a = math.radians(data["north_deg"])
        bx, by = P(W + 0.55, D + 0.55)
        tip = (bx + 30 * math.sin(a), by - 30 * math.cos(a))
        dr.line([(bx, by), tip], fill=(20, 20, 20), width=3)
        dr.text((tip[0], tip[1] - 12), "N", fill=(20, 20, 20), font=f_m, anchor="mm")

    # legend
    lx = (W + 2 * margin) * ppm + 10
    y = 20
    dr.text((lx, y), f"{data.get('name_zh', data['id'])}", fill=(20, 20, 20), font=f_l)
    y += 36
    dr.text((lx, y), f"{data['id']} {data.get('version', '')}  {W}×{D} m，高 {room['height']} m", fill=(60, 60, 60), font=f_s)
    y += 30
    dr.line([(lx, y + 8), (lx + ppm, y + 8)], fill=(20, 20, 20), width=4)
    dr.text((lx + ppm + 8, y), "＝1 m（淺格 0.5 m）", fill=(20, 20, 20), font=f_s)
    y += 30
    for txt, col in [("黑：牆　棕：門和開門方向　藍：窗", (60, 60, 60)), ("米色：地上家具　淡紫：放在家具上或掛牆的東西", (60, 60, 60)),
                     ("紫色空框：1.8 m 以上（高處和天花板）", (120, 90, 160)),
                     ("家具上的圓點＝正面　藍框＝前方要留的空間", (60, 60, 60)), ("綠帶：走道（寬度照比例）", (40, 150, 70)),
                     ("粉紅：攝影機、鏡頭方向和水平視角" if cameras else "攝影機另見 plan_cameras.png", (200, 40, 140)),
                     ("青色圓：人物替身和面向", (0, 140, 140)), ("紅框：有問題的物件", (210, 30, 30))]:
        dr.text((lx, y), txt, fill=col, font=f_s)
        y += 24
    y += 10
    dr.text((lx, y), "檢查結果", fill=(20, 20, 20), font=f_m)
    y += 30
    for r in results:
        col = {"PASS": (40, 150, 70), "WARN": (200, 130, 0), "FAIL": (210, 30, 30)}[r["status"]]
        text = f"{r['status']} {r['detail']}"
        # wrap long lines
        line = ""
        for ch in text:
            if dr.textlength(line + ch, font=f_s) > legend_w * ppm - 30:
                dr.text((lx, y), line, fill=col, font=f_s)
                y += 20
                line = "　"
            line += ch
        dr.text((lx, y), line, fill=col, font=f_s)
        y += 24
        if y > img_h - 30:
            dr.text((lx, y), "……其餘見 plan_check.json", fill=(60, 60, 60), font=f_s)
            break
    img.save(out_png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--font", default=None, help="font file with CJK glyphs (default: msjh.ttc on Windows)")
    args = ap.parse_args()
    raw = args.set.read_bytes()
    data = json.loads(raw.decode("utf-8-sig"))
    validate(data)
    args.out.mkdir(parents=True, exist_ok=False)
    results = run_checks(data)
    draw_plan(data, results, args.out / "plan.png", args.font, cameras=False)
    draw_plan(data, results, args.out / "plan_cameras.png", args.font)
    counts = {s: sum(r["status"] == s for r in results) for s in ("PASS", "WARN", "FAIL")}
    report = {"set": data["id"], "version": data.get("version"), "input_sha256": hashlib.sha256(raw).hexdigest(),
              "counts": counts, "results": results, "plan": "plan.png", "plan_cameras": "plan_cameras.png",
              "scope": "2D footprint checks only; heights, sightlines and looks are checked in Blender and by eye"}
    (args.out / "plan_check.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.stdout.buffer.write((json.dumps(counts) + "\n").encode())
    for r in results:
        if r["status"] != "PASS":
            sys.stdout.buffer.write(f"{r['status']} {r['check']}: {r['detail']}\n".encode("utf-8"))
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
