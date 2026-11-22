#!/usr/bin/env python3
"""RQT-575 exact HNF, rational LLL, finite norm search.
Run with archived conversation artifacts RQT-541, RQT-544, RQT-545 in /mnt/data.
See local /mnt/data/rqt575/rqt575.py for fully reproducible 152-step run.
"""
import sympy as s,itertools,json,sys
from pathlib import Path
P=Path(sys.argv[1]); F=s.Matrix(json.loads((P/'rqt575/reduced_gram.json').read_text()))
W=s.Matrix(json.loads((P/'rqt575/unimodular_transform.json').read_text()))
F0=s.Matrix(json.loads((P/'rqt545/rank4_gram.json').read_text()))
assert W.det()==1 and W.T*F0*W==F
for r in (2,3,5,8,12):
 count=0
 for z in itertools.product(range(-r,r+1),repeat=4):
  q=sum(z[i]*F[i,j]*z[j] for i in range(4) for j in range(4))
  assert q!=-2
  count+=1
 print('PASS bound',r,'tested',count,'hits 0')
print('RQT-575 finite nonfinding only. Root19 OPEN.')
