#!/usr/bin/env python3
"""RQT-566 exact factor and local norm certificate. Replays RQT-565 and RQT-550 source data."""
import json,sys,sympy as s
from pathlib import Path
prior=json.loads(Path(sys.argv[1]).read_text())
source=json.loads(Path(sys.argv[2]).read_text())
n=int(prior['cofactor']);p=22361230963
assert n.bit_length()==293 and n%p==0 and (n//p).bit_length()==259 and s.isprime(p)
x=s.Symbol('x');f=s.Poly(s.sympify(source['quartic_characteristic'].replace('lambda','x')),x)
A=-int(f.all_coeffs()[1]);B=-int(f.all_coeffs()[2]);a,b=map(s.Rational,source['M_invariant_coefficients'])
Delta=A*A+4*(B+2)
assert Delta%p==0 and Delta%(p*p)!=0
k=A*pow(2,-1,p)%p;rad=(k*k-4)%p
c=(int(s.numer(a))*pow(int(s.denom(a)),-1,p)+k*int(s.numer(b))*pow(int(s.denom(b)),-1,p))%p
assert (k,rad,c,int(s.legendre_symbol(rad,p)))==(2379782987,17464168712,16478607289,-1)
print('RQT-566 PASS: new prime, v_p(Delta)=1, unramified quadratic, C unit => local norm PASS.')
print('259-bit residual, global norm and root19 OPEN.')
