def select_gpu(devices, gpu_name=''):
    candidates=[d for d in devices if d.type != 'CPU']
    if gpu_name:
        candidates=[d for d in candidates if gpu_name.casefold() in d.name.casefold()]
    if not candidates:
        raise RuntimeError(f'Requested GPU not found: {gpu_name or "any"}')
    return candidates[0]


def configure_cycles(scene, gpu_name='', backend='AUTO'):
    import bpy

    prefs=bpy.context.preferences.addons['cycles'].preferences
    attempts=[]
    backends=['OPTIX','CUDA','HIP','METAL','ONEAPI'] if backend=='AUTO' else [backend]
    supported_gpus=[]
    supported_backend=False
    for candidate in backends:
        try:
            prefs.compute_device_type=candidate
        except TypeError as exc:
            attempts.append({'backend':candidate,'status':'NOT_SUPPORTED_BY_BUILD','detail':str(exc)})
            continue
        supported_backend=True
        prefs.refresh_devices()
        devices=[d for d in prefs.devices if d.type==candidate]
        if not devices:
            attempts.append({'backend':candidate,'status':'NO_SUPPORTED_GPU_EXPOSED'})
            continue
        supported_gpus.extend(d.name for d in devices)
        matches=[d for d in devices if not gpu_name or gpu_name.casefold() in d.name.casefold()]
        if not matches:
            attempts.append({'backend':candidate,'status':'REQUESTED_GPU_ABSENT','devices':[d.name for d in devices]})
            continue
        chosen=select_gpu(matches,gpu_name)
        for device in prefs.devices:
            device.use=device.id==chosen.id and device.type==candidate
        scene.cycles.device='GPU'
        return {'device':'GPU','backend':candidate,'gpu_name':chosen.name,'gpu_id':chosen.id,'enabled_devices':[d.name for d in prefs.devices if d.use],'cpu_fallback_reason':None,'discovery':attempts}
    if supported_backend or supported_gpus or backend!='AUTO' or gpu_name:
        raise RuntimeError(f'GPU selection failed; CPU fallback prohibited. GPU devices: {supported_gpus}; attempts: {attempts}')
    scene.cycles.device='CPU'
    return {'device':'CPU','backend':None,'gpu_name':None,'enabled_devices':[],'cpu_fallback_reason':'This Blender build supports none of the configured GPU compute backends.','discovery':attempts}
