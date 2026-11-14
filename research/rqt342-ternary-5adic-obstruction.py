#!/usr/bin/env python3
"""RQT-342 exact 5-adic obstruction, original frozen F4; no global root."""
import json
from itertools import product
from sympy import Matrix
F=Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
def counts(k,m):
 T=Matrix([[-k,0,0],[0,1,0],[1,0,0],[0,0,1]])
 J=T.T*F*T
 a,b,c,d,e,f=[int(J[i,j])%m for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))]
 total=0
 for x,y,z in product(range(m),repeat=3):
  if x%5==y%5==z%5==0:continue
  if (a*x*x+b*y*y+c*z*z+2*(d*x*y+e*x*z+f*y*z))%m==0:total+=1
 return total
rows=[]
for k in range(25):
 n5=counts(k,5);n25=counts(k,25)
 assert n5==(4 if k%5==1 else 24)
 assert n25==(0 if k%5==1 else 600)
 rows.append({'k_mod25':k,'primitive_mod5':n5,'primitive_mod25':n25})
print(json.dumps({'status':'PASS exact 5-adic obstruction','source':'stoicheion RQT-242 original F4','excluded_rational_planes':'x0=-k*x2 where k%5==1','residue_checks_per_k':25**3,'results':rows,'global_root18':'OPEN'},indent=2))
