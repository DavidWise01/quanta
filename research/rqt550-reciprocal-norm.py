#!/usr/bin/env python3
"""RQT-550 reciprocal norm reduction. Requires exact F,H from frozen.py and RQT-545 rank4_wall.json/rank4_gram.json; SymPy.
Run with Python and those source files in /mnt/data/rqt516 and /mnt/data/rqt545, or update paths.
This is a public reproduction of the exact two-equation reduction.
"""
import sys,json
from pathlib import Path
import sympy as s
sys.path.insert(0,sys.argv[1])
from frozen import F as Fh,H as Hh
p=Path(sys.argv[2])
Hn=s.Matrix(json.loads((p/'rank4_wall.json').read_text()))
Fn=s.Matrix(json.loads((p/'rank4_gram.json').read_text()))
Dh=s.eye(4)+Hh.inv()*Fh;Dn=s.eye(4)+Hn.inv()*Fn
v=s.eye(4)[:,0]
Ch=s.Matrix.hstack(*[(Dh**i)*v for i in range(4)])
Cn=s.Matrix.hstack(*[(Dn**i)*v for i in range(4)])
U0=Cn*Ch.inv()
assert Dn*U0==U0*Dh
S=U0.T*Hn*U0;M=Hh.inv()*S;K=Dh+Dh.inv()
assert Dh.T*S*Dh==S and M*Dh==Dh*M
a,b=s.symbols('a b')
sol=list(s.linsolve([(M-a*s.eye(4)-b*K)[i,j] for i in range(4) for j in range(4)],(a,b)))[0]
assert M==sol[0]*s.eye(4)+sol[1]*K
t=s.symbols('t0:4')
P=sum((t[i]*Dh**i for i in range(4)),s.zeros(4))
Pstar=sum((t[i]*Dh**(-i) for i in range(4)),s.zeros(4))
E=Pstar*P*M-s.eye(4)
i,j=next((i,j) for i in range(4) for j in range(4) if i!=j and K[i,j])
q1=s.cancel(E[i,j]/K[i,j]);q0=s.cancel(E[0,0]-q1*K[0,0])
assert all(s.cancel(E[ii,jj]-(q0*s.eye(4)+q1*K)[ii,jj])==0 for ii in range(4) for jj in range(4))
assert s.Poly(q0,*t).total_degree()==2 and s.Poly(q1,*t).total_degree()==2
print('PASS: rational Wall equivalence reduced exactly to two quadratic equations:')
print('q0=',q0)
print('q1=',q1)
print('Rational solution NOT found; integral equivalence and root19 OPEN.')
