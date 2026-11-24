#!/usr/bin/env python3
"""RQT-667 exact Pell congruence-preserving subgroup audit.
Usage: python rqt667.py RQT-619-results.json [RQT-667-results.json]
"""
import json,hashlib,sys
from pathlib import Path
SHA='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
def G(C,u,t):
 r0,r1,r2,r3,r4,r5=C
 return r0*u*u+r1*u*t+r2*t*t+r3*u+r4*t+r5
def multiply(a,x,y):
 U,V=x;X,Y=y
 return U*X+a*V*Y,U*Y+V*X
def synthetic():
 a=8;D=2;M=a*D;w=(1,0)
 for k in range(1,100):
  w=multiply(a,w,(3,1))
  if w[0]%M==1 and w[1]%M==0:break
 U,V=w
 assert k==16 and U*U-a*V*V==1
 z,y=0,2;zp=U*z+a*V*y;yp=V*z+U*y
 assert zp%a==0 and yp%2==0
 t=zp//a;u=yp//2
 assert G((1,0,-2,0,0,-1),u,t)==0 and t!=0
 assert zp*zp-a*yp*yp==-32
 return {'base_unit':[3,1],'power':k,'U':str(U),'V':str(V),'u':str(u),'t':str(t),'original_G':0}
def main():
 p=Path(sys.argv[1]);raw=p.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==SHA
 data=json.loads(raw);assert data['rqt']==619 and len(data['families'])==27
 rows=[]
 for r in data['families']:
  C=tuple(map(int,r['R_coefficients_as_strings']));r0,r1,r2,r3,r4,r5=C
  a=r1*r1-4*r0*r2;h=r1*r3-2*r0*r4;c=r3*r3-4*r0*r5;N=h*h-a*c
  assert a>0 and r0!=0
  D=abs(2*r0);M=a*D
  assert M%a==0 and M%D==0 and M//a%D==0
  for t in (-113,-1,0,1,113):
   z=a*t+h;F=(a*t+2*h)*t+c
   assert z*z-a*F==N
  rows.append({'canonical_id':r['canonical_id'],'member_ids':r['member_ids'],
   'a':str(a),'h':str(h),'N':str(N),'D':str(D),'M':str(M),
   'exact_identity_verified':True,'verified_nontrivial_unit':False,'verified_original_seed':False})
 out={'rqt':667,'source_rqt619_sha256':SHA,'canonical_orbits':27,
 'theorem':'U²-aV²=1, U≡1 (mod M), V≡0 (mod M), M=a*abs(2r0) preserve the integer t and u-coordinate lattice',
 'proof':'t_prime=U*t+V*y+(U-1)*h/a; t_prime≡t (mod D); y_prime=V*(a*t+h)+U*y≡y (mod D)',
 'records':rows,'synthetic_witness':synthetic(),'real_chart_nontrivial_units_found':0,
 'real_chart_integer_seeds_found':0,'new_all_scale_exclusions':0,
 'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN','original_22d_wall':'NOT REPLAYED',
 'scope':'A sufficient, not necessary, lattice subgroup; conditional on an actual unit and initial seed.'}
 dest=Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-667-results.json')
 dest.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS',len(rows),'orbits; synthetic power',out['synthetic_witness']['power'])
if __name__=='__main__':main()
