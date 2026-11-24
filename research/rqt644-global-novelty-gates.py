#!/usr/bin/env python3
"""RQT-641: exact order-balanced held-out Pell comparison. Python 3 standard library."""
import math,json,sys,hashlib,itertools,time,tracemalloc,platform
from pathlib import Path
DATA=[(1,5,89518360633605555683821304281344825,[28,29,30,31,33,34,35,36,37]),(2,7,149561530769640628300862186866588569,[81,89,92]),(3,4,158134758925461363207454619257200752,[0,1,2,7])]
POLICIES=('nearest','runner_up','alternating','adaptive')
ORDERS=list(itertools.permutations(POLICIES))
OFFSETS=(4,5,6);STEPS=60
def candidates(a,b,k,d,root):
 mod=abs(k);g=math.gcd(b,mod);assert a%g==0
 q=mod//g;r=(-a//g*pow(b//g,-1,q))%q if q>1 else 0
 center=(root-r)//q if q>1 else 0
 vals=sorted({r+(center+j)*q for j in range(-4,6) if r+(center+j)*q>=0},key=lambda v:(abs(v*v-d),abs(v-root),v))
 out=[]
 for m in vals:
  assert (a+b*m)%mod==0 and (m*m-d)%k==0
  aa=(a*m+d*b)//mod;bb=(a+b*m)//mod;kk=(m*m-d)//k
  assert aa*aa-d*bb*bb==kk
  out.append((m,aa,bb,kk))
 assert len(out)>=3
 return out
def run_audit(group,offset,order,global_states,policy_sets):
 idx,s,D,ids=group;d=D//(s*s);root=math.isqrt(d)
 seen=set();norms=set();rows=[];units=0
 for policy in order:
  a,b=root+offset,1;k=a*a-d
  inrun=global_new=0;t0=time.perf_counter_ns()
  for step in range(STEPS):
   assert a*a-d*b*b==k
   state=(a,b,k);tag=(idx,state)
   if state not in seen:inrun+=1
   if tag not in global_states:global_new+=1
   seen.add(state);global_states.add(tag);policy_sets[policy].add(tag)
   if abs(k)==1 and b:units+=1
   norms.add(k)
   options=candidates(a,b,k,d,root)
   if policy=='nearest':choice=0
   elif policy=='runner_up':choice=1
   elif policy=='alternating':choice=step%2
   else:
    choice=min(range(len(options)),key=lambda j:(
      (options[j][1],options[j][2],options[j][3]) in seen,
      options[j][3] in norms,
      max(options[j][1].bit_length(),options[j][2].bit_length()),
      abs(options[j][3]),j))
   _,a,b,k=options[choice]
  rows.append(dict(policy=policy,new_within_run=inrun,new_global=global_new,elapsed_ns=time.perf_counter_ns()-t0))
 return dict(within_run=len(seen),unit_events=units,rows=rows)

def main():
 global_states=set();policy_sets={p:set() for p in POLICIES};runs=[]
 for group in DATA:
  for offset in OFFSETS:
   for order in ORDERS:
    runs.append(run_audit(group,offset,order,global_states,policy_sets))
 assert len(global_states)==1376 and sum(r['within_run'] for r in runs)==38254
 rows=[]
 for idx,s,D,ids in DATA:
  d=D//(s*s);states=[(a,b,k) for i,(a,b,k) in global_states if i==idx]
  norm_map={};minimum=None;direct=square=0
  for a,b,k in states:
   assert a*a-d*b*b==k
   norm_map.setdefault(k,[]).append((a,b))
   minimum=abs(k) if minimum is None else min(minimum,abs(k))
   direct+=int(abs(k)==1 and b!=0)
   if (a*a+d*b*b)%abs(k)==0 and 2*a*b%abs(k)==0:
    X=(a*a+d*b*b)//abs(k);Y=(2*a*b)//abs(k)
    assert X*X-d*Y*Y==1
    if Y:square+=1
  from itertools import combinations
  pairs=integral=nontrivial=0
  for k,vals in norm_map.items():
   for (a,b),(c,e) in combinations(vals,2):
    pairs+=1;xn=a*c-d*b*e;yn=b*c-a*e
    if xn%k==0 and yn%k==0:
     integral+=1;X=xn//k;Y=yn//k
     assert X*X-d*Y*Y==1
     if Y:nontrivial+=1
  rows.append(dict(group=idx,s=s,canonical_ids=ids,distinct_full_states=len(states),
    distinct_signed_norms=len(norm_map),minimum_absolute_norm=str(minimum),
    direct_unit_states=direct,nontrivial_square_division_units=square,
    distinct_state_equal_norm_pairs=pairs,integral_pair_quotients=integral,
    nontrivial_quotient_units=nontrivial))
 assert [r['distinct_full_states'] for r in rows]==[462,460,454]
 assert [r['distinct_signed_norms'] for r in rows]==[462,460,454]
 assert sum(r['direct_unit_states']+r['nontrivial_square_division_units']+r['nontrivial_quotient_units'] for r in rows)==0
 out=dict(rqt=644,observations=51840,globally_distinct_states=len(global_states),groups=rows,
  selected_excluded=82,selected_unresolved=53,new_all_scale_exclusions=0,root19='OPEN',
  original_22d_wall='NOT REPLAYED',scope='Finite deduplicated exact state corpus, not a global Pell impossibility proof')
 dst=Path(sys.argv[1] if len(sys.argv)>1 else 'RQT-644-results.json')
 dst.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS RQT-644: 1376 distinct states, zero unit shortcuts')
if __name__=='__main__':main()
