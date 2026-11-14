#!/usr/bin/env python3
"""RQT-343: authentic F4 ternary slices; exact primitive mod32 and mod25.
Necessary local sieve only, not proof of global rational point or root18.
"""
import json
from itertools import product
from sympy import Matrix
F=Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
def counts(k,p,m):
 T=Matrix([[-k,0,0],[0,1,0],[1,0,0],[0,0,1]])
 A=T.T*F*T
 a,b,c,d,e,f=[int(A[i,j])%m for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))]
 n=0
 for x,y,z in product(range(m),repeat=3):
  if x%p==y%p==z%p==0:continue
  if (a*x*x+b*y*y+c*z*z+2*(d*x*y+e*x*z+f*y*z))%m==0:n+=1
 return n
m32=[counts(k,2,32) for k in range(32)]
m25=[counts(k,5,25) for k in range(25)]
assert set(m32)=={0,2048} and set(m25)=={0,600}
assert all((v==0)==(k%2==1 and k%8!=5) for k,v in enumerate(m32))
assert all((v==0)==(k%5==1) for k,v in enumerate(m25))
good=[k for k in range(40) if (k%2==0 or k%8==5) and k%5!=1]
assert len(good)==20
print(json.dumps({'status':'PASS original F4 joint local sieve',
'mod32_primitive_counts':m32,'mod25_primitive_counts':m25,
'necessary_k_mod8':'0,2,4,5,6','necessary_k_mod5':'0,2,3,4',
'candidate_k_mod40':good,'excluded_fraction':'20/40',
'rational_isotropic_witness':'OPEN','integer_root18':'OPEN',
'roots19_20_21':'OPEN'},indent=2))
