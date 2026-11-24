#!/usr/bin/env python3
"""RQT-646 exact higher precision Pell and integer-coordinate recovery.
Usage: python rqt646.py RQT-619-results.json RQT-626-results.json [output.json].
"""
import json,hashlib,math,sys
from pathlib import Path
rp=Path(sys.argv[1]);pp=Path(sys.argv[2])
dest=Path(sys.argv[3]) if len(sys.argv)>3 else Path('RQT-646-results.json')
R=json.loads(rp.read_text());P=json.loads(pp.read_text())
assert R['rqt']==619 and P['rqt']==626
assert hashlib.sha256(rp.read_bytes()).hexdigest()=='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
assert hashlib.sha256(pp.read_bytes()).hexdigest()=='1d901288a9a6007f79496615ef421bd0c6aa147aab1ecc33355e5ef71d4c1052'
byid={r['canonical_id']:r for r in P['records']}
moduli=[16,32,64,128,256];records=[]
for r in R['families']:
 idx=r['canonical_id'];p=byid[idx]
 r0,r1,r2,r3,r4,r5=map(int,r['R_coefficients_as_strings'])
 a=int(p['pell_a']);h=int(p['pell_h'])
 c=int(p['primitive_discriminant_coefficients'][2]);N=int(p['pell_N'])
 assert (a,h,c,N)==(r1*r1-4*r0*r2,r1*r3-2*r0*r4,r3*r3-4*r0*r5,h*h-a*c)
 D=abs(2*r0);out=[]
 for m in moduli:
  g=math.gcd(m,D);roots=[[] for _ in range(m)]
  for y in range(m):roots[y*y%m].append(y)
  pell_params=[];recovered_params=[];pell_pairs=recovery_pairs=0
  for t in range(m):
   L=r1*t+r3;F=(a*t*t+2*h*t+c)%m
   poss=roots[F]
   chosen=[y for y in poss if (y-L)%g==0 or (y+L)%g==0]
   pell_pairs+=len(poss);recovery_pairs+=len(chosen)
   if poss:pell_params.append(t)
   if chosen:recovered_params.append(t)
  out.append({'modulus':m,'gcd_coordinate_denominator':g,'pell_pairs':pell_pairs,
   'coordinate_pairs':recovery_pairs,'pell_t_count':len(pell_params),
   'coordinate_t_count':len(recovered_params),'pell_t':pell_params,
   'coordinate_t':recovered_params,'rejected_t':sorted(set(pell_params)-set(recovered_params))})
 records.append({'canonical_id':idx,'members':r['member_ids'],
  'coordinate_denominator':str(D),'moduli':out})
assert len(records)==27
aggregate=[{'modulus':m,'pell_pairs':sum(v['moduli'][i]['pell_pairs'] for v in records),
'coordinate_pairs':sum(v['moduli'][i]['coordinate_pairs'] for v in records),
'pell_t':sum(v['moduli'][i]['pell_t_count'] for v in records),
'coordinate_t':sum(v['moduli'][i]['coordinate_t_count'] for v in records)}
 for i,m in enumerate(moduli)]
assert [(r['pell_t'],r['coordinate_t']) for r in aggregate]==[(432,432),(784,704),(1488,1408),(2824,2704),(5328,5168)]
for r in records:
 for j in range(len(moduli)-1):
  n=moduli[j];new=set(r['moduli'][j+1]['coordinate_t'])
  old=set(r['moduli'][j]['coordinate_t'])
  assert {t%n for t in new}.issubset(old)
assert [r['canonical_id'] for r in records if r['moduli'][-1]['rejected_t']]==[28,31,34,37,55,61,64,67,109,112]
result={'rqt':646,'source_sha256':{'rqt619':hashlib.sha256(rp.read_bytes()).hexdigest(),'rqt626':hashlib.sha256(pp.read_bytes()).hexdigest()},'moduli':moduli,
'aggregate':aggregate,'families':records,'new_full_family_exclusions':0,
'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN','original_22d_wall':'NOT REPLAYED',
'scope':'Exact finite necessary congruences; surviving classes do not prove integer roots.'}
dest.write_text(json.dumps(result,indent=2)+'\n')
print('PASS RQT-646: 27 canonical orbits, mod-256 5328 to 5168.')
