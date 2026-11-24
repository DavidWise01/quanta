#!/usr/bin/env python3
"""RQT-636: exact Chakravala unit construction, no external packages.
Usage: python rqt636-chakravala.py [output.json] [steps=10000]
"""
import math,hashlib,json,sys
from pathlib import Path
DATA=[
 (1,5,3,89518360633605555683821304281344825,[3,13,1693],[28,29,30,31,33,34,35,36,37]),
 (2,7,3,149561530769640628300862186866588569,[3],[81,89,92]),
 (3,4,2,158134758925461363207454619257200752,[12097,87083],[0,1,2,7])]
def fingerprint(a):
 return hashlib.sha256(a.to_bytes((a.bit_length()+7)//8 or 1,'big')).hexdigest()
def multiply(u,v,d):
 a,b=u;c,e=v
 return a*c+d*b*e,a*e+b*c
def power(u,n,d):
 result=(1,0)
 while n:
  if n&1:result=multiply(result,u,d)
  u=multiply(u,u,d);n//=2
 return result
def run(spec,limit):
 index,s,E,D,primes,ids=spec
 assert D%(s*s)==0
 d=D//(s*s);root=math.isqrt(d);assert root*root<d
 a=root+1;b=1;k=a*a-d
 checkpoints=[];unit=None
 for step in range(limit):
  assert a*a-d*b*b==k
  if abs(k)==1:
   unit=(a,b) if k==1 else multiply((a,b),(a,b),d)
   assert unit[0]**2-d*unit[1]**2==1
   break
  mod=abs(k);g=math.gcd(b,mod);assert a%g==0
  q=mod//g
  residue=(-a//g*pow(b//g,-1,q))%q if q>1 else 0
  center=(root-residue)//q if q>1 else 0
  values=[residue+(center+j)*q for j in (-2,-1,0,1,2,3)]
  m=min((v for v in values if v>=0),key=lambda v:(abs(v*v-d),abs(v-root)))
  assert (a+b*m)%mod==0 and (m*m-d)%k==0
  aa=(a*m+d*b)//mod;bb=(a+b*m)//mod;kk=(m*m-d)//k
  assert aa*aa-d*bb*bb==kk
  a,b,k=aa,bb,kk
  if step+1 in (1,2,3,10,100,1000,5000,10000):
   checkpoints.append({'steps':step+1,'k':str(k),'a_bits':a.bit_length(),
    'b_bits':b.bit_length(),'a_sha256':fingerprint(a),'b_sha256':fingerprint(b)})
 row={'group':index,'s':s,'recovery_power':E,'D':str(D),'d':str(d),
  'canonical_ids':ids,'known_prime_support':primes,'steps_completed':step+1,
  'last_k':str(k),'last_a_bits':a.bit_length(),'last_b_bits':b.bit_length(),
  'last_a_sha256':fingerprint(a),'last_b_sha256':fingerprint(b),
  'checkpoints':checkpoints,'reduced_unit_found':bool(unit)}
 if unit:
  x,Y=unit;assert Y and x*x-d*Y*Y==1
  X,YY=power(unit,E,d);assert YY%s==0
  y=YY//s;assert X*X-D*y*y==1
  row['verified_original_unit']={'X':str(X),'y':str(y)}
 return row
limit=int(sys.argv[2]) if len(sys.argv)>2 else 10000
assert 1<=limit<=50000
rows=[run(v,limit) for v in DATA]
result={'rqt':636,'algorithm':'deterministic exact nearest-square Chakravala',
'steps_budget_per_group':limit,'groups':rows,'total_steps':sum(v['steps_completed'] for v in rows),
'verified_reduced_units':sum(v['reduced_unit_found'] for v in rows),
'new_all_scale_family_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
'original_22D_wall':'NOT REPLAYED','root19':'OPEN'}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'RQT-636-results.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print('PASS',result['total_steps'],'steps; units:',result['verified_reduced_units'])
