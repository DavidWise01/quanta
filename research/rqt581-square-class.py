#!/usr/bin/env python3
"""RQT-581 exact all-scale modular square-class sieve.
Usage: python rqt581.py path/to/reduced_gram.json
"""
import json,itertools,sys
F=[[int(v) for v in row] for row in json.load(open(sys.argv[1]))]
rays=[(35,-10,14),(45,-13,18),(80,-23,32),(95,-27,38),(115,-33,46)]
mods=(8,16,32,64,128,256,3,9,27,5,25,7,11,13,17,19,23,29,31)
def delta(v):
 b=sum(F[0][i+1]*v[i] for i in range(3))
 c=sum(F[i+1][j+1]*v[i]*v[j] for i in range(3) for j in range(3))
 return b*b-F[0][0]*(c+2)
excluded=[]
for r in rays:
 for e in itertools.product((-1,0,1),repeat=3):
  C=delta(e);d1=delta(tuple(r[i]+e[i] for i in range(3)));d2=delta(tuple(2*r[i]+e[i] for i in range(3)))
  A=(d2-2*d1+C)//2;B=d1-C-A
  assert all(A*t*t+B*t+C==delta(tuple(t*r[i]+e[i] for i in range(3))) for t in (-5,-2,0,1,3,17))
  obstruct=[]
  for m in mods:
   squares={j*j%m for j in range(m)}
   if not any((A*t*t+B*t+C)%m in squares for t in range(m)):obstruct.append(m)
  if obstruct:excluded.append(min(obstruct))
from collections import Counter
assert len(excluded)==15 and dict(sorted(Counter(excluded).items()))=={5:3,7:1,25:8,29:1,32:2}
print('PASS: 15/135 ray-offset families excluded for every integer scale; 120 unresolved; Root19 OPEN.')
