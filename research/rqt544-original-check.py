#!/usr/bin/env python3
"""Direct original-source RQT-544 root16 certificate, requires SymPy.
Usage: python rqt544-original-check.py path/to/gram-22x22.txt path/to/X-22x22.txt
Original sources: DavidWise01/stoicheion/research/rqt/source/.
The full exact rational-LLL engine and kernel matrices are separate conversation artifacts.
"""
import ast,sys
from pathlib import Path
import sympy as S
def load(f):
 t=Path(f).read_text().strip()
 assert t.startswith('Matrix(') and t.endswith(')')
 return S.Matrix(ast.literal_eval(t[7:-1]))
G,X=load(sys.argv[1]),load(sys.argv[2]);I=S.eye(22);h=S.Matrix([1]*4+[0]*18)
r=S.Matrix([-258262,-493604,-422875,-592850,51717,66640,81581,160887,194458,616634,267720,35952,-21087,144493,264594,86378,-91090,-231560,-127187,267461,-164768,262574])
r17=S.Matrix([-81063977012102286234,-153892023405221254112,-132067200787998198463,-185245221115581814246,16383707096216432726,21120884186178917215,25625554797703072911,50078338891768650985,60508471858444630856,191699679577122427194,83293030118575271770,11417878305766798118,-6290320518382323831,44858867800146464867,82508336889992162559,27082442786787395429,-28264397546118826981,-71648763066825579167,-38992279547178481555,82886990690706539959,-51050518961627658773,81715467130859631337])
assert G==G.T and X.T*G*X==G and X*h==h
assert (r.T*G*r)[0]==-2 and (r.T*G*h)[0]==0
R=I+r*(r.T*G)
assert R*R==I and R.T*G*R==G and R*h==h
K=S.Matrix.hstack(*[I[:,j]-I[:,0] if j<20 else I[:,j] for j in range(1,22)])
assert K*r[1:22,0]==r and K*r17[1:22,0]==r17
Y=(X*K)[1:22,:];assert X*K==K*Y
W=K.T*G*K*(Y-S.eye(21)).inv()
assert W+W.T==-K.T*G*K
pair=(r17[1:22,0].T*W*r[1:22,0])[0]
assert pair==0,('Wall17to16 nonzero',pair)
print('RQT-544 DIRECT 22D PASS: integral norm−2 reflection and r17→new-r16 one-sided Wall compatibility.')
print('Not the original Branch2 identity; complete 21-word and root19 remain OPEN.')
