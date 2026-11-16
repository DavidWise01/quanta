#!/usr/bin/env python3
"""RQT-427: Cassels small-zero bound for full RQT-401 frozen candidate Gram.
Requires the full JSON with restricted_Gram. No witness search performed.
"""
import argparse,hashlib,json,math
from pathlib import Path
def audit(data):
 Q=[[int(x) for x in row] for row in data["restricted_Gram"]]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(x%2==0 for row in Q for x in row)
 A=[[x//2 for x in row] for row in Q]
 H=[row+[0] for row in A]+[[0,0,0,1]]
 U=[[-9,-25,0,0],[-5,-14,0,0],[0,0,1,0],[0,0,0,1]]
 assert U[0][0]*U[1][1]-U[0][1]*U[1][0]==1
 G=[[sum(U[k][i]*H[k][l]*U[l][j] for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
 sha=hashlib.sha256(json.dumps([[str(t) for t in row] for row in Q],separators=(',',':')).encode()).hexdigest()
 assert sha=="5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809"
 systems={}
 for name,M in (("original",H),("transformed",G)):
  S=sum(abs(x) for row in M for x in row)
  B=math.isqrt((3*S)**3)
  assert B*B<=(3*S)**3<(B+1)**2
  systems[name]={"S":str(S),"S_bits":S.bit_length(),"height_bound":str(B),"bound_digits":len(str(B)),"bound_bits":B.bit_length()}
 assert int(systems["transformed"]["height_bound"])<int(systems["original"]["height_bound"])
 return {"RQT":427,"status":"PASS exact Cassels height bound","Gram_sha256":sha,"systems":systems,
  "theorem":"For isotropic integral 4-variable H, there exists nonzero integral H-null x with max_i |x_i| <= (3*sum_ij abs(H_ij))**(3/2)",
  "hypotheses":"RQT-414 rational isotropy and RQT-405 anisotropic ternary subform",
  "integer_coordinate_bound":"floor(sqrt((3S)**3))",
  "explicit_rational_witness":"NOT CONSTRUCTED","root19":"OPEN","position18":"UNVERIFIED",
  "warning":"Finite search is mathematically complete but computationally enormous; a 4D null vector need not have denominator one"}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("full_lattice_json");p.add_argument("--out")
 a=p.parse_args();r=audit(json.loads(Path(a.full_lattice_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+"\n")
 print(json.dumps(r,indent=2))
