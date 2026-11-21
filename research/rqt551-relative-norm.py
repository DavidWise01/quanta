#!/usr/bin/env python3
"""RQT-551 exact reciprocal fixed-field norm audit. 
Usage: python rqt551.py /path/to/rqt550/results.json
Requires SymPy. Not a relative norm solver.
"""
import json,sys
from pathlib import Path
import sympy as s
data=json.loads(Path(sys.argv[1]).read_text());l=s.Symbol('l')
p=s.Poly(s.sympify(data['quartic_characteristic'].replace('lambda','l')),l)
assert p.degree()==4 and len(s.factor_list(p)[1])==1 and s.factor_list(p)[1][0][0].degree()==4
A=-p.all_coeffs()[1];B=-p.all_coeffs()[2];disc=A*A+4*(B+2)
assert not s.integer_nthroot(disc,2)[1]
a,b=map(s.Rational,data['M_invariant_coefficients']);assert b>0 and a>2*b>0
v=s.cancel(a*a+A*a*b-(B+2)*b*b)
U=s.Matrix([[s.Rational(x) for x in row] for row in data['U0_rational_conjugator']])
assert v==U.det(method='domain-ge') and v>0
assert not (s.integer_nthroot(s.numer(v),2)[1] and s.integer_nthroot(s.denom(v),2)[1])
assert 4+2*A-(B+2)>0 and 4-2*A-(B+2)<0
print('RQT-551 PASS: irreducible quartic; quadratic fixed field; nonsquare discriminant; exact target field norm equals det(U0).')
print('Rational relative norm equation remains OPEN; no isometry or root19 witness established.')
