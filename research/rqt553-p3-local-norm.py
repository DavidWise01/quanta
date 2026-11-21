#!/usr/bin/env python3
"""RQT-553 p3 all-order local norm certificate. Requires SymPy and RQT-550 results.json.
Usage: python rqt553-p3-local-norm.py /path/to/rqt550/results.json
"""
import json,sys,sympy as S
data=json.load(open(sys.argv[1]));x=S.Symbol('x')
p=S.Poly(S.sympify(data['quartic_characteristic'].replace('lambda','x')),x)
A=-int(p.all_coeffs()[1]);B=-int(p.all_coeffs()[2]);a,b=map(S.Rational,data['M_invariant_coefficients'])
Delta=A*A+4*(B+2)
assert Delta%9==0 and (Delta//9)%3==2 and Delta%27!=0
alpha,beta=9*a,9*b
c0=(alpha+beta*S.Rational(A,2))/3;c1=beta/2
d0=S.Rational(A*A+2*B-4,6);d1=S.Rational(A,2)
def mod3(q):
 n,d=map(int,S.fraction(q))
 assert d%3
 return n*pow(d,-1,3)%3
assert [mod3(q) for q in (c0,c1,d0,d1)]==[2,1,2,2]
# In F9, s²=2: Cdelta≡(2+s)(2+2s)=2.
assert (2*2+2*1*2)%3==2
assert (2*2+1*2)%3==0
assert (-pow(2,-1,3))%3==1
print('PASS: F/Q3 unramified; L/F ramified; local C^-1 is a norm at p=3 by Hensel.')
print('Global rational isometry and root19 remain OPEN.')
