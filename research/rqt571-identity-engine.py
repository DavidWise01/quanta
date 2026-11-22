#!/usr/bin/env python3
"""RQT-571: exact one-degree {{i}} identity-covariance engine.
Usage: python rqt571-identity-engine.py /path/to/rank4_gram.json /path/to/rank4_wall.json
Requires sympy.
"""
import json,sys,sympy as s
F=s.Matrix(json.load(open(sys.argv[1])));H=s.Matrix(json.load(open(sys.argv[2])))
I=s.eye(4);D=I+H.inv()*F;x=s.Matrix([1,0,1,0]);y=s.Matrix([0,1,0,-1])
assert F==F.T and H+H.T==-F and H.det()==1
n=0
for a in (-1,0,1):
 for b in (-1,0,1):
  U=I.copy();U[0,1]=a;U[2,3]=b
  Ui=U.inv();Fp=U.T*F*U;Hp=U.T*H*U;Dp=I+Hp.inv()*Fp
  xp=Ui*x;yp=Ui*y
  checks=[U.det()==1,all(z.q==1 for z in Ui),Fp==Fp.T,Hp+Hp.T==-Fp,
   Fp.det()==F.det(),Hp.det()==H.det(),Dp==Ui*D*U,
   (xp.T*Fp*xp)[0]==(x.T*F*x)[0],
   (xp.T*Hp*yp)[0]==(x.T*H*y)[0]]
  assert all(checks),(a,b,checks)
  if (a,b)!=(0,0):assert Fp!=F or Hp!=H
  n+=len(checks)
assert n==81
print('PASS 9 frames, 81 exact identities; 8 are coordinate changes, NOT original-form isometries.')
print('Root19 still OPEN; Josephson equivalence UNTESTED.')
