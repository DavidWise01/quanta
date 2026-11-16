#!/usr/bin/env python3
"""RQT-434: two-corridor check and bounded exact d=1 root19 sieve.
Input: RQT-401 full JSON with original_F4, reduced_kernel_basis, restricted_Gram.
"""
import argparse,hashlib,json,math
from pathlib import Path
SHA="5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809"
def audit(src,N=3000):
 Q=[[int(t) for t in r] for r in src["restricted_Gram"]]
 B=[[int(t) for t in r] for r in src["reduced_kernel_basis"]]
 F=[[int(t) for t in r] for r in src["original_F4"]]
 assert len(Q)==3 and all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(t%2==0 for r in Q for t in r)
 assert all(sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4))==Q[i][j] for i in range(3) for j in range(3))
 digest=hashlib.sha256(json.dumps([[str(t) for t in r] for r in Q],separators=(",",":")).encode()).hexdigest()
 assert digest==SHA
 A=[[v//2 for v in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2]
 assert f<0 and f%13==f%23==0 and math.isqrt(-f)**2!=-f
 assert (c+5*e)%13==(c+5*e)%23==0
 assert (-a-10*b-25*g)%13==11 and (-a-10*b-25*g)%23==7
 square256={v*v%256 for v in range(256)}
 counts={k:0 for k in ("cone_pairs","excluded_p13","excluded_p23","excluded_union","prime_survivors","square_residue_mod256","nonnegative_discriminants","exact_squares","integral_z")}
 witnesses=[]
 for y in range(1,N+1):
  start=177065*y//100000+1
  stop=(178600*y-1)//100000
  for x in range(start,stop+1):
   assert 177065*y<100000*x<178600*y
   counts["cone_pairs"]+=1
   p13=(x%13!=0 and (y-5*x)%13==0)
   p23=(x%23!=0 and (y-5*x)%23==0)
   counts["excluded_p13"]+=bool(p13);counts["excluded_p23"]+=bool(p23)
   if p13 or p23:counts["excluded_union"]+=1;continue
   counts["prime_survivors"]+=1
   L=c*x+e*y;M=a*x*x+2*b*x*y+g*y*y;E=L*L-f*(M+1)
   if E%256 not in square256:continue
   counts["square_residue_mod256"]+=1
   if E<0:continue
   counts["nonnegative_discriminants"]+=1
   s=math.isqrt(E)
   if s*s!=E:continue
   counts["exact_squares"]+=1
   for root in (-s,s):
    if (root-L)%f:continue
    z=(root-L)//f
    w=(x,y,z)
    assert sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))==-1
    r=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)]
    assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2
    witnesses.append([x,y,z]);counts["integral_z"]+=1
 if N==3000:
  assert counts==dict(cone_pairs=69094,excluded_p13=4905,excluded_p23=2873,excluded_union=7575,prime_survivors=61519,square_residue_mod256=13486,nonnegative_discriminants=13477,exact_squares=0,integral_z=0)
 return {"RQT":434,"status":"PASS exact two-corridor scope and finite d=1 sieve",
  "source_sha256":digest,"positive_y_range":[1,N],"counts":counts,"witnesses":witnesses,
  "identity":"E_d=L²-f(M+d²)=E_1+(-f)(d²-1)",
  "scope_correction":"RQT-394 slope cone necessary for integer d=1; not automatically for unrestricted rational denominators",
  "root19":"OPEN","rational_witness":"OPEN","frozen_position18":"UNVERIFIED"}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("full_rqt401_json");p.add_argument("--ymax",type=int,default=3000);p.add_argument("--out")
 a=p.parse_args();r=audit(json.loads(Path(a.full_rqt401_json).read_text()),a.ymax)
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+"\n")
 print(json.dumps(r,indent=2))
