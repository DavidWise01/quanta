#!/usr/bin/env python3
"""RQT-345: original F4 adjacent rational slope cone and primitive local census."""
from itertools import product
import json
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
A=F.extract([0,2],[0,2]);B=F.extract([0,2],[1,3]);C=F.extract([1,3],[1,3]);K=A-B*C.inv()*B.T
assert C[0,0]<0 and C.det()>0 and K.det()<0
L=s.Rational(19893,20000);R=s.Rational(2503,2500)
assert 186<1/(1-L)<187 and 833<1/(R-1)<834
def count(n,d,p,M):
 m=n+d
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 G=T.T*F*T
 a,b,c,h,i,j=[int(G[u,v])%M for u,v in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))]
 total=0
 for x in range(M):
  for y in range(M):
   xy=a*x*x+b*y*y+2*h*x*y
   for z in range(M):
    if x%p==y%p==z%p==0:continue
    if (xy+c*z*z+2*i*x*z+2*j*y*z)%M==0:total+=1
 return total
out=[]
for d in (-1,1):
 r={}
 for p,M,expected in ((2,32,2048),(5,25,600)):
  counts=[count(n,d,p,M) for n in range(M)]
  assert all(v==expected for v in counts)
  r[str(M)]={'classes':M,'primitive_each':expected,'excluded':0}
 out.append({'numerator_minus_denominator':d,
             'minimum_denominator':187 if d==-1 else 834,
             'local_results':r})
print(json.dumps({'status':'PASS authentic rational-slope necessary tests',
 'cone':['19893/20000','2503/2500'],'families':out,
 'exact_isotropic_vector':'OPEN','root18':'OPEN','roots19_to21':'OPEN'},indent=2))
