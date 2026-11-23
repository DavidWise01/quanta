#!/usr/bin/env python3
"""RQT-612: exact necessary mod343 and Pell discriminant sieve, families 2 and 24.
Usage: python rqt612.py RQT-611-verified.json RQT-591-results.json RQT-583-results.json [result.json]
"""
import sys,json,hashlib,math
from pathlib import Path
sources=list(map(Path,sys.argv[1:4]))
r611,r591,r583=[json.loads(p.read_text()) for p in sources]
assert r611["rqt"]==611 and r591["rqt"]==591 and r583["rqt"]==583
expected=["f0c2e02fe5e35847574c334de7c56d61a54f3e9d44dbb8cfcae4490145078e32",
"6dadba9f74f9f5625b4a1d87ab4b2d42d293851b54d40cd18c4b6e1aa91ecb67",
"5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92"]
assert [hashlib.sha256(p.read_bytes()).hexdigest() for p in sources]==expected
G=[[int(x) for x in row] for row in r591["reduced_gram"]]
eq={e["index"]:e for e in r583["equations"]}
primes=[31,29,17,19,23,5,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
bound=1000000;N=2*bound+1;result=[]
for family in r611["families"]:
 idx=family["family_index"];e=eq[idx];A,B,C=[int(e[k]) for k in "ABC"]
 ray,offset=e["ray"],e["offset"]
 def q(u,t):
  v=[u]+[ray[j]*t+offset[j] for j in range(3)]
  return sum(v[i]*G[i][j]*v[j] for i in range(4) for j in range(4))+2
 # Check all t and u residues modulo 343; project the admissible t onto mod 49.
 actual={t%49 for t in range(343) for u in range(343) if q(u,t)%343==0}
 allowed=sorted(actual)
 assert allowed==family["allowed_t_mod49"]==({2:[13,20,27,34],24:[15,22,29,36]})[idx]
 mask=bytearray(N)
 for t in allowed:
  start=(t+bound)%49
  mask[start::49]=b'\x01'*len(mask[start::49])
 steps=[{"modulus":343,"projected_t_mod49":allowed,"remaining":mask.count(1)}]
 assert steps[0]["remaining"]==163264
 for p in primes:
  squares={x*x%p for x in range(p)}
  good={t for t in range(p) if (A*t*t+B*t+C)%p in squares}
  for bad in range(p):
   if bad not in good:
    start=(bad+bound)%p
    mask[start::p]=b'\x00'*len(mask[start::p])
  steps.append({"prime":p,"remaining":mask.count(1),"allowed_mod_p":len(good)})
 assert steps[-2]["prime"]==89 and steps[-2]["remaining"]==1
 assert steps[-1]["prime"]==97 and steps[-1]["remaining"]==0
 result.append({"index":idx,"window":[-bound,bound],"stages":steps,"integer_seeds":[]})
out={"rqt":612,"input_sha256":dict(zip([p.name for p in sources],expected)),"families":result,
"new_all_scale_exclusions":0,"selected_excluded":82,"selected_unresolved":53,
"original_22d_wall":"NOT REPLAYED","root19":"OPEN"}
Path(sys.argv[4] if len(sys.argv)>4 else "RQT-612-results.json").write_text(json.dumps(out,indent=2)+"\n")
print("PASS RQT-612: both windows cleared, 4,000,002 parameter pairs; root19 OPEN")
