#!/usr/bin/env python3
"""RQT-594 odd-prime-power exact integer coordinate gates.
Usage: python rqt594.py GRAM RQT583 RQT584 RQT586 [OUTPUT]
"""
import json,sys,hashlib,math
from pathlib import Path
P=list(map(Path,sys.argv[1:5])); F,E,C584,C586=[json.loads(p.read_text()) for p in P]
assert hashlib.sha256(P[0].read_bytes()).hexdigest()=="f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228"
assert hashlib.sha256(P[1].read_bytes()).hexdigest()=="5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92"
blocked={int(c["family_index"]) for d in (C584,C586) for c in d["certificates"]}|{13}
families=[e for e in E["equations"] if int(e["index"]) not in blocked]
assert len(families)==53 and math.gcd(F[0][0],15)==1
def q(u,t,e):
 v=[u]+[e["ray"][i]*t+e["offset"][i] for i in range(3)]
 return sum(v[i]*F[i][j]*v[j] for i in range(4) for j in range(4))+2
records=[]
for e in families:
 item={"family_index":e["index"],"powers":{}}
 for p,limit in ((3,9),(5,6)):
  levels=[]
  for k in range(1,limit+1):
   m=p**k; root={}
   for z in range(m):root.setdefault(z*z%m,z)
   A,B,C=[int(e[key])%m for key in "ABC"]
   count=0;witness=None
   for t in range(m):
    s=root.get((A*t*t+B*t+C)%m)
    if s is None:continue
    count+=1
    if witness is None:
     v=[e["ray"][j]*t+e["offset"][j] for j in range(3)]
     b=sum(F[0][j+1]*v[j] for j in range(3))
     u=(-b+s)*pow(F[0][0],-1,m)%m
     assert q(u,t,e)%m==0
     witness={"u":u,"t":t}
   levels.append({"modulus":m,"admissible_t_residues":count,"witness":witness})
   assert count>0
  item["powers"][str(p)]=levels
 records.append(item)
res={"rqt":594,"families_tested":53,"new_exclusions":0,"excluded_total":82,"unresolved":53,"powers_tested":{"3":9,"5":6},"records":records,"original_22d_wall":"NOT REPLAYED","root19":"OPEN"}
Path(sys.argv[5] if len(sys.argv)>5 else "RQT-594-results.json").write_text(json.dumps(res,indent=2)+"\n")
print("PASS: 53/53 modular survivors through 3^9 and 5^6; zero new all-scale exclusions; root19 OPEN")
