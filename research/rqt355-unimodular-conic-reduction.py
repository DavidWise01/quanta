#!/usr/bin/env python3
"""RQT-355: exact unimodular ternary reduction and finite null search.
Authentic RQT-242 F4; RQT-351 supplies rational existence.
No explicit rational/null vector or root18 is claimed.
"""
import json
from fractions import Fraction as Q
from math import isqrt, floor, ceil
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
cases=[(194,195,[[1,3,1],[-25,-74,-24],[113,340,113]]),
       (201,202,[[1,2,1],[-26,-51,-25],[117,235,117]])]
results=[];limit=250
for m,n,Vlist in cases:
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 G=T.T*F*T;V=s.Matrix(Vlist)
 assert abs(V.det())==1
 A=V.T*G*V
 ix=[0,2];P=-A.extract(ix,ix);b=A.extract(ix,[1])
 assert P[0,0]>0 and P.det()>0
 center=P.inv()*b; beta=A[1,1]+(b.T*P.inv()*b)[0]
 assert beta>0
 c0=center[0];rad2=beta*P.inv()[0,0]
 c0=Q(int(c0.p),int(c0.q));rad2=Q(int(rad2.p),int(rad2.q))
 J=[[int(z) for z in row] for row in A.tolist()]
 pairs=positive=squares=0
 for h in range(1,limit+1):
  rr=rad2*h*h
  radius=isqrt(rr.numerator//rr.denominator)+2
  cp=c0*h;low=floor(cp)-radius-1;high=ceil(cp)+radius+1
  assert (cp-low)**2>=rr and (high-cp)**2>=rr
  for z0 in range(low,high+1):
   pairs+=1
   aa=J[2][2];bb=2*(J[0][2]*z0+J[1][2]*h)
   cc=J[0][0]*z0*z0+2*J[0][1]*z0*h+J[1][1]*h*h
   disc=bb*bb-4*aa*cc
   if disc<0:continue
   positive+=1;root=isqrt(disc)
   if root*root!=disc:continue
   squares+=1
   for numerator in set((-bb+root,-bb-root)):
    if numerator%(2*aa)==0:
     zz=s.Matrix([z0,h,numerator//(2*aa)])
     u=T*V*zz
     assert (u.T*F*u)[0]==0
     raise AssertionError('EXACT ISOTROPIC WITNESS: '+str(list(u)))
 results.append({'slope':f'{m}/{n}','detV':int(V.det()),
  'transformV':Vlist,
  'reduced_gram':[[int(v) for v in row] for row in A.tolist()],
  'old_max_entry_digits':len(str(max(abs(int(v)) for v in G))),
  'new_max_entry_digits':len(str(max(abs(int(v)) for v in A))),
  'reduced_height_z1_abs_excluded':[1,limit],
  'coordinate_pairs':pairs,'nonnegative_discriminants':positive,
  'perfect_square_discriminants':squares})
assert [(x['coordinate_pairs'],x['nonnegative_discriminants'],x['perfect_square_discriminants']) for x in results]==[(229554,227820,0),(185752,184006,0)]
print(json.dumps({'status':'PASS exact unimodular reduction and finite null search',
 'source':'stoicheion RQT242 authentic F4','search_results':results,
 'explicit_isotropic':'OPEN','root18':'OPEN','roots19_to21':'OPEN'},indent=2))
