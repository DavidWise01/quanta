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
 tracemalloc.start();start=time.perf_counter_ns()
 for group in DATA:
  for offset in OFFSETS:
   for order in ORDERS:
    runs.append(run_audit(group,offset,order,global_states,policy_sets))
 elapsed=time.perf_counter_ns()-start
 current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
 assert len(runs)==216 and sum(r['within_run'] for r in runs)==38254
 assert sum(r['unit_events'] for r in runs)==0
 assert set().union(*policy_sets.values())==global_states
 stats={}
 for p in POLICIES:
  vals=[v for r in runs for v in r['rows'] if v['policy']==p]
  stats[p]=dict(standalone_union_states=len(policy_sets[p]),
    within_run_marginal=sum(v['new_within_run'] for v in vals),
    global_new_in_execution_order=sum(v['new_global'] for v in vals),
    elapsed_ns=sum(v['elapsed_ns'] for v in vals))
 assert [stats[p]['within_run_marginal'] for p in POLICIES]==[8134,9612,7710,12798]
 assert len(global_states)==1376
 from itertools import permutations,combinations
 shapley={p:0.0 for p in POLICIES}
 for order in permutations(POLICIES):
  seen=set()
  for p in order:
   shapley[p]+=len(policy_sets[p]-seen)/24
   seen.update(policy_sets[p])
 assert abs(sum(shapley.values())-len(global_states))<0.00001
 out=dict(rqt=643,observations=51840,within_run_distinct_summed=38254,
   globally_distinct_group_scoped_full_states=len(global_states),repeated_observations=51840-len(global_states),
   policies=stats,shapley=shapley,unit_events=0,
   performance=dict(elapsed_ns=elapsed,tracemalloc_peak_bytes=peak,python=platform.python_version(),platform=platform.platform()),
   warnings=['Performance is a single instrumented run, not a portable benchmark.','Shapley attribution uses aggregate policy state unions; adaptive trajectories depend on ledger order.'],
   selected_excluded=82,selected_unresolved=53,root19='OPEN',original_22D_wall='NOT REPLAYED')
 path=Path(sys.argv[1] if len(sys.argv)>1 else 'RQT-643-results.json')
 path.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS RQT-643:',len(global_states),'global states, 0 unit events')
if __name__=='__main__':main()
