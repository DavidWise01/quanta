#!/usr/bin/env python3
"""RQT-637 exact norm-composition audit of RQT-636 Chakravala paths.
Usage: python rqt637-norm-composition.py [output.json] [steps=10000]
"""
import math,json,hashlib,sys
from pathlib import Path
DATA=[
(1,5,3,89518360633605555683821304281344825,[28,29,30,31,33,34,35,36,37]),
(2,7,3,149561530769640628300862186866588569,[81,89,92]),
(3,4,2,158134758925461363207454619257200752,[0,1,2,7])]
def digest(x):
 return hashlib.sha256(x.to_bytes((x.bit_length()+7)//8 or 1,'big')).hexdigest()
def run(entry,limit):
 index,s,E,D,ids=entry
 assert D%(s*s)==0
 d=D//(s*s);root=math.isqrt(d);assert root*root<d
 a=root+1;b=1;k=a*a-d;seen={};repeats=0;squares=0;best=None;unit=None
 for n in range(limit):
  assert a*a-d*b*b==k
  if best is None or abs(k)<best[0]:best=(abs(k),n,k)
  X=a*a+d*b*b;Y=2*a*b
  if X%abs(k)==0 and Y%abs(k)==0:
   X//=abs(k);Y//=abs(k);assert X*X-d*Y*Y==1
   squares+=1
   if Y:unit=('square',n,X,Y)
  if k in seen:
   repeats+=1
   for olda,oldb,oldn in seen[k]:
    xx=a*olda-d*b*oldb;yy=b*olda-a*oldb
    if xx%k==0 and yy%k==0:
     X=xx//k;Y=yy//k;assert X*X-d*Y*Y==1
     if Y:unit=('pair',oldn,n,X,Y)
  else:seen[k]=[]
  if len(seen[k])<3:seen[k].append((a,b,n))
  if unit:break
  modulus=abs(k);g=math.gcd(b,modulus);assert a%g==0
  q=modulus//g
  residue=(-a//g*pow(b//g,-1,q))%q if q>1 else 0
  center=(root-residue)//q if q>1 else 0
  vals=[residue+(center+j)*q for j in (-2,-1,0,1,2,3)]
  m=min((v for v in vals if v>=0),key=lambda v:(abs(v*v-d),abs(v-root)))
  assert (a+b*m)%modulus==0 and (m*m-d)%k==0
  a,b,k=(a*m+d*b)//modulus,(a+b*m)//modulus,(m*m-d)//k
 assert not unit,('unit recovered, check!',unit)
 return {'group':index,'removed_factor_s':s,'original_D':str(D),'reduced_d':str(d),
 'canonical_ids':ids,'steps_checked':limit,'norms_seen':len(seen),
 'repeated_signed_k_states':repeats,'integral_square_division_units':squares,
 'shortcuts_found':0,'minimum_absolute_norm':str(best[0]),
 'minimum_norm_step':best[1],'minimum_signed_norm':str(best[2]),
 'last_norm':str(k),'last_a_bits':a.bit_length(),'last_b_bits':b.bit_length(),
 'last_a_sha256':digest(a),'last_b_sha256':digest(b),'unit_found':False,
 'theorem_square':'If |k| divides a^2+d*b^2 and 2*a*b, then ((a^2+d*b^2)/|k|,2*a*b/|k|) has norm +1.',
 'theorem_pair':'If two states have same signed norm k and k divides both a1*a2-d*b1*b2 and b1*a2-a1*b2, their quotient is an integral norm-one unit.'}
limit=int(sys.argv[2]) if len(sys.argv)>2 else 10000
assert 1<=limit<=10000
rows=[run(spec,limit) for spec in DATA]
if limit==10000:
 assert [int(r['last_norm']) for r in rows]==[28593118985286961,-19593923905788665,34613556081881122]
 assert [r['last_a_bits'] for r in rows]==[24637,24942,24762]
 assert all(r['norms_seen']==10000 and r['repeated_signed_k_states']==0 and r['integral_square_division_units']==0 for r in rows)
assert sum(len(r['canonical_ids']) for r in rows)==16
out={'rqt':637,'title':'Exact norm-composition shortcuts for Chakravala states',
'source_lineage':'RQT-636 deterministic Chakravala states reconstructed from original reduced coefficients',
'groups':rows,'states_audited_total':sum(r['steps_checked'] for r in rows),
'repeated_norm_pairs':sum(r['repeated_signed_k_states'] for r in rows),
'integral_square_shortcuts':sum(r['integral_square_division_units'] for r in rows),
'numerical_units_constructed':0,'new_global_family_exclusions':0,
'selected_excluded':82,'selected_unresolved':53,'canonical_unresolved':27,
'original_22d_wall':'NOT REPLAYED','root19':'OPEN',
'scope':'Theorems are all-integer conditional identities; nonfinding only covers stated deterministic trajectories.'}
dst=Path(sys.argv[1]) if len(sys.argv)>1 else Path('RQT-637-results.json')
dst.write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-637',out['states_audited_total'],'states, no numerical unit')
print('SHA256',hashlib.sha256(dst.read_bytes()).hexdigest())
