#!/usr/bin/env python3
"""RQT-627 exact Pell-unit congruence stabilizers.
Usage: python rqt627-pell-unit-gates.py RQT-626-results.json [out.json]
"""
import sys,json,hashlib,math
from pathlib import Path
from collections import defaultdict
p=Path(sys.argv[1]);raw=p.read_bytes();d=json.loads(raw)
assert d['rqt']==626 and hashlib.sha256(raw).hexdigest()=='1d901288a9a6007f79496615ef421bd0c6aa147aab1ecc33355e5ef71d4c1052'
groups=defaultdict(list);mods=set();rows=[]
for r in d['records']:
 a,h,N=map(int,(r['pell_a'],r['pell_h'],r['pell_N']))
 A,B,C=map(int,r['primitive_discriminant_coefficients'])
 assert A==a and B==2*h and h*h-a*C==N
 assert a>0 and math.isqrt(a)**2!=a
 g=math.gcd(a,h);m=a//g
 # A norm-one unit satisfies x^2 ≡ 1 mod a.
 # For z ≡ h mod a, one step gives z' ≡ xh mod a.
 # Thus even powers always return to h; odd powers iff m divides x-1.
 for t in (-11,-1,0,1,13):
  z=a*t+h;y2=a*t*t+2*h*t+C
  assert z*z-a*y2==N and z%a==h%a
 assert (((-1-1)*h)%a==0)==(m<=2)
 groups[a].append(r['canonical_id']);mods.add(m)
 rows.append({'canonical_id':r['canonical_id'],'member_ids':r['member_ids'],
 'pell_a':str(a),'pell_h':str(h),'pell_N':str(N),
 'gcd_a_h':str(g),'odd_step_stabilizer_modulus':str(m),
 'even_unit_power':'always preserves z ≡ h mod a',
 'odd_unit_power':'preserves iff x ≡ 1 mod a/gcd(a,h)'})
assert len(rows)==27 and len(groups)==5 and len(mods)==10
assert [v['canonical_id'] for v in rows if v['odd_step_stabilizer_modulus']=='1']==[67]
# Explicit norm-one test for a small nonsquare reference coefficient.
a,x,w=2,3,2
assert x*x-a*w*w==1
for z,y in ((1,0),(3,4),(-7,9)):
 Z=x*z+a*w*y;Y=w*z+x*y
 assert Z*Z-a*Y*Y==z*z-a*y*y
 ZZ=x*Z+a*w*Y
 assert ZZ%a==z%a
out={'rqt':627,'source_sha256':hashlib.sha256(raw).hexdigest(),
 'canonical_orbits':27,'original_family_ids':53,'leading_coefficient_groups':5,
 'distinct_odd_step_stabilizer_moduli':10,'unconditional_odd_step_canonical_ids':[67],
 'even_step_rule':'all even powers preserve seed congruence',
 'odd_step_rule':'(x-1)h divisible by a',
 'records':rows,'computed_fundamental_units':0,'computed_generalized_pell_seeds':0,
 'new_all_scale_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
 'original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-627-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-627: 27 orbit actions, 10 stabilizers, no seeds claimed')
