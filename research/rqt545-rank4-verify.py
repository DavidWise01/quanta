#!/usr/bin/env python3
"""RQT-545 exact four-dimensional successor from original-source matrices.
Inputs: RQT-541 historical_index64_basis.json, historical_root15_coordinates.json,
saturated_rank6_basis.json, RQT-544 root16_new_ambient.json and original Stoicheion
G/X source in Matrix([...]) syntax. Requires sympy. All inputs share exact ancestry.
"""
import ast,json,sys
from pathlib import Path
import sympy as s
p=Path(sys.argv[1]);src=Path(sys.argv[2])
load=lambda f:s.Matrix(json.loads((p/f).read_text()))
read=lambda f:s.Matrix(ast.literal_eval((src/f).read_text().strip()[7:-1]))
G=read("gram-22x22.txt");X=read("X-22x22.txt");I=s.eye(22);h=s.Matrix([1]*4+[0]*18)
K=s.Matrix.hstack(*[I[:,j]-I[:,0] if j<20 else I[:,j] for j in range(1,22)])
Y=(X*K)[1:22,:];assert X*K==K*Y and X.T*G*X==G
B=load("historical_index64_basis.json");T15=load("historical_root15_coordinates.json")
N=load("saturated_rank6_basis.json");GK=K.T*G*K
W=GK*(Y-s.eye(21)).inv();Q=B.T*GK*B;H=B.T*W*B
r16=s.Matrix(json.loads(Path(sys.argv[3]).read_text()))
r17=s.Matrix([-81063977012102286234,-153892023405221254112,-132067200787998198463,-185245221115581814246,16383707096216432726,21120884186178917215,25625554797703072911,50078338891768650985,60508471858444630856,191699679577122427194,83293030118575271770,11417878305766798118,-6290320518382323831,44858867800146464867,82508336889992162559,27082442786787395429,-28264397546118826981,-71648763066825579167,-38992279547178481555,82886990690706539959,-51050518961627658773,81715467130859631337])
T=T15.row_join(B.inv()*r16[1:22,0]).row_join(B.inv()*r17[1:22,0])
J=T.T*H*T
assert T.rank()==17 and all(J[i,i]==1 for i in range(17))
assert all(J[i,j]==0 for i in range(17) for j in range(i))
assert T.T*Q*T==-J-J.T
for r in (r16,r17):
 assert (r.T*G*r)[0]==-2 and (r.T*G*h)[0]==0
 R=I+r*(r.T*G);assert R*R==I and R.T*G*R==G and R*h==h
content=[]
for i in (15,16):
 row=T[:,i].T*H.T*N;U=s.eye(N.cols)
 for j in range(1,N.cols):
  aa=int((row*U)[0]);bb=int((row*U)[j])
  if not bb:continue
  u,v,g=map(int,s.gcdex(aa,bb));C=s.eye(N.cols)
  C[0,0]=u;C[j,0]=v;C[0,j]=-bb//g;C[j,j]=aa//g;U=U*C
 content.append(abs(int((row*U)[0])));N=N*U[:,1:]
 assert T[:,:i+1].T*H.T*N==s.zeros(i+1,N.cols)
F=N.T*Q*N;HH=N.T*H*N
assert content==[1,1] and F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
assert HH.det()==1 and HH+HH.T==-F
print('PASS: original 17-root Wall flag; saturated 4D successor; determinant match.')
print('PENDING: integral simultaneous equivalence with historical F/H; root19 OPEN.')
