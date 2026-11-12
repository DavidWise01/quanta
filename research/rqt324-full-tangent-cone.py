#!/usr/bin/env python3
"""RQT-324: full tangent isotropic cone at bridge root; frozen root 18 OPEN."""
import json
from math import gcd
import sympy as s
F=s.Matrix([[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]])
X=s.Matrix([[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]])
I=s.eye(4);D=X-I;B=(F*D.adjugate()+D.adjugate().T*F)/2
p=s.Matrix([1,0,0,1])
a,b,c,d,k,m,n=s.symbols('a b c d k m n',integer=True)
v=s.Matrix([a,b,c,d])
q=lambda M,w:s.expand((w.T*M*w)[0])
pair=lambda M,u,w:s.expand((u.T*M*w)[0])
mod2=lambda M:M.applyfunc(lambda z:int(z)%2)
assert X.T*F*X==F and B==-6*F and D.det()==12
assert pair(F,p,v)==-2*a+b
cone=s.factor(q(F,v).subs(b,2*a))
assert s.expand(cone-(c*c-(d-a)**2-6*a*a))==0
A=2*m*n;C=6*m*m+n*n;E=6*m*m-n*n+A
vp=2*s.Matrix([A,2*A,C,E])
assert pair(F,p,vp)==0 and q(F,vp)==0
assert pair(B,p,vp)==0 and q(B,vp)==0
assert [int(z)%2 for z in p]==[1,0,0,1]
assert s.expand((F*(p+k*vp))[0]+(F*(p+k*vp))[3])==-2
assert s.expand((F*(p+k*vp))[1])==1-3*k*vp[0]
assert mod2(X**3)==I and mod2(X)!=I and mod2(X**2)!=I
Y0=(I+p*(p.T*F))*X
assert (Y0-I).rank()==3 and mod2(Y0**2)==I and mod2(Y0)!=I
dirs=[];replays=0
for aa in range(-14,15,2):
 for cc in range(-14,15,2):
  for dd in range(-14,15,2):
   vv=s.Matrix([aa,2*aa,cc,dd])
   if q(F,vv)!=0:continue
   dirs.append(tuple(map(int,vv)))
   for kk in range(-2,3):
    rr=p+kk*vv;Y=(I+rr*(rr.T*F))*X
    assert q(F,rr)==-2 and q(B,rr)==D.det()
    assert gcd(*map(int,F*rr))==1
    assert [int(z)%2 for z in rr]==[1,0,0,1]
    assert (Y-I).rank()==3 and mod2(Y**2)==I and mod2(Y)!=I
    replays+=1
assert any(w[0]!=0 for w in dirs)
print(json.dumps({'status':'PASS','cone':'c^2-(d-a)^2=6a^2; b=2a',
 'parametrized_even_direction':'2*(2mn,4mn,6m^2+n^2,6m^2-n^2+2mn)',
 'bounded_even_directions':len(dirs),'replay_cases':replays,
 'example_new_direction':next(w for w in dirs if w[0]!=0),
 'primitive_invariant':'(Fr)_1+(Fr)_4=-2; (Fr)_2 odd',
 'frozen_root18':'OPEN'},indent=2))
