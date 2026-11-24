#!/usr/bin/env python3
"""RQT-641: exact order-balanced held-out Pell comparison. Python 3 standard library."""
import math,json,sys,hashlib,itertools
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
def run(group,offset,order):
 idx,s,D,ids=group;d=D//(s*s);root=math.isqrt(d)
 seen=set();norms=set();rows=[];nunits=0;costsum=0
 for policy in order:
  a,b=root+offset,1;k=(root+offset)**2-d
  new=0;cost=0;peak=0;ranking={}
  for t in range(STEPS):
   assert a*a-d*b*b==k
   v=(a,b,k)
   if v not in seen:new+=1
   seen.add(v)
   if abs(k)==1 and b:nunits+=1
   norms.add(k)
   options=candidates(a,b,k,d,root)
   cost+=sum(a.bit_length()+b.bit_length()+abs(k).bit_length()+m.bit_length() for m,_,_,_ in options)
   peak=max(peak,a.bit_length(),b.bit_length())
   if policy=='nearest':choice=0
   elif policy=='runner_up':choice=1
   elif policy=='alternating':choice=t%2
   else:
    choice=min(range(len(options)),key=lambda j:((options[j][1],options[j][2],options[j][3]) in seen,
     options[j][3] in norms,max(options[j][1].bit_length(),options[j][2].bit_length()),abs(options[j][3]),j))
   ranking[choice]=ranking.get(choice,0)+1
   _,a,b,k=options[choice]
  costsum+=cost
  rows.append({'policy':policy,'new_states':new,'proxy_bit_work':cost,'new_states_per_1000_proxy_bit_work':round(new*1000/cost,6),'end_a_bits':a.bit_length(),'peak_bits':peak,'selection_rank_counts':ranking})
 return {'group':idx,'offset':offset,'order':list(order),'rows':rows,'distinct_full_states':len(seen),'state_observations':4*STEPS,'unit_events':nunits,'total_proxy_bit_work':costsum}
result=[run(group,offset,order) for group in DATA for offset in OFFSETS for order in ORDERS]
aggregates={}
for policy in POLICIES:
 rs=[r for e in result for r in e['rows'] if r['policy']==policy]
 aggregates[policy]={'policy':policy,'executions':len(rs),'ordered_new_states':sum(x['new_states'] for x in rs),'proxy_bit_work':sum(x['proxy_bit_work'] for x in rs),'new_states_per_1000_proxy_bit_work':round(1000*sum(x['new_states'] for x in rs)/sum(x['proxy_bit_work'] for x in rs),6),'mean_end_a_bits':round(sum(x['end_a_bits'] for x in rs)/len(rs),3),'first_position_new_states':sum(e['rows'][0]['new_states'] for e in result if e['rows'][0]['policy']==policy)}
out={'rqt':642,'design':'3 coefficients x 3 held-out offsets x 4 cyclic orders x 4 policies x 60 steps','steps_per_policy':STEPS,'held_out_offsets':OFFSETS,'policy_orders':[list(x) for x in ORDERS],'runs':result,'policy_aggregates':aggregates,'total_state_observations':sum(x['state_observations'] for x in result),'total_distinct_within_run':sum(x['distinct_full_states'] for x in result),'unit_events':sum(x['unit_events'] for x in result),'selected_excluded':82,'selected_unresolved':53,'new_all_scale_exclusions':0,'original_22d_wall':'NOT REPLAYED','root19':'OPEN','method_warning':'All 24 orders are balanced at each position, but adaptive is ledger-dependent; proxy work is not runtime; distinct states are summed within independent runs.'}
assert out['total_state_observations']==51840 and out['total_distinct_within_run']==38254 and out['unit_events']==0
assert [aggregates[p]['ordered_new_states'] for p in POLICIES]==[8134,9612,7710,12798]
path=Path(sys.argv[1] if len(sys.argv)>1 else 'RQT-642-results.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-642',out['total_state_observations'],out['total_distinct_within_run'],out['unit_events'])
print(hashlib.sha256(path.read_bytes()).hexdigest())
