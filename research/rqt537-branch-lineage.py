#!/usr/bin/env python3
"""RQT-537 branch-sensitive Wall test: local Stoicheion source required.
Usage: python rqt537.py gram-22x22.txt X-22x22.txt RQT-224-summary.json RQT-241-summary.json
Requires sympy. Only initial root16 + Branch2 root17 mismatch is audited.
"""
import sys,ast,json
from pathlib import Path
import sympy as s
def load(path):
 t=Path(path).read_text().strip();assert t.startswith('Matrix(')
 return s.Matrix(ast.literal_eval(t[7:-1]))
G,X=load(sys.argv[1]),load(sys.argv[2])
u=s.Matrix(json.loads(Path(sys.argv[3]).read_text())['root_ambient_coordinates'])
v=s.Matrix(list(map(int,json.loads(Path(sys.argv[4]).read_text())['original_22_coordinates'])))
I=s.eye(22);h=s.Matrix([1,1,1,1]+[0]*18)
assert G==G.T and X.T*G*X==G and X*h==h
for r in (u,v):
 assert (r.T*G*r)[0]==-2 and (r.T*G*h)[0]==0
 S=I+r*(r.T*G)
 assert S*S==I and S.T*G*S==G and S*h==h
K=s.Matrix.hstack(*[I[:,j]-I[:,0] if j<20 else I[:,j] for j in range(1,22)])
Y=(X*K)[1:22,:]
assert X*K==K*Y
GK=K.T*G*K
H=GK*(Y-s.eye(21)).inv()
assert H+H.T==-GK
a,b=u[1:22,0],v[1:22,0]
assert K*a==u and K*b==v
lower=int((b.T*H*a)[0]);upper=int((a.T*H*b)[0])
assert lower==307135354231451946557
assert upper==3944793163432264597963
assert lower+upper== -int((u.T*G*v)[0])
print(json.dumps({'rqt':537,'mixed_branch_Wall17_to_16':str(lower),'status':'INCOMPATIBLE — use Branch2 root16','root19':'OPEN'},indent=2))
