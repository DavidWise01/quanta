#!/usr/bin/env python3
"""RQT-323: exact classification of root-preserving directions in a fixed primitive-coordinate slice.

Bridge lattice only, NOT the unrecovered frozen RQT-257 lattice.
"""
import sympy as s
from math import gcd
F=s.Matrix([[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]])
X=s.Matrix([[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]])
I=s.eye(4); D=X-I
B=(F*D.adjugate()+D.adjugate().T*F)/2
p=s.Matrix([1,0,0,1]); a,b,c,d=s.symbols('a b c d',integer=True)
v=s.Matrix([a,b,c,d])
norm=lambda Q,w:s.expand((w.T*Q*w)[0])
pair=lambda Q,u,w:s.expand((u.T*Q*w)[0])
mod2=lambda M:M.applyfunc(lambda x:int(x)%2)
assert F.det()==-3 and D.det()==12 and B==-6*F
assert norm(F,p)==-2 and (F*p)[1]==1
L=s.Matrix.vstack((p.T*F),(p.T*B),F.row(1))
assert L.rank()==2
assert L.nullspace()==[s.Matrix([0,0,1,0]),s.Matrix([0,0,0,1])]
assert s.factor(norm(F,v.subs({a:0,b:0})))==(c-d)*(c+d)
for eps in (-1,1):
    t=s.symbols('t',integer=True)
    ve=s.Matrix([0,0,2*t,2*eps*t]); r=p+ve
    assert norm(F,ve)==0 and pair(F,p,ve)==0 and (F*ve)[1]==0
    assert norm(B,ve)==0 and pair(B,p,ve)==0
    assert norm(F,r)==-2 and norm(B,r)==D.det() and (F*r)[1]==1
    for tt in range(-15,16):
        rr=r.subs(t,tt); Y=(I+rr*(rr.T*F))*X
        assert norm(F,rr)==-2 and gcd(*map(int,F*rr))==1
        assert [int(z)%2 for z in rr]==[1,0,0,1]
        assert (Y-I).rank()==3 and mod2(Y**2)==I and mod2(Y)!=I
assert mod2(X**3)==I and mod2(X)!=I and mod2(X**2)!=I
print('PASS: linear constraints rank 2; v=(0,0,c,d); residual cone (c-d)(c+d)=0')
print('PASS: two and only two even integer direction lines in fixed primitive slice')
print('PASS: 62 root replay cases (31 per line)')
print('OPEN: original frozen root 18 and directions outside the fixed slice')
