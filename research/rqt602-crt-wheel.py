#!/usr/bin/env python3
"""RQT-602 exact finite CRT-wheel sieve.
Usage: python rqt602.py RQT-595-results.json RQT-601-results.json
"""
import json,hashlib,math,sys
from pathlib import Path
s,t=map(Path,sys.argv[1:3]);eq=json.loads(s.read_text());prev=json.loads(t.read_text())
assert hashlib.sha256(s.read_bytes()).hexdigest()=="5e68fddb78395b02f5cc4f6cbdd5c4c3cfc341b1ed036d86174175b9e7aee699"
assert hashlib.sha256(t.read_bytes()).hexdigest()=="c1105a199d980f713aa28983ae9d4e75ee77b719bb848e729da62658b777c76e"
A,B,C=(int(eq[k]) for k in "ABC")
primes=[g["prime"] for g in prev["filters"]]+[137]
allowed={g["prime"]:set(g["admissible_residues"]) for g in prev["filters"]}
allowed[137]={r for r in range(137) if (A*r*r+B*r+C)%137 in {x*x%137 for x in range(137)}}
for p in primes:
 squares={x*x%p for x in range(p)}
 assert allowed[p]=={r for r in range(p) if (A*r*r+B*r+C)%p in squares}
wheel_primes=primes[:4];res=[0];M=1
for p in wheel_primes:
 inv=pow(M,-1,p)
 res=[r+M*((v-r)*inv%p) for r in res for v in sorted(allowed[p])]
 M*=p
res.sort()
assert M==106981 and len(res)==504 and len(set(res))==504
assert hashlib.sha256(','.join(map(str,res)).encode()).hexdigest()=="dafdc839f5493ca45468404f876b063b4c823b675903352495941eca685be7bf"
def scan(bound):
 lo=-bound;hi=bound
 candidates=[]
 for r in res:
  k=(lo-r+M-1)//M
  candidates.extend(range(r+k*M,hi+1,M))
 initial=len(candidates);stages=[]
 for p in primes[4:]:
  candidates=[v for v in candidates if v%p in allowed[p]]
  stages.append((p,len(candidates)))
  if not candidates:break
 return initial,stages,candidates
old=scan(1000000);large=scan(100000000)
assert old[0]==9423 and old[1][-1]==(103,0) and not old[2]
assert large[0]==942225 and large[1][-2:]==[(113,1),(137,0)] and not large[2]
candidate=78589011
D=A*candidate*candidate+B*candidate+C
assert D%137==66 and pow(66,68,137)==136
print("PASS RQT-602: CRT wheel modulus 106981, 504 residues, 200000001 t values, 0 survivors after prime 137.")
print("82 of 135 selected families excluded globally; 53 unresolved; original 22D Wall not replayed; Root19 OPEN.")
