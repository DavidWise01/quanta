#!/usr/bin/env python3
"""RQT-377 exact integer Wall-kernel ladder. No authentic roots found."""
import argparse,itertools,json
from math import gcd
from functools import reduce
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
def xgcd(a,b):
 a=int(a);b=int(b)
 ra,rb=abs(a),abs(b);sa,sb=1,0;ta,tb=0,1
 while rb:
  k=ra//rb;ra,rb=rb,ra-k*rb;sa,sb=sb,sa-k*sb;ta,tb=tb,ta-k*tb
 return ra,sa*(1 if a>=0 else -1),ta*(1 if b>=0 else -1)
def annihilator(row):
 row=s.Matrix(1,len(row),list(row));n=row.cols;P=s.eye(n)
 for j in range(1,n):
  a,b=int((row*P)[0,0]),int((row*P)[0,j]);g,x,y=xgcd(a,b)
  if not g:continue
  E=s.eye(n);E[0,0]=x;E[j,0]=y;E[0,j]=-b//g;E[j,j]=a//g
  assert abs(E.det())==1
  P=P*E
 assert abs(P.det())==1
 assert all((row*P)[0,j]==0 for j in range(1,n))
 return P,int((row*P)[0,0])
def kernel_ladder(prefix,F=F,H=H):
 roots=[s.Matrix(v) for v in prefix];B=s.eye(4);history=[]
 for i,r in enumerate(roots):
  P,content=annihilator(list(r.T*H.T*B))
  assert content,'dependent Wall equation'
  B=B*P[:,1:]
  assert r.T*H.T*B==s.zeros(1,B.cols)
  history.append({'root_number':18+i,'row_content':content,'remaining_rank':B.cols})
 Q=B.T*F*B
 assert Q==Q.T and all(int(Q[j,j])%2==0 for j in range(Q.rows))
 return B,Q,history
def minor_content(R):
 k=R.cols
 return reduce(gcd,(abs(int(R[list(z),:].det())) for z in itertools.combinations(range(4),k)),0)
def prefix_validation(prefix):
 if not prefix:return {'valid':True,'reason':'empty'}
 R=s.Matrix.hstack(*(s.Matrix(r) for r in prefix))
 W=R.T*H*R
 norm=[int((R[:,j].T*F*R[:,j])[0]) for j in range(R.cols)]
 lower=[int(W[j,i]) for j in range(R.cols) for i in range(j)]
 minors=[minor_content(R[:,:k]) for k in range(1,R.cols+1)]
 parity=''.join(str(int(x)%2) for x in prefix[0])
 return {'norms':norm,'lower_Wall_pairings':lower,'minor_gcd':minors,
  'root18_parity':parity,'valid':all(x==-2 for x in norm) and
  all(x==0 for x in lower) and all(x==1 for x in minors) and
  parity in ('0111','1001','1110')}
def scan(B,Q,R):
 if Q.rows==1:
  return [[int(x) for x in B*s.Matrix([sgn])] for sgn in (-1,1) if int(Q[0,0])==-2]
 hits=[]
 for v in itertools.product(range(-R,R+1),repeat=Q.rows):
  u=s.Matrix(v)
  if int((u.T*Q*u)[0])==-2:hits.append([int(x) for x in B*u])
 return hits
def main():
 p=argparse.ArgumentParser();p.add_argument('--prefix-json');p.add_argument('--bound',type=int,default=5)
 args=p.parse_args();assert 0<=args.bound<=20
 for k in (1,2,3):
  fake=[[int(i==j) for i in range(4)] for j in range(k)]
  B,Q,_=kernel_ladder(fake,-2*s.eye(4),s.eye(4))
  assert Q==-2*s.eye(4-k)
  if k==3:
   assert set(tuple(r) for r in scan(B,Q,1))=={(0,0,0,1),(0,0,0,-1)}
 illustrative=s.Matrix([1,0,0,0])
 B,Q,_=kernel_ladder([[1,0,0,0]])
 assert illustrative.T*H.T*B==s.zeros(1,3) and Q==B.T*F*B
 result={'rqt':377,'status':'PASS exact saturated integral Wall-kernel construction',
  'original_F4_H4_verified':True,'synthetic_controls_for_ranks_3_2_1':'PASS',
  'illustrative_invalid_prefix_original_F4_kernel_identity':'PASS',
  'next_ranks_after_roots18_19_20':[3,2,1],
  'root21_last_step':'Only +/- primitive generator of saturated rank-one kernel; both require F4 norm -2',
  'roots18_19_20_21':'OPEN','frozen17_prefix_factorization':'NOT CHECKED'}
 if args.prefix_json:
  with open(args.prefix_json) as f:roots=json.load(f)
  assert 1<=len(roots)<=3 and all(len(r)==4 for r in roots)
  val=prefix_validation(roots);result['candidate_prefix']=val
  if val['valid']:
   B,Q,h=kernel_ladder(roots)
   result['kernel_basis']=B.tolist();result['restricted_Gram']=Q.tolist()
   result['rank_history']=h
   result['bounded_next_candidates']=scan(B,Q,args.bound)
  else:result['result']='INVALID candidate prefix rejected'
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
