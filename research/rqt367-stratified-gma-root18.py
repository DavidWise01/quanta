#!/usr/bin/env python3
"""RQT-367: fair, collision-free {{9x9}}^9 GMA root-18 exact search."""
import argparse,json,math
from collections import Counter
F=[[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]]
U=[[224,29,-224,-130],[-193,-25,193,112],[40,5,-40,-23],[-336,-43,335,195]]
G=[[sum(U[i][k]*F[k][l]*U[j][l] for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
assert G[3][3]==-5868287405277328266
TOTAL=81**9;STEP=6364136223846793007%TOTAL
assert TOTAL==150094635296999121 and math.gcd(STEP,TOTAL)==1
AXES=[(0,1),(1,2),(2,0)]*3
ACCEPT={'0111','1001','1110'}
MODS=[256,3,5,7,11,13,17,19,23,29,31,37]
SQ={p:frozenset(i*i%p for i in range(p)) for p in MODS}
H=[[G[i][3]*G[j][3]-G[3][3]*G[i][j] for j in range(3)] for i in range(3)]
HM={p:([[z%p for z in row] for row in H],(-2*G[3][3])%p) for p in MODS}
def index_to_address(index):
 out=[]
 for _ in range(9):
  index,d=divmod(index,81);out.append((d//9-4,d%9-4))
 assert index==0
 return out
def address_to_coord(addr):
 t=[0,0,0];c=[0,0,0]
 for g,(i,j) in enumerate(addr):
  x,y=AXES[g];t[x]+=i*9**c[x];c[x]+=1;t[y]+=j*9**c[y];c[y]+=1
 assert c==[6,6,6]
 return tuple(t)
def check(t):
 for mod in MODS:
  h,c=HM[mod]
  d=(c+sum(t[i]*h[i][j]*t[j] for i in range(3) for j in range(3)))%mod
  if d not in SQ[mod]:return 'modular',[]
 B=sum(G[i][3]*t[i] for i in range(3))
 C=sum(t[i]*G[i][j]*t[j] for i in range(3) for j in range(3))+2
 D=B*B-G[3][3]*C
 if D<0:return 'negative',[]
 root=math.isqrt(D)
 if root*root!=D:return 'nonsquare',[]
 hits=[]
 for sign in (-1,1):
  numerator=-B+sign*root
  if numerator%G[3][3]:continue
  v=(*t,numerator//G[3][3])
  r=tuple(sum(U[j][i]*v[j] for j in range(4)) for i in range(4))
  assert sum(r[i]*F[i][j]*r[j] for i in range(4) for j in range(4))==-2
  parity=''.join(str(x%2) for x in r)
  if parity in ACCEPT:hits.append({'t':v,'original_r':r,'parity':parity})
 return 'square',hits
def run(start,budget):
 assert 0<=start and 0<budget and start+budget<=TOTAL
 counts=Counter();families=Counter();generation=[set() for _ in range(9)]
 hits=[];checksum=0
 for k in range(start,start+budget):
  index=STEP*k%TOTAL;addr=index_to_address(index)
  families[tuple(addr[0])]+=1
  for g,a in enumerate(addr):generation[g].add(tuple(a))
  cls,found=check(address_to_coord(addr));counts[cls]+=1
  hits.extend([{'address':addr,'index':index,**r} for r in found])
  checksum=(checksum*1000003+index)%((1<<127)-1)
 return {'status':'PASS exact stratified sampled root search',
 'first_sequence_offset':start,'total_leaves_tested':budget,
 'total_address_space':TOTAL,'permutation_step':STEP,
 'distinct_addresses':budget,'unique_generation_cells':[len(v) for v in generation],
 'top_generation_family_count':len(families),
 'top_family_min_hits':min(families.values()),'top_family_max_hits':max(families.values()),
 'sieve_counts':dict(counts),'accepted_norm_minus_two_candidates':hits,
 'permutation_index_checksum_127bit':str(checksum),
 'coverage':'NONEXHAUSTIVE; exactly the listed sequence indices',
 'root18':'OPEN unless candidates pass additional frozen prefix tests'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--budget',type=int,default=200000);p.add_argument('--start',type=int,default=0)
 args=p.parse_args()
 assert address_to_coord([(0,0)]*9)==(0,0,0)
 assert address_to_coord([(4,4)]*9)==((9**6-1)//2,)*3
 assert address_to_coord([(-4,-4)]*9)==(-((9**6-1)//2),)*3
 print(json.dumps(run(args.start,args.budget),indent=2))
if __name__=='__main__':main()
