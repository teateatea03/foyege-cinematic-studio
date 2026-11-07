import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def vector(value, label):
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{label} requires three coordinates")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in value):
        raise ValueError(f"{label} coordinates must be finite numbers")
    return Vector(value)


def validate_keys(keys, frames, fields):
    if not isinstance(keys, list) or len(keys) < 2:
        raise ValueError("keys require start and end")
    points = [key["frame"] for key in keys]
    if any(type(frame) is not int for frame in points):
        raise ValueError("key frames must be integers")
    if points[0] != 1 or points[-1] != frames or points != sorted(set(points)):
        raise ValueError("keys must increase from frame 1 to the final frame")
    for key in keys:
        for field in fields:
            vector(key[field], field)


def interpolate(keys, frame, field):
    for left, right in zip(keys, keys[1:]):
        if frame <= right["frame"]:
            fraction = (frame - left["frame"]) / (right["frame"] - left["frame"])
            return Vector(left[field]).lerp(Vector(right[field]), fraction)
    return Vector(keys[-1][field])


def material(name, color):
    result = bpy.data.materials.new(name)
    result.diffuse_color = (*color, 1)
    result.use_nodes = True
    result.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*color, 1)
    return result


def cube(name, location, size, surface):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = size
    obj.data.materials.append(surface)
    return obj


def render(scene, path):
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    raw = args.scene.read_bytes()
    data = json.loads(raw.decode("utf-8-sig"))
    frames, fps = data["frames"], data["fps"]
    if type(frames) is not int or not 2 <= frames <= 1800:
        raise ValueError("frames must be an integer between 2 and 1800")
    if type(fps) is not int or not 1 <= fps <= 120:
        raise ValueError("fps must be an integer between 1 and 120")
    resolution = data["resolution"]
    if len(resolution) != 2 or any(type(x) is not int or not 64 <= x <= 4096 for x in resolution):
        raise ValueError("resolution requires two integers between 64 and 4096")
    ids = [item["id"] for item in data["actors"] + data["boxes"]]
    if len(set(ids)) != len(ids) or any(not isinstance(x, str) or not x.strip() for x in ids):
        raise ValueError("object IDs must be nonempty and unique")
    for actor in data["actors"]:
        validate_keys(actor["keys"], frames, ["location"])
        color = vector(actor["color"], "color")
        if any(x < 0 or x > 1 for x in color):
            raise ValueError("color values must be in 0..1")
        if not math.isfinite(actor["yaw_deg"]):
            raise ValueError("yaw must be finite")
    for box in data["boxes"]:
        vector(box["location"], "box location")
        if any(x <= 0 for x in vector(box["size"], "box size")):
            raise ValueError("box size must be positive")
    camera_data = data["camera"]
    validate_keys(camera_data["keys"], frames, ["location", "look_at"])
    if not 1 <= camera_data["lens_mm"] <= 300:
        raise ValueError("lens_mm must be in 1..300")
    for frame in range(1, frames + 1):
        direction = interpolate(camera_data["keys"], frame, "look_at") - interpolate(camera_data["keys"], frame, "location")
        if direction.length < 0.001:
            raise ValueError(f"camera and target coincide at frame {frame}")
    top = data["topview"]
    center = vector(top["center"], "topview center")
    if not math.isfinite(top["height"]) or top["height"] <= 0 or not math.isfinite(top["ortho_scale"]) or top["ortho_scale"] <= 0:
        raise ValueError("topview height and scale must be positive finite numbers")
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 8
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.fps = fps
    scene.frame_start, scene.frame_end = 1, frames
    scene.world = bpy.data.worlds.new("PrevisWorld")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.4, 0.4, 0.4, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.7
    gray = material("neutral_proxy", (0.55, 0.55, 0.55))
    cube("ground", (0, 0, -0.06), (20, 20, 0.1), gray)
    for box in data["boxes"]:
        cube(box["id"], box["location"], box["size"], gray)
    labels = []
    label_surface = material("map_labels", (0.01, 0.01, 0.01))
    for actor in data["actors"]:
        root = bpy.data.objects.new(actor["id"], None)
        scene.collection.objects.link(root)
        root.rotation_euler.z = math.radians(actor["yaw_deg"])
        surface = material(actor["id"] + "_color", actor["color"])
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.22, depth=1.38, location=(0, 0, 0.69))
        body = bpy.context.object
        body.name = actor["id"] + "_body"
        body.parent = root
        body.data.materials.append(surface)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.22, location=(0, 0, 1.6))
        head = bpy.context.object
        head.name = actor["id"] + "_head"
        head.parent = root
        head.data.materials.append(surface)
        nose = cube(actor["id"] + "_front", (0, -0.23, 1.6), (0.1, 0.12, 0.08), surface)
        nose.parent = root
        for frame in range(1, frames + 1):
            root.location = interpolate(actor["keys"], frame, "location")
            root.keyframe_insert(data_path="location", frame=frame)
        bpy.ops.object.text_add(location=Vector(actor["keys"][0]["location"]) + Vector((0.3, 0, 0.02)))
        label = bpy.context.object
        label.data.body = actor["id"]
        label.data.size = 0.3
        label.data.materials.append(label_surface)
        label.hide_render = True
        labels.append(label)
    bpy.ops.object.light_add(type="AREA", location=(1, -3, 7))
    bpy.context.object.data.energy = 1400
    bpy.context.object.data.shape = "DISK"
    bpy.context.object.data.size = 8
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = "ShotCamera"
    camera.data.lens = camera_data["lens_mm"]
    scene.camera = camera
    for frame in range(1, frames + 1):
        camera.location = interpolate(camera_data["keys"], frame, "location")
        target = interpolate(camera_data["keys"], frame, "look_at")
        camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
        camera.keyframe_insert(data_path="location", frame=frame)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)
    previews = []
    for frame in sorted({1, (frames + 1) // 2, frames}):
        scene.frame_set(frame)
        filename = f"shot_{frame:04d}.png"
        render(scene, output / filename)
        previews.append(filename)
    bpy.ops.object.camera_add(location=center + Vector((0, 0, top["height"])))
    map_camera = bpy.context.object
    map_camera.name = "TopviewCamera"
    map_camera.rotation_euler = (0, 0, 0)
    map_camera.data.type = "ORTHO"
    map_camera.data.ortho_scale = top["ortho_scale"]
    scene.frame_set(1)
    scene.camera = map_camera
    for label in labels:
        label.hide_render = False
    render(scene, output / "topview.png")
    for label in labels:
        label.hide_render = True
    scene.camera = camera
    scene.render.filepath = str(output / "sequence" / "frame_")
    bpy.ops.wm.save_as_mainfile(filepath=str(output / "scene.blend"))
    manifest = {
        "status": "completed", "blender": bpy.app.version_string,
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "fps": fps, "frames": frames, "duration_seconds": frames / fps,
        "resolution": resolution, "actor_ids": [a["id"] for a in data["actors"]],
        "previews": previews, "topview": "topview.png", "scene": "scene.blend",
        "validation_scope": "geometry and camera previews; facial performance untested"
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
