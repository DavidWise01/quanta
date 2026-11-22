#!/usr/bin/env python3
"""RQT-597 exact squarefree Pell verification (requires sympy for factor discovery).
Run: python research/rqt597-squarefree.py
"""
from math import gcd,isqrt
from sympy import factorint
A=89518360633605555683821304281344825
B=-7483520243911231029085168265101895934
C=-64071240985594466694007969119178624871
K=78945285068193588880454794453306132157010594392916809771448116369654302656
N=4*A
d=3580734425344222227352852171253793
P=54231366340197528698151546659
assert N==100*d and d==3*13*1693*P
assert factorint(d)=={3:1,13:1,1693:1,P:1}
assert B*B-4*A*C==K
# Recursive Lucas/Pratt primality verification of each prime appearing in d
def prime_certificate(p):
    if p==2:return True
    f=factorint(p-1)
    for q in f: assert prime_certificate(int(q))
    assert all(int(q)>1 for q in f)
    assert __import__('math').prod(int(q)**int(k) for q,k in f.items())==p-1
    for a in range(2,100):
        if pow(a,p-1,p)==1 and all(gcd(pow(a,(p-1)//int(q),p)-1,p)==1 for q in f):
            return True
    raise AssertionError('Missing witness')
assert all(prime_certificate(p) for p in (3,13,1693,P))
for X,Y in ((0,0),(1,0),(23,-17),(54321,98765)):
    Z=10*Y
    assert X*X-N*Y*Y==X*X-d*Z*Z
print('PASS exact squarefree d, recursively checked prime factors, Z=10Y.')
print('No integral Pell unit, generalized seed, 22D Wall, or root19 certified.')
