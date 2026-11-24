#!/usr/bin/env python3
"""RQT-638: cross-trajectory exact Chakravala norm comparison.
Usage: python rqt638-cross-trajectory.py [output.json] [steps_per_trajectory=600].
"""
import json,math,hashlib,sys
from pathlib import Path
DATA=[(1,5,3,89518360633605555683821304281344825,[28,29,30,31,33,34,35,36,37]),(2,7,3,149561530769640628300862186866588569,[81,89,92]),(3,4,2,158134758925461363207454619257200752,[0,1,2,7])]
START_OFFSETS=(1,2,3)
def product(u,v,d):
 a,b=u;c,e=v
 return a*c+d*b*e,a*e+b*c
def powpair(v,e,d):
 out=(1,0)
 while e:
  if e&1:out=product(out,v,d)
  v=product(v,v,d);e//=2
 return out
def step(a,b,k,d,root):
 mod=abs(k);g=math.gcd(b,mod)
 assert a%g==0
 q=mod//g
 residue=(-a//g*pow(b//g,-1,q))%q if q>1 else 0
 center=(root-residue)//q if q>1 else 0
 choices=[residue+(center+j)*q for j in (-2,-1,0,1,2,3)]
 m=min((v for v in choices if v>=0),key=lambda v:(abs(v*v-d),abs(v-root)))
 assert (a+b*m)%mod==0 and (m*m-d)%k==0
 aa=(a*m+d*b)//mod;bb=(a+b*m)//mod;kk=(m*m-d)//k
 assert aa*aa-d*bb*bb==kk
 return aa,bb,kk
def run(spec,limit):
 idx,s,E,D,ids=spec
 assert D%(s*s)==0
 d=D//(s*s);root=math.isqrt(d);assert root*root!=d
 states={};collisions=checks=trivial=0;units=[]
 starts=[];end=[];total=0
 for offset in START_OFFSETS:
  a=root+offset;b=1;k=a*a-d
  starts.append({'offset':offset,'initial_k':str(k)})
  for n in range(limit):
   assert a*a-d*b*b==k
   total+=1
   for oa,ob,oo,on in states.get(k,[]):
    if oo==offset:continue
    collisions+=1
    xx=a*oa-d*b*ob;yy=b*oa-a*ob
    checks+=1
    if xx%k==0 and yy%k==0:
     X,Y=xx//k,yy//k
     assert X*X-d*Y*Y==1
     if Y==0:trivial+=1
     else:
      XX,YY=powpair((X,Y),E,d)
      assert YY%s==0 and XX*XX-D*(YY//s)**2==1
      units.append({'X':str(X),'Y':str(Y),'X_original':str(XX),'y_original':str(YY//s)})
   states.setdefault(k,[]).append((a,b,offset,n))
   if abs(k)==1:
    X,Y=(a,b) if k==1 else product((a,b),(a,b),d)
    assert X*X-d*Y*Y==1
    if Y:units.append({'direct':True,'X':str(X),'Y':str(Y)})
   a,b,k=step(a,b,k,d,root)
  end.append({'offset':offset,'last_k':str(k),'last_a_bits':a.bit_length()})
 return {'group':idx,'s':s,'E':E,'d':str(d),'original_D':str(D),
  'canonical_ids':ids,'trajectories':len(START_OFFSETS),
  'steps_per_trajectory':limit,'total_states':total,
  'starts':starts,'end_states':end,'distinct_signed_k':len(states),
  'cross_trajectory_matching_norm_pairs':collisions,
  'integrality_checks':checks,'trivial_quotients':trivial,
  'constructed_nontrivial_units':units}
limit=int(sys.argv[2]) if len(sys.argv)>2 else 600
assert 1<=limit<=2000
rows=[run(x,limit) for x in DATA]
result={'rqt':638,'algorithm':'separate exact Chakravala starts root+1, root+2, root+3',
 'groups':rows,'total_states':sum(x['total_states'] for x in rows),
 'cross_trajectory_matches':sum(x['cross_trajectory_matching_norm_pairs'] for x in rows),
 'integral_quotient_checks':sum(x['integrality_checks'] for x in rows),
 'nontrivial_units_constructed':sum(len(x['constructed_nontrivial_units']) for x in rows),
 'selected_excluded':82,'selected_unresolved':53,'new_all_scale_exclusions':0,
 'root19':'OPEN','original_22d_wall':'NOT REPLAYED',
 'scope':'Finite multistart search, not proof of unit nonexistence'}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'RQT-638-results.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print('PASS RQT-638:',result['total_states'],'states,',
result['cross_trajectory_matches'],'cross-path matches,',
result['nontrivial_units_constructed'],'nontrivial units')
