#!/usr/bin/env python3
"""RQT-371 exact g4 cubic core routing; authentic frozen F4."""
import itertools,json,hashlib
from collections import Counter
F=[[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]]
U=[[224,29,-224,-130],[-193,-25,193,112],[40,5,-40,-23],[-336,-43,335,195]]
G=[[sum(U[i][k]*F[k][l]*U[j][l] for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
assert G[3][3]==-5868287405277328266
K=[[G[i][3]*G[j][3]-G[3][3]*G[i][j] for j in range(3)] for i in range(3)]
def qdisc(v):
 x,y,z=v
 return -2*G[3][3]+K[0][0]*x*x+K[1][1]*y*y+K[2][2]*z*z+2*(K[0][1]*x*y+K[0][2]*x*z+K[1][2]*y*z)
def square3(v,k):
 r=v%(9**k)
 if r==0:return True
 t=0
 while r%3==0:r//=3;t+=1
 return t%2==0 and r%3==1
def digit(x):return (x+4)%9-4
def core(v):
 def band(x):return 0 if x<=-2 else (1 if x<=1 else 2)
 x,y,z=v
 return 'RCF'[band(z)]+'UCD'[2-band(y)]+'LCR'[band(x)]
def main():
 rows={z+y+x:{'g2':0,'first':[],'kinds':{},'candidates':[]} for z,y,x in itertools.product('RCF','UCD','LCR')}
 g2=Counter()
 for x in range(-40,41):
  for y in range(-40,41):
   for z in range(-40,41):
    v=(x,y,z);d=qdisc(v);name=core(tuple(digit(t) for t in v))
    if not square3(d,2):g2['pruned']+=1;continue
    g2['survive']+=1;row=rows[name];row['g2']+=1
    kind='zero' if d%81==0 else ('div9' if d%9==0 else 'unit')
    row['kinds'].setdefault(kind,v)
    if len(row['candidates'])<150:row['candidates'].append(v)
 assert g2=={'pruned':124659,'survive':406782}
 squarelist={i*i%6561 for i in range(6561)}
 total=Counter();packets=[];prev='0'*64
 for name,row in sorted(rows.items()):
  pref=list(dict.fromkeys([row['kinds'][k] for k in ('zero','div9','unit') if k in row['kinds']]+row['candidates']))
  count=Counter();parents=[]
  for parent in pref:
   if len(parents)==3:break
   first=None;n=0
   for d in itertools.product(range(-4,5),repeat=3):
    v=tuple(parent[i]+81*d[i] for i in range(3))
    if square3(qdisc(v),3):
     n+=1
     if first is None:first=v
   if first is None:continue
   parents.append({'g2_parent':list(parent),'g3_representative':list(first),'surviving_g3_siblings':n})
   for d in itertools.product(range(-4,5),repeat=3):
    v=tuple(first[i]+729*d[i] for i in range(3))
    q=qdisc(v)
    a=square3(q,4)
    assert a==(q%6561 in squarelist)
    assert q%729==qdisc(first)%729
    count['g4_survive' if a else 'g4_pruned']+=1
  assert len(parents)==3 and sum(count.values())==2187
  total.update(count)
  packet={'rqt':'RQT-371','core':name,'g2_survivors':row['g2'],
          'routed_parents':parents,'g4_children_tested':2187,
          'g4_pruned':count['g4_pruned'],'g4_survived':count['g4_survive'],
          'witnesses':{'A':'exact 3-adic valuation parity',
                      'B':'enumerated quadratic residues modulo 6561',
                      'shared_source_ancestry':'stoicheion frozen F4'},
          'previous_hash':prev}
  prev=hashlib.sha256(json.dumps(packet,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  packet['sha256']=prev;packets.append(packet)
 assert len(packets)==27 and total=={'g4_survive':57834,'g4_pruned':1215}
 return packets

def next_main():
 upstream=main()
 assert len(upstream)==27
 residue_squares={i*i%59049 for i in range(59049)}
 parent_hash='0'*64
 totals=Counter();outputs=[];dead=[]
 for source in upstream:
  routes=[];counts=Counter()
  for parent in source['routed_parents']:
   g2=list(parent['g2_parent'])
   g3=list(parent['g3_representative'])
   g4=None
   for bits in itertools.product(range(-4,5),repeat=3):
    v=[g3[i]+729*bits[i] for i in range(3)]
    if square3(qdisc(v),4):g4=v;break
   replaced=False
   if g4 is None:
    replaced=True
    dead.append({'core':source['core'],'g2':g2,'g3':g3})
    for bits3 in itertools.product(range(-4,5),repeat=3):
     sibling=[g2[i]+81*bits3[i] for i in range(3)]
     if not square3(qdisc(sibling),3):continue
     for bits4 in itertools.product(range(-4,5),repeat=3):
      child=[sibling[i]+729*bits4[i] for i in range(3)]
      if square3(qdisc(child),4):
       g3=sibling;g4=child;break
     if g4 is not None:break
    assert g4 is not None
   counts['replacements']+=int(replaced)
   result=Counter()
   for bits5 in itertools.product(range(-4,5),repeat=3):
    child=[g4[i]+6561*bits5[i] for i in range(3)]
    d=qdisc(child)
    accepts=square3(d,5)
    assert accepts==(d%59049 in residue_squares)
    assert d%6561==qdisc(g4)%6561
    result['survived' if accepts else 'pruned']+=1
   assert sum(result.values())==729
   counts.update(result)
   routes.append({'g2':g2,'g3':g3,'g4':g4,'repaired':replaced,'g5':dict(result)})
  assert len(routes)==3 and counts['survived']+counts['pruned']==2187
  totals.update(counts)
  packet={'rqt':'RQT-372','core':source['core'],'rqt371_sha256':source['sha256'],
   'routes':routes,'g5_descendants_tested':2187,'g5_results':dict(counts),
   'source_ancestry':'one authentic stoicheion F4; two exact residue algorithms',
   'previous_sha256':parent_hash}
  parent_hash=hashlib.sha256(json.dumps(packet,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  packet['sha256']=parent_hash
  outputs.append(packet)
 assert totals=={'survived':59049,'replacements':1}
 assert len(dead)==1 and dead[0]['core']=='FCL'
 print(json.dumps({'status':'PASS exact original F4 generation-five routing',
   'cores':27,'routes':81,'g5_children':59049,'g5_survived':59049,'g5_excluded':0,
   'dead_g3_routes':dead,'repaired_routes':1,'chain_sha256':parent_hash,
   'scope':'selected 81 g4 representatives; not exhaustive g5',
   'root18':'OPEN','core_packets':outputs},indent=2))

if __name__=='__main__':next_main()
