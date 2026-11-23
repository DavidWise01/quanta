#!/usr/bin/env python3
"""RQT-630: known-square-factor reductions, exact Pell recovery gates.
Python 3 standard library; no complete factorization is claimed.
"""
import json, math, hashlib, sys
from pathlib import Path
D=[89518360633605555683821304281344825,149561530769640628300862186866588569,158134758925461363207454619257200752,865181362726903603566834179921037649,1957113882671124377864756294075131977]
S=[5,7,4,1,1]
orbits=[[28,29,30,31,33,34,35,36,37],[81,89,92],[0,1,2,7],[55,56,57,61,62,64,65,67],[109,110,112]]
rows=[]
for i,(a,s,ids) in enumerate(zip(D,S,orbits),1):
 assert a%(s*s)==0
 d=a//(s*s)
 assert math.isqrt(d)**2!=d
 for x,y in ((0,0),(1,0),(7,9),(-11,12)):
  assert x*x-a*y*y==x*x-d*(s*y)**2
 rows.append(dict(group=i,coefficient_a=str(a),known_square_factor=s,known_square_divisor=s*s,reduced_d=str(d),canonical_ids=ids,
 original_unit_equation=f'x^2-{a}y^2=1',reduced_unit_equation=f'x^2-{d}Y^2=1',
 recovery_gate=f'Y % {s} == 0',maximal_squarefree_reduction_verified=False,positive_unit_found=False))
assert len(rows)==5 and sum(len(r['canonical_ids']) for r in rows)==27
assert sum(r['known_square_factor']>1 for r in rows)==3
out={'rqt':630,'method':'exact known square-divisor extraction only (not complete factorization)',
'source':'RQT-626 group coefficients and RQT-629 period bounds',
'group_results':rows,'nontrivial_square_reductions':3,
'recovery_theorem':'If D=s²d, original norm-one units correspond exactly to reduced norm-one units with Y ≡ 0 mod s, via Y=s*y.',
'existence_transfer':'For any reduced norm-one unit, a positive power has Y divisible by s, by finite multiplicative reduction mod s; no explicit unit was constructed.',
'fundamental_units_found':0,'generalized_pell_seeds_found':0,'new_whole_family_exclusions':0,
'selected_excluded':82,'selected_unresolved':53,'wall22d':'NOT REPLAYED','root19':'OPEN'}
dst=Path(sys.argv[1]) if len(sys.argv)>1 else Path('RQT-630-results.json')
dst.write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-630: three exact square reductions, 27 orbits; root19 OPEN')
