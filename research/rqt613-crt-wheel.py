#!/usr/bin/env python3
"""RQT-613 exact CRT corridor verifier.
Run: python research/rqt613-crt-wheel.py RQT611.json RQT591.json RQT583.json [BOUND=20000000]
"""
import json,hashlib,math,sys
from pathlib import Path
P=list(map(Path,sys.argv[1:4]));J,G,E=[json.loads(p.read_text()) for p in P]
bound=int(sys.argv[4]) if len(sys.argv)>4 else 20000000
F=[[int(x) for x in row] for row in G['reduced_gram']]
eq={e['index']:e for e in E['equations']}
primes=[31,29,17,19,23,5,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109]
def crt_wheel(sets):
 m=1;res=[0]
 for p in (49,31,29):
  inv=pow(m,-1,p)
  res=[x+m*((y-x)*inv%p) for x in res for y in sorted(sets[p])]
  m*=p
 return m,sorted(res)
for f in J['families']:
 i=f['family_index'];e=eq[i];A,B,C=[int(e[k]) for k in 'ABC']
 r,o=e['ray'],e['offset']
 def q(u,t):
  v=[u]+[r[j]*t+o[j] for j in range(3)]
  return sum(v[j]*F[j][k]*v[k] for j in range(4) for k in range(4))+2
 allowed={t%49 for t in range(343) for u in range(343) if q(u,t)%343==0}
 assert sorted(allowed)==f['allowed_t_mod49']
 sets={49:allowed}
 for p in primes:
  squares={x*x%p for x in range(p)}
  sets[p]={t for t in range(p) if (A*t*t+B*t+C)%p in squares}
 M,wheel=crt_wheel(sets)
 assert M==44051 and len(wheel)==1088
 if i==2:
  assert hashlib.sha256(','.join(map(str,wheel)).encode()).hexdigest()=='6d181f89dab733ac7694ba23877c88924358f7dc29796a9489e50a1ce30b68b0'
 def scan(R):
  vals=[]
  for w in wheel:
   first=w+((-R-w+M-1)//M)*M
   vals.extend(range(first,R+1,M))
  states=[len(vals)]
  for p in primes[2:]:
   vals=[x for x in vals if x%p in sets[p]]
   states.append(len(vals))
   if not vals:break
  return states,vals
 old,prior=scan(1000000);now,remaining=scan(bound)
 assert old[0]==49397 and not prior
 assert now[0]==987942 and not remaining
 assert now[-5:]==[8,3,2,1,0]
 print(i, 'wheel=',len(wheel),'expanded=',2*bound+1,'final=',len(remaining))
print('PASS: 80,000,002 bounded family-parameter pairs; no all-scale exclusion; root19 OPEN')
