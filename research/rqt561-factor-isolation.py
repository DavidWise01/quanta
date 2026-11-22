#!/usr/bin/env python3
"""RQT-561 bounded exact factor search. Expects RQT-559 results.json."""
from pathlib import Path
from math import gcd
from sympy import integer_nthroot,primerange,jacobi_symbol
import json,sys
v=json.loads(Path(sys.argv[1]).read_text());N=int(v['numerator']);T=int(v['T']);beta=int(v['beta'])
assert N.bit_length()==942 and gcd(N,T)==gcd(N,beta)==1 and jacobi_symbol(T,N)==1
assert not any(integer_nthroot(N,e)[1] for e in range(2,17))
a=integer_nthroot(N,2)[0]+1
for i in range(10000):
 b,ok=integer_nthroot(a*a-N,2)
 assert not (ok and 1<gcd(a-b,N)<N),'Factor discovered by Fermat offset '+str(i)
 a+=1
ps=list(primerange(2,100001))
assert all(N%p for p in ps)
for base in (2,3,5):
 x=base
 for p in ps:
  pp=p
  while pp*p<=100000:pp*=p
  x=pow(x,pp,N)
 assert gcd(x-1,N) in (1,N)
for c in (1,2,3):
 x=y=2
 for i in range(150000):
  x=(x*x+c)%N;y=(y*y+c)%N;y=(y*y+c)%N
  d=gcd(abs(x-y),N)
  assert not (1<d<N),'Factor discovered rho c='+str(c)
  if d==N:break
print('RQT-561 PASS: no factor in stated finite budgets. Composite proven previously; factorization unresolved.')
