#!/usr/bin/env python3
"""RQT-584 exact p-adic square-class obstruction for 12 Pell ray families.
Usage: python rqt584.py RQT-583-results.json RQT-575-reduced_gram.json
"""
import json,sys
from sympy import primerange
src=json.load(open(sys.argv[1]))
F=[[int(v) for v in row] for row in json.load(open(sys.argv[2]))]
def delta(v):
 a=F[0][0]; b=sum(F[0][j+1]*v[j] for j in range(3))
 c=sum(F[i+1][j+1]*v[i]*v[j] for i in range(3) for j in range(3))
 return b*b-a*(c+2)
found={}
for eq in src['equations']:
 A,B,C=[int(eq[k]) for k in 'ABC']
 D=B*B-4*A*C
 r=eq['ray'];e=eq['offset']
 assert D==int(eq['D'])
 assert all(delta([r[j]*t+e[j] for j in range(3)])==A*t*t+B*t+C for t in (-4,-1,0,1,7))
 for p in primerange(251,2001):
  p=int(p)
  if A%p==0 or D%p or D%(p*p)==0 or pow(A%p,(p-1)//2,p)!=p-1:continue
  t0=(-B*pow(2*A,-1,p))%p
  residue=(A*t0*t0+B*t0+C)%(p*p)
  assert residue%p==0 and residue!=0
  found[int(eq['index'])]=p;break
expected={6:1583,20:1583,60:281,74:281,82:409,86:257,88:1223,100:1223,102:257,106:409,108:1151,134:1151}
assert found==expected
print('PASS: 12 exact infinite-family exclusions; 67/135 excluded, 68 open; root19 OPEN')
