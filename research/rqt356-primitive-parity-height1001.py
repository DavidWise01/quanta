#!/usr/bin/env python3
"""RQT-356: original F4 primitive parity and exact reduced null-height scan."""
import itertools,json
from fractions import Fraction as Q
from math import floor,ceil,isqrt
from collections import Counter
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
cases=[(194,195,[[1,3,1],[-25,-74,-24],[113,340,113]]),(201,202,[[1,2,1],[-26,-51,-25],[117,235,117]])]
rat=lambda a:Q(int(a.p),int(a.q))
results=[]
for m,n,Vdata in cases:
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 V=s.Matrix(Vdata)
 assert abs(V.det())==1
 A=V.T*T.T*F*T*V
 parity=Counter()
 for xyz in itertools.product(range(4),repeat=3):
  if all(t%2==0 for t in xyz):continue
  z=s.Matrix(xyz)
  if int((z.T*A*z)[0]//2)%4==0:parity[xyz[1]%2]+=1
 assert dict(parity)=={1:16}
 # Every primitive exact null vector must have odd z1.
 P=-A.extract([0,2],[0,2]);b=A.extract([0,2],[1])
 assert P[0,0]>0 and P.det()>0
 v=P.inv()*b;beta=A[1,1]+(b.T*P.inv()*b)[0]
 assert beta>0
 center=rat(v[0]);r2=rat(beta*P.inv()[0,0])
 J=[[int(z) for z in row] for row in A.tolist()]
 pairs=nonnegative=squares=0
 for h in range(251,1002,2):
  bound=r2*h*h
  extent=isqrt(bound.numerator//bound.denominator)+2
  mid=center*h;lo=floor(mid)-extent-1;hi=ceil(mid)+extent+1
  assert (mid-lo)**2>=bound and (hi-mid)**2>=bound
  for x in range(lo,hi+1):
   pairs+=1
   aa=J[2][2];bb=2*(J[0][2]*x+J[1][2]*h)
   cc=J[0][0]*x*x+2*J[0][1]*x*h+J[1][1]*h*h
   discriminant=bb*bb-4*aa*cc
   if discriminant<0:continue
   nonnegative+=1
   root=isqrt(discriminant)
   if root*root!=discriminant:continue
   squares+=1
   for numerator in {-bb+root,-bb-root}:
    if numerator%(2*aa)==0:
     z=s.Matrix([x,h,numerator//(2*aa)])
     u=T*V*z
     assert (u.T*F*u)[0]==0
     raise AssertionError('EXPLICIT INTEGER NULL VECTOR: '+str(list(u)))
 results.append({'plane':f'{m}/{n}','primitive_mod4_null_classes':16,
 'even_height_classes':0,'new_odd_heights':[251,1001],
 'pairs':pairs,'nonnegative_discriminants':nonnegative,'square_discriminants':squares})
assert [(r['pairs'],r['nonnegative_discriminants'],r['square_discriminants']) for r in results]==[(1711654,1709013,0),(1383028,1380396,0)]
print(json.dumps({'status':'PASS exact finite certificate',
 'source':'authentic stoicheion RQT-242 F4','results':results,
 'new_necessary_primitive_height':'abs(z1)>=1003 conditional on RQT-355',
 'explicit_isotropic':'OPEN','original_roots18_to21':'OPEN'},indent=2))
