#!/usr/bin/env python3
"""RQT-375: exact mod6561 fourth-coordinate obstruction in 27 cubed-nine cores."""
import itertools,json,hashlib
from collections import Counter
F=[[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]]
U=[[224,29,-224,-130],[-193,-25,193,112],[40,5,-40,-23],[-336,-43,335,195]]
G=[[sum(U[i][k]*F[k][l]*U[j][l] for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
A=G[3][3]
assert A%6561==1668
def bc(t,m):
 b=sum(G[i][3]*t[i] for i in range(3))%m
 c=(2+sum(G[i][j]*t[i]*t[j] for i in range(3) for j in range(3)))%m
 return b,c
def rootsmod(b,c,m):
 return [d for d in range(m) if (A*d*d+2*b*d+c)%m==0]
def lift(b,c,roots):
 for d0 in roots:
  f=(A*d0*d0+2*b*d0+c)%6561
  if f%729:continue
  target=(-f//729)%9
  derivative=(2*A*d0+2*b)%9
  if any((j*derivative)%9==target for j in range(9)):return True
 return False
def digit(x):return (x+4)%9-4
def core(v):
 def region(x):return 0 if x<=-2 else (1 if x<=1 else 2)
 x,y,z=(digit(t) for t in v)
 return 'RCF'[region(z)]+'UCD'[2-region(y)]+'LCR'[region(x)]
def main():
 # Reconstruct the exact same RQT-371 parent-order convention:
 # first distinguished g2 candidate of each residue kind, then first 150.
 sq81={d*d%81 for d in range(81)}
 sq6561={d*d%6561 for d in range(6561)}
 def disc(t):
  b,c=bc(t,81)
  return (b*b-A*c)%81
 rows={name:{'candidates':[],'kinds':{},'count':0} for name in
  (z+y+x for z in 'RCF' for y in 'UCD' for x in 'LCR')}
 for x in range(-40,41):
  for y in range(-40,41):
   for z in range(-40,41):
    v=(x,y,z)
    if disc(v) not in sq81:continue
    row=rows[core(v)];row['count']+=1
    kind='zero' if disc(v)==0 else ('div9' if disc(v)%9==0 else 'unit')
    row['kinds'].setdefault(kind,v)
    if len(row['candidates'])<150:row['candidates'].append(v)
 allresults=[];totals=Counter();prev='0'*64;examples=[]
 for name,row in sorted(rows.items()):
  pref=list(dict.fromkeys([row['kinds'][k] for k in ('zero','div9','unit') if k in row['kinds']]+row['candidates']))
  parents=[]
  for p in pref:
   if len(parents)==3:break
   # RQT-371 promoted iff a g3 child existed modulo 729.
   for bits in itertools.product(range(-4,5),repeat=3):
    t=tuple(p[i]+81*bits[i] for i in range(3))
    roots=rootsmod(*bc(t,729),729)
    if roots:
     parents.append((p,t,roots));break
  assert len(parents)==3
  counts=Counter();routes=[]
  for p,g3,roots in parents:
   cnt=Counter()
   for bits in itertools.product(range(-4,5),repeat=3):
    t=tuple(g3[i]+729*bits[i] for i in range(3))
    b,c=bc(t,6561);D=(b*b-A*c)%6561
    if D not in sq6561:kind='nonsquare_discriminant'
    elif not lift(b,c,roots):
     kind='new_integer_coordinate_obstruction'
     if len(examples)<6:examples.append({'core':name,'g3':g3,'g4':t,'B':b,'C':c,'Delta':D})
    else:kind='survives'
    cnt[kind]+=1
   assert sum(cnt.values())==729
   counts.update(cnt)
   routes.append({'g2':p,'g3':g3,'g3_d_roots_mod729':len(roots),'g4':dict(cnt)})
  totals.update(counts)
  packet={'core':name,'routes':routes,'g4_counts':dict(counts),'previous_hash':prev}
  prev=hashlib.sha256(json.dumps(packet,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  packet['sha256']=prev;allresults.append(packet)
 assert totals=={'survives':58482,'nonsquare_discriminant':486,'new_integer_coordinate_obstruction':81},totals
 print(json.dumps({'rqt':375,'status':'PASS','root18_to21':'OPEN',
  'generation':4,'modulus':6561,'cores':27,'selected_g3_parents':81,
  'g4_children':59049,'counts':dict(totals),'examples':examples,
  'hash_tip':prev,'core_packets':allresults,
  'scope':'selected 81 g3 witnesses only; roots18-21 not constructed'},indent=2))
if __name__=='__main__':main()
