#!/usr/bin/env python3
"""RQT-631. Usage: python rqt631.py RQT-630-results.json [OUTPUT.json]"""
from pathlib import Path
from collections import Counter
import json,hashlib,math,sys
p=Path(sys.argv[1]);raw=p.read_bytes();d=json.loads(raw)
assert hashlib.sha256(raw).hexdigest()=='25d228f0176e366deca4fa3401b66789650ad2ef2c0dcb68d054c95a1de83ea6'
assert d['rqt']==630
rows=[]
for group in d['group_results']:
 D=int(group['coefficient_a']);s=int(group['known_square_factor']);a=int(group['reduced_d'])
 assert D==s*s*a and math.isqrt(a)**2!=a
 one=(1%s,0)
 def mult(v,w):
  x,y=v;z,t=w
  return ((x*z+a*y*t)%s,(x*t+y*z)%s)
 elements=[(x,y) for x in range(s) for y in range(s) if (x*x-a*y*y)%s==1%s]
 orders={}
 for v in elements:
  w=one
  for k in range(1,s*s+2):
   w=mult(w,v)
   if w==one:orders[v]=k;break
  else:raise AssertionError('non-unit')
 E=math.lcm(*orders.values()); witness=next((v for v,n in orders.items() if n==E),None) if s>1 else None
 for v in elements:
  w=one
  for _ in range(E):w=mult(w,v)
  assert w==one
 rows.append({'group':group['group'],'s':s,'d':str(a),'d_mod_s':a%s,
 'original_D':str(D),'member_ids':group['canonical_ids'],'norm_one_residue_count':len(elements),
 'universal_exponent':E,'sharp_residue_witness':witness,
 'orders':{str(k):n for k,n in sorted(Counter(orders.values()).items())},
 'elements':[{'x':x,'Y':y,'order':orders[(x,y)]} for x,y in elements]})
assert [r['universal_exponent'] for r in rows]==[6,6,4,1,1]
assert [r['norm_one_residue_count'] for r in rows]==[6,6,8,1,1]
assert sum(len(r['member_ids']) for r in rows)==27
out={'rqt':631,'source_sha256':hashlib.sha256(raw).hexdigest(),'groups':rows,
 'theorem':'U^E is 1 modulo s for every reduced norm-one unit; its root coefficient is divisible by s',
 'numerical_nontrivial_units_found':0,'new_family_exclusions':0,
 'excluded':82,'unresolved':53,'wall22d':'NOT REPLAYED','root19':'OPEN'}
dst=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-631-results.json')
dst.write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-631, sharp universal exponents 6, 6, 4.')
