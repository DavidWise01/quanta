#!/usr/bin/env python3
"""RQT-353A: exact odd-prime completion of primitive-isotropic divisibility gate.
Original frozen F4; proofs for 194/195 and 201/202, 199/200 p=3 unresolved.
"""
import sympy as s,itertools,json
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
primes=[3,4966811,140001169580740529,330823854880640721967014002817981344723960683]
assert abs(F.det())==4*9*4966811*140001169580740529*330823854880640721967014002817981344723960683
assert all(s.isprime(p) for p in primes)
def rankmod(M,p):
 A=[[int(M[i,j])%p for j in range(M.cols)] for i in range(M.rows)];r=0
 for j in range(M.cols):
  t=next((i for i in range(r,M.rows) if A[i][j]),None)
  if t is None:continue
  A[r],A[t]=A[t],A[r];inv=pow(A[r][j],-1,p)
  A[r]=[(x*inv)%p for x in A[r]]
  for i in range(M.rows):
   if i!=r:
    z=A[i][j];A[i]=[(A[i][k]-z*A[r][k])%p for k in range(M.cols)]
  r+=1
 return r
rows=[]
for m,n in [(194,195),(199,200),(201,202)]:
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 G=T.T*F*T;num=0
 for tt in itertools.product(range(8),repeat=3):
  if all(z%2==0 for z in tt):continue
  v=s.Matrix(tt)
  if int((v.T*G*v)[0]//2)%8:continue
  num+=1
  assert any(int(z)%2 for z in F*T*v)
 assert num==64
 ranks={str(p):rankmod(F*T,p) for p in primes}
 full=all(z==3 for z in ranks.values())
 assert full==(m in (194,201))
 rows.append({'slope':f'{m}/{n}','primitive_null_mod8':num,
 'ranks_FT_at_odd_discriminant_primes':ranks,
 'every_primitive_null_has_divisibility_one':full,
 'possible_odd_divisibility_prime':None if full else 3})
print(json.dumps({'status':'PASS exact original lattice divisibility proof',
 'theorem':'gcd(Fu)|detF for primitive u; rank(F*T) at odd determinant primes plus mod8 resolves gcd.',
 'rational_existence_dependency':'RQT-351',
 'Bezout_parity_dependency':'RQT-334',
 'planes':rows,'integral_first_root_exists_abstractly_in_two_planes':True,
 'actual_root18_coordinates':'OPEN','roots19_to21':'OPEN'},indent=2))
