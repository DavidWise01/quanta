#!/usr/bin/env python3
"""RQT-640 exact novelty-aware vs fixed Chakravala policy comparison.
Python 3 stdlib. Reproduce: python rqt640.py [out.json]
"""
import math,json,hashlib,sys
from pathlib import Path
DATA=[(1,5,89518360633605555683821304281344825,[28,29,30,31,33,34,35,36,37]),(2,7,149561530769640628300862186866588569,[81,89,92]),(3,4,158134758925461363207454619257200752,[0,1,2,7])]
POLICIES=('nearest','runner_up','alternating','adaptive')
def candidates(a,b,k,d,root):
 mod=abs(k);g=math.gcd(b,mod);assert a%g==0
 q=mod//g;r=(-a//g*pow(b//g,-1,q))%q if q>1 else 0
 center=(root-r)//q if q>1 else 0
 options=sorted({r+(center+j)*q for j in range(-4,6) if r+(center+j)*q>=0},key=lambda v:(abs(v*v-d),abs(v-root),v))
 out=[]
 for m in options:
  assert (a+b*m)%mod==0 and (m*m-d)%k==0
  aa=(a*m+d*b)//mod;bb=(a+b*m)//mod;kk=(m*m-d)//k
  assert aa*aa-d*bb*bb==kk
  out.append((m,aa,bb,kk))
 return out
def run(group,limit):
 idx,s,D,ids=group;d=D//s**2;root=math.isqrt(d);seen=set();norms={};rows=[];all_norms={}
 for policy in POLICIES:
  a,b=root+1,1;k=a*a-d
  new=0;choices=[];peak=0;history=[]
  for n in range(limit):
   state=(a,b,k);assert a*a-d*b*b==k
   if state not in seen:new+=1
   seen.add(state);norms.setdefault(k,[]).append((policy,state))
   peak=max(peak,a.bit_length(),b.bit_length())
   options=candidates(a,b,k,d,root)
   if policy=='nearest':selection=0
   elif policy=='runner_up':selection=1
   elif policy=='alternating':selection=n%2
   else:
    selection=min(range(len(options)),key=lambda j:(
     (options[j][1],options[j][2],options[j][3]) in seen,
     options[j][3] in norms,
     max(options[j][1].bit_length(),options[j][2].bit_length()),
     abs(options[j][3]),j))
   m,a,b,k=options[selection];choices.append(selection)
   if n+1 in (1,10,30,60,90,120):history.append(dict(step=n+1,k=str(k),a_bits=a.bit_length(),m_rank=selection))
  rows.append(dict(policy=policy,states=limit,new_global_states=new,peak_coordinate_bits=peak,
   end_a_bits=a.bit_length(),choice_rank_histogram={str(i):choices.count(i) for i in sorted(set(choices))},checkpoints=history))
 pairs=trivial=nontrivial=nonintegral=0
 for k,rec in norms.items():
  for i,(pol1,one) in enumerate(rec):
   for pol2,two in rec[:i]:
    if pol1==pol2:continue
    pairs+=1
    a,b,_=one;c,e,_=two
    X=a*c-d*b*e;Y=b*c-a*e
    if X%k or Y%k:nonintegral+=1;continue
    X//=k;Y//=k
    assert X*X-d*Y*Y==1
    if Y:nontrivial+=1
    else:trivial+=1
 return dict(group=idx,canonical_ids=ids,observations=limit*4,distinct_full_states=len(seen),
  policy_results=rows,matching_norm_pairs=pairs,integral_trivial_quotients=trivial,
  integral_nontrivial_quotients=nontrivial,nonintegral_quotients=nonintegral)
groups=[run(row,120) for row in DATA]
result={'rqt':640,'policies':POLICIES,'steps_per_policy':120,'groups':groups,
 'total_observations':sum(x['observations'] for x in groups),
 'distinct_full_states':sum(x['distinct_full_states'] for x in groups),
 'cross_policy_same_norm_pairs':sum(x['matching_norm_pairs'] for x in groups),
 'nontrivial_units':sum(x['integral_nontrivial_quotients'] for x in groups),
 'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN',
 'original_22d_wall':'NOT REPLAYED','new_all_scale_exclusions':0}
assert result['total_observations']==1440 and result['distinct_full_states']==1250
assert result['cross_policy_same_norm_pairs']==199 and result['nontrivial_units']==0
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path('RQT-640-results.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print('PASS RQT-640:',result['total_observations'],'states,',result['distinct_full_states'],'distinct,',result['nontrivial_units'],'units')
