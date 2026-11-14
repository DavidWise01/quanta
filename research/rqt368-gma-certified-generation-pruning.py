#!/usr/bin/env python3
"""RQT-368: exact mod-81 GMA ancestor sieve + diversified depth-nine samples."""
import json,math
from collections import Counter,defaultdict,deque
F=[[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]]
U=[[224,29,-224,-130],[-193,-25,193,112],[40,5,-40,-23],[-336,-43,335,195]]
G=[[sum(U[i][k]*F[k][l]*U[j][l] for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
assert G[3][3]==-5868287405277328266
H=[[G[i][3]*G[j][3]-G[3][3]*G[i][j] for j in range(3)] for i in range(3)]
C=-2*G[3][3]
def digits(n):
 assert -40<=n<=40
 d=(n+4)%9-4;e=(n-d)//9
 assert -4<=d<=4 and -4<=e<=4
 return d,e
def family(a,b,c):
 a0,a1=digits(a);b0,b1=digits(b);c0,c1=digits(c)
 return (a0,b0)
def delta_mod(t,m):
 return (C+sum(t[i]*(H[i][j]%m)*t[j] for i in range(3) for j in range(3)))%m
def lift(a,b,c,k):
 k%=81**6
 coords=[]
 for v in (a,b,c):
  n=k%9**4;k//=9**4
  high=0
  for j in range(4):
   n,d=divmod(n,9);high+=(d-4)*9**j
  coords.append(v+81*high)
 return tuple(coords)
def norm_test(t):
 B=sum(G[i][3]*t[i] for i in range(3))
 cc=sum(t[i]*G[i][j]*t[j] for i in range(3) for j in range(3))+2
 D=B*B-G[3][3]*cc
 if D<0:return 'negative',[]
 root=math.isqrt(D)
 if root*root!=D:return 'nonsquare',[]
 found=[]
 for sign in (-1,1):
  num=-B+sign*root
  if num%G[3][3]:continue
  tt=(*t,num//G[3][3])
  r=tuple(sum(U[j][i]*tt[j] for j in range(4)) for i in range(4))
  assert sum(r[i]*F[i][j]*r[j] for i in range(4) for j in range(4))==-2
  found.append({'t':tt,'original_r':r,'accepted':''.join(str(x%2) for x in r) in {'0111','1001','1110'}})
 return 'square',found
def main():
 squares81={n*n%81 for n in range(81)}
 survivors=[];fam=Counter();surv=Counter()
 for a in range(-40,41):
  for b in range(-40,41):
   for c in range(-40,41):
    key=family(a,b,c);fam[key]+=1
    if delta_mod((a,b,c),81) in squares81:
     survivors.append((a,b,c));surv[key]+=1
 assert len(squares81)==31 and len(survivors)==406782
 assert len(fam)==81 and all(x==6561 for x in fam.values())
 assert min(surv.values())==4374 and max(surv.values())==6075
 for j in range(1000):
  t=survivors[(137*j)%len(survivors)]
  v=lift(*t,j*65537+123)
  assert all((v[k]-t[k])%81==0 for k in range(3))
  assert delta_mod(v,81)==delta_mod(t,81)
 groups=defaultdict(deque)
 for v in survivors:groups[family(*v)].append(v)
 keys=sorted(groups);selected=[]
 while len(selected)<150000:
  for key in keys:
   if len(selected)>=150000:break
   selected.append(groups[key].popleft())
 fcount=Counter(family(*v) for v in selected)
 assert len(fcount)==81 and min(fcount.values())==1851 and max(fcount.values())==1852
 mods=[256,3,5,7,11,13,17,19,23,29,31,37]
 squaremods={m:{z*z%m for z in range(m)} for m in mods}
 counts=Counter();hits=[]
 for i,v in enumerate(selected):
  t=lift(*v,i*1299709+17)
  if any(delta_mod(t,m) not in squaremods[m] for m in mods):
   counts['modular']+=1;continue
  status,found=norm_test(t);counts[status]+=1;hits.extend(found)
 assert dict(counts)=={'modular':149869,'negative':125,'nonsquare':6}
 print(json.dumps({'status':'PASS exact','first_three_nodes':81**3,
 'pruned_mod81':81**3-len(survivors),'survivors_mod81':len(survivors),
 'first_families':len(fam),'survivors_per_first_family_min':min(surv.values()),
 'survivors_per_first_family_max':max(surv.values()),
 'sampled_full_depth':len(selected),'sampled_per_family_min':min(fcount.values()),
 'sampled_per_family_max':max(fcount.values()),'sample_results':dict(counts),
 'norm_minus_two_candidates':hits,'global_search_exhausted':False,
 'original_root18':'OPEN'},indent=2))
if __name__=='__main__':main()
