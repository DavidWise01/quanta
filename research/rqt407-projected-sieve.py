#!/usr/bin/env python3
"""RQT-407: project local Z/2^kZ solutions for A=Q/2, A(v)=-1.
Requires full RQT-401 JSON with restricted_Gram. Exact integer only.
"""
import argparse,itertools,json
from collections import Counter
from pathlib import Path
def audit(src,max_power=8):
 Q=[[int(t) for t in row] for row in src['restricted_Gram']]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(t%2==0 for row in Q for t in row)
 A=[[v//2 for v in row] for row in Q]
 assert [[v%4 for v in row] for row in A]==[[1,0,1],[0,2,3],[1,3,3]]
 def N(v):
  return 1+sum(A[i][j]*v[i]*v[j] for i in range(3) for j in range(3))
 R=[(0,0,0)];m=1;levels=[]
 for k in range(1,max_power+1):
  m2=m*2;new=[]
  for v in R:
   for t in itertools.product((0,1),repeat=3):
    w=tuple(v[i]+m*t[i] for i in range(3))
    if N(w)%m2==0:new.append(w)
  R=new;m=m2
  projection={(x,y) for x,y,z in R}
  parity=Counter(''.join(str(t%2) for t in v) for v in R)
  levels.append(dict(power=k,modulus=m,triples=len(R),xy_pairs=len(projection),
                     rejected_xy_pairs=m*m-len(projection),
                     parity_counts=dict(sorted(parity.items()))))
 return {'RQT':407,'status':'PASS exact candidate successor modular projection',
         'normalization':'A=Q/2; solve v^T A v=-1 modulo 2^k',
         'levels':levels,
         'obstruction':'A pair (x,y) outside the projected set cannot produce any integer z with norm -2',
         'limitations':'Modular projection is necessary, not sufficient; no global integer root and no frozen predecessor test',
         'root19':'OPEN','root20':'OPEN','root21':'conditional'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json')
 p.add_argument('--max-power',type=int,default=8);p.add_argument('--out')
 a=p.parse_args()
 if not 1<=a.max_power<=9:raise ValueError('max-power must be between 1 and 9')
 out=audit(json.loads(Path(a.full_rqt401_json).read_text()),a.max_power)
 if a.out:Path(a.out).write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
