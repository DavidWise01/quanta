#!/usr/bin/env python3
"""RQT-352: exact finite null-vector search, authentic F4 and 3 proved isotropic planes.
No witness up to abs(a)<=1000; this is NOT global nonexistence.
"""
import sympy as s,json
from fractions import Fraction as Q
from math import floor,ceil,isqrt
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
rat=lambda x:Q(int(x.p),int(x.q))
expected=[(196406,189393),(249206,242207),(267470,260463)]
out=[]
for (m,n),(ep,ed) in zip(((194,195),(199,200),(201,202)),expected):
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 G=T.T*F*T;P=-G[1:3,1:3]
 assert P[0,0]>0 and P.det()>0
 v=P.inv()*G[1:3,0]
 beta=G[0,0]+(G[0,1:3]*P.inv()*G[1:3,0])[0]
 assert beta>0
 center=rat(v[0]);radius2=rat(beta)*rat(P.inv()[0,0])
 M=[[int(z) for z in row] for row in G.tolist()]
 pairs=nonnegative=squares=0;witness=[]
 for a in range(1,1001):
  R=radius2*a*a
  h=isqrt(R.numerator//R.denominator)+2
  lo=floor(center*a)-h-1;hi=ceil(center*a)+h+1
  assert (lo-center*a)**2>=R and (hi-center*a)**2>=R
  for b in range(lo,hi+1):
   pairs+=1
   A=M[2][2];B=2*(M[0][2]*a+M[1][2]*b)
   C=M[0][0]*a*a+2*M[0][1]*a*b+M[1][1]*b*b
   disc=B*B-4*A*C
   if disc<0:continue
   nonnegative+=1;root=isqrt(disc)
   if root*root!=disc:continue
   squares+=1
   for num in {-B+root,-B-root}:
    if num%(2*A)==0:
     c=num//(2*A)
     u=T*s.Matrix([a,b,c])
     assert (u.T*F*u)[0]==0
     witness.append(list(map(int,u)))
 assert pairs==ep and nonnegative==ed and squares==0 and not witness
 out.append({'slope':f'{m}/{n}','abs_a_excluded':[1,1000],
 'pairs':pairs,'nonnegative_discriminants':nonnegative,'perfect_squares':squares,'exact_witnesses':witness})
assert sum(z['pairs'] for z in out)==713082
print(json.dumps({'status':'PASS exhaustive finite search on original F4',
'planes':out,'scope':'only 1<=abs(a)<=1000 (and a=0 nonisotropic since transverse form negative definite)',
'exact_integer_isotropic':'OPEN','root18_to21':'OPEN'},indent=2))
