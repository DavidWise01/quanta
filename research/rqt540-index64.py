#!/usr/bin/env python3
"""RQT-540 parity-kernel lattice from original Stoicheion G/X; sympy required.
Usage: python rqt540-index64.py gram-22x22.txt X-22x22.txt
Produces index64_basis.json in current directory. This is an alternative valid B.
"""
import sys,ast,json
from pathlib import Path
import sympy as s
def load(f):
 t=Path(f).read_text().strip();assert t.startswith('Matrix(')
 return s.Matrix(ast.literal_eval(t[7:-1]))
G,X=map(load,sys.argv[1:3]);I=s.eye(22)
K=s.Matrix.hstack(*[I[:,j]-I[:,0] if j<20 else I[:,j] for j in range(1,22)])
Y=(X*K)[1:22,:];assert X*K==K*Y and X.T*G*X==G
GK=K.T*G*K;W=GK*(Y-s.eye(21)).inv();assert W+W.T==-GK
Z=4*W;assert all(q.q==1 for q in Z)
A=[[int(Z[j,i])%2 for j in range(21)] for i in range(21)]
piv=[];k=0
for j in range(21):
 i=next((i for i in range(k,21) if A[i][j]),None)
 if i is None:continue
 A[i],A[k]=A[k],A[i]
 for t in range(21):
  if t!=k and A[t][j]:A[t]=[a^b for a,b in zip(A[t],A[k])]
 piv.append(j);k+=1
assert piv==[0,1,9,10,15,19]
cols=[]
for j in range(21):
 if j in piv:continue
 v=[0]*21;v[j]=1
 for i,p in enumerate(piv):v[p]=A[i][j]
 cols.append(s.Matrix(v))
for p in piv:
 v=[0]*21;v[p]=2;cols.append(s.Matrix(v))
B=s.Matrix.hstack(*cols)
assert abs(B.det())==64 and all(int(q)%2==0 for q in Z.T*B)
HB=B.T*W*B;QB=B.T*GK*B
assert all(q.q==1 for q in HB) and HB.det()==1
assert HB+HB.T==-QB and QB.det()==-16384
Path('index64_basis.json').write_text(json.dumps(B.tolist(),indent=2))
print('RQT-540 PASS: rank6, index64, detWall1, detGram-16384; canonical RQT-216 transport still pending.')
