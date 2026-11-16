#!/usr/bin/env python3
"""RQT-413: exact all-odd-prime solvability for conditional RQT-401 successor.
Input full RQT-401 JSON with restricted_Gram. Python integers only.
"""
import argparse,itertools,json,math
from pathlib import Path
def audit(data):
 q=[[int(t) for t in row] for row in data['restricted_Gram']]
 assert len(q)==3 and all(len(row)==3 for row in q)
 assert all(q[i][j]==q[j][i] for i in range(3) for j in range(3))
 assert all(t%2==0 for row in q for t in row)
 A=[[t//2 for t in row] for row in q]
 pairs=list(itertools.combinations(range(3),2))
 minors=[]
 for r in pairs:
  for c in pairs:
   i,j=r;k,l=c
   minors.append(A[i][k]*A[j][l]-A[i][l]*A[j][k])
 content=math.gcd(*minors)
 assert content==9
 assert math.gcd(*(t for row in A for t in row))==1
 assert [[t%3 for t in row] for row in A]==[[2,0,2],[0,0,0],[2,0,2]]
 def n(v): return 1+sum(A[i][j]*v[i]*v[j] for i in range(3) for j in range(3))
 v=[0,0,1];gradient=[2*sum(A[i][j]*v[j] for j in range(3))%3 for i in range(3)]
 assert n(v)%3==0 and gradient==[1,0,1]
 j=0;mod=3;chain=[]
 for k in range(1,9):
  assert n(v)%mod==0
  chain.append({'power':k,'vector':list(map(str,v))})
  t=(-(n(v)//mod)*pow(gradient[j],-1,3))%3
  v[j]+=mod*t;mod*=3
 a=A[0][0];b=A[0][2];c=A[2][2]+1
 D=b*b-a*c
 assert a%2==1 and D%8==1
 roots=[r for r in range(8) if (r*r-D)%8==0];m=8
 while m<65536:
  roots=[r+m*t for r in roots for t in (0,1) if ((r+m*t)**2-D)%(2*m)==0]
  m*=2
 x=((roots[0]-b)*pow(a,-1,m))%m
 assert n([x,0,1])%m==0
 return {'RQT':413,'status':'PASS exact finite-prime local solvability',
  'gcd_all_nine_2x2_minors':content,'matrix_entry_gcd':1,
  'odd_primes_except_3':'rank >= 2, binary nondegenerate representation -1, regular Hensel lifting',
  'p3_seed':[0,0,1],'p3_gradient_mod3':gradient,
  'p3_chain_to_power8':chain,'two_adic_D_mod8':D%8,
  'two_adic_witness_x_mod65536':str(x),
  'all_finite_prime_local_gates':'OPEN',
  'integer_root19':'OPEN','root18_predecessor_position':'UNVERIFIED',
  'scope':'Local solvability does not imply integral representation'}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('full_rqt401_json');p.add_argument('--out')
 a=p.parse_args()
 result=audit(json.loads(Path(a.full_rqt401_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
