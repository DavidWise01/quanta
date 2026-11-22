#!/usr/bin/env python3
"""RQT-596: exact nonintegral rational Pell multiplier proof.
Usage: python rqt596.py RQT-595-results.json RQT-583-results.json RQT-591-reduced_gram.json
"""
import sys,json,hashlib,math
from pathlib import Path
from fractions import Fraction
R,E,G=map(Path,sys.argv[1:4])
r=json.loads(R.read_text()); raw=E.read_bytes(); e=json.loads(raw)
assert hashlib.sha256(raw).hexdigest()=="5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92"
assert hashlib.sha256(G.read_bytes()).hexdigest()=="f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228"
F=json.loads(G.read_text()); f=next(x for x in e["equations"] if x["index"]==28)
A,B,C,D=(int(f[k]) for k in "ABCD"); N=4*A; p=math.isqrt(N)
U=p*p+N;V=2*p;W=p*p-N
assert (U,V,W)==tuple(int(r["explicit_rational_unit"][k]) for k in ("U","V","denominator_W"))
assert B*B-4*A*C==D and U*U-N*V*V==W*W
trace=Fraction(2*U,W)
assert math.gcd(2*U,abs(W))==325 and trace.denominator==2698204764356087
# Nonintegral trace => lambda=(U+V sqrt(N))/W is not an algebraic integer.
# If lambda^k were integral, lambda would be integral by transitivity; contradiction.
for t in (-101,-3,-1,0,1,3,101):
 v=[f["ray"][i]*t+f["offset"][i] for i in range(3)]
 b=sum(F[0][i+1]*v[i] for i in range(3))
 c=sum(F[i+1][j+1]*v[i]*v[j] for i in range(3) for j in range(3))
 delta=b*b-F[0][0]*(c+2)
 assert delta==A*t*t+B*t+C and (2*A*t+B)**2-N*delta==D
print("RQT-596 PASS: exact nonintegral trace denominator",trace.denominator)
print("This multiplier and its positive powers cannot be integral Pell units; family 28 is NOT excluded; root19 OPEN.")
