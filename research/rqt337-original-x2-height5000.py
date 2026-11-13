#!/usr/bin/env python3
"""RQT-337 exact x2 height exclusion in the original stoicheion RQT-242 Gram."""
import json
from fractions import Fraction as Q
from math import floor,ceil,isqrt
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
ix=[0,1,3];P=-F.extract(ix,ix);b=F.extract(ix,[2]);v=P.inv()*b
beta=F[2,2]+(b.T*P.inv()*b)[0];K=P.inv()[:2,:2].inv()
assert beta>0 and all(P[:k,:k].det()>0 for k in (1,2,3))
f=lambda x:Q(int(x.p),int(x.q))
v0,v1=f(v[0]),f(v[1]);beta=f(beta)
a,h,c=f(K[0,0]),f(K[0,1]),f(K[1,1]);alpha=a-h*h/c
assert alpha>0 and c>0
M=[[int(z) for z in row] for row in F.tolist()]
def enc(center,r2):
 assert r2>=0
 d=isqrt(r2.numerator//r2.denominator)+2
 lo,hi=floor(center)-d-1,ceil(center)+d+1
 assert (center-lo)**2>=r2 and (hi-center)**2>=r2
 return lo,hi
report=[]
for target in (0,-2):
 count=nonnegative=square=0
 for t in range(1,5001):
  R=beta*t*t-target
  lo0,hi0=enc(v0*t,R/alpha)
  for x0 in range(lo0,hi0+1):
   delta=Q(x0)-v0*t
   remaining=R-alpha*delta*delta
   if remaining<0:continue
   lo1,hi1=enc(v1*t-h/c*delta,remaining/c)
   for x1 in range(lo1,hi1+1):
    count+=1
    A=M[3][3];B=2*(M[3][0]*x0+M[3][1]*x1+M[3][2]*t)
    C=(M[0][0]*x0*x0+M[1][1]*x1*x1+M[2][2]*t*t+
       2*M[0][1]*x0*x1+2*M[0][2]*x0*t+2*M[1][2]*x1*t-target)
    disc=B*B-4*A*C
    if disc<0:continue
    nonnegative+=1;root=isqrt(disc)
    if root*root!=disc:continue
    square+=1
    for n in {-B+root,-B-root}:
     if n%(2*A)==0:
      x3=n//(2*A);x=s.Matrix([x0,x1,t,x3])
      assert (x.T*F*x)[0]==target
      raise AssertionError('EXACT WITNESS: '+str(list(x)))
 assert count==1729528 and square==0
 report.append({'norm':target,'pairs':count,'nonnegative_disc':nonnegative,'square_disc':square,'roots':0})
print(json.dumps({'status':'PASS original lattice exhaustive finite bound',
 'x2_positive':[1,5000],'x2_negative':'central symmetry',
 'x2_zero':'negative-definite (RQT-336)',
 'necessary_height':'abs(x2)>=5001',
 'results':report,'root18_19_20_21':'OPEN'},indent=2))
