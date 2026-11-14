#!/usr/bin/env python3
"""RQT-353: exact primitive-isotropic divisibility gate on authentic F4.
RQT-351 proves rational existence; no explicit integer coordinates here.
"""
import itertools,json
from collections import Counter
from math import gcd
import sympy as s
F=s.Matrix([
[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
q=lambda x:int((x.T*F*x)[0]//2)
wanted={'0111','1001','1110'}
res=[]
for m,n in [(194,195),(199,200),(201,202)]:
 assert gcd(m,n)==1
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 G=T.T*F*T
 assert G.det()!=0
 counts=Counter()
 for t in itertools.product(range(8),repeat=3):
  if all(z%2==0 for z in t):continue
  x=T*s.Matrix(t)
  if q(x)%8:continue
  assert any(int(z)%2 for z in F*x)
  counts[''.join(str(z%2) for z in t)]+=1
  targets=set()
  for b in itertools.product(range(2),repeat=4):
   v=s.Matrix(b)
   if int((x.T*F*v)[0])%2!=1:continue
   r=(1+q(v))*x-v
   parity=''.join(str(int(z)%2) for z in r)
   if parity in wanted:targets.add(parity)
  assert len(targets)==2
 assert dict(counts)=={'001':16,'011':16,'100':16,'110':16}
 res.append({'slope':f'{m}/{n}','primitive_null_residues_mod8':sum(counts.values()),
             'ternary_parities':dict(sorted(counts.items())),
             'divisibility_two_cases':0,'admissible_first_root_parity':'AVAILABLE'})
print(json.dumps({'result':'PASS conditional constructive existence gate',
 'original_F4':'stoicheion RQT-242',
 'rational_existence_input':'RQT-351 local-global certificate',
 'theorem':'Every primitive integer null point on these planes has gcd(F4*u)=1; an admissible norm -2 root exists by RQT-334 Bezout.',
 'planes':res,'explicit_integral_null_coordinates':'OPEN',
 'explicit_root18_coordinates':'OPEN','roots19_to21':'OPEN'},indent=2))
