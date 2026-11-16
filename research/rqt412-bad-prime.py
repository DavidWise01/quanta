#!/usr/bin/env python3
"""RQT-412: exact determinant-critical odd primes for frozen candidate successor.
Requires RQT-401 full JSON with restricted_Gram and SymPy.
"""
import argparse,json
from pathlib import Path
from sympy import Matrix
def norm(A,v):return 1+sum(A[i][j]*v[i]*v[j] for i in range(3) for j in range(3))
def lift(A,p,v,n):
 v=list(v);mod=p;assert norm(A,v)%p==0
 grad=[2*sum(A[i][j]*v[j] for j in range(3))%p for i in range(3)]
 j=next(i for i,t in enumerate(grad) if t)
 out=[]
 for k in range(1,n+1):
  assert norm(A,v)%mod==0
  out.append({'power':k,'witness':list(map(str,v))})
  if k<n:
   t=(-(norm(A,v)//mod)*pow(grad[j],-1,p))%p
   v[j]+=mod*t;mod*=p
 return out
def audit(data):
 Q=[[int(v) for v in row] for row in data['restricted_Gram']]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(v%2==0 for row in Q for v in row)
 A=[[v//2 for v in row] for row in Q]
 det=int(Matrix(A).det())
 assert det!=0 and det%81==0 and det%243!=0
 assert det%1129==0 and det%(1129**2)!=0
 seeds={3:(0,0,1),1129:(1,4,15)}
 chains={str(p):lift(A,p,seed,8 if p==3 else 4) for p,seed in seeds.items()}
 return {'RQT':412,'status':'PASS determinant-critical exact local checks',
   'determinant_bits':abs(det).bit_length(),
   'valuations':{'3':4,'1129':1},'regular_lifting_chains':chains,
   'good_prime_theorem':'Every odd p not dividing det A admits regular mod-p representation of -1 and infinite Hensel lifts',
   'cofactor':'NOT FULLY FACTORED','root18_position':'UNVERIFIED',
   'root19':'OPEN','root20':'OPEN','root21':'conditional'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--out')
 args=p.parse_args();out=audit(json.loads(Path(args.full_rqt401_json).read_text()))
 if args.out:Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
