#!/usr/bin/env python3
"""RQT-421: verify the original F4 backmap, reduced Gram, and congruent form.
Requires full RQT-401 JSON with original_F4, reduced_kernel_basis,
restricted_Gram. These are three arithmetic checks from ONE source ancestry.
"""
import argparse,hashlib,json,math
from pathlib import Path
import sympy as s

def audit(src):
 F=s.Matrix([[int(t) for t in row] for row in src["original_F4"]])
 B=s.Matrix([[int(t) for t in row] for row in src["reduced_kernel_basis"]])
 Q=s.Matrix([[int(t) for t in row] for row in src["restricted_Gram"]])
 assert F.shape==(4,4) and B.shape==(4,3) and Q.shape==(3,3)
 assert F==F.T and Q==Q.T and B.T*F*B==Q
 assert all(int(t)%2==0 for t in Q)
 A=Q/2
 H=s.diag(1,1,1,1);H[:3,:3]=A
 U=s.Matrix([[-9,-25,0,0],[-5,-14,0,0],[0,0,1,0],[0,0,0,1]])
 assert U.det()==1
 Hnew=U.T*H*U
 def norm(M,v):
  v=s.Matrix(v)
  return int((v.T*M*v)[0])
 trials=[[1,0,0,1],[0,0,1,1],[1,1,0,1],[2,3,4,5],[16,9,1,3]]
 checks=[]
 for v in trials:
  w,d=v[:3],v[3]
  full=norm(F,B*s.Matrix(w))
  reduced=norm(A,w)
  homogeneous=norm(H,v)
  transported=[int(t) for t in U.inv()*s.Matrix(v)]
  assert full==2*reduced
  assert homogeneous==reduced+d*d==norm(Hnew,transported)
  checks.append({"vector":v,"backmap_valid":True,"congruence_valid":True,
                 "isotropic":homogeneous==0})
 assert not any(c["isotropic"] for c in checks)
 sha=hashlib.sha256(json.dumps([[str(t) for t in row] for row in Q.tolist()],
                              separators=(",",":")).encode()).hexdigest()
 assert sha=="5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809"
 return {"RQT":421,"status":"PASS exact backmapping and integral congruence",
         "Gram_SHA256":sha,"B_transpose_F4_B_equals_Q":True,
         "Q_even":True,"det_U":1,"sample_checks":checks,
         "isotropic_sample_count":0,
         "witness_status":"NOT CONSTRUCTED",
         "independence":"One frozen Gram ancestry; not three independent sources",
         "root19":"OPEN","position18":"UNVERIFIED"}

if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("full_rqt401_json")
 ap.add_argument("--out")
 args=ap.parse_args()
 result=audit(json.loads(Path(args.full_rqt401_json).read_text()))
 if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
