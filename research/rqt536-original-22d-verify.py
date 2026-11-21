#!/usr/bin/env python3
"""Independent original-source RQT-536 22D verification. Requires SymPy.
Download gram-22x22.txt and X-22x22.txt from stoicheion/research/rqt/source/.
Run python rqt536.py gram-22x22.txt X-22x22.txt
"""
import ast,sys
from pathlib import Path
import sympy as S
r17=[-81063977012102286234,-153892023405221254112,-132067200787998198463,-185245221115581814246,16383707096216432726,21120884186178917215,25625554797703072911,50078338891768650985,60508471858444630856,191699679577122427194,83293030118575271770,11417878305766798118,-6290320518382323831,44858867800146464867,82508336889992162559,27082442786787395429,-28264397546118826981,-71648763066825579167,-38992279547178481555,82886990690706539959,-51050518961627658773,81715467130859631337]
def load(p):
 raw=Path(p).read_text().strip()
 assert raw.startswith("Matrix(") and raw.endswith(")")
 return S.Matrix(ast.literal_eval(raw[7:-1]))
if __name__=="__main__":
 G,X=load(sys.argv[1]),load(sys.argv[2]);I=S.eye(22);h=S.Matrix([1,1,1,1]+[0]*18);r=S.Matrix(r17)
 assert G.shape==X.shape==(22,22) and G==G.T and X.T*G*X==G and X*h==h
 assert (r.T*G*r)[0]==-2 and (r.T*G*h)[0]==0
 R=I+r*(r.T*G)
 assert R*R==I and R.T*G*R==G and R*h==h
 print("RQT-536 PASS original 22D G/X and original root17 checks; 17-root chain still pending.")
