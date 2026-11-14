#!/usr/bin/env python3
"""RQT-361: exact split-prime CRT branches for two original F4 conics.
Composite target cofactors remain un-factored. No global point asserted.
"""
from functools import reduce
from operator import mul
import json
import sympy as s
from sympy.ntheory.modular import crt
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
cases=[
(194,195,[[1,3,1],[-25,-74,-24],[113,340,113]],2,{2:3,3:1,223:1,281297:1},4341012393885871793429166991367328918895695969836018205135496291),
(201,202,[[1,2,1],[-26,-51,-25],[117,235,117]],18,{2:3,3:2,5:1,23:1,103:1,12967:1},1856169084206954410930471425091180170460861602787423710191998241)]
result=[]
for m,n,Vdata,c,known,cofactor in cases:
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 V=s.Matrix(Vdata);assert abs(V.det())==1
 A=V.T*T.T*F*T*V
 p=-int(A[0,0]);N=int(A.det());D=int(A[0,0]*A[2,2]-A[0,2]**2)
 assert D>0 and D%c**2==0
 delta=D//c**2
 target=p*N
 assert target==cofactor*reduce(mul,(k**e for k,e in known.items()),1)
 assert not s.isprime(cofactor)
 assert s.gcd(delta,cofactor)==1
 assert all(cofactor%t for t in s.primerange(2,25001))
 assert all(s.isprime(k) for k in known)
 split={};ramified={}
 for k,e in known.items():
  if k==2:continue
  chi=int(s.legendre_symbol(-delta,k))
  if chi==1:
   root=int(min(s.sqrt_mod(-delta,k,all_roots=True)))
   assert (root*root+delta)%k==0
   split[k]=root
  elif chi==0:ramified[k]=e
  else:raise AssertionError('Unexpected known inert prime')
 primes=list(split);roots=list(split.values())
 R,P=map(int,crt(primes,roots))
 assert R**2%P==(-delta)%P
 assert P==reduce(mul,primes,1)
 result.append({'slope':f'{m}/{n}','delta':str(delta),
 'target_pN':str(target),'known_prime_factors':{str(k):e for k,e in known.items()},
 'composite_unfactored_cofactor':str(cofactor),
 'split_prime_roots':{str(k):r for k,r in split.items()},
 'known_ramified_prime_exponents':{str(k):e for k,e in ramified.items()},
 'split_product':str(P),'CRT_root':str(R),
 'cofactor_Jacobi':int(s.jacobi_symbol(-delta,cofactor))})
assert [(z['split_product'],z['CRT_root']) for z in result]==[
 ('62729231','60807973'),('153594115','145065656')]
print(json.dumps({'status':'PASS exact CRT split-prime certificates',
'source':'authentic frozen RQT-242 F4','results':result,
'cofactor_factorization':'INCOMPLETE',
'exact_integer_null_u':'OPEN','roots18_to21':'OPEN'},indent=2))
