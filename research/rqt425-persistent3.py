#!/usr/bin/env python3
"""RQT-425: exact 3-adic persistence in the RQT-401 candidate-successor lattice.
Requires full RQT-401 JSON with restricted_Gram. Local theorem only.
"""
import argparse,itertools,json
from pathlib import Path
def audit(src):
 Q=[[int(t) for t in row] for row in src['restricted_Gram']]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(t%2==0 for row in Q for t in row)
 A=[[t//2 for t in row] for row in Q]
 assert [[t%27 for t in row] for row in A]==[[8,3,14],[3,0,21],[14,21,2]]
 a,b,c=A[0];d,e=A[1][1:];f=A[2][2]
 def q(v,m):
  x,y,z=v
  return (a*x*x+2*b*x*y+2*c*x*z+d*y*y+2*e*y*z+f*z*z)%m
 C0=a+4*c+4*f;L0=2*(b+2*e);M0=d
 assert all(n%9==0 for n in (C0,L0,M0))
 C,L,M=C0//9,L0//9,M0//9
 assert (C%3,L%3,M%3)==(2,1,0)
 def P(y,k):return C+L*y+M*y*y+k*k
 chains={}
 for k in (1,3,9):
  y=(-2-k*k)%3;mod=3;chain=[str(y)]
  for n in range(2,13):
   assert P(y,k)%mod==0
   grad=(L+2*M*y)%3;assert grad==1
   digit=(-((P(y,k)//mod)%3)*pow(grad,-1,3))%3
   y+=mod*digit;mod*=3
   assert P(y,k)%mod==0
   chain.append(str(y))
  chains[str(k)]=chain
 def primitive(v):return not all(t%3==0 for t in v)
 def base(D):
  return [(x,y,z) for x,y,z in itertools.product(range(9),repeat=3)
          if primitive((x,y,z)) and (q((x,y,z),9)+D*D)%9==0]
 def lift(V,m,D):
  n=3*m;out=[]
  for x,y,z in V:
   for i,j,k in itertools.product(range(3),repeat=3):
    w=(x+m*i,y+m*j,z+m*k)
    if (q(w,n)+D*D)%n==0:out.append(w)
  return out
 counts={}
 for D in (3,9):
  V=base(D);m=9;counts[str(D)]={'9':len(V)}
  for _ in range(3):
   V=lift(V,m,D);m*=3;counts[str(D)][str(m)]=len(V)
 assert counts=={'3':{'9':216,'27':972,'81':8748,'243':78732},
                 '9':{'9':216,'27':1944,'81':17496,'243':157464}}
 return {'RQT':425,'status':'PASS exact enumeration and infinite local Hensel proof',
  'A_mod27':[[t%27 for t in row] for row in A],
  'normalized_polynomial_mod3':[2,1,0],
  'theorem':'P_k(y)=q(1,y,2)/9+k^2 has P_k(y)=2+y+k^2 mod3 and derivative=1 mod3, so for every k in Z_3 there is a unique y in Z_3 solving q(1,y,2)=-(3k)^2',
  'primitive_counts':counts,'sample_y_lift_chains_mod3_powers_1_to_12':chains,
  'root19':'OPEN','rational_witness':'NOT CONSTRUCTED',
  'root18_position':'UNVERIFIED'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--out')
 args=p.parse_args();r=audit(json.loads(Path(args.full_rqt401_json).read_text()))
 if args.out:Path(args.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
