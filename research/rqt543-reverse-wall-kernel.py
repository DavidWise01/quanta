#!/usr/bin/env python3
"""RQT-543 exact reverse-Wall kernel from local RQT-541 JSON artifacts (requires sympy)."""
import json
from pathlib import Path
import sympy as S
P=Path(__file__).resolve().parents[1]/'rqt541'
B=S.Matrix(json.loads((P/'historical_index64_basis.json').read_text()))
N=S.Matrix(json.loads((P/'saturated_rank6_basis.json').read_text()))
T=S.Matrix(json.loads((P/'historical_root15_coordinates.json').read_text()))
d=json.loads((P/'original_QH.json').read_text()); H=S.Matrix(d['H'])
F6=S.Matrix(json.loads((P/'rank6_gram.json').read_text()))
r=S.Matrix([-81063977012102286234,-153892023405221254112,-132067200787998198463,-185245221115581814246,16383707096216432726,21120884186178917215,25625554797703072911,50078338891768650985,60508471858444630856,191699679577122427194,83293030118575271770,11417878305766798118,-6290320518382323831,44858867800146464867,82508336889992162559,27082442786787395429,-28264397546118826981,-71648763066825579167,-38992279547178481555,82886990690706539959,-51050518961627658773,81715467130859631337])
x=B.inv()*r[1:22,0];assert x.T*H*T==S.zeros(1,15)
ell=x.T*H*N
assert S.igcd(*map(int,ell))==1
U=S.eye(6);a=int(ell[0]);row=list(ell)
for j in range(1,6):
 b=int(row[j])
 if b==0:continue
 p,q,g=map(int,S.gcdex(a,b));C=S.eye(6)
 C[0,0]=p;C[j,0]=q;C[0,j]=-b//g;C[j,j]=a//g
 U=U*C;a=g
assert [abs(int(z)) for z in ell*U]==[1,0,0,0,0,0]
M=U[:,1:];assert ell*M==S.zeros(1,5)
F5=M.T*F6*M
assert F5.det()==14475655451912186696519612575357291954504440205448582259540099784
ds=[S.Integer(1)]+[F5[:i,:i].det() for i in range(1,6)]
assert [int(S.sign(ds[i]*ds[i-1])) for i in range(1,6)].count(1)==1
print('RQT-543 PASS: 15 ordered Wall zeros; primitive row; saturated rank5; determinant and signature (1,4).')
print('Branch2 root16 not constructed; root19 OPEN.')
