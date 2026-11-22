#!/usr/bin/env python3
"""RQT-564 exact new prime-factor local norm check.
Usage: python rqt564-prime-check.py /path/to/rqt550/results.json
"""
import json,sys,sympy as S
d=json.load(open(sys.argv[1])); x=S.Symbol('x')
f=S.Poly(S.sympify(d['quartic_characteristic'].replace('lambda','x')),x)
A=-int(f.all_coeffs()[1]);B=-int(f.all_coeffs()[2])
a,b=map(S.Rational,d['M_invariant_coefficients'])
Delta=A*A+4*(B+2)
p1,p2=981893141,153603501791
assert p1*p2==150822224842164115531
for p,expected in [(p1,(10698669,271138905,916020174,1)),(p2,(99488999186,104191447306,101587243882,-1))]:
 assert p<2**64 and S.isprime(p) and Delta%p==0 and Delta%(p*p)!=0
 k=A*pow(2,-1,p)%p;rad=(k*k-4)%p
 c=(int(S.numer(a))*pow(int(S.denom(a)),-1,p)+k*int(S.numer(b))*pow(int(S.denom(b)),-1,p))%p
 assert rad and c and (k,rad,c,int(S.legendre_symbol(rad,p)))==expected
 print('PASS',p,'relative','SPLIT' if expected[3]==1 else 'UNRAMIFIED QUADRATIC','C unit norm')
print('RQT-564 two new all-order local norm gates passed; global norm and root19 OPEN.')
