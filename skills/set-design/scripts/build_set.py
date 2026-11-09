"""Build a grey blockout of a set from set.json in Blender, check it, and render reference views.

    blender --background --factory-startup --python-exit-code 1 --python build_set.py -- \
        --set set.json --out OUT_DIR [--samples 24] [--res 960x540] [--times morning,night] [--no-render]

OUT_DIR must not exist yet. Writes:
  scene.blend                 the blockout (master model for this set version)
  plan_top.png                orthographic top view with item ids
  elev_N/S/E/W.png            orthographic elevations, looking at that wall from inside
  cam_<camera>_<time>.png     each camera at each time of day
  manifest.json               input SHA-256, checks, files with SHA-256, render seconds

Rendering uses one Cycles GPU; CPU is allowed only when no GPU backend is supported.
Coordinates: metres, room corner at the origin, X = width, Y = depth, Z = up.
yaw 0 means the front faces -Y; 90 faces +X (counterclockwise seen from above).
Geometry comes from plan_check.py (wall_pieces, door_leaves, item_parts, actor_body) so the plan and the model agree.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Euler, Matrix, Vector

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True  # keep __pycache__ out of the skill folder
_spec = importlib.util.spec_from_file_location("plan_check", HERE / "plan_check.py")
pc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pc)
_device_spec = importlib.util.spec_from_file_location("render_device", HERE / "render_device.py")
rd = importlib.util.module_from_spec(_device_spec)
_device_spec.loader.exec_module(rd)

_sun_spec = importlib.util.spec_from_file_location('sunlight_check', HERE / 'sunlight_check.py')
sc = importlib.util.module_from_spec(_sun_spec)
_sun_spec.loader.exec_module(sc)
PROXY_GRAY = (0.5, 0.5, 0.5)


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--samples", type=int, default=24)
    ap.add_argument("--res", default="960x540", help="camera render size, WxH")
    ap.add_argument("--times", default="", help="comma-separated time ids; default all")
    ap.add_argument("--no-render", action="store_true", help="build, check and save only")
    ap.add_argument("--gpu-name", default="", help="GPU name substring; selects one device only")
    ap.add_argument("--backend", default="AUTO", choices=["AUTO", "OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"])
    return ap.parse_args(argv)


# ---------- helpers ----------

def kelvin_rgb(k):
    """Approximate blackbody colour (Tanner Helland fit), returned as linear RGB with max 1."""
    t = max(1000.0, min(40000.0, float(k))) / 100.0
    r = 255.0 if t <= 66 else 329.698727446 * (t - 60) ** -0.1332047592
    g = 99.4708025861 * math.log(t) - 161.1195681661 if t <= 66 else 288.1221695283 * (t - 60) ** -0.0755148492
    b = 255.0 if t >= 66 else (0.0 if t <= 19 else 138.5177312231 * math.log(t - 10) - 305.0447927307)
    srgb = [min(255.0, max(0.0, c)) / 255.0 for c in (r, g, b)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    m = max(lin) or 1.0
    return tuple(c / m for c in lin)


def material(name, rgb):
    mat = bpy.data.materials.new(name)
    if mat.node_tree is None:
        mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.8
    mat.diffuse_color = (*rgb, 1.0)
    return mat


def mesh_object(name, fill, mat, coll):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    fill(bm)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def box(name, center, size, mat, coll):
    ob = mesh_object(name, lambda bm: bmesh.ops.create_cube(bm, size=1.0), mat, coll)
    ob.location = center
    ob.scale = size
    return ob


def aabb(name, b, mat, coll):
    x0, y0, z0, x1, y1, z1 = b
    return box(name, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), (x1 - x0, y1 - y0, z1 - z0), mat, coll)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ---------- build ----------

def build_actor(a, mat, coll):
    """Stand-in person: capsule body named by the id, head, nose marker; sitting adds thighs and shins."""
    body = pc.actor_body(a)
    root = bpy.data.objects.new(f"{a['id']}__root", None)
    root.location = (a["center"][0], a["center"][1], a.get("base", 0.0))
    root.rotation_euler = Euler((0, 0, math.radians(a.get("yaw", 0))))
    coll.objects.link(root)
    r, z0, z1 = body["capsule"]
    length = max(0.0, z1 - z0 - 2 * r)

    def capsule(bm):
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=r, radius2=r, depth=length,
                              matrix=Matrix.Translation((0, 0, z0 + r + length / 2)))
        for zc in (z0 + r, z1 - r):
            bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=r, matrix=Matrix.Translation((0, 0, zc)))

    parts = [mesh_object(a["id"], capsule, mat, coll)]
    (hx, hy, hz), hr = body["head"]
    parts.append(mesh_object(f"{a['id']}__head", lambda bm: bmesh.ops.create_uvsphere(
        bm, u_segments=16, v_segments=8, radius=hr, matrix=Matrix.Translation((hx, hy, hz))), mat, coll))
    for suffix, c, s in body["boxes"]:
        parts.append(box(f"{a['id']}{suffix}", c, s, mat, coll))
    for p in parts:
        p.parent = root


def build_furniture(it, mat, coll):
    root = bpy.data.objects.new(it['id'], None)
    root.location = (*it['center'], it.get('base',0))
    root.rotation_euler.z = math.radians(it.get('yaw',0))
    coll.objects.link(root)
    for p in pc.fg.primitives(it):
        surface = mat
        if p['suffix'] in ['phone','clamp']:
            surface = material('m_'+it['id']+'_'+p['suffix'],(0.05,0.05,0.06))
        elif it['shape']=='potted_plant' and p['suffix']=='pot':
            surface = material('m_'+it['id']+'_pot',(0.42,0.40,0.36))
        elif it['shape']=='bookcase' and p['suffix'].startswith('book'):
            value = 0.32+0.10*(int(p['suffix'][-1])%4)
            surface = material('m_'+it['id']+'_'+p['suffix'],(value,value,value))
        name = it['id']+'__'+p['suffix']
        kind = p['kind']
        if kind == 'box':
            ob = box(name,p['center'],p['size'],mat,coll)
        elif kind == 'ring':
            verts, faces = [], []
            for u in range(64):
                a = 2*math.pi*u/64
                for v in range(12):
                    b = 2*math.pi*v/12
                    rr = p['radius']+p['tube']*math.cos(b)
                    verts.append((p['center'][0]+rr*math.cos(a),p['center'][1]+p['tube']*math.sin(b),p['center'][2]+rr*math.sin(a)))
            for u in range(64):
                for v in range(12):
                    faces.append((u*12+v,((u+1)%64)*12+v,((u+1)%64)*12+(v+1)%12,u*12+(v+1)%12))
            me = bpy.data.meshes.new(name)
            me.from_pydata(verts,[],faces)
            me.materials.append(mat)
            ob = bpy.data.objects.new(name,me)
            coll.objects.link(ob)
        elif kind == 'rod':
            a,b = Vector(p['a']),Vector(p['b'])
            transform = Matrix.Translation((a+b)/2) @ (b-a).to_track_quat('Z','Y').to_matrix().to_4x4()
            ob = mesh_object(name,lambda bm: bmesh.ops.create_cone(bm,cap_ends=True,segments=16,radius1=p['radius'],radius2=p['radius'],depth=(b-a).length,matrix=transform),mat,coll)
        elif kind == 'cylinder':
            ob = mesh_object(name,lambda bm: bmesh.ops.create_cone(bm,cap_ends=True,segments=32,radius1=p['size'][0]*0.4,radius2=p['size'][0]/2,depth=p['size'][2],matrix=Matrix.Translation(p['center'])),mat,coll)
        else:
            transform = Matrix.Translation(p['center']) @ Matrix.Diagonal(Vector((*[s/2 for s in p['size']],1)))
            ob = mesh_object(name,lambda bm: bmesh.ops.create_uvsphere(bm,u_segments=32,v_segments=16,radius=1,matrix=transform),mat,coll)
        if surface != mat:
            ob.data.materials.clear()
            ob.data.materials.append(surface)
        ob.parent = root


def build(data):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    room = data["room"]
    W, D, H, T = room["width"], room["depth"], room["height"], room.get("wall", 0.12)
    coll = {n: bpy.data.collections.new(n) for n in ("architecture", "items", "actors", "lights", "cameras", "labels")}
    for c in coll.values():
        scene.collection.children.link(c)
    m_wall = material("wall", (0.72, 0.72, 0.70))
    m_door = material("door", (0.40, 0.28, 0.18))
    m_mark = material("front_mark", (0.05, 0.05, 0.06))
    m_label = material("label", (0.02, 0.02, 0.02))
    m_actor = material("actor", (0.85, 0.85, 0.88))

    aabb("floor", (-T, -T, -0.02, W + T, D + T, 0.0), material("floor", (0.33, 0.30, 0.27)), coll["architecture"])
    aabb("ceiling", (-T, -T, H, W + T, D + T, H + 0.02), material("ceiling", (0.80, 0.80, 0.80)), coll["architecture"])
    for name, _wall, b in pc.wall_pieces(data):
        aabb(name, b, m_wall, coll["architecture"])
    for name, _wall, b in pc.door_leaves(data):
        aabb(name, b, m_door, coll["architecture"])

    for i, it in enumerate(data.get("items", [])):
        rgb = tuple(it["color"]) if it.get("color") else PROXY_GRAY
        mat = material(f"m_{it['id']}", rgb)
        if it.get('shape') in pc.fg.SHAPES:
            build_furniture(it,mat,coll['items'])
        else:
            for name, c, s in pc.item_parts(it):
                box(name, c, s, m_mark if name.endswith("__front") else mat, coll["items"])
        cu = bpy.data.curves.new(f"label_{it['id']}", "FONT")  # id label, shown only in the top view
        cu.body = it["id"]
        cu.size = 0.14
        cu.align_x, cu.align_y = "CENTER", "CENTER"
        lab = bpy.data.objects.new(f"label_{it['id']}", cu)
        lab.location = (it["center"][0], it["center"][1], it.get("base", 0.0) + it["size"][2] + 0.01)
        lab.data.materials.append(m_label)
        lab.hide_render = True
        coll["labels"].objects.link(lab)

    for a in data.get("actors", []):
        build_actor(a, m_actor, coll["actors"])

    for lt in data.get("lights", []):
        kind = {"area": "AREA", "point": "POINT", "spot": "SPOT"}[lt.get("type", "point")]
        ld = bpy.data.lights.new(lt["id"], kind)
        ld.energy = lt.get("energy", 50)
        ld.color = kelvin_rgb(lt.get("kelvin", 3000))
        if kind == "AREA":
            ld.size = lt.get("size", 0.5)
        else:
            ld.shadow_soft_size = lt.get("size", 0.05)
        ob = bpy.data.objects.new(lt["id"], ld)
        ob.location = lt["location"]
        if lt.get("aim"):
            ob.rotation_euler = (Vector(lt["aim"]) - Vector(lt["location"])).to_track_quat("-Z", "Y").to_euler()
        coll["lights"].objects.link(ob)

    sun_data = bpy.data.lights.new("sun", "SUN")
    sun_data.angle = math.radians(1.0)
    coll["lights"].objects.link(bpy.data.objects.new("sun", sun_data))

    world = bpy.data.worlds.new("world")
    if world.node_tree is None:
        world.use_nodes = True
    scene.world = world

    for cam in data.get("cameras", []):
        cd = bpy.data.cameras.new(cam["id"])
        cd.lens = cam["lens"]
        cd.sensor_width = cam.get("sensor_width", 36.0)
        cd.clip_start = 0.02
        ob = bpy.data.objects.new(cam["id"], cd)
        ob.location = cam["location"]
        aim = Vector(cam["look_at"]) - Vector(cam["location"])
        if cam.get("level"):
            # keep verticals vertical: aim level, then shift the frame to put look_at back on the centre line
            flat = Vector((aim.x, aim.y, 0.0))
            cd.shift_y = math.tan(math.atan2(aim.z, flat.length)) * cd.lens / cd.sensor_width
            aim = flat
        ob.rotation_euler = aim.to_track_quat("-Z", "Y").to_euler()
        coll["cameras"].objects.link(ob)

    bpy.context.view_layer.update()
    return scene


def set_time(scene, data, t):
    """t is a time dict from set.json, or None for flat clay light (top view and elevations)."""
    bg = scene.world.node_tree.nodes["Background"]
    sun = bpy.data.objects["sun"]
    if t is None:
        bg.inputs["Color"].default_value = (1, 1, 1, 1)
        bg.inputs["Strength"].default_value = 1.0
        sun.data.energy = 0.0
        on = set()
    else:
        bg.inputs["Color"].default_value = (*kelvin_rgb(t.get("world_kelvin", 7000)), 1)
        bg.inputs["Strength"].default_value = t.get("world", 0.2)
        s = t.get("sun")
        if s:
            toward_sun = Vector(sc.sun_vector(s))
            sun.rotation_euler = toward_sun.to_track_quat("Z", "Y").to_euler()
            sun.data.energy = s.get("energy", 3.0)
            sun.data.color = kelvin_rgb(s.get("kelvin", 5500))
        else:
            sun.data.energy = 0.0
        on = {lt["id"] for lt in data.get("lights", []) if t["id"] in lt.get("times", [])}
    for lt in data.get("lights", []):
        bpy.data.objects[lt["id"]].hide_render = lt["id"] not in on
    for it in data.get("items", []):
        if not it.get("light"):
            continue
        rgb = it.get("color", (0.95, 0.95, 0.9)) if t is None or it["light"] in on else it.get("color_off", (0.08, 0.08, 0.08))
        mat = bpy.data.materials[f"m_{it['id']}"]
        mat.diffuse_color = (*rgb, 1.0)
        bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    scene.view_settings.exposure = 0.0 if t is None else t.get("exposure", 0.0)


# ---------- checks ----------

def window_sunlight(scene, data):
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    def cast(origin, direction):
        hit, point, normal, face, ob, _matrix = scene.ray_cast(depsgraph, Vector(origin), Vector(direction), distance=10000)
        if not hit:
            return None
        axis = max(range(3), key=lambda i: abs(normal[i]))
        side = ('+' if normal[axis] >= 0 else '-') + 'XYZ'[axis]
        return {'object': ob.name, 'face_axis': side, 'polygon_index': face, 'xyz': [round(v, 6) for v in point], 'normal': [round(v, 6) for v in normal]}
    return sc.trace_window_sunlight(data, cast)


def wild_objects(data, wall):
    """Everything removed when a wall is pulled for a camera: the wall pieces and the doors in it."""
    if not wall:
        return set()
    return {n for n, w, _b in pc.wall_pieces(data) + pc.door_leaves(data) if w == wall}


def direct_sunlight_on_objects(scene, sun, targets):
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    toward = Vector(sc.sun_vector(sun))
    enabled = sun.get('energy', 3) > 0 and sun['elevation'] > 0
    results = []
    for target in targets:
        samples = []
        weights = []
        for ob in bpy.data.objects:
            if ob.type != 'MESH' or ob.name not in group_names(target):
                continue
            evaluated = ob.evaluated_get(depsgraph)
            mesh = evaluated.to_mesh()
            try:
                mesh.calc_loop_triangles()
                matrix = evaluated.matrix_world
                for triangle in mesh.loop_triangles:
                    verts = [matrix @ mesh.vertices[i].co for i in triangle.vertices]
                    cross = (verts[1]-verts[0]).cross(verts[2]-verts[0])
                    if cross.length < 1e-12 or cross.normalized().dot(toward) <= 0:
                        continue
                    for bary in [(1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6)]:
                        point = sum((p*w for p,w in zip(verts,bary)), Vector((0,0,0)))
                        hit, loc, _normal, _face, blocker, _matrix = scene.ray_cast(depsgraph, point+toward*.0001, toward, distance=10000) if enabled else (True,None,None,None,None,None)
                        samples.append({'object':ob.name,'xyz':[round(q,6) for q in point],'direct_sun':enabled and not hit,'blocker':blocker.name if blocker else None,'blocker_xyz':[round(q,6) for q in loc] if loc is not None else None})
                        weights.append(cross.length/8)
            finally:
                evaluated.to_mesh_clear()
        total = sum(weights)
        visible = sum(w for w,s in zip(weights,samples) if s['direct_sun'])
        count = sum(s['direct_sun'] for s in samples)
        results.append({'target':target,'sunlit_samples':count,'samples_count':len(samples),'area_weighted_sample_fraction':visible/total if total else None,'verdict':'DIRECT_SUN_CONFIRMED' if count else 'NO_DIRECT_SUN_OBSERVED_IN_SAMPLES','samples':samples})
    return {'method':'Four barycentric samples per sun-facing native mesh triangle; cast toward sun through full scene including window tunnel.','sun':sun,'limits':['Finite surface sampling: a positive ray proves that point lit; zero samples do not prove every point unlit','Full source scene includes every stand-in before camera hiding; no time-specific occupancy inferred','Sample fraction estimates modeled sun-facing surface exposure, not irradiance or total-body coverage'],'targets':results}


def first_hit(scene, depsgraph, origin, target, skip):
    """First object hit on the segment origin->target, ignoring names in skip. Returns (name, distance) or None."""
    direction = target - origin
    remaining = direction.length
    direction.normalize()
    o = origin.copy()
    travelled = 0.0
    for _ in range(12):
        hit, loc, _n, _i, ob, _m = scene.ray_cast(depsgraph, o, direction, distance=remaining)
        if not hit:
            return None
        step = (loc - o).length
        if ob.name in skip or ob.name.startswith("label_"):
            o = loc + direction * 1e-4
            remaining -= step + 1e-4
            travelled += step + 1e-4
            continue
        return ob.name, travelled + step
    return None


def group_names(name):
    """An object and its parts (<name>__*), e.g. a booth's shell or a stand-in's head and limbs."""
    return {o.name for o in bpy.data.objects if o.name == name or o.name.startswith(name + "__")}


def hidden_actors(data, cam):
    """Stand-in objects a camera leaves out: every actor not in its actors list (no list keeps them all)."""
    if "actors" not in cam:
        return set()
    return set().union(*[group_names(a["id"]) for a in data.get("actors", []) if a["id"] not in cam["actors"]])


def surface_visibility(scene, depsgraph, cam_ob, ob, skip, n=5):
    """Sample a grid on each face, turned to the camera, of the world bounding box around the object and its parts.
    Returns (samples, samples inside the frame, samples inside the frame with a clear line of sight)."""
    origin = cam_ob.location.copy()
    owner = ob.name
    pts = [o.matrix_world @ Vector(c) for o in bpy.data.objects
           if o.type == "MESH" and o.name in group_names(owner) for c in o.bound_box]
    lo = Vector([min(p[i] for p in pts) for i in range(3)])
    hi = Vector([max(p[i] for p in pts) for i in range(3)])
    mid, half = (lo + hi) / 2, (hi - lo) / 2
    total = in_frame = visible = 0
    steps = [-0.8 + 1.6 * k / (n - 1) for k in range(n)]
    for axis in range(3):
        for sign in (-1, 1):
            wn = Vector([sign if i == axis else 0 for i in range(3)])
            face_c = mid + Vector([wn[i] * half[i] for i in range(3)])
            if wn.dot(origin - face_c) <= 0:
                continue
            u_ax, v_ax = [i for i in range(3) if i != axis]
            for su in steps:
                for sv in steps:
                    local = face_c.copy()
                    local[u_ax] += su * half[u_ax]
                    local[v_ax] += sv * half[v_ax]
                    p = local + wn * 0.002
                    total += 1
                    v = world_to_camera_view(scene, cam_ob, p)
                    if not (0.0 <= v.x <= 1.0 and 0.0 <= v.y <= 1.0 and v.z > 0):
                        continue
                    in_frame += 1
                    hit = first_hit(scene, depsgraph, origin, p, skip)
                    if hit is None or hit[0] == owner or hit[0].startswith(owner + "__"):
                        visible += 1
    return total, in_frame, visible


def opening_visibility(scene, depsgraph, cam_ob, data, op, skip, n=5):
    """Sample a grid on a door or window opening, just inside the room. A point counts as visible when the line of
    sight reaches it unblocked, or ends on that door's own leaf. Same return as surface_visibility."""
    room = data["room"]
    x0, y0, x1, y1 = pc.opening_span(op, room)
    sill, head = pc.opening_z(op)
    head = min(head, room["height"])
    nx, ny = pc.INWARD[op["wall"]]
    origin = cam_ob.location.copy()
    total = in_frame = visible = 0
    for i in range(n):
        for j in range(n):
            u, v = (i + 0.5) / n, (j + 0.5) / n
            p = Vector((x0 + (x1 - x0) * u + nx * 0.01, y0 + (y1 - y0) * u + ny * 0.01, sill + (head - sill) * v))
            total += 1
            c = world_to_camera_view(scene, cam_ob, p)
            if not (0.0 <= c.x <= 1.0 and 0.0 <= c.y <= 1.0 and c.z > 0):
                continue
            in_frame += 1
            hit = first_hit(scene, depsgraph, origin, p, skip)
            if hit is None or hit[0] == f"door_{op['id']}":
                visible += 1
    return total, in_frame, visible


