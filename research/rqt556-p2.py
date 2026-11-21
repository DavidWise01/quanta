#!/usr/bin/env python3
"""RQT-556 exact all-order p2 local norm certificate; frozen RQT-550 inputs.
Usage: python rqt556-p2.py /path/to/rqt550/results.json
Requires sympy, no approximate arithmetic.
"""
import sys,json,sympy as S
d=json.load(open(sys.argv[1]));x=S.Symbol('x')
P=S.Poly(S.sympify(d['quartic_characteristic'].replace('lambda','x')),x)
A=-int(P.all_coeffs()[1]);B=-int(P.all_coeffs()[2]);a,b=map(S.Rational,d['M_invariant_coefficients'])
assert A%8==5 and B%8==4 and (A*A+4*(B+2))%8==1
def reduce8(v):return int(S.numer(v))*pow(int(S.denom(v)),-1,8)%8
assert reduce8(a)==1 and reduce8(b)==0
for parity in (0,1):
 k=parity;m=2
 f=lambda z:z*z-A*z-(B+2)
 for _ in range(1,24):
  assert (2*k-A)%2
  if f(k)%(2*m):k+=m
  m*=2;assert f(k)%m==0
 delta=k*k-4;v=0
 while delta%2==0:delta//=2;v+=1
 assert v==(6 if parity==0 else 0)
 assert delta%8==(3 if parity==0 else 5)
 assert reduce8(a+b*k)==1
 print('PASS:', 'even' if parity==0 else 'odd','K mod 4096',k%4096,'radicand valuation',v,'unit mod8',delta%8,'C mod8 1')
print('ALL-ORDER LOCAL NORM CERTIFICATE: C^-1 square in each Q2 factor. Global norm and root19 OPEN.')
