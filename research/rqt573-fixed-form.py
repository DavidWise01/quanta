#!/usr/bin/env python3
"""RQT-573: exact fixed-form signed-permutation audit. Run with RQT-545 F/H JSON files."""
import itertools,json,sys
import sympy as s
F=s.Matrix(json.load(open(sys.argv[1])));H=s.Matrix(json.load(open(sys.argv[2])))
assert H+H.T==-F and H.det()==1
survivors=[];count=0
for perm in itertools.permutations(range(4)):
 for signs in itertools.product((-1,1),repeat=4):
  U=s.zeros(4)
  for j,k in enumerate(perm):U[k,j]=signs[j]
  count+=1
  if U.T*H*U==H:
   assert U.T*F*U==F
   survivors.append((perm,signs))
assert count==384
assert survivors==[((0,1,2,3),(-1,-1,-1,-1)),((0,1,2,3),(1,1,1,1))]
print('RQT-573 PASS: 384 signed permutations, only +/-I preserve fixed Wall form. Root19 OPEN.')
