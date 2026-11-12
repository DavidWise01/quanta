#!/usr/bin/env python3
"""RQT-321: exact bridge-lattice infinite family. NOT original frozen RQT-257."""
import sympy as S
from math import gcd

F=S.Matrix([[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]])
X=S.Matrix([[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]])
I=S.eye(4)
D=X-I
B=(F*D.adjugate()+D.adjugate().T*F)/2
assert D.det()==12 and B==-6*F
assert F.det()==-3 and F[0,0]<0 and F[2,2]>0
assert X.T*F*X==F
k=S.symbols('k',integer=True)
r=S.Matrix([1,0,2*k,1+2*k])
Fr=F*r
assert S.expand((r.T*F*r)[0])==-2
assert Fr[1]==1
assert S.expand((r.T*B*r)[0])==D.det()
assert [int(t.subs(k,0))%2 for t in r]==[1,0,0,1]

def binary(M):
    return M.applyfunc(lambda a:int(a)%2)

for n in range(-15,16):
    rn=r.subs(k,n)
    sr=I+rn*(rn.T*F)
    y=sr*X
    assert (rn.T*F*rn)[0]==-2
    assert gcd(*[int(t) for t in F*rn])==1
    assert [int(t)%2 for t in rn]==[1,0,0,1]
    assert (y-I).rank()==3
    assert binary(X**3)==I and binary(X)!=I and binary(X**2)!=I
    assert binary(y**2)==I and binary(y)!=I

# Symbolic rank proof: det(Y-I)=det(D)*(1-r^T F D^-1 r)=0;
# rank(Y-I)>=rank(D)-1=3, hence exactly 3.
# Order mod2 is constant for all k because r_k mod2=1001.
# No positive-definite pencil: B=-6F, and F is indefinite.
print('PASS: symbolic family r_k=(1,0,2k,1+2k) for all integer k')
print('Fr =',list(Fr),' ; det(D)=12 ; B=-6F')
print('PASS: 31 instances k=-15..15 checked all five bridge conditions')
print('OPEN: original frozen eighteenth-root witness')
