#!/usr/bin/env python3
"""RQT-621 exact third-level singular branch verification.
python rqt621-third-level.py RQT-620-results.json [RQT-621-results.json]
"""
import json,hashlib,sys
from pathlib import Path
p=Path(sys.argv[1]);raw=p.read_bytes();src=json.loads(raw)
assert hashlib.sha256(raw).hexdigest()=='c23027155b581a22983649642141ba95d0a00c081ece6c8b1215443a2f97b7b3'
assert src['rqt']==620
def val(c,u,t):
 a,b,d,e,f,g=c
 return a*u*u+b*u*t+d*t*t+e*u+f*t+g
def grad(c,u,t):
 a,b,d,e,f,g=c
 return 2*a*u+b*t+e,b*u+2*d*t+f
def regular(c,u,t):return any(x%2 for x in grad(c,u,t))
cases=[]
for rec in src['cases']:
 if not rec['S_singular_roots_mod2']:continue
 i=rec['canonical_id'];c=list(map(int,rec['S_coefficients_exact']))
 assert len(rec['S_singular_roots_mod2'])==1
 u0,t0=rec['S_singular_roots_mod2'][0]
 q=val(c,u0,t0);gu,gt=grad(c,u0,t0)
 assert q%2==gu%2==gt%2==0
 row={'canonical_id':i,'member_ids':rec['member_ids'],'singular_S_root':[u0,t0],'S_value_mod4':q%4}
 if q%4==2:
  assert all(val(c,u0+2*x,t0+2*y)%4==2 for x in (0,1) for y in (0,1))
  row['status']='BLOCKED_FIXED_BRANCH'
 else:
  assert q%4==0
  T=[c[0],c[1],c[2],gu//2,gt//2,q//4]
  for x,y in ((0,0),(-3,5),(2,9)):
   assert val(c,u0+2*x,t0+2*y)==4*val(T,x,y)
  roots=[(x,y) for x in (0,1) for y in (0,1) if val(T,x,y)%2==0]
  good=[z for z in roots if regular(T,*z)]
  deep=[z for z in roots if not regular(T,*z)]
  assert good
  jets=[]
  for x0,y0 in good:
   x,y=x0,y0;m=2
   for _ in range(2,14):
    h=(val(T,x,y)//m)%2;gx,gy=grad(T,x,y)
    if gx%2:x+=h*m
    else:
     assert gy%2;y+=h*m
    m*=2;assert val(T,x,y)%m==0
   assert val(c,u0+2*x,t0+2*y)%(4*m)==0
   jets.append({'initial':[x0,y0],'coordinates':[x,y]})
  weight=2+len(rec['S_regular_roots_mod2'])+len(good)
  for k in range(6,11):
   assert rec['archived_counts_k1_to_k10'][k-1]>=weight*2**k
  row.update(status='THIRD_NORMAL_FORM',T_coefficients=list(map(str,T)),
    T_regular_mod2=good,T_singular_mod2=deep,Hensel_jets=jets,
    certified_bound=f'C_Q(k)>={weight}*2^k for k>=6')
 cases.append(row)
assert sorted(x['canonical_id'] for x in cases)==[29,30,56,62,81,92]
assert sorted(x['canonical_id'] for x in cases if x['status']=='THIRD_NORMAL_FORM')==[29,30]
assert sum(x['status']=='BLOCKED_FIXED_BRANCH' for x in cases)==4
assert [len(x['T_regular_mod2']) for x in cases if x['status']=='THIRD_NORMAL_FORM']==[2,1]
assert sum(len(x['T_singular_mod2']) for x in cases if x['status']=='THIRD_NORMAL_FORM')==1
out={'rqt':621,'source_sha256':hashlib.sha256(raw).hexdigest(),'cases':cases,
 'new_all_scale_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
 'original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-621-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-621: four blocked branches, two third forms, one deeper singular root')
