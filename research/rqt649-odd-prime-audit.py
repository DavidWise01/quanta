#!/usr/bin/env python3
"""RQT-649: odd-prime local root audit; exact integer and finite-field arithmetic.
Usage: python rqt649-odd-prime-audit.py RQT-619-results.json [output.json]
"""
import json,hashlib,sys
from pathlib import Path
src=Path(sys.argv[1]);data=json.loads(src.read_text())
assert data['rqt']==619 and len(data['families'])==27
assert hashlib.sha256(src.read_bytes()).hexdigest()=='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
PRIMES=[3,5,7,11,13,17,19,23,29,31,37,41,43]
records=[]
for row in data['families']:
 A,B,C,D,E,F=map(int,row['R_coefficients_as_strings'])
 def G(u,t):return A*u*u+B*u*t+C*t*t+D*u+E*t+F
 def Du(u,t):return 2*A*u+B*t+D
 def Dt(u,t):return B*u+2*C*t+E
 prime_rows=[]
 for p in PRIMES:
  roots=[];regular=[]
  for t in range(p):
   for u in range(p):
    if G(u,t)%p==0:
     roots.append((u,t))
     if Du(u,t)%p or Dt(u,t)%p:regular.append((u,t))
  lifted=None
  if regular:
   u,t=regular[0];var='u' if Du(u,t)%p else 't'
   for k in range(1,7):
    assert G(u,t)%(p**k)==0
    if k==6:break
    partial=(Du(u,t) if var=='u' else Dt(u,t))%p
    digit=(-(G(u,t)//p**k)*pow(partial,-1,p))%p
    if var=='u':u+=digit*p**k
    else:t+=digit*p**k
   lifted={'u':str(u),'t':str(t),'variable_lifted':var,'verified_modulus':str(p**6)}
  exceptional_lifts=None
  if not regular and roots:
   exceptional_lifts=sum(G(u+p*i,t+p*j)%(p*p)==0 for u,t in roots for i in range(p) for j in range(p))
  prime_rows.append({'prime':p,'mod_p_roots':len(roots),'nonsingular_mod_p_roots':len(regular),
   'nonsingular_witness':list(regular[0]) if regular else None,'lift_to_p6':lifted,
   'singular_lifts_mod_p2':exceptional_lifts})
 records.append({'canonical_id':row['canonical_id'],'member_ids':row['member_ids'],'primes':prime_rows})
summary=[]
for i,p in enumerate(PRIMES):
 row=[r['primes'][i] for r in records]
 summary.append({'prime':p,'orbits_with_any_root':sum(v['mod_p_roots']>0 for v in row),
  'orbits_with_nonsingular_root':sum(v['nonsingular_mod_p_roots']>0 for v in row),
  'total_mod_p_roots':sum(v['mod_p_roots'] for v in row),
  'total_nonsingular_roots':sum(v['nonsingular_mod_p_roots'] for v in row)})
exceptions=[{'canonical_id':r['canonical_id'],'prime':v['prime'],'mod_p2_lifts':v['singular_lifts_mod_p2']}
 for r in records for v in r['primes'] if not v['nonsingular_mod_p_roots']]
assert [(x['canonical_id'],x['prime'],x['mod_p2_lifts']) for x in exceptions]==[(2,7,49),(28,31,961)]
assert sum(x['orbits_with_nonsingular_root'] for x in summary)==349
assert sum(x['orbits_with_any_root'] for x in summary)==351
out={'rqt':649,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'primes':PRIMES,'aggregate':summary,'orbits':records,'singular_exceptions':exceptions,
 'new_all_scale_family_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
 'root19':'OPEN','original_22d_wall':'NOT REPLAYED',
 'scope':'Nonsingular mod p roots prove local Z_p solvability for listed primes only; singular cases verified only to p^2.'}
dest=Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-649-results.json')
dest.write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-649: 351 finite field tests, 349 nonsingular, 2 singular cases with p² lifts')
