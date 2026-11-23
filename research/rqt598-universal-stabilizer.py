#!/usr/bin/env python3
"""RQT-598: verify universal congruence-stabilizer exponent for any integral Pell unit."""
import math,json,sys
from pathlib import Path
r=json.loads(Path(sys.argv[1]).read_text()) # RQT-597-results.json
s=json.loads(Path(sys.argv[2]).read_text()) # RQT-595-results.json
d=int(r['squarefree_D']);A=int(s['A']);M=2*A
P=54231366340197528698151546659
assert int(s['N'])==100*d and d==3*13*1693*P
# Recursive Pratt certificate for large prime.
def cert(c):
 p=int(c['p']); a=int(c['a'])
 if p==2:return a==1 and c['factors']==[]
 fac=c['factors'];prod=math.prod(int(x['q'])**int(x['exp']) for x in fac)
 assert prod==p-1 and all(cert(x['certificate']) and int(x['certificate']['p'])==int(x['q']) for x in fac)
 assert pow(a,p-1,p)==1
 assert all(math.gcd(pow(a,(p-1)//int(x['q']),p)-1,p)==1 for x in fac)
 return True
assert cert(r['large_prime_pratt_certificate'])
f={2:1,3:1,5:2,13:1,1693:1,P:1}
assert math.prod(p**k for p,k in f.items())==M and M%10==0
orders={p:p**(3*k-2)*(p*p-1) for p,k in f.items()}
E=math.lcm(*orders.values())
assert E==2495428846376980414842976695320325076410511060575086680674879676418181949822869503902337202645000
# Theorem: for any x,z with x²-dz²=1, T=[[x,dz],[z,x]] is in SL2(Z/M).
# By Lagrange and CRT, T**E=I (mod M). This preserves X mod 2A and Z mod 10.
print('PASS RQT-598; universal conditional exponent E =',E)
print('No explicit Pell unit or generalized Pell seed constructed; Root19 OPEN.')
