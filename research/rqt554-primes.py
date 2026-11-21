#!/usr/bin/env python3
"""RQT-554 six discriminant prime local norm audit. SymPy required.
Usage: python rqt554-primes.py /path/to/rqt550/results.json
"""
import sys,json
from fractions import Fraction
import sympy as s
d=json.load(open(sys.argv[1]));x=s.Symbol('x')
f=s.Poly(s.sympify(d['quartic_characteristic'].replace('lambda','x')),x)
A=-int(f.all_coeffs()[1]);B=-int(f.all_coeffs()[2])
a,b=map(Fraction,d['M_invariant_coefficients'])
Delta=A*A+4*(B+2)
for p in (7,29,89,1063,18149,27179):
 assert s.isprime(p) and Delta%p==0 and (Delta//p)%p!=0
 assert a.denominator%p and b.denominator%p
 k=A*pow(2,-1,p)%p;delta=(k*k-4)%p
 c=(a.numerator*pow(a.denominator,-1,p)+k*b.numerator*pow(b.denominator,-1,p))%p
 assert delta and c
 leg=pow(delta,(p-1)//2,p)
 assert leg in (1,p-1)
 kind='SPLIT' if leg==1 else 'UNRAMIFIED_QUADRATIC'
 if leg==1:
  root=int(s.sqrt_mod(delta,p));assert root*root%p==delta
 print('PASS',p,'K',k,'delta',delta,'C',c,kind)
print('All six exact local norm conditions PASS; global norm and root19 OPEN.')
