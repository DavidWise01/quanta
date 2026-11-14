#!/usr/bin/env python3
"""RQT-351: exact local-global rational isotropy for three authentic F4 planes.
Uses Hasse-Minkowski; does not construct explicit integer null coordinates.
"""
import json
import sympy as s
F=s.Matrix([
[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
A=F.extract([0,2],[0,2]);B=F.extract([0,2],[1,3]);C=F.extract([1,3],[1,3])
K=A-B*C.inv()*B.T
assert C[0,0]<0 and C.det()>0 and K.det()<0
result=[]
for m,n in [(194,195),(199,200),(201,202)]:
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 G=T.T*F*T
 assert G.det()!=0
 assert (s.Matrix([-m,n]).T*K*s.Matrix([-m,n]))[0]>0
 det=abs(int(G.det()));f=s.factorint(det)
 assert s.prod(p**e for p,e in f.items())==det
 assert all(s.isprime(p) for p in f)
 # Primitive 2-adic smooth lift, q(z)=z^TGz, gradient=2Gz.
 # Since q(z)=0 mod 8 and (Gz)_i is odd, shifts by 2^k e_i
 # toggle the bit 2^(k+1) for all k>=2, giving an infinite lift.
 v=s.Matrix([0,1,1])
 assert int((v.T*G*v)[0])%8==0
 assert any(int(a)%2 for a in G*v)
 primes=[]
 for p,e in sorted(f.items()):
  if p==2:continue
  if p==3 and e>=2:
   assert int((v.T*G*v)[0])%3==0
   assert any(int(a)%3 for a in G*v)
   primes.append([str(p),e,'smooth mod-p point'])
   continue
  assert e==1
  h=(int(G[0,0])*int(G[1,1])-int(G[0,1])**2)%p
  assert h!=0
  assert pow((-h)%p,(p-1)//2,p)==1
  primes.append([str(p),e,'split rank-two quotient'])
 # Odd p not dividing det: nondegenerate ternary over F_p has
 # nonzero smooth isotropic vector, hence an infinite Hensel lift.
 result.append({'slope':f'{m}/{n}',
  'det_abs':str(det),'prime_factorization':{str(p):e for p,e in f.items()},
  'real':'indefinite','2_adic':'primitive lift from (0,1,1)',
  'odd_bad_primes':primes,'rational_isotropy':'PROVED BY HASSE-MINKOWSKI',
  'explicit_integer_u':'NOT YET CONSTRUCTED'})
print(json.dumps({'status':'PASS exact local-global prerequisites',
 'frozen_source':'stoicheion RQT-242 original F4','results':result,
 'integral_root18':'OPEN','roots19_to21':'OPEN'},indent=2))
