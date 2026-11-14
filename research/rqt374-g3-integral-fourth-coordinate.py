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

def rqt374():
 parents=main()
 assert len(parents)==27
 modulus=729
 A=G[3][3]%modulus
 # Every (B,C) pair admitting a genuine fourth integer coordinate.
 # Cache by B to avoid storing 729 separate quadratic-solution lists.
 reachable={}
 squares={x*x%modulus for x in range(modulus)}
 def residue_pair(t):
  b=sum(G[i][3]*t[i] for i in range(3))%modulus
  c=(2+sum(t[i]*G[i][j]*t[j] for i in range(3) for j in range(3)))%modulus
  return b,c
 def can_solve(b,c):
  if b not in reachable:
   reachable[b]={(-A*d*d-2*b*d)%modulus for d in range(modulus)}
  return c in reachable[b]
 tally=Counter()
 reports=[]
 exemplar=[]
 for packet in parents:
  counts=Counter()
  ancestry=[p['g2_parent'] for p in packet['routed_parents']]
  for par in ancestry:
   for x,y,z in itertools.product(range(-4,5),repeat=3):
    child=tuple(par[i]+81*(x,y,z)[i] for i in range(3))
    b,c=residue_pair(child)
    disc=(b*b-A*c)%modulus
    if disc not in squares:
     counts['discriminant_exclusion']+=1
    elif not can_solve(b,c):
     counts['new_integral_coordinate_exclusion']+=1
     if len(exemplar)<6:
      exemplar.append({'core':packet['core'],'triple':child,
                       'B_mod729':b,'C_mod729':c,'discriminant_mod729':disc})
    else:counts['survived']+=1
    # Future digits are multiples of 729 and cannot alter the proof.
    assert residue_pair(tuple(child[i]+729*(i+2) for i in range(3)))==(b,c)
  assert sum(counts.values())==2187
  tally.update(counts)
  reports.append({'core':packet['core'],'rqt371_parent_sha256':packet['sha256'],
    'g2_parents':ancestry,'counts':dict(counts)})
 assert tally=={'survived':55647,'discriminant_exclusion':2916,'new_integral_coordinate_exclusion':486},tally
 assert len(reports)==27
 print(json.dumps({'rqt':'RQT-374','root18_to21':'OPEN',
  'source':'authentic frozen stoicheion F4 / exact RQT-363 unimodular U',
  'geometry':'27 cubic cores; selected 3 g2 parents/core; all 729 g3 children/parent',
  'parents':81,'generation3_children':59049,'counts':dict(tally),
  'additional_integral_exclusions_over_square_only':486,
  'representative_failures':exemplar,'core_packets':reports,
  'proof':'All future descendants preserve B,C modulo 729; every integer d must solve the quadratic modulo 729',
  'coverage':'selected families only; not the full 729^3 third-generation cube'},
  indent=2))

if __name__=='__main__':rqt374()
