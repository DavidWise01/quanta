#!/usr/bin/env python3
"""RQT-322: exact affine-line family certificate. Bridge lattice only."""
import json
from math import gcd
from sympy import Matrix, eye, symbols, expand

F=Matrix([[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]])
X=Matrix([[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]])
I=eye(4); D=X-I
B=(F*D.adjugate()+D.adjugate().T*F)/2
p=Matrix([1,0,0,1]); v=Matrix([0,0,2,2]); k=symbols('k',integer=True)
q=lambda M,r:expand((r.T*M*r)[0])
pair=lambda M,a,b:expand((a.T*M*b)[0])
assert F==F.T and D.det()!=0 and X.T*F*X==F
assert [q(F,p),pair(F,p,v),q(F,v)]==[-2,0,0]
assert [q(B,p),pair(B,p,v),q(B,v)]==[D.det(),0,0]
assert all(int(t)%2==0 for t in v)
assert [int(t)%2 for t in p]==[1,0,0,1]
assert (F*p)[1]==1 and (F*v)[1]==0
r=p+k*v
assert q(F,r)==-2 and q(B,r)==D.det() and (F*r)[1]==1
mod2=lambda A:A.applyfunc(lambda z:int(z)%2)
assert mod2(X**3)==I and mod2(X)!=I and mod2(X**2)!=I
S=lambda a:I+a*(a.T*F)
Y=S(p)*X
assert mod2(Y**2)==I and mod2(Y)!=I and (Y-I).rank()==3
for n in range(-15,16):
    rn=p+n*v; Yn=S(rn)*X
    assert q(F,rn)==-2 and gcd(*map(int,F*rn))==1
    assert [int(t)%2 for t in rn]==[1,0,0,1]
    assert (Yn-I).rank()==3
    assert mod2(Yn**2)==I and mod2(Yn)!=I
print(json.dumps({'status':'verified bridge-only','base':[1,0,0,1],
 'direction':[0,0,2,2],'quadratic_six':[int(q(F,p)),int(pair(F,p,v)),int(q(F,v)),int(q(B,p)),int(pair(B,p,v)),int(q(B,v))],
 'sampled_roots':31,'frozen_root_18':'OPEN'},indent=2))
