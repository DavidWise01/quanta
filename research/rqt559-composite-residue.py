#!/usr/bin/env python3
"""RQT-559 aggregate Jacobi obstruction screen; requires RQT-550 and 551 JSON and SymPy."""
from pathlib import Path
import json,math,sympy as S,sys
root=Path(sys.argv[1])
d=json.loads((root/'rqt550/results.json').read_text())
v=json.loads((root/'rqt551/results.json').read_text())
a,b=map(S.Rational,d['M_invariant_coefficients'])
m=int(S.ilcm(S.denom(a),S.denom(b)))
alpha,beta=int(a*m),int(b*m)
N=int(S.numer(S.Rational(v['norm_C'])))
T=alpha**2-4*beta**2
assert N%2 and N.bit_length()==942 and math.gcd(N,beta)==math.gcd(N,T)==1
jac=int(S.jacobi_symbol(T%N,N));assert jac==1
print('PASS gcds=1, Jacobi(T/N)=+1; no obstruction established, global norm OPEN.')
