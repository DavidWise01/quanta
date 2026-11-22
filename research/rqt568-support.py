#!/usr/bin/env python3
"""RQT-568 factor-free discriminant-support local norm proof, requires sympy.
Usage: python rqt568-support.py path/to/rqt550/results.json
"""
import json,math,sys
from pathlib import Path
from sympy import Poly,Rational,Symbol,sympify,numer,denom,ilcm
d=json.loads(Path(sys.argv[1]).read_text());x=Symbol('x')
f=Poly(sympify(d['quartic_characteristic'].replace('lambda','x')),x)
A=-int(f.all_coeffs()[1]);B=-int(f.all_coeffs()[2])
a,b=map(Rational,d['M_invariant_coefficients'])
c=a*a+A*a*b-(B+2)*b*b
N=abs(int(numer(c)));D=int(denom(c));Delta=A*A+4*(B+2)
R=abs((B-2)**2-4*A*A);m=int(ilcm(denom(a),denom(b)))
assert math.gcd(N,Delta)==1 and math.gcd(D,Delta)==9
assert math.gcd(R,Delta)==9 and math.gcd(m,Delta)==9
# Therefore for p>=5 dividing Delta, C and delta are units at each local F place.
# Unit quadratic extensions of odd residue characteristic are split or unramified.
# Their local norm maps are surjective on units.
print('RQT-568 PASS: all odd discriminant primes p>=5 cleared by factor-free local norm theorem')
print('Global rational norm and root19 OPEN.')
