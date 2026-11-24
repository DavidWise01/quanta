#!/usr/bin/env python3
"""RQT-639: exact alternative transition-policy audit (Python 3 stdlib).
Usage: python rqt639-transition-policies.py [output.json] [steps=120]
"""
import math,json,hashlib,sys
from pathlib import Path
DATA=[(1,5,89518360633605555683821304281344825,[28,29,30,31,33,34,35,36,37]),(2,7,149561530769640628300862186866588569,[81,89,92]),(3,4,158134758925461363207454619257200752,[0,1,2,7])]
POLICIES=('nearest','runner_up','alternating')
def next_state(a,b,k,d,root,policy,n):
 mod=abs(k);g=math.gcd(b,mod);assert a%g==0
 q=mod//g
 r=(-a//g*pow(b//g,-1,q))%q if q>1 else 0
 center=(root-r)//q if q>1 else 0
 opts=sorted({r+(center+j)*q for j in range(-4,6) if r+(center+j)*q>=0},key=lambda x:(abs(x*x-d),abs(x-root),x))
 m=opts[0 if policy=='nearest' else 1 if policy=='runner_up' else n%2]
 assert (a+b*m)%mod==0 and (m*m-d)%k==0
 x=(a*m+d*b)//mod;y=(a+b*m)//mod;z=(m*m-d)//k
 assert x*x-d*y*y==z
 return x,y,z
def run(entry,limit):
 idx,s,D,ids=entry;d=D//(s*s);root=math.isqrt(d);assert root*root!=d
 full={};norms={};records=[];pairs=trivial=nonintegral=0;units=[]
 for pol in POLICIES:
  a=root+1;b=1;k=a*a-d;seen=set()
  for n in range(limit):
   assert a*a-d*b*b==k
   state=(a,b,k);seen.add(state);full.setdefault(state,set()).add(pol)
   for oldpol,olda,oldb in norms.get(k,[]):
    if oldpol==pol:continue
    pairs+=1
    Xnum=a*olda-d*b*oldb;Ynum=b*olda-a*oldb
    if Xnum%k or Ynum%k:nonintegral+=1;continue
    X=Xnum//k;Y=Ynum//k;assert X*X-d*Y*Y==1
    if Y==0:trivial+=1
    else:units.append([pol,oldpol,str(X),str(Y)])
   norms.setdefault(k,[]).append((pol,a,b))
   if abs(k)==1 and b:
    X,Y=(a,b) if k==1 else (a*a+d*b*b,2*a*b)
    assert X*X-d*Y*Y==1
    units.append([pol,'direct',str(X),str(Y)])
   a,b,k=next_state(a,b,k,d,root,pol,n)
  records.append({'policy':pol,'states':limit,'distinct_within_policy':len(seen),'last_k':str(k),'last_a_bits':a.bit_length(),'last_a_sha256':hashlib.sha256(a.to_bytes((a.bit_length()+7)//8 or 1,'big')).hexdigest()})
 return {'group':idx,'s':s,'d':str(d),'canonical_ids':ids,'state_observations':limit*3,
 'distinct_full_states':len(full),'distinct_signed_norms':len(norms),
 'states_seen_by_multiple_policies':sum(len(v)>1 for v in full.values()),
 'cross_policy_matching_norm_comparisons':pairs,'trivial_quotients':trivial,
 'nonintegral_quotients':nonintegral,'nontrivial_units':units,'policy_records':records}
limit=int(sys.argv[2]) if len(sys.argv)>2 else 120
assert 1<=limit<=500
rows=[run(v,limit) for v in DATA]
out={'rqt':639,'policies':list(POLICIES),'steps_per_policy_group':limit,'groups':rows,
'total_observations':sum(x['state_observations'] for x in rows),
'distinct_full_states_total':sum(x['distinct_full_states'] for x in rows),
'cross_policy_comparisons':sum(x['cross_policy_matching_norm_comparisons'] for x in rows),
'trivial_quotients':sum(x['trivial_quotients'] for x in rows),
'nonintegral_quotients':sum(x['nonintegral_quotients'] for x in rows),
'nontrivial_units':sum(len(x['nontrivial_units']) for x in rows),
'selected_excluded':82,'selected_unresolved':53,'new_all_scale_exclusions':0,
'original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
if limit==120:
 assert [r['distinct_full_states'] for r in rows]==[297,298,298]
 assert [r['cross_policy_matching_norm_comparisons'] for r in rows]==[64,63,63]
 assert out['total_observations']==1080 and out['nontrivial_units']==0
dst=Path(sys.argv[1]) if len(sys.argv)>1 else Path('RQT-639-results.json')
dst.write_text(json.dumps(out,indent=2)+'\n')
print('PASS',out['total_observations'],out['distinct_full_states_total'],out['cross_policy_comparisons'])
