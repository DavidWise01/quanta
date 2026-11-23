#!/usr/bin/env python3
"""RQT-633: negative Pell obstruction and even-period certificate.
Usage: python rqt633-period-parity.py RQT-632-results.json [OUT.json]
"""
from pathlib import Path
import json,hashlib,math,sys
p=Path(sys.argv[1]);raw=p.read_bytes();d=json.loads(raw)
assert d['rqt']==632
assert hashlib.sha256(raw).hexdigest()=='0c5cc30a499222457339908b0ff6556f898bd83ce0a7b0e17df2549b70286ed2'
rows=[];steps=100000
for rec in d['group_results']:
    D=int(rec['reduced_d']); s=int(rec['s']);i=int(rec['group'])
    assert math.isqrt(D)**2 != D
    modulus=3 if D%3==0 else 4 if D%4==3 else None
    assert modulus is not None
    roots=[(x,y) for x in range(modulus) for y in range(modulus)
           if (x*x-D*y*y+1)%modulus==0]
    assert not roots
    a0=math.isqrt(D);m=0;den=1;a=a0;period=None
    for n in range(1,steps+1):
        m=den*a-m
        assert (D-m*m)%den==0
        den=(D-m*m)//den
        assert den>0
        a=(a0+m)//den
        if (m,den,a)==(a0,1,2*a0):
            period=n;break
    assert period is None
    rows.append({'group':i,'s':s,'reduced_d':str(D),
        'canonical_ids':rec['canonical_ids'],'negative_unit_obstruction_modulus':modulus,
        'negative_unit_residue_roots':0,'norm_minus_one_globally_impossible':True,
        'period_parity':'even','period_length_strictly_greater_than':steps,
        'prior_convergent_denominator_bits':rec['q_last_bit_length'],
        'fundamental_unit_found':False})
assert len(rows)==3
assert [r['negative_unit_obstruction_modulus'] for r in rows]==[3,3,4]
assert sum(len(r['canonical_ids']) for r in rows)==16
out={'rqt':633,'source_RQT632_SHA256':hashlib.sha256(raw).hexdigest(),
     'period_states_per_group':steps,'period_states_total':3*steps,
     'negative_Pell_equations_proved_impossible':3,
     'periods_proved_even':3,'periods_computed':0,'norm_plus_one_units_found':0,
     'new_family_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
     'root19':'OPEN','original_22d_wall':'NOT REPLAYED','groups':rows}
dst=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-633-results.json')
dst.write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 3 global norm-minus-one obstructions; even periods > 100000')
