#!/usr/bin/env python3
"""RQT-346: exact real-cone thresholds and prime-square obstructions in authentic F4.
No integral root18 or rational global witness is claimed. SymPy required.
"""
import json
from itertools import product
import sympy as s
F=s.Matrix([
[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
A=F.extract([0,2],[0,2]); B=F.extract([0,2],[1,3])
C=F.extract([1,3],[1,3]); K=A-B*C.inv()*B.T
assert C[0,0]<0 and C.det()>0 and K.det()<0
def gram(n,d):
 T=s.Matrix([[-(n+d),0,0],[0,1,0],[n,0,0],[0,0,1]])
 return T.T*F*T
def cone(n,d):
 v=s.Matrix([-(n+d),n]); return (v.T*K*v)[0]
thresholds=[]
for d,before,first in [(-1,187,188),(1,836,837)]:
 assert cone(before,d)<0 and cone(first,d)>0
 assert all(cone(n,d)<0 for n in range(1,first))
 thresholds.append({'difference':d,'first_real_feasible_n':first})
def local(n,d,p):
 G=gram(n,d)
 a=[[int(G[i,j])%(p*p) for j in range(3)] for i in range(3)]
 root=smooth=singular=liftable=0
 for x,y,z in product(range(p),repeat=3):
  if x==y==z==0:continue
  v=(x,y,z)
  Q=sum(v[i]*a[i][j]*v[j] for i in range(3) for j in range(3))
  if Q%p:continue
  root+=1
  grad=[2*sum(a[i][j]*v[j] for j in range(3))%p for i in range(3)]
  if any(grad):smooth+=1
  else:
   singular+=1
   if Q%(p*p)==0:liftable+=1
 return {'n':n,'d':d,'prime':p,'primitive_mod_p':root,
 'smooth_mod_p':smooth,'singular_mod_p':singular,
 'singular_liftable_mod_p2':liftable,
 'primitive_mod_p2_exists':bool(smooth or liftable)}
tests=[local(190,-1,17),local(837,1,83),local(188,-1,3),local(838,1,3)]
assert [(a['primitive_mod_p'],a['smooth_mod_p'],a['singular_liftable_mod_p2']) for a in tests[:2]]==[(16,0,0),(82,0,0)]
assert all(a['primitive_mod_p2_exists'] for a in tests[2:])
print(json.dumps({'status':'PASS exact original F4 local obstruction',
 'thresholds':thresholds,'prime_tests':tests,
 'excluded_slopes':['189/190 (p=17)','838/837 (p=83)'],
 'global_isotropic_vector':'OPEN','roots18_to21':'OPEN'},indent=2))
