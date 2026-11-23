#!/usr/bin/env python3
"""RQT-603: deterministic exact CRT mesh across 53 Pell families.
python rqt603.py RQT583.json RQT584.json RQT586.json RQT591-gram.json [bound]
"""
import json,hashlib,math,sys
from fractions import Fraction
from pathlib import Path
src=list(map(Path,sys.argv[1:5]));sha=[hashlib.sha256(p.read_bytes()).hexdigest() for p in src]
assert sha==['5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92','29f0eb2b4ef29d3194185ee45d72c58a793b41bd44993b0b6ad33bf3435cbe5f','45d129e80c7d6b19af2ba7a7e8e541f865e37646a2709efebbba87bb584a4859','f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228']
E,A,B,F=[json.loads(p.read_text()) for p in src]
blocked={int(x['family_index']) for d in (A,B) for x in d['certificates']}|{13}
todo=[e for e in E['equations'] if int(e['index']) not in blocked]
assert len(blocked)==27 and len(todo)==53
primes=[31,29,7,17,19,23,5,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251]
assert len(primes)==50 and all(all(p%d for d in range(2,math.isqrt(p)+1)) for p in primes)
R=int(sys.argv[5]) if len(sys.argv)>5 else 100000
result=[]
for e in todo:
 a,b,c=[int(e[x]) for x in 'ABC']
 for t in (-19,-1,0,1,23):
  v=[e['ray'][j]*t+e['offset'][j] for j in range(3)]
  z=sum(F[0][j+1]*v[j] for j in range(3))
  w=sum(v[j]*F[j+1][k+1]*v[k] for j in range(3) for k in range(3))
  assert z*z-F[0][0]*(w+2)==a*t*t+b*t+c
 gates=[]
 for p in primes:
  square={i*i%p for i in range(p)}
  good={i for i in range(p) if (a*i*i+b*i+c)%p in square}
  assert good # otherwise an all-scale exclusion requiring separate certification
  gates.append((Fraction(len(good),p),p,good))
 gates.sort(key=lambda x:(x[0],x[1]))
 width=2*R+1;mask=bytearray(b'\x01')*width;history=[]
 for _,p,good in gates:
  for bad in range(p):
   if bad in good:continue
   start=(bad+R)%p
   if start<width:mask[start::p]=b'\x00'*(((width-1-start)//p)+1)
  left=mask.count(1)
  history.append({'prime':p,'admissible_residues':len(good),'survivors':left})
  if left==0:break
 assert mask.count(1)==0
 result.append({'family_index':e['index'],'ray':e['ray'],'offset':e['offset'],'gates':history})
assert len(result)==53 and sum(len(x['gates']) for x in result)==989
print('PASS: 53 families,',53*(2*R+1),'family-parameter pairs; all finite windows empty')
print('Global ledger unchanged: 82/135 excluded, 53 unresolved; Root19 OPEN')
