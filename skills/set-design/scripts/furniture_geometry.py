import math

SHAPES={'ring_light','bookcase','potted_plant'}


def primitives(it):
    w,d,h=it['size']
    pieces=[]
    def box(suffix,center,size):
        pieces.append({'suffix':suffix,'kind':'box','center':center,'size':size})
    if it['shape']=='bookcase':
        t=min(0.025,w/12,d/5,h/12)
        box('back',(0,d/2-t/2,h/2),(w,t,h))
        for side in [-1,1]:
            box('side'+str(side),(side*(w-t)/2,0,h/2),(t,d,h))
        for n,z in enumerate([t/2]+[t+(h-2*t)*k/5 for k in range(1,5)]+[h-t/2]):
            box('shelf'+str(n),(0,0,z),(w-2*t,d,t))
            if n==5:
                continue
            available=(h-2*t)/5-t
            for j,factor in enumerate([0.80,0.72,0.88,0.77]):
                bh=available*factor
                box(f'book{n}_{j}',((j-1.5)*w*0.22,-d*0.04,z+t/2+bh/2),(w*(0.10+0.015*(j%2)),d*0.70,bh))
    elif it['shape']=='ring_light':
        radius=min(0.225,w/2,d/2,h/4)
        tube=radius*0.08
        z=h-radius
        pieces.append({'suffix':'ring','kind':'ring','center':(0,0,z),'radius':radius-tube,'tube':tube})
        pieces.append({'suffix':'column','kind':'rod','a':(0,0,0.25),'b':(0,0,z-radius),'radius':0.012})
        for k,(x,y) in enumerate([(-w/2+0.015,-d/2+0.015),(w/2-0.015,-d/2+0.015),(0,d/2-0.015)]):
            pieces.append({'suffix':f'leg{k}','kind':'rod','a':(x,y,0.015),'b':(0,0,0.40),'radius':0.012})
            box(f'foot{k}',(x,y,0.006),(0.030,0.030,0.012))
        box('phone',(0,-0.018,z),(0.070,0.015,0.140))
        box('clamp',(0,0.01,z-0.04),(0.095,0.025,0.018))
    elif it['shape']=='potted_plant':
        pot_h=h*0.38
        pot_d=min(w,d)*0.70
        pieces.append({'suffix':'pot','kind':'cylinder','center':(0,0,pot_h/2),'size':(pot_d,pot_d,pot_h)})
        pieces.append({'suffix':'leaves','kind':'ellipsoid','center':(0,0,pot_h+(h-pot_h)/2),'size':(w,d,h-pot_h)})
    else:
        raise ValueError(it['shape'])
    return pieces


def local_boxes(p):
    if p['kind']=='ring':
        x,y,z=p['center']
        r,t=p['radius'],p['tube']
        out=[]
        for k in range(32):
            a,b=2*math.pi*k/32,2*math.pi*(k+1)/32
            xs=[x+r*math.cos(a),x+r*math.cos(b)]
            zs=[z+r*math.sin(a),z+r*math.sin(b)]
            lo=(min(xs)-t,y-t,min(zs)-t)
            hi=(max(xs)+t,y+t,max(zs)+t)
            out.append((f"{p['suffix']}{k}",tuple((lo[i]+hi[i])/2 for i in range(3)),tuple(hi[i]-lo[i] for i in range(3))))
        return out
    if p['kind']=='rod':
        r=p['radius']
        lo=[min(p['a'][i],p['b'][i])-r for i in range(3)]
        hi=[max(p['a'][i],p['b'][i])+r for i in range(3)]
        return [(p['suffix'],tuple((lo[i]+hi[i])/2 for i in range(3)),tuple(hi[i]-lo[i] for i in range(3)))]
    return [(p['suffix'],p['center'],p['size'])]
