#!/usr/bin/env python3
"""RQT-366: centered GMA (9x9)^9 root search. Exact, lazy, bounded."""
import argparse, functools, itertools, json, math
F=[[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]]
U=[[224,29,-224,-130],[-193,-25,193,112],[40,5,-40,-23],[-336,-43,335,195]]
G=[[sum(U[i][k]*F[k][l]*U[j][l] for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
assert G[3][3]==-5868287405277328266
AXES=[(0,1),(1,2),(2,0)]*3
ACCEPT={'0111','1001','1110'}
def delta(t):
 B=sum(G[i][3]*t[i] for i in range(3))
 C=sum(t[i]*G[i][j]*t[j] for i in range(3) for j in range(3))+2
 return B*B-G[3][3]*C,B
@functools.lru_cache(None)
def square_residues(k):
 m=9**k
 return frozenset(x*x%m for x in range(m))
def candidates(t):
 D,B=delta(t)
 if D<0:return []
 root=math.isqrt(D)
 if root*root!=D:return []
 hits=[]
 for sign in (-1,1):
  num=-B+sign*root
  if num%G[3][3]:continue
  v=(*t,num//G[3][3])
  r=tuple(sum(U[j][i]*v[j] for j in range(4)) for i in range(4))
  assert sum(r[i]*F[i][j]*r[j] for i in range(4) for j in range(4))==-2
  if ''.join(str(z%2) for z in r) in ACCEPT:hits.append({'t':v,'r':r})
 return hits
def address_to_t(address):
 assert len(address)==9
 coords=[0,0,0];counts=[0,0,0]
 for g,(i,j) in enumerate(address):
  assert -4<=i<=4 and -4<=j<=4
  a,b=AXES[g]
  coords[a]+=i*9**counts[a];counts[a]+=1
  coords[b]+=j*9**counts[b];counts[b]+=1
 assert counts==[6,6,6]
 return tuple(coords)
def scan(depth,budget):
 checked=pruned=leaves=deepest=0;truncated=False;hits=[]
 digits=(0,-1,1,-2,2,-3,3,-4,4)
 def walk(coords,counts,g):
  nonlocal checked,pruned,leaves,deepest,truncated
  deepest=max(g,deepest)
  if g==depth:
   leaves+=1
   if g==9:hits.extend(candidates(coords))
   return
  a,b=AXES[g]
  for i,j in itertools.product(digits,repeat=2):
   if checked>=budget:truncated=True;return
   checked+=1;v=list(coords);c=list(counts)
   v[a]+=i*9**c[a];c[a]+=1
   v[b]+=j*9**c[b];c[b]+=1
   frozen=min(c)
   if frozen:
    m=9**frozen
    if delta(v)[0]%m not in square_residues(frozen):
     pruned+=1;continue
   walk(tuple(v),tuple(c),g+1)
   if truncated:return
 walk((0,0,0),(0,0,0),0)
 return {'generation_reached':deepest,'nodes_examined':checked,
         'pruned_by_sound_square_test':pruned,'complete_addresses_tested':leaves,
         'truncated':truncated,'exact_root_candidates':hits}
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--depth',type=int,default=9)
 ap.add_argument('--budget',type=int,default=10000)
 args=ap.parse_args()
 assert 1<=args.depth<=9 and args.budget>0
 assert 81**9==(9**6)**3==150094635296999121
 assert address_to_t(((0,0),)*9)==(0,0,0)
 assert address_to_t(((4,4),)*9)==((9**6-1)//2,)*3
 result=scan(args.depth,args.budget)
 result.update({'depth_requested':args.depth,'node_budget':args.budget,
  'addresses_possible':81**9,'half_width_per_coordinate':(9**6-1)//2,
  'coverage':'PARTIAL' if result['truncated'] else 'COMPLETE WITHIN REQUESTED DEPTH',
  'original_root18':'OPEN unless candidate passes frozen 17-prefix constraints'})
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
