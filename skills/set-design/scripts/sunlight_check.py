import math

OUTWARD={'W':(-1,0,0),'E':(1,0,0),'S':(0,-1,0),'N':(0,1,0)}

def sun_vector(sun):
    az=math.radians(float(sun['azimuth']));el=math.radians(float(sun['elevation']))
    return (math.cos(el)*math.cos(az),math.cos(el)*math.sin(az),math.sin(el))

def window_corners(window,room,inset=0):
    a=window['offset']+inset;b=window['offset']+window['width']-inset
    lo=window.get('sill',.9)+inset;hi=window.get('sill',.9)+window.get('height',1.2)-inset
    wall=window['wall'];points=[]
    for tag,u,z in [('lower_start',a,lo),('lower_end',b,lo),('upper_start',a,hi),('upper_end',b,hi)]:
        xyz=(0,u,z) if wall=='W' else (room['width'],u,z) if wall=='E' else (u,0,z) if wall=='S' else (u,room['depth'],z)
        points.append((tag,xyz))
    return points

def trace_window_sunlight(data,cast_ray):
    records=[];inset=.001
    for t in data.get('times',[]):
        if not t.get('sun'):continue
        sun=t['sun'];toward=sun_vector(sun);direction=tuple(-v for v in toward)
        for window in [op for op in data.get('openings',[]) if op['type']=='window']:
            dot=sum(a*b for a,b in zip(toward,OUTWARD[window['wall']]))
            reason='SUN_OFF' if sun.get('energy',3)<=0 else 'SUN_BELOW_HORIZON' if sun['elevation']<=0 else 'NOT_ENTERING_WINDOW' if dot<=1e-8 else 'DIRECT_SUN'
            exact=window_corners(window,data['room']);samples=window_corners(window,data['room'],inset);rays=[]
            for (name,corner),(_,sample) in zip(exact,samples):
                thickness=float(data['room'].get('wall',.12))
                to_inside=(thickness+.001)/dot if dot>1e-8 else 0
                origin=tuple(p+s*to_inside for p,s in zip(sample,toward))
                hit=cast_ray(origin,direction) if reason=='DIRECT_SUN' else None
                distance=sum((q-p)*d for q,p,d in zip(hit['xyz'],origin,direction)) if hit else None
                blocked=hit is not None and distance<=to_inside+.0001
                status=reason if reason!='DIRECT_SUN' else 'OCCLUDED_APERTURE' if blocked else 'HIT' if hit else 'ESCAPED_OR_NO_SURFACE'
                rays.append({'corner':name,'corner_xyz':list(corner),'inside_sample_xyz':list(sample),'sample_xyz':list(origin),'direction':list(direction),'wall_thickness_m':thickness,'distance_to_inside_m':to_inside,'first_hit_distance_m':distance,'status':status,'first_hit':hit,'landing':None if blocked else hit})
            records.append({'time':t['id'],'window':window['id'],'sun':sun,'status':reason,'rays':rays})
    return {'method':'For each interior aperture corner inset1mm, back-project toward sun to1mm beyond the exterior wall face. Trace incoming ray through the entire wall thickness. A first hit before reaching the interior aperture is OCCLUDED_APERTURE, with no invented interior landing. Azimuth follows set.json room coordinates.','aperture_inset_m':inset,'limits':['Four boundary rays are a footprint diagnostic, not complete irradiance/penumbra/whole-patch visibility proof','Diffuse skylight, glazing and exterior obstructions absent from model are not simulated by this report','Full modeled scene before camera hides; mutually exclusive stand-ins can occlude rays. Derive per-time scene inputs when needed.'],'windows':records}
