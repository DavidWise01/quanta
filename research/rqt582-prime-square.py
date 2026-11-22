#!/usr/bin/env python3
"""RQT-582 exact prime-square all-scale exclusions.
Requires RQT-575 reduced_gram.json and RQT-581 results.json. Full self-contained
verifier + 135-family JSON output available in local conversation artifacts.
"""
import itertools,json,math,sys
from collections import Counter
F=[[int(z) for z in row] for row in json.load(open(sys.argv[1]))]
old=json.load(open(sys.argv[2]))
rays=old['rays']; assert old['excluded']==15 and len(old['certificates'])==135
def delta(x):
 b=sum(F[0][i+1]*x[i] for i in range(3))
 c=sum(F[i+1][j+1]*x[i]*x[j] for i in range(3) for j in range(3))
 return b*b-F[0][0]*(c+2)
fams=[]
for ray in rays:
 for eps in itertools.product((-1,0,1),repeat=3):
  z=lambda t: delta([t*ray[i]+eps[i] for i in range(3)])
  C=z(0);A=(z(2)-2*z(1)+C)//2;B=z(1)-C-A
  assert all(A*t*t+B*t+C==z(t) for t in (-5,-1,0,1,2,17))
  fams.append((A,B,C))
assert all(tuple(map(int,(old['certificates'][i]['A'],old['certificates'][i]['B'],old['certificates'][i]['C'])))==f for i,f in enumerate(fams))
prior={i:min(c['excluding_moduli']) for i,c in enumerate(old['certificates']) if c['excluding_moduli']}
assert len(prior)==15
new={}
for p in range(2,251):
 if any(p%d==0 for d in range(2,math.isqrt(p)+1)):continue
 m=p*p; squares={v*v%m for v in range(m)}
 for i,(A,B,C) in enumerate(fams):
  if i in prior or i in new:continue
  if not any((A*t*t+B*t+C)%m in squares for t in range(m)):new[i]=m
assert len(new)==40 and Counter(new.values())=={49:14,289:4,361:2,529:10,2809:2,3481:2,6889:4,26569:2}
for i,m in {**prior,**new}.items():
 squares={v*v%m for v in range(m)}
 A,B,C=fams[i]
 assert all((A*t*t+B*t+C)%m not in squares for t in range(m))
print('PASS: 15 previously + 40 newly excluded = 55/135; 80 unresolved. Root19 OPEN.')
