#!/usr/bin/env python3
"""RQT-669 exact affine Pell modular action, closure and inverse verifier.
python rqt669.py RQT-619-results.json [RQT-669-results.json]
Stdlib only. No new original-family Pell unit or seed asserted.
"""
import hashlib,json,math,sys
from pathlib import Path
SOURCE='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
def entries(c):
 r0,r1,r2,r3,r4,r5=c
 a=r1*r1-4*r0*r2;h=r1*r3-2*r0*r4;D=abs(2*r0)
 return a,h,D
def gate(c,U,V):
 r0,r1,r2,r3,r4,r5=c;a,h,D=entries(c)
 if U*U-a*V*V!=1 or ((U-1)*h)%a:return False
 C=((U-1)*h)//a
 return V*(a-r1*r1)%D==0 and ((U-r1*V-1)*r3+V*h-r1*C)%D==0
def affine(c,U,V):
 assert gate(c,U,V)
 r0,r1,r2,r3,r4,r5=c;a,h,D=entries(c)
 C=((U-1)*h)//a
 A=((U+V*r1,V*D),(V*(a-r1*r1)//D,U-r1*V))
 b=(V*r3+C,((U-r1*V-1)*r3+V*h-r1*C)//D)
 assert A[0][0]*A[1][1]-A[0][1]*A[1][0]==1
 return A,b
def step(T,x):
 A,b=T;t,k=x
 return (A[0][0]*t+A[0][1]*k+b[0],A[1][0]*t+A[1][1]*k+b[1])
def mul(T,S):
 A,b=T;B,c=S
 C=tuple(tuple(sum(A[i][l]*B[l][j] for l in range(2)) for j in range(2)) for i in range(2))
 d=tuple(sum(A[i][l]*c[l] for l in range(2))+b[i] for i in range(2))
 return C,d
def unit_mul(a,x,y):
 U,V=x;X,Y=y;return U*X+a*V*Y,U*Y+V*X
def G(c,u,t):
 r0,r1,r2,r3,r4,r5=c
 return r0*u*u+r1*u*t+r2*t*t+r3*u+r4*t+r5
def orbit_cycles(T,m):
 remaining={(t,k) for t in range(m) for k in range(m)}
 cycles=[]
 while remaining:
  start=min(remaining);cur=start;length=0
  while True:
   assert cur in remaining
   remaining.remove(cur);length+=1
   nx=step(T,cur);cur=(nx[0]%m,nx[1]%m)
   if cur==start:break
  cycles.append(length)
 return {'modulus':m,'points':m*m,'cycle_histogram':{str(n):cycles.count(n) for n in sorted(set(cycles))},'max_cycle':max(cycles),'permutation_order':math.lcm(*cycles)}
def main():
 src=Path(sys.argv[1]);raw=src.read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE
 obj=json.loads(raw);assert obj['rqt']==619 and len(obj['families'])==27
 identity=(((1,0),(0,1)),(0,0));recs=[];checks=0
 for record in obj['families']:
  c=tuple(map(int,record['R_coefficients_as_strings']));a,h,D=entries(c)
  assert a>0 and D>0
  assert gate(c,1,0) and affine(c,1,0)==identity
  for t in (-101,0,103):
   for k in (-101,0,103):
    assert step(identity,(t,k))==(t,k);checks+=1
  recs.append({'canonical_id':record['canonical_id'],'a':str(a),'h':str(h),'D':str(D),
               'integer_parameter_shift_modulus':str(a//math.gcd(a,h)),
               'identity_affine_action_verified':True})
 assert checks==243
 c=(1,0,-2,0,0,-1);a,h,D=entries(c);assert (a,h,D)==(8,0,2)
 base=(3,1);assert gate(c,*base)
 T=affine(c,*base);assert T==(((3,2),(4,3)),(0,0))
 inverse=affine(c,3,-1)
 assert mul(T,inverse)==identity==mul(inverse,T)
 U,V=(1,0);power=identity;steps=[]
 for n in range(1,17):
  U,V=unit_mul(a,(U,V),base);power=mul(T,power)
  assert gate(c,U,V) and affine(c,U,V)==power
  assert mul(power,affine(c,U,-V))==identity
  t,k=step(power,(0,1))
  assert G(c,k,t)==0
  steps.append({'power':n,'U':str(U),'V':str(V),'u':str(k),'t':str(t),'original_equation':0})
 mods=[2,4,8,16,32,64]
 modular=[orbit_cycles(T,m) for m in mods]
 result={'rqt':669,'source_rqt619_sha256':SOURCE,'canonical_orbits':27,
 'identity_coordinate_checks':checks,'exact_affine_formula':{'matrix':[['U+V*r1','V*D'],['V*(a-r1^2)/D','U-r1*V']],
 'translation':['V*r3+(U-1)*h/a','((U-r1*V-1)*r3+V*h-r1*(U-1)*h/a)/D'],
 'determinant':'U^2-a*V^2=1'},
 'proof':'Integral affine matrices with determinant 1 and integer shifts form a subgroup; negative-V Pell inverse preserves the lattice as the inverse automorphism.',
 'real_orbits':recs,'synthetic':{'G':'u^2-2t^2-1','base_unit':[3,1],
 'unit_matrix':[[3,2],[4,3]],'inverse_unit':[3,-1],
 'powers_1_to_16':steps,'modular_cycle_decompositions':modular},
 'new_nontrivial_real_units':0,'new_real_integer_seeds':0,
 'selected_excluded':82,'selected_unresolved':53,'new_all_scale_exclusions':0,
 'root19':'OPEN','original_22d_wall':'NOT REPLAYED',
 'scope':'Symbolic exact affine subgroup; numeric finite modular cycles synthetic only.'}
 dst=Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-669-results.json')
 dst.write_text(json.dumps(result,indent=2)+'\n')
 print('PASS: 27 source charts,',checks,'identity checks; synthetic cycles',[(x['modulus'],x['permutation_order']) for x in modular])
 print('SHA256',hashlib.sha256(dst.read_bytes()).hexdigest())
if __name__=='__main__':main()
