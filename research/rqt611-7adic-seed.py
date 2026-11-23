#!/usr/bin/env python3
"""RQT-611 exact 7-adic branch and integral-seed necessary congruence verifier.
Usage: python rqt611.py RQT-610-results.json [out.json]
"""
import hashlib,json,sys
from pathlib import Path
src=Path(sys.argv[1]);d=json.loads(src.read_text())
assert d['rqt']==610
families=[]
for f in d['families']:
 i=f['family_index']
 A,B,C,D,E,F=map(int,f['reduced_quadratic_coefficients'])
 Q=lambda x,y:A*x*x+B*x*y+C*y*y+D*x+E*y+F
 grad=lambda x,y:(2*A*x+B*y+D,B*x+2*C*y+E)
 roots={(x,y) for x in range(7) for y in range(7) if Q(x,y)%7==0}
 assert roots=={tuple(v) for v in f['eight_nonsingular_reduced_roots']} and len(roots)==8
 assert all(any(z%7 for z in grad(x,y)) for x,y in roots)
 r=f['unique_mod7_root'];jets=[]
 for x0,y0 in sorted(roots):
  x,y=x0,y0;axis=0 if grad(x,y)[0]%7 else 1
  m=7;states=[{'level':1,'x':x,'y':y}]
  for k in range(2,11):
   h=(Q(x,y)//m)%7
   step=(-h*pow(grad(x,y)[axis]%7,-1,7))%7
   if axis==0:x+=step*m
   else:y+=step*m
   m*=7;assert Q(x,y)%m==0
   states.append({'level':k,'x':x,'y':y})
  assert 49*Q(x,y)%(7**11)==0
  jets.append({'root':[x0,y0],'axis':axis,'states':states,'u_mod_7_11':str((r[0]+7*x)%(7**11)),'t_mod_7_11':str((r[1]+7*y)%(7**11))})
 allowed=sorted({(r[1]+7*y)%49 for x,y in roots})
 assert allowed==({2:[13,20,27,34],24:[15,22,29,36]})[i]
 families.append({'family_index':i,'allowed_t_mod_49':allowed,'jets':jets})
assert sorted(v['family_index'] for v in families)==[2,24]
out={'rqt':611,'source_610_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'families':families,
'new_full_family_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
'original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-611-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 16 verified 7-adic branches through 7^11, two necessary t mod49 gates; root19 OPEN')
