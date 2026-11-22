#!/usr/bin/env python3
"""RQT-574 exact active fixed-form automorphism and norm search.
Usage: python rqt574.py rank4_gram.json rank4_wall.json
"""
import json,itertools,sys
import sympy as s
F=s.Matrix(json.load(open(sys.argv[1])));H=s.Matrix(json.load(open(sys.argv[2])))
I=s.eye(4)
assert F==F.T and H+H.T==-F and H.det()==1
D=I+H.inv()*F
assert D==-H.inv()*H.T and D!=I and D!=-I
assert D.det()==1 and all(x.q==1 for x in D)
assert all(x.q==1 for x in D.inv())
assert D.T*F*D==F and D.T*H*D==H
assert s.trace(D)>4
count=0;hits=[]
for v in itertools.product(range(-3,4),repeat=4):
 if not any(v):continue
 count+=1;x=s.Matrix(v)
 if (x.T*F*x)[0]==-2:hits.append(v)
assert count==2400 and not hits
print('PASS: nontrivial infinite-order integral fixed F/H automorphism D; root19 OPEN')
