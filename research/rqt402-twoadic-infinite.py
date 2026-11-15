#!/usr/bin/env python3
"""RQT-402: two-adic solvability of the exact RQT-401 candidate-successor Gram.
Requires the full JSON output of research/rqt401-frozen-matrix.py --out FILE.
The theorem concerns Z_2; it does not construct an ordinary integer root.
"""
import argparse,json
from pathlib import Path

def audit(source,powers=(8,16,32,64)):
 Q=[[int(t) for t in row] for row in source['restricted_Gram']]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(t%2==0 for row in Q for t in row)
 A=[[t//2 for t in row] for row in Q]
 assert [[v%8 for v in row] for row in A]==[[1,4,1],[4,2,3],[1,3,7]]
 a,b,c=A[0][0],A[0][2],A[2][2]+1
 assert a%2==b%2==1 and c%8==0
 D=b*b-a*c
 assert D%8==1
 def f(x):return a*x*x+2*b*x+c
 assert f(0)%8==0
 roots=[x for x in range(8) if f(x)%8==0]
 modulus=8;out=[]
 for k in range(3,max(powers)+1):
  if k>3:
   nextmod=modulus*2
   roots=[v+t*modulus for v in roots for t in (0,1) if f(v+t*modulus)%nextmod==0]
   modulus=nextmod
  if k in powers:
   assert roots and all(f(v)%modulus==0 for v in roots)
   out.append({'power':k,'modulus':str(modulus),'count':len(roots),
               'witness_x':str(roots[0]),'other_x':list(map(str,roots[1:4]))})
 return {'RQT':402,
  'theorem':'a,b odd and 8|c imply D=b*b-a*c == 1 (mod 8), hence D is a square in Z_2; x=(-b+sqrt(D))/a solves a*x*x+2*b*x+c=0 in Z_2',
  'A_mod_8':[[v%8 for v in row] for row in A],
  'D_mod_8':D%8,'D_mod_256':D%256,'witnesses':out,
  'status':'2-ADIC EXISTENCE PROVED, ORDINARY INTEGER ROOT19 OPEN',
  'root18_position':'CONDITIONAL on frozen 17-reflection prefix'}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('full_kernel_json');p.add_argument('--out')
 args=p.parse_args()
 result=audit(json.loads(Path(args.full_kernel_json).read_text()))
 if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
