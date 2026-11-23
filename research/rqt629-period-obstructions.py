#!/usr/bin/env python3
"""RQT-629: exact sqrt(D) CF period lower bounds and negative Pell obstructions.
Usage: python rqt629-period-obstructions.py RQT-628-results.json [OUTPUT.json] [STEPS]
"""
import json,hashlib,math,sys
from pathlib import Path
p=Path(sys.argv[1]);raw=p.read_bytes();d=json.loads(raw)
assert d['rqt']==628 and hashlib.sha256(raw).hexdigest()=='f83082dd9e106a9e1bad0c43eac2d8a4608650b1a658c98fa69cd8e2c4f49b83'
steps=int(sys.argv[3]) if len(sys.argv)>3 else 1000000
assert steps>=10000
rows=[]
for i,r in enumerate(d['five_a_units'],1):
 D=int(r['a']);a0=math.isqrt(D);assert a0*a0!=D
 m,den,a=0,1,a0
 period=None
 for k in range(1,steps+1):
  m=den*a-m
  assert (D-m*m)%den==0
  den=(D-m*m)//den;assert den>0
  a=(a0+m)//den
  if (m,den,a)==(a0,1,2*a0):
   period=k;break
 obs='mod3' if D%3==0 else 'mod4' if D%4==0 else None
 rows.append({'group':i,'a':str(D),'canonical_ids':r['family_ids'],
 'period_steps_checked':k,'completed_period':period,
 'period_length_greater_than':steps if period is None else None,
 'norm_minus_one_impossible_for_all_integers':bool(obs),
 'obstruction':obs,
 'prior_q9999_bits':r['last_denominator_bit_length']})
assert len(rows)==5 and all(r['completed_period'] is None for r in rows)
assert [r['obstruction'] for r in rows]==['mod3','mod3','mod4',None,'mod3']
out={'rqt':629,'source_628_sha256':hashlib.sha256(raw).hexdigest(),
 'period_states_checked_per_group':steps,'group_results':rows,
 'negative_unit_groups_globally_obstructed':4,
 'positive_norm_one_units_found':0,'generalized_pell_seeds_found':0,
 'new_all_scale_family_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
 'original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
dst=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-629-results.json')
dst.write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-629: five periods >',steps,'four global norm-negative-one obstructions')
