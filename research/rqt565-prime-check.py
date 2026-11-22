#!/usr/bin/env python3
"""RQT-565 exact factor and local norm verifier. Requires SymPy.
Usage: python rqt565-check.py /path/to/rqt550/results.json /path/to/rqt564/results.json
"""
import sys,json,sympy as S
from pathlib import Path
d=json.loads(Path(sys.argv[1]).read_text());v=json.loads(Path(sys.argv[2]).read_text())
entry=next(x for x in v['ecm_work'] if x['cofactor']=='discriminant' and x['factor_found'])
n=int(entry['cofactor_after']);p=114941221
assert n%p==0 and (n//p).bit_length()==293 and S.isprime(p)
x=S.Symbol('x');f=S.Poly(S.sympify(d['quartic_characteristic'].replace('lambda','x')),x)
A=-int(f.all_coeffs()[1]);B=-int(f.all_coeffs()[2])
a,b=map(S.Rational,d['M_invariant_coefficients'])
Delta=A*A+4*(B+2)
assert Delta%p==0 and Delta%(p*p)!=0
k=A*pow(2,-1,p)%p
rad=(k*k-4)%p
c=(int(S.numer(a))*pow(int(S.denom(a)),-1,p)+k*int(S.numer(b))*pow(int(S.denom(b)),-1,p))%p
assert (k,rad,c,int(S.legendre_symbol(rad,p)))==(16821420,56841795,21500151,1)
print('RQT-565 PASS exact prime divisor, discriminant valuation 1, split relative local norm.')
print('293-bit residual and global relative norm/root19 remain OPEN.')
