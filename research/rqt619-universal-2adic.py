#!/usr/bin/env python3
"""RQT-619: exact regularized all-exponent 2-adic solvability, Python 3.
Usage: python rqt619.py RQT-618-results.json RQT-591-results.json RQT-583-results.json [out.json]
"""
import json,hashlib,sys
from pathlib import Path
from collections import Counter
src=[Path(x) for x in sys.argv[1:4]]
prev,gram,equations=[json.loads(x.read_text()) for x in src]
assert prev['rqt']==618 and gram['rqt']==591 and equations['rqt']==583
assert hashlib.sha256(src[2].read_bytes()).hexdigest()=='5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92'
F=[[int(x) for x in row] for row in gram['reduced_gram']]
byid={e['index']:e for e in equations['equations']}
assert len(prev['two_adic']['canonical_jobs'])==27
def coeff(e):
 r,o=e['ray'],e['offset']
 dot=lambda v,w:sum(v[i]*F[i+1][j+1]*w[j] for i in range(3) for j in range(3))
 return (F[0][0],2*sum(F[0][i+1]*r[i] for i in range(3)),dot(r,r),
         2*sum(F[0][i+1]*o[i] for i in range(3)),2*dot(r,o),dot(o,o)+2)
def value(c,u,t):
 a,b,d,e,f,g=c
 return a*u*u+b*u*t+d*t*t+e*u+f*t+g
def gradient(c,u,t):
 a,b,d,e,f,g=c
 return 2*a*u+b*t+e,b*u+2*d*t+f
result=[]
for job in prev['two_adic']['canonical_jobs']:
 idx=job['canonical_id']
 c=coeff(byid[idx])
 assert all(z%2==0 for z in c)
 r=tuple(v//2 for v in c)
 roots=[(u,t) for u in (0,1) for t in (0,1) if value(r,u,t)%2==0]
 regular=[(u,t) for u,t in roots if any(z%2 for z in gradient(r,u,t))]
 singular=[(u,t) for u,t in roots if not any(z%2 for z in gradient(r,u,t))]
 assert regular
 jets=[]
 for u0,t0 in regular:
  u,t=u0,t0;m=2
  for _ in range(2,16):
   assert value(r,u,t)%m==0
   correction=(value(r,u,t)//m)%2
   gu,gt=gradient(r,u,t)
   if gu%2:u+=correction*m
   else:
    assert gt%2
    t+=correction*m
   m*=2
   assert value(r,u,t)%m==0
  assert value(c,u,t)%(2*m)==0
  jets.append({'initial':[u0,t0],'coordinates_mod_2_power_15':[u,t]})
 counts=job['branch_counts_2_1_to_2_10']
 assert counts[0]==4
 for k in range(2,11):
  assert counts[k-1]>=len(regular)*2**k
 result.append({'canonical_id':idx,'member_ids':job['member_ids'],
  'Q_even_coefficients':True,'R_coefficients_as_strings':list(map(str,r)),
  'roots_R_mod_2':[list(z) for z in roots],
  'regular_roots_R_mod_2':[list(z) for z in regular],
  'singular_roots_R_mod_2':[list(z) for z in singular],
  'root_count_lower_bound':f'C_Q(k) >= {len(regular)} * 2^k (k>=2)',
  'regular_jets':jets,'archived_counts_k1_to_k10':counts})
assert Counter(len(x['regular_roots_R_mod_2']) for x in result)=={2:17,1:10}
assert Counter(len(x['singular_roots_R_mod_2']) for x in result)=={0:14,1:13}
out={'rqt':619,'input_sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in src},
 'canonical_jobs':27,'source_family_ids':53,'all_k_local_solvability':True,
 'normal_form':'Q=2R, R has at least one regular root mod 2 for each orbit',
 'certified_all_k_lower_bound':'For k>=2, C_Q(k)>=r*2^k where r is count of regular R roots mod2',
 'regular_count_distribution':{'one':10,'two':17},'families':result,
 'new_all_scale_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
 'original_22D_wall':'NOT REPLAYED','root19':'OPEN'}
Path(sys.argv[4] if len(sys.argv)>4 else 'RQT-619-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 27 all-exponent 2-adic local solvability theorems; Root19 OPEN')
