import sys
import numpy as np
import math

rho_water = 1025.0      # water density
wdepth = 200.0          # water depth
ma  = 685.0             # mass per length in air
D   = 0.333             # mooring line diameter
A   = np.pi/4*D**2      
mw = ma - rho_water*A   # mass per length in water
EA  = 3.27e+09          # mooring line stiffness 
cm  = 1.82
cdp = 1.11
cdl = .20               
L   = 850.0             # un-stretched length of mooring lines
R_anchor   = 837.6      # radius from origin to anchor (in xy-plane)
R_fairlead = 58.0       # radius from origin to fairlead (in xy-plane)
z_anchor    = wdepth    # z-pos of anchor (at bottom)
z_fairlead  = 14.0      # z-pos of fairlead
z_ifb = -15.0           # z-pos of interface body (body ifb)
nelem = 20

outfile = ['mooring_sys.inc','mooring_sys_init.inc']
for file in outfile:
    sys.stdout = open(file, 'w')
    print('; THIS FILE IS GENERATED BY \'gen_mooring.py\'')
    for i in range(3):
        phi = i*np.pi*2/3
        dvec = np.array([math.sin(phi),-math.cos(phi)])
        xy_anchor        = dvec *  R_anchor
        xy_fairlead_init = dvec * (R_anchor - L)
        xy_fairlead      = dvec *  R_fairlead
        print('begin ext_sys ;')
        print('  module elasticBar ;')
        print('  name   line{:1d} ;'.format(i+1))
        print('  dll    ESYSMooring.dll ;')
        print('  ndata 9  ;') 
        print('  data nelem {:d} ;'.format(nelem))
        print('  data mass {:10.3e} {:10.3e} ; '.format(ma,mw));
        print('  data start_pos {:10.3e} {:10.3e} {:10.3e} ;'.format(xy_anchor[0],xy_anchor[1],z_anchor))
        print('  data end_pos {:10.3e} {:10.3e} {:10.3e} ;'.format(xy_fairlead_init[0],xy_fairlead_init[1],z_anchor))
        print('  data cdp_cdl_cm {:10.3e} {:10.3e} {:10.3e} ;'.format(1/2*rho_water*cdp*D,1/2*rho_water*cdl*D,rho_water*cm*A))
        print('  data axial_stiff {:10.3e} ;'.format(EA))
        print(';  data read_write_initcond_file <fname> ;')
        if (file == outfile[0]):
            print('  data read_write_initcond 1 0 ;')
        else:
            print('  data read_write_initcond 0 1 ;')
        print('  data bottom_prop {:10.3e} 0.01 0.1 ;'.format(wdepth))
        print(';  data apply_wave_forces <wa> ;')
        print(';  data apply_wind_forces <wi> ;')     
        print(';  data output position <node> ;')     
        print(';  data output force <node> ;')     
        print(';  data mass_summary <file> ;')     
        print('  data end ;')     
        print('end ext_sys ;')
        print(';')
    
sys.stdout.close()
sys.stdout = open('mooring_cstr.inc', 'w')
print('; THIS FILE IS GENERATED BY \'gen_mooring.py\'')
for i in range(3):
    phi = i*np.pi*2/3
    dvec = np.array([math.sin(phi),-math.cos(phi)])
    xy_fairlead      = dvec *  R_fairlead
    print('begin dll ;    ')   
    print('  dll ESYSMooring.DLL ; ')
    print('  init    cstrbarfixedtoglobal_init   ;')
    print('  update  cstrbarfixedtoglobal_update ;')
    print('  neq     3 ;')
    print('  nbodies 0 ;')
    print('  nesys   1 ;')
    print('  esys_node  line{:1d} {:d} ;'.format(i+1,1))
    print('end dll ;')   
    print(';')   
   
    print('begin dll ;    ')   
    print('  dll ESYSMooring.DLL ; ')
    print('  ID  {:10.3e} {:10.3e} {:10.3e} 10.0 ;  '.format(xy_fairlead[0],xy_fairlead[1],z_fairlead - z_ifb))
    print('  init    cstrbarsfixedtobodyrelative_init ;')
    print('  update  cstrbarsfixedtobodyrelative_update ;')
    print('  neq     3 ;')
    print('  nbodies 1 ;')
    print('  nesys   1 ;')
    print('  mbdy_node  ifb {:d} ;'.format(1))
    print('  esys_node  line{:1d} {:d} ;'.format(i+1,nelem+1))
    print('end dll ;')   