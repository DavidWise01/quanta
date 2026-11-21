#!/usr/bin/env python3
"""RQT-538 branch-2 transport gate. Run after fetching original Stoicheion
source files, and supplying a 22x6 JSON integer transport from RQT-216/224."""
import ast,json,sys
from pathlib import Path
import sympy as s
if len(sys.argv)!=4:raise SystemExit("python rqt538-branch2-verify.py gram-22x22.txt X-22x22.txt transport-22x6.json")
def load(f):
 a=Path(f).read_text().strip();assert a.startswith("Matrix(")
 return s.Matrix(ast.literal_eval(a[7:-1]))
G,X=load(sys.argv[1]),load(sys.argv[2]);T=s.Matrix(json.loads(Path(sys.argv[3]).read_text()))
I=s.eye(22);h=s.Matrix([1,1,1,1]+[0]*18)
a=s.Matrix([-183,-198,174,572,-368,-188])
b=s.Matrix([-232,-246,223,729,-473,-242])
initial=s.Matrix([199942,383386,329827,461310,-41442,-52679,-65082,-125589,-153660,-481817,-207896,-25459,18678,-110547,-206072,-66620,69930,182115,99059,-207384,126089,-206587])
r17=s.Matrix([-81063977012102286234,-153892023405221254112,-132067200787998198463,-185245221115581814246,16383707096216432726,21120884186178917215,25625554797703072911,50078338891768650985,60508471858444630856,191699679577122427194,83293030118575271770,11417878305766798118,-6290320518382323831,44858867800146464867,82508336889992162559,27082442786787395429,-28264397546118826981,-71648763066825579167,-38992279547178481555,82886990690706539959,-51050518961627658773,81715467130859631337])
assert G==G.T and X.T*G*X==G and X*h==h
assert T.shape==(22,6) and T.rank()==6 and all(v.q==1 for v in T)
assert T*a==initial
r=T*b
assert (r.T*G*r)[0]==-2 and (r.T*G*h)[0]==0
R=I+r*(r.T*G)
assert R*R==I and R.T*G*R==G and R*h==h
K=s.Matrix.hstack(*[I[:,j]-I[:,0] if j<20 else I[:,j] for j in range(1,22)])
Y=(X*K)[1:22,:];assert X*K==K*Y
W=K.T*G*K*(Y-s.eye(21)).inv();assert W+W.T==-K.T*G*K
assert K*r[1:22,0]==r and K*r17[1:22,0]==r17
pair=(r17[1:22,0].T*W*r[1:22,0])[0]
print(json.dumps({"rqt":538,"r16_branch2_ambient":list(map(str,r)),"original_Wall_pairing":str(pair),"gate":"PASS" if pair==0 else "FAIL"},indent=2))
