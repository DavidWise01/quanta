#!/usr/bin/env python3
"""RQT-385: independently check complete split-prime target, 194/195 plane."""
import itertools,json
import sympy as s
from sympy.ntheory import sqrt_mod
from sympy.ntheory.modular import crt
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
T=s.Matrix([[-194,0,0],[0,1,0],[195,0,0],[0,0,1]])
V=s.Matrix([[1,3,1],[-25,-74,-24],[113,340,113]])
A=V.T*T.T*F*T*V
assert abs(V.det())==1 and H.det()==1 and H+H.T==-F
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
assert A==s.Matrix([[-561555435662335446,907442644571173949,758956630833872688],[907442644571173949,258493091816306268,2583803041170332031],[758956630833872688,2583803041170332031,-4624133667290001854]])
p=-int(A[0,0]);q=-int(A[0,2]);r=-int(A[2,2])
D=p*r-q*q;Delta=D//4;N=int(A.det());C=p*N
fac={2:3,3:1,223:1,281297:1,419697635024167:1,
10343190029259773932231107365537334388821979446373:1}
assert D==4*Delta and Delta==505173057152301646549882234879392885
assert s.prod(f**k for f,k in fac.items())==C
assert all(s.isprime(f) for f in fac)
keys=[f for f in fac if f>3]
roots={f:int(sqrt_mod(-Delta,f)) for f in keys}
assert all(pow(roots[f],2,f)==(-Delta)%f for f in keys)
assert all(s.legendre_symbol(-Delta,f)==1 for f in keys)
P=s.prod(keys)
assert C==24*P
branches=[]
for signs in itertools.product((1,-1),repeat(4)):
 rr,modulus=crt(keys,[sgn*roots[f]%f for f,sgn in zip(keys,signs)])
 assert modulus==P
 assert all((int(rr)**2+Delta)%f==0 for f in keys)
 branches.append({'signs':''.join('+' if sg==1 else '-' for sg in signs),
 'crt_root':str(int(rr))})
assert len(branches)==16 and len(set(x['crt_root'] for x in branches))==16
print(json.dumps({'rqt':385,'plane':'194/195',
 'status':'PASS exact complete factorization and CRT atlas',
 'D':str(D),'Delta':str(Delta),'N':str(N),'C':str(C),
 'factorization':{str(f):v for f,v in fac.items()},
 'large_Q1_factorization':[str(f) for f in keys[2:]],
 'split_primes':[{'prime':str(f),'sqrt_minus_Delta':str(roots[f])} for f in keys],
 'split_product':str(P),'CRT_branches':branches,
 'original_integer_null_vector':'NOT FOUND','roots18_to21':'OPEN',
 'scope':'Norm-target factorization and local split checks, not global norm representation'},indent=2))
