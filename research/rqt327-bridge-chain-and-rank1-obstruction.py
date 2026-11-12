#!/usr/bin/env python3
"""RQT-327: bridge reflection chain 18-20, exact step-21 obstruction.
NOT the frozen RQT-257 lattice. Requires sympy.
"""
import json
from math import gcd
import sympy as s
F=s.Matrix([[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]])
X=s.Matrix([[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]])
I=s.eye(4)
roots={18:s.Matrix([1,0,0,1]),19:s.Matrix([0,-1,-1,-1]),20:s.Matrix([0,-1,-1,1])}
mod2=lambda M:M.applyfunc(lambda t:int(t)%2)
assert X.T*F*X==F and (X-I).rank()==4
assert mod2(X**3)==I and mod2(X)!=I and mod2(X**2)!=I
steps=[]
for index,r in roots.items():
    assert (r.T*F*r)[0]==-2 and gcd(*map(int,F*r))==1
    if index>18: assert X*r==-r
    S=I+r*(r.T*F)
    assert S*S==I and S.T*F*S==F
    X=S*X
    assert X.T*F*X==F and X*X==I
    rank=int((X-I).rank())
    assert rank==21-index
    steps.append({'root_number':index,'root':list(map(int,r)),'moving_rank':rank})
v=s.Matrix([0,1,2,0])
assert (X+I).nullspace()==[v/2]
assert (v.T*F*v)[0]==2 and X==I-v*(v.T*F)
assert (X-I).rank()==1 and (I-v*(v.T*F))*X==I
print(json.dumps({'status':'bridge-only','steps':steps,
 '21st_norm_minus_two_obstruction':'every integral -1 eigenvector is t*(0,1,2,0), with norm 2*t²',
 'plus_two_reflection_closes_bridge':'(0,1,2,0)',
 'frozen_root_18_to_21':'OPEN; original F4 and X4 not recovered'},indent=2))
