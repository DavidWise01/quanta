#!/usr/bin/env python3
"""RQT-410: exact square-root sign coherence in original RQT-401 Gram.
Usage: python research/rqt410-integral-square.py FULL_RQT401.json
"""
import argparse,json,math
from pathlib import Path
def audit(data):
 Q=[[int(t) for t in row] for row in data["restricted_Gram"]]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(t%2==0 for row in Q for t in row)
 A=[[t//2 for t in row] for row in Q]
 a,b,c=A[0];d,e=A[1][1:];f=A[2][2]
 assert f%2 and f%13==f%23==0
 x,y=16,9
 assert 177065*y<100000*x<178600*y
 L=c*x+e*y;M=a*x*x+2*b*x*y+d*y*y+1;E=L*L-f*M
 assert E%299==(L*L)%299
 assert L%13==5 and L%23==10
 s=5+13*((-10-5)*pow(13,-1,23)%23)
 assert s==174 and s*s%299==E%299
 assert (s-L)%299!=0 and (s+L)%299!=0
 assert E>0 and math.isqrt(E)**2!=E
 return dict(RQT=410,status="PASS mixed-sign modular counterexample",
    exact_integer_z_condition="E=s^2 and f divides one of (s-L),(s+L)",
    f_bits=abs(f).bit_length(),f_divisible_by=[13,23],
    xy=[x,y],s_mod299=s,L_mod13=L%13,L_mod23=L%23,
    square_mod299=True,coherent_sign_mod299=False,
    exact_integer_square=False,root19="OPEN",
    frozen_root18_position="UNVERIFIED")
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("full_rqt401_json");p.add_argument("--out")
 args=p.parse_args();result=audit(json.loads(Path(args.full_rqt401_json).read_text()))
 if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