def run_checks(scene, data, res):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    openings = {op["id"]: op for op in data.get("openings", [])}
    scene.render.resolution_x, scene.render.resolution_y = res
    results = []
    for cam in data.get("cameras", []):
        cob = bpy.data.objects[cam["id"]]
        skip = wild_objects(data, cam.get("wild_wall")) | hidden_actors(data, cam)
        origin = cob.location.copy()
        near = []
        for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            hit = first_hit(scene, depsgraph, origin, origin + Vector(d) * 5.0, skip)
            if hit:
                near.append((hit[1], hit[0]))
        if near:
            dist, name = min(near)
            status = "PASS" if dist >= 0.3 else "WARN"
            results.append({"check": "camera_clearance", "status": status, "ids": [cam["id"]],
                            "detail": f"{cam['id']} 最近的東西是 {name}，{dist:.2f} m"
                                      + ("" if status == "PASS" else "（少於 0.3 m，實拍放不下機器，AI 也容易穿模）")})
        for tid in cam.get("must_see", []):
            if tid in skip:
                results.append({"check": "must_see", "status": "FAIL", "ids": [cam["id"], tid],
                                "detail": f"{cam['id']} 要看到的 {tid} 在這個機位被拿掉了（actors 或 wild_wall）"})
                continue
            if tid in openings:
                total, in_frame, visible = opening_visibility(scene, depsgraph, cob, data, openings[tid], skip)
            elif tid in bpy.data.objects:
                total, in_frame, visible = surface_visibility(scene, depsgraph, cob, bpy.data.objects[tid], skip)
            else:
                results.append({"check": "must_see", "status": "FAIL", "ids": [cam["id"], tid],
                                "detail": f"{cam['id']} 要看到的 {tid} 不存在"})
                continue
            frac = visible / total if total else 0.0
            status = "PASS" if frac >= 0.4 else ("WARN" if frac > 0.1 else "FAIL")
            results.append({"check": "must_see", "status": status, "ids": [cam["id"], tid], "visible": round(frac, 3),
                            "detail": f"{cam['id']} 看得到 {tid} 朝向鏡頭那幾面的 {frac:.0%}（取樣 {total} 點，在畫面內 {in_frame}）"})
    return results


