#!/usr/bin/env python3
"""RQT-620: independently verify all 13 second-level singular 2-adic forms.
Usage: python rqt620.py RQT-619-results.json [RQT-620-results.json]
"""
import sys,json,hashlib
from pathlib import Path
from collections import Counter
P=Path(sys.argv[1]);source=json.loads(P.read_text());assert source['rqt']==619
assert hashlib.sha256(P.read_bytes()).hexdigest()=='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
def q(c,u,t):
 a,b,d,e,f,g=c
 return a*u*u+b*u*t+d*t*t+e*u+f*t+g
def gradient(c,u,t):
 a,b,d,e,f,g=c
 return 2*a*u+b*t+e,b*u+2*d*t+f
cases=[]
for rec in source['families']:
 old=rec['singular_roots_R_mod_2']
 if not old:continue
 assert len(old)==1
 c=list(map(int,rec['R_coefficients_as_strings']));u0,t0=old[0]
 gu,gt=gradient(c,u0,t0);z=q(c,u0,t0)
 assert z%4==gu%2==gt%2==0
 S=[c[0],c[1],c[2],gu//2,gt//2,z//4]
 for x,y in ((0,0),(1,2),(-7,11)):
  assert q(c,u0+2*x,t0+2*y)==4*q(S,x,y)
 roots=[(x,y) for x in range(2) for y in range(2) if q(S,x,y)%2==0]
 regular=[(x,y) for x,y in roots if any(z%2 for z in gradient(S,x,y))]
 singular=[(x,y) for x,y in roots if not any(z%2 for z in gradient(S,x,y))]
 assert len(regular) in (1,2) and len(rec['regular_roots_R_mod_2'])==2
 jets=[]
 for x0,y0 in regular:
  x,y=x0,y0;m=2
  for k in range(2,14):
   h=(q(S,x,y)//m)%2;gx,gy=gradient(S,x,y)
   if gx%2:x+=h*m
   else:
    assert gy%2;y+=h*m
   m*=2;assert q(S,x,y)%m==0
  assert q(c,u0+2*x,t0+2*y)%(4*m)==0
  jets.append({'root':[x0,y0],'x':x,'y':y})
 for k in range(4,11):
  assert rec['archived_counts_k1_to_k10'][k-1]>=(2+len(regular))*2**k
 cases.append({'canonical_id':rec['canonical_id'],'member_ids':rec['member_ids'],
  'R_singular_mod2':[u0,t0],'S_coefficients_exact':list(map(str,S)),
  'S_regular_mod2':[list(v) for v in regular],
  'S_singular_mod2':[list(v) for v in singular],
  'Hensel_jets':jets,'archived_counts':rec['archived_counts_k1_to_k10'],
  'lower_bound':f'C_Q(k)>={2+len(regular)}*2^k for k>=4'})
assert len(cases)==13
assert Counter(len(c['S_regular_mod2']) for c in cases)=={1:7,2:6}
assert sum(len(c['S_singular_mod2']) for c in cases)==6
out={'rqt':620,'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),
 'cases':cases,'second_level_forms':13,'one_regular':7,'two_regular':6,
 'deeper_singular':6,'new_exclusions':0,'selected_excluded':82,
 'selected_unresolved':53,'original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-620-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS 13 second forms; 20 regular Hensel jets; six deeper singular branches; Root19 OPEN')
