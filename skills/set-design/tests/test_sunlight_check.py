import importlib.util, math, sys, unittest
from pathlib import Path
sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('sunlight_check',Path(__file__).resolve().parents[1]/'scripts/sunlight_check.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
class WindowSunlightTests(unittest.TestCase):
    def data(self,az=195,el=32,energy=4):return {'room':{'width':5.6,'depth':4.4},'openings':[{'id':'W1','type':'window','wall':'W','offset':.9,'width':1.8,'height':1.35,'sill':.85}],'times':[{'id':'afternoon','sun':{'azimuth':az,'elevation':el,'energy':energy}}]}
    def floor(self,origin,direction):
        t=-origin[2]/direction[2]
        return {'object':'floor','xyz':[origin[i]+t*direction[i] for i in range(3)]}
    def test_west_afternoon_four_corners_hit_floor_extent(self):
        r=s.trace_window_sunlight(self.data(),self.floor)['windows'][0]
        self.assertEqual(len(r['rays']),4);self.assertTrue(all(x['status']=='HIT' for x in r['rays']))
        xs=[x['landing']['xyz'][0] for x in r['rays']];ys=[x['landing']['xyz'][1] for x in r['rays']]
        self.assertAlmostEqual(min(xs),.851*math.cos(math.radians(15))/math.tan(math.radians(32)),places=5)
        self.assertTrue(3.3<max(xs)<3.5);self.assertTrue(1.2<min(ys)<1.4);self.assertTrue(3.5<max(ys)<3.7)
    def test_east_sun_cannot_enter_west_window(self):
        r=s.trace_window_sunlight(self.data(az=0),lambda *_:self.fail('must not cast'))['windows'][0]
        self.assertEqual(r['status'],'NOT_ENTERING_WINDOW');self.assertEqual(len(r['rays']),4)
    def test_below_horizon_and_disabled_sun(self):
        for d,expected in [(self.data(el=-1),'SUN_BELOW_HORIZON'),(self.data(energy=0),'SUN_OFF')]:
            self.assertEqual(s.trace_window_sunlight(d,lambda *_:self.fail('must not cast'))['windows'][0]['status'],expected)
    def test_north_window_maps_to_room_depth(self):
        d=self.data(az=90);d['openings'][0]['wall']='N';r=s.trace_window_sunlight(d,self.floor)['windows'][0]
        self.assertEqual(r['status'],'DIRECT_SUN');self.assertTrue(all(abs(x['corner_xyz'][1]-4.4)<1e-8 for x in r['rays']))
    def test_first_occluder_is_preserved(self):
        def curtain(origin,direction):
            distance=(.1-origin[0])/direction[0]
            return {'object':'curtain','xyz':[p+distance*d for p,d in zip(origin,direction)]}
        r=s.trace_window_sunlight(self.data(),curtain)['windows'][0]
        self.assertTrue(all(x['landing']['object']=='curtain' for x in r['rays']))
    def test_no_sun_or_no_window(self):
        d=self.data();d['times']=[{'id':'night'}];self.assertEqual(s.trace_window_sunlight(d,self.floor)['windows'],[])
        d=self.data();d['openings']=[];self.assertEqual(s.trace_window_sunlight(d,self.floor)['windows'],[])
    def test_start_is_outside_entire_wall_thickness(self):
        d=self.data();d['room']['wall']=.24
        r=s.trace_window_sunlight(d,self.floor)['windows'][0]
        self.assertTrue(all(x['sample_xyz'][0]<-.24 for x in r['rays']))
        self.assertTrue(all(abs(x['inside_sample_xyz'][0])<1e-10 for x in r['rays']))
    def test_lintel_hit_is_blocked_without_interior_landing(self):
        def lintel(origin,direction):return {'object':'window_lintel','xyz':[origin[i]+direction[i]*.02 for i in range(3)]}
        rays=s.trace_window_sunlight(self.data(),lintel)['windows'][0]['rays']
        self.assertTrue(all(r['status']=='OCCLUDED_APERTURE' and r['landing'] is None and r['first_hit']['object']=='window_lintel' for r in rays))
    def test_exterior_start_maps_all_four_wall_axes(self):
        for wall,az,axis,value,sign in [('W',180,0,0,-1),('E',0,0,5.6,1),('S',270,1,0,-1),('N',90,1,4.4,1)]:
            d=self.data(az=az);d['openings'][0]['wall']=wall;d['room']['wall']=.12
            rays=s.trace_window_sunlight(d,self.floor)['windows'][0]['rays']
            self.assertTrue(all((r['sample_xyz'][axis]-value)*sign>.12 for r in rays))
if __name__=='__main__':unittest.main()
