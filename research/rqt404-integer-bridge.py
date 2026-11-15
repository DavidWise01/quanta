#!/usr/bin/env python3
"""RQT-404: exact quadratic-discriminant search inside global RQT-394 cone.
Run: python research/rqt404-integer-bridge.py FULL_RQT401.json --max-y 30000
The published RQT-401 reduced Gram is REQUIRED. Not a global existence proof.
"""
import argparse,json,math,time
from pathlib import Path

def scan(data,max_y):
 Q=[[int(t) for t in row] for row in data['restricted_Gram']]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 a,b,c=Q[0];d,e=Q[1][1:];f=Q[2][2]
 assert f
 A=c*c-f*a;K=c*e-f*b;C=e*e-f*d
 moduli=(64,63,65,11,13,17,19,23)
 squares={m:{x*x%m for x in range(m)} for m in moduli}
 counts={str(m):0 for m in moduli}
 total=positive=exact_square=0;roots=[]
 for y in range(1,max_y+1):
  lo=(177065*y)//100000+1
  hi=(178600*y-1)//100000
  for x in range(lo,hi+1):
   total+=1
   D=A*x*x+2*K*x*y+C*y*y-2*f
   if D<0: continue
   positive+=1
   for m in moduli:
    if D%m not in squares[m]:break
    counts[str(m)]+=1
   else:
    t=math.isqrt(D)
    if t*t!=D: continue
    exact_square+=1
    L=c*x+e*y
    for sign in (-1,1):
     n=-L+sign*t
     if n%f:continue
     z=n//f
     assert a*x*x+2*b*x*y+2*c*x*z+d*y*y+2*e*y*z+f*z*z==-2
     roots.append([str(x),str(y),str(z)])
 return {'RQT':404,'status':'FINITE CONE EXCLUSION ONLY',
   'max_positive_y':max_y,'pairs_tested':total,'nonnegative_D':positive,
   'cumulative_modular_square_filters':counts,
   'perfect_square_D':exact_square,'exact_integer_root_candidates':roots,
   'negative_y':'covered by overall sign reversal',
   'frozen_root18_position':'NOT VERIFIED',
   'root19':'OPEN','root20':'OPEN','root21':'conditional'}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('full_kernel_json')
 p.add_argument('--max-y',type=int,default=30000)
 p.add_argument('--out')
 args=p.parse_args()
 assert args.max_y>=0
 result=scan(json.loads(Path(args.full_kernel_json).read_text()),args.max_y)
 if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