# ---------- render ----------

def render(scene, path, cam_ob, hide=(), res=(960, 540)):
    hidden = []
    for name in hide:
        ob = bpy.data.objects.get(name)
        if ob and not ob.hide_render:
            ob.hide_render = True
            hidden.append(ob)
    scene.camera = cam_ob
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.filepath = str(path)
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    for ob in hidden:
        ob.hide_render = False
    return round(time.time() - t0, 2)


def ortho_camera(name, location, rotation, scale):
    cd = bpy.data.cameras.new(name)
    cd.type = "ORTHO"
    cd.ortho_scale = scale
    cd.clip_start, cd.clip_end = 0.01, 100.0
    ob = bpy.data.objects.new(name, cd)
    ob.location = location
    ob.rotation_euler = rotation
    bpy.context.scene.collection.objects.link(ob)
    return ob


def main():
    args = parse_args()
    raw = args.set.read_bytes()
    data = json.loads(raw.decode("utf-8-sig"))
    pc.validate(data)
    out = args.out.resolve()  # Blender resolves a relative render path against the drive root, not the cwd
    out.mkdir(parents=True, exist_ok=False)
    res = tuple(int(v) for v in args.res.lower().split("x"))

    t_build = time.time()
    scene = build(data)
    scene.render.engine = "CYCLES"
    render_device = {"device": "NOT_USED", "reason": "no-render geometry checks"} if args.no_render else rd.configure_cycles(scene, args.gpu_name, args.backend)
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    build_s = round(time.time() - t_build, 2)

    sunlight = window_sunlight(scene, data)
    (out / 'sunlight.json').write_text(json.dumps(sunlight, ensure_ascii=False, indent=2), encoding='utf-8')
    checks = run_checks(scene, data, res)
    files, timings = {}, {}

    if not args.no_render:
        room = data["room"]
        W, D, H, T = room["width"], room["depth"], room["height"], room.get("wall", 0.12)
        pad, px = 0.4, 1200
        doors = {n for n, _w, _b in pc.door_leaves(data)}

        # top view with id labels
        set_time(scene, data, None)
        labels = [o for o in bpy.data.objects if o.name.startswith("label_")]
        for o in labels:
            o.hide_render = False
        ext_x, ext_y = W + 2 * T + pad, D + 2 * T + pad
        top = ortho_camera("view_top", (W / 2, D / 2, H + 5), (0, 0, 0), max(ext_x, ext_y))
        timings["plan_top.png"] = render(scene, out / "plan_top.png", top, {"ceiling"},
                                         (px, max(1, round(px * ext_y / ext_x))))
        for o in labels:
            o.hide_render = True

        def far_from(wall, limit=1.0):
            """Items and stand-ins more than limit metres from a wall; an elevation shows only what stands along it."""
            names = set()
            for it in data.get("items", []):
                r = pc.rect_of(it)
                if {"N": D - r[3], "S": r[1], "E": W - r[2], "W": r[0]}[wall] > limit:
                    names |= {n for n, _c, _s in pc.item_parts(it)}
            for a in data.get("actors", []):
                x, y = a["center"]
                if {"N": D - y, "S": y, "E": W - x, "W": x}[wall] > limit:
                    names |= group_names(a["id"])
            return names

        # elevations: look at wall X from inside; hide the opposite wall, all door leaves, the ceiling, and
        # everything more than 1 m away from wall X
        views = {
            "N": ((W / 2, -T - 6, H / 2), (math.pi / 2, 0, 0), "S", W),
            "S": ((W / 2, D + T + 6, H / 2), (math.pi / 2, 0, math.pi), "N", W),
            "E": ((-T - 6, D / 2, H / 2), (math.pi / 2, 0, -math.pi / 2), "W", D),
            "W": ((W + T + 6, D / 2, H / 2), (math.pi / 2, 0, math.pi / 2), "E", D),
        }
        for wall, (loc, rot, hide_wall, span) in views.items():
            ext_x, ext_y = span + 2 * T + pad, H + pad
            cam = ortho_camera(f"view_elev_{wall}", loc, rot, max(ext_x, ext_y))
            hide = wild_objects(data, hide_wall) | doors | {"ceiling"} | far_from(wall)
            timings[f"elev_{wall}.png"] = render(scene, out / f"elev_{wall}.png", cam, hide,
                                                (px, max(1, round(px * ext_y / ext_x))))

        # camera views at each time of day
        wanted = [s for s in args.times.split(",") if s]
        times = [t for t in data.get("times", []) if not wanted or t["id"] in wanted] or [{"id": "neutral", "world": 0.6}]
        for cam in data.get("cameras", []):
            hide = wild_objects(data, cam.get("wild_wall")) | hidden_actors(data, cam)
            for t in [t for t in times if not cam.get("times") or t["id"] in cam["times"]]:
                set_time(scene, data, t)
                name = f"cam_{cam['id']}_{t['id']}.png"
                timings[name] = render(scene, out / name, bpy.data.objects[cam["id"]], hide, res)

    set_time(scene, data, None)
    bpy.ops.wm.save_as_mainfile(filepath=str(out / "scene.blend"), check_existing=False, compress=True)
    for p in sorted(out.iterdir()):
        files[p.name] = sha256(p)
    counts = {s: sum(r["status"] == s for r in checks) for s in ("PASS", "WARN", "FAIL")}
    manifest = {
        "set": data["id"], "version": data.get("version"), "input": str(args.set), "input_sha256": hashlib.sha256(raw).hexdigest(),
        "blender": bpy.app.version_string, "engine": "CYCLES", "render_device": render_device, "samples": args.samples, "camera_res": list(res),
        "build_seconds": build_s, "render_seconds": timings, "checks": checks, "counts": counts, "files": files,
        "sunlight_report": "sunlight.json", "proxy_color_policy": "explicit material color or neutral gray; no cycling identification palette",
        "scope": "grey blockout: geometry, sightlines, light direction; stand-ins only for scale",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.stdout.buffer.write((json.dumps(counts) + "\n").encode())
    for r in checks:
        if r["status"] != "PASS":
            sys.stdout.buffer.write(f"{r['status']} {r['check']}: {r['detail']}\n".encode("utf-8"))


if __name__ == "__main__":
    main()
