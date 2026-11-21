#!/usr/bin/env python3
"""RQT-546 exact rational conjugacy plus mod2 Wall equivalence.
Run alongside historical frozen.py from RQT-516 and rank4_gram.json/rank4_wall.json
from RQT-545; requires sympy. Full computational script/results supplied as
conversation artifacts. This public script verifies core identities.
"""
import sys,json
import sympy as s
sys.path.insert(0,sys.argv[1])
from frozen import F as Fh,H as Hh
from pathlib import Path
p=Path(sys.argv[2])
Fn=s.Matrix(json.loads((p/'rank4_gram.json').read_text()))
Hn=s.Matrix(json.loads((p/'rank4_wall.json').read_text()))
Dh=s.eye(4)+Hh.inv()*Fh;Dn=s.eye(4)+Hn.inv()*Fn
assert Dh.charpoly().as_expr()==Dn.charpoly().as_expr()
e=s.eye(4)[:,0]
Ch=s.Matrix.hstack(*[Dh**i*e for i in range(4)])
Cn=s.Matrix.hstack(*[Dn**i*e for i in range(4)])
assert Ch.det() and Cn.det()
U=Cn*Ch.inv()
assert Dn*U==U*Dh
assert not all(x.q==1 for x in U) and U.T*Hn*U!=Hh
U2=s.Matrix([[1,1,1,1],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
assert U2.det()%2 and all(int(x)%2==0 for x in U2.T*Hn*U2-Hh)
assert all(int(x)%2==0 for x in U2.T*Fn*U2-Fh)
print('RQT-546 PASS rational operator conjugacy and simultaneous Wall/Gram mod2; integral GL4 still OPEN')
