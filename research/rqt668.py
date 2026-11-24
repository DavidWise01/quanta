#!/usr/bin/env python3
"""RQT-668 exact affine Pell chart stabilizer. Run:
python research/rqt668.py RQT-619-results.json [RQT-668-results.json]
Python standard library; no real-orbit unit or seed claimed.
"""
import json,hashlib,math,sys
from pathlib import Path
SHA='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
def coeffs(c):
 r0,r1,r2,r3,r4,r5=c
 return r1*r1-4*r0*r2,r1*r3-2*r0*r4,r3*r3-4*r0*r5
def gate(c,U,V):
 r0,r1,r2,r3,r4,r5=c;a,h,_=coeffs(c);D=abs(2*r0)
 if U*U-a*V*V!=1 or ((U-1)*h)%a:return False
 C=((U-1)*h)//a
 return (V*(a-r1*r1))%D==0 and ((U-r1*V-1)*r3+V*h-r1*C)%D==0
def apply(c,U,V,t,u):
 r0,r1,r2,r3,r4,r5=c;a,h,_=coeffs(c)
 z=a*t+h;y=2*r0*u+r1*t+r3
 Z=U*z+a*V*y;Y=V*z+U*y
 if (Z-h)%a:return None
 T=(Z-h)//a;v=Y-r1*T-r3
 if v%(2*r0):return None
 return T,v//(2*r0)
def G(c,u,t):
 r0,r1,r2,r3,r4,r5=c
 return r0*u*u+r1*u*t+r2*t*t+r3*u+r4*t+r5
def multiply(a,x,y):
 U,V=x;X,Y=y
 return U*X+a*V*Y,U*Y+V*X
def main():
 p=Path(sys.argv[1]);raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
 data=json.loads(raw);assert len(data['families'])==27
 rows=[];automatic=[];checks=0
 for rec in data['families']:
  c=tuple(map(int,rec['R_coefficients_as_strings']));r0,r1,r2,r3,r4,r5=c
  a,h,v=coeffs(c);D=abs(2*r0);assert a>0 and D>0
  residue_modulus=a//math.gcd(a,h)
  if residue_modulus==1:automatic.append(rec['canonical_id'])
  assert gate(c,1,0)
  for t in (-1,0,1):
   for u in (-1,0,1):
    assert apply(c,1,0,t,u)==(t,u);checks+=1
  rows.append({'canonical_id':rec['canonical_id'],'members':rec['member_ids'],
   'a':str(a),'h':str(h),'D':str(D),'conservative_M':str(a*D),
   'minimal_U_shift_modulus':str(residue_modulus),'parameter_shift_automatic':residue_modulus==1})
 assert automatic==[67] and checks==243
 synthetic_c=(1,0,-2,0,0,-1);a,h,v=coeffs(synthetic_c);M=a*2
 assert gate(synthetic_c,3,1) and apply(synthetic_c,3,1,0,1)==(2,3)
 z=(1,0);first=None;steps=[]
 for i in range(1,17):
  z=multiply(a,z,(3,1));U,V=z
  assert gate(synthetic_c,U,V)
  t,u=apply(synthetic_c,U,V,0,1)
  assert G(synthetic_c,u,t)==0
  steps.append({'power':i,'u':str(u),'t':str(t),'original_G':0})
  if U%M==1 and V%M==0 and first is None:first=i
 assert first==16
 out={'rqt':668,'source_sha256':SHA,'canonical_orbits':27,
 'exact_gate':'U²-aV²=1; a|(U-1)h; D|V(a-r1²); D|(U-r1V-1)r3+Vh-r1((U-1)h/a)',
 'parameter_shift_modulus':'a/gcd(a,h)','automatic_parameter_shift_orbits':automatic,
 'identity_chart_coordinate_checks':checks,'records':rows,
 'synthetic':{'base_unit':[3,1],'exact_gate_power':1,'old_gate_power':16,'steps':steps},
 'new_all_scale_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
 'root19':'OPEN','original_22d_wall':'NOT REPLAYED',
 'real_chart_units_or_seeds_constructed':0,
 'scope':'Exact all-affine-lattice gate, not a minimum for norm-specific subset.'}
 dst=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-668-results.json')
 dst.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS RQT-668: 27 charts, 243 identity checks, synthetic 16 to 1')
if __name__=='__main__':main()
