#!/usr/bin/env python3
"""RQT-370: 27 executable spatial cores, 729 cells/generation, nine generations.
Certified prefix pruning from authentic frozen F4; root18 remains OPEN.
"""
import json,itertools,math,random
from collections import Counter,defaultdict
F=[[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]]
U=[[224,29,-224,-130],[-193,-25,193,112],[40,5,-40,-23],[-336,-43,335,195]]
G=[[sum(U[i][k]*F[k][l]*U[j][l] for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
K=[[G[i][3]*G[j][3]-G[3][3]*G[i][j] for j in range(3)] for i in range(3)]
assert G[3][3]==-5868287405277328266
D=range(-4,5)
def region(d):return 0 if d<=-2 else (1 if d<=1 else 2)
def core(v):
 x,y,z=v
 return 'RCF'[region(z)]+'UCD'[2-region(y)]+'LCR'[region(x)]
def digit(n):return (n+4)%9-4
def disc(v):
 return -2*G[3][3]+sum(v[i]*K[i][j]*v[j] for i in range(3) for j in range(3))
def sq3(n,k):
 r=n%(9**k)
 if r==0:return True
 a=0
 while r%3==0:a+=1;r//=3
 return a%2==0 and r%3==1
def test(v):
 d=disc(v)
 if d<0:return 'negative',[]
 s=math.isqrt(d)
 if s*s!=d:return 'nonsquare',[]
 b=sum(v[i]*G[i][3] for i in range(3));hits=[]
 for sign in (-1,1):
  numerator=-b+sign*s
  if numerator%G[3][3]:continue
  t=(*v,numerator//G[3][3])
  r=[sum(U[j][i]*t[j] for j in range(4)) for i in range(4)]
  assert sum(r[i]*F[i][j]*r[j] for i in range(4) for j in range(4))==-2
  if ''.join(str(a%2) for a in r) in ('0111','1001','1110'):
   hits.append({'t':list(t),'r':r})
 return 'square',hits
cores={f'{z}{y}{x}':{'microcells':0,'surviving_g2':0,'parents':[],'buckets':{}}
 for z,y,x in itertools.product('RCF','UCD','LCR')}
for v in itertools.product(D,repeat=3):cores[core(v)]['microcells']+=1
assert len(cores)==27 and all(v['microcells']==27 for v in cores.values())
assert core((0,0,0))=='CCC' and core((-4,4,-4))=='RUL'
g2=Counter()
for v in itertools.product(range(-40,41),repeat=3):
 key=core(tuple(digit(x) for x in v))
 if sq3(disc(v),2):
  g2['survive']+=1;row=cores[key];row['surviving_g2']+=1
  residue=disc(v)%81
  kind='zero' if residue==0 else ('div9' if residue%9==0 else 'unit')
  row['buckets'].setdefault(kind,v)
  if len(row['parents'])<3:row['parents'].append(v)
 else:g2['pruned']+=1
assert g2=={'survive':406782,'pruned':124659}
g3=Counter();ledger={}
for name,row in sorted(cores.items()):
 parents=list(dict.fromkeys(
  [row['buckets'][t] for t in ('zero','div9','unit') if t in row['buckets']]
  +row['parents']))[:3]
 assert len(parents)==3
 counts=Counter()
 for parent in parents:
  assert sq3(disc(parent),2)
  for ds in itertools.product(D,repeat=3):
   v=tuple(parent[i]+81*ds[i] for i in range(3))
   counts['survive' if sq3(disc(v),3) else 'pruned']+=1
 assert sum(counts.values())==2187
 g3.update(counts)
 ledger[name]={'microcells':27,'g2_survivors':row['surviving_g2'],
               'selected_parents':[list(v) for v in parents],
               'g3_pruned':counts['pruned'],'g3_survive':counts['survive']}
assert g3=={'survive':51030,'pruned':8019}
mods=(256,3,5,7,11,13,17,19,23,29,31,37)
squaremods={m:{i*i%m for i in range(m)} for m in mods}
rng=random.Random(370);counts=Counter();hits=[]
for name in sorted(cores):
 micro=[v for v in itertools.product(D,repeat=3) if core(v)==name]
 assert len(micro)==27
 for k in range(400):
  address=[micro[k%27]]+[tuple(rng.choice(D) for _ in range(3)) for g in range(8)]
  t=[0,0,0];possible=True
  for gen,v in enumerate(address,1):
   t=[t[i]+v[i]*9**(gen-1) for i in range(3)]
   if not sq3(disc(t),gen):
    counts['pruned_at_g'+str(gen)]+=1;possible=False;break
  if not possible:continue
  if any(disc(t)%m not in squaremods[m] for m in mods):
   counts['modular_sieve']+=1;continue
  status,found=test(t);counts[status]+=1;hits.extend(found)
assert not hits and sum(counts.values())==10800
print(json.dumps({'status':'PASS','core_count':27,'cells_per_core':27,
 'cells_per_generation':729,'generations':9,'singlet':'CCC/000',
 'generation2_complete':dict(g2),
 'generation3_selected':{'parents':81,'children':59049,**dict(g3)},
 'sampled_full_depth':{'paths':10800,'per_core':400,'results':dict(sorted(counts.items()))},
 'core_ledger':ledger,'actual_root18':'OPEN',
 'scope':'g2 exhaustive; g3 only chosen parents; g9 sampled'},indent=2))
