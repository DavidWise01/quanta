#!/usr/bin/env python3
"""RQT-405: exact two-adic anisotropy of the candidate-successor Gram.
Run: python research/rqt405-isotropic-obstruction.py FULL_RQT401.json
"""
import argparse,itertools,json
from pathlib import Path

def audit(source):
 Q=[[int(x) for x in row] for row in source["restricted_Gram"]]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(x%2==0 for row in Q for x in row)
 A=[[x//2 for x in row] for row in Q]
 q4=[[x%4 for x in row] for row in A]
 assert q4==[[1,0,1],[0,2,3],[1,3,3]]
 entries=[]
 for p in itertools.product((0,1),repeat=3):
  if not any(p):continue
  residue=sum(A[i][j]*p[i]*p[j] for i in range(3) for j in range(3))%4
  assert residue!=0
  entries.append({"parity":"".join(map(str,p)),"half_norm_mod4":residue})
  for t in itertools.product((0,1),repeat=3):
   w=tuple(p[i]+2*t[i] for i in range(3))
   assert sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))%4==residue
 return {"RQT":405,"status":"PASS global rational null obstruction by mod8",
   "A_mod4":q4,"parity_classes":entries,
   "proof":"Primitive v has nonzero parity, hence v.T(Q/2)v != 0 mod4, so v.TQv != 0 mod8. Any rational null vector scales to primitive integral one, contradiction.",
   "null_vector_over_rationals":"NONEXISTENT",
   "norm_minus_two_root19":"OPEN",
   "root18_position":"UNVERIFIED"}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("full_json");p.add_argument("--out")
 a=p.parse_args();r=audit(json.loads(Path(a.full_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+"\n")
 print(json.dumps(r,indent=2))
