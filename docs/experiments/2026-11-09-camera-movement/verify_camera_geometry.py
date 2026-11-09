"""Blender-only geometric checks; no rendering or video generation."""
import argparse,hashlib,json,math
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
p=argparse.ArgumentParser()
p.add_argument('--out',required=True)
import sys
args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
scene=bpy.context.scene
scene.render.resolution_x=960;scene.render.resolution_y=540
scene.render.resolution_percentage=100;scene.render.fps=24
scene.frame_start=1;scene.frame_end=49
def camera(name,location,lens=50):
    data=bpy.data.cameras.new(name)
    data.type='PERSP';data.lens=lens;data.sensor_width=36;data.sensor_fit='HORIZONTAL'
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=location
    obj.rotation_euler=(Vector((0,0,1.6))-obj.location).to_track_quat('-Z','Y').to_euler()
    return obj
def height(cam,depth):
    low=world_to_camera_view(scene,cam,Vector((0,depth,1.1)))
    high=world_to_camera_view(scene,cam,Vector((0,depth,2.1)))
    return abs(high.y-low.y)
def measure(cam):
    bpy.context.view_layer.update()
    return {'location':list(cam.location),'lens_mm':cam.data.lens,'subject_height':height(cam,0),'background_height':height(cam,6),'background_to_subject':height(cam,6)/height(cam,0)}
dolly=camera('Dolly_fixed50',(0,-6,1.6))
start=measure(dolly)
dolly.keyframe_insert(data_path='location',frame=1)
dolly.location=(0,-3,1.6)
dolly.keyframe_insert(data_path='location',frame=49)
dolly_end=measure(dolly)
zoom=camera('Zoom_fixed_position',(0,-6,1.6))
zoom.data.lens=50;zoom.data.keyframe_insert(data_path='lens',frame=1)
zoom.data.lens=100;zoom.data.keyframe_insert(data_path='lens',frame=49)
zoom_end=measure(zoom)
assert abs(dolly_end['subject_height']-zoom_end['subject_height'])<1e-5
assert abs(start['background_to_subject']-.5)<1e-5
assert abs(dolly_end['background_to_subject']-1/3)<1e-5
assert abs(zoom_end['background_to_subject']-.5)<1e-5
curve=bpy.data.curves.new('CameraPath','CURVE');curve.dimensions='3D';curve.path_duration=48
spline=curve.splines.new('POLY');spline.points.add(2)
for point,coordinate in zip(spline.points,[(0,-6,1.6,1),(2,-5,1.6,1),(3,-3,1.6,1)]):point.co=coordinate
path=bpy.data.objects.new('CameraPath',curve);scene.collection.objects.link(path)
target=bpy.data.objects.new('LookTarget',None);scene.collection.objects.link(target);target.location=(0,0,1.6)
pathcam=camera('PathCamera',(0,0,0))
follow=pathcam.constraints.new('FOLLOW_PATH');follow.target=path;follow.use_fixed_location=True;follow.use_curve_follow=False
track=pathcam.constraints.new('TRACK_TO');track.target=target;track.track_axis='TRACK_NEGATIVE_Z';track.up_axis='UP_Y'
samples=[]
for factor in [0,.5,1]:
    follow.offset_factor=factor;bpy.context.view_layer.update()
    ev=pathcam.evaluated_get(bpy.context.evaluated_depsgraph_get())
    pos=ev.matrix_world.translation.copy()
    direction=(ev.matrix_world.to_quaternion()@Vector((0,0,-1))).normalized()
    expected=(target.matrix_world.translation-pos).normalized()
    assert direction.dot(expected)>.9999
    samples.append({'offset_factor':factor,'position':list(pos),'aim_dot':direction.dot(expected)})
assert (Vector(samples[0]['position'])-Vector(samples[-1]['position'])).length>1
follow.offset_factor=.5;bpy.context.view_layer.update()
before=pathcam.evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.copy()
target.location.x=1;bpy.context.view_layer.update()
after=pathcam.evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.copy()
assert (before.translation-after.translation).length<1e-6
assert abs(before.to_quaternion().dot(after.to_quaternion()))<.999999
target.location.x=0
follow.offset_factor=0;follow.keyframe_insert(data_path='offset_factor',frame=1)
follow.offset_factor=1;follow.keyframe_insert(data_path='offset_factor',frame=49)
# Default Blender interpolation is deliberately not treated as a measured speed profile.
scene.camera=dolly;scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'camera_geometry.blend'))
report={'blender':bpy.app.version_string,'rendered':False,'gpu_inference':False,'scope':'CPU-only Blender projection and dependency-graph evaluation, not media quality','projection':{'sensor_width_mm':36,'sensor_fit':'HORIZONTAL','resolution':[960,540],'equal_world_height_m':1,'start':start,'dolly_end':dolly_end,'zoom_end':zoom_end},'follow_path':{'samples':samples,'target_move_preserves_path_position':True,'camera_aim_follows_target':True,'animation_speed_profile_tested':False},'checks_passed':7}
(out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
