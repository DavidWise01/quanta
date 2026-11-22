#!/usr/bin/env python3
"""RQT-590 exact lattice invariant check.
Usage: python rqt590.py rank4_gram.json rank4_wall.json RQT-589-results.json
"""
import sys,hashlib,json
import sympy as S
from pathlib import Path
g,w,r=map(Path,sys.argv[1:4])
assert hashlib.sha256(g.read_bytes()).hexdigest()=="e93f43e85f6b70c76d5eb8c043644cf7862ed08593ed0549e814a4a774d3c58c"
assert hashlib.sha256(w.read_bytes()).hexdigest()=="5893d5c8b6b7b8048d68d115c8e935ae509f5d4e11c828e7439dae924a64d031"
G=S.Matrix(json.loads(g.read_text())); W=S.Matrix(json.loads(w.read_text())); d=json.loads(r.read_text())
M=S.Matrix([[int(y) for y in x] for x in d["M"]]);a=S.Integer(d["a"])
assert G.shape==(4,4) and W.shape==(4,4) and M.shape==(3,3)
assert G==G.T and W+W.T==-G
assert a!=0 and -M.det()%a**2==0 and G.det()==-M.det()//a**2
print("PASS exact SHA, Gram symmetry, Wall symmetrization, Schur determinant")
print("Canonical reduced 4x4 Gram missing; original 22D Wall not replayed; Root 19 OPEN")
