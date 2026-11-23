#!/usr/bin/env python3
"""RQT-632: exact reduced Pell continued-fraction unit search.
Usage: python rqt632.py RQT-630-results.json OUTPUT.json
"""
import json,hashlib,math,sys
from pathlib import Path
assert len(sys.argv)==3
src,out=map(Path,sys.argv[1:3])
raw=src.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='25d228f0176e366deca4fa3401b66789650ad2ef2c0dcb68d054c95a1de83ea6'
d=json.loads(raw);assert d['rqt']==630
rows=[]
for r in d['group_results'][:3]:
 D=int(r['coefficient_a']);s=int(r['known_square_factor']);red=int(r['reduced_d'])
 assert D==s*s*red
 a0=math.isqrt(red);m,den,a=0,1,a0
 pmm,pm=0,1;qmm,qm=1,0;first=[];hits=[];last=None
 for n in range(20000):
  p=a*pm+pmm;q=a*qm+qmm
  norm=p*p-red*q*q
  if n<6:first.append([n,str(a),str(norm)])
  if abs(norm)==1:hits.append([n,norm])
  last=(n,p,q,norm)
  m=den*a-m;den=(red-m*m)//den
  assert den>0 and (red-m*m)>=0
  a=(a0+m)//den
  pmm,pm=pm,p;qmm,qm=qm,q
 assert not hits
 n,p,q,norm=last
 finger=lambda z:hashlib.sha256(z.to_bytes((z.bit_length()+7)//8 or 1,'big')).hexdigest()
 rows.append(dict(group=r['group'],s=s,D=str(D),reduced_d=str(red),
  canonical_ids=r['canonical_ids'],limit=20000,hits_norm_plus_one=0,hits_norm_minus_one=0,
  q_last_bit_length=q.bit_length(),q_last_sha256=finger(q),p_last_sha256=finger(p),
  last_norm=str(norm),initial_convergents=first,transfer_exponent={5:6,7:6,4:4}[s],
  unit_recovered=False))
result=dict(rqt=632,source_rqt630_sha256=hashlib.sha256(raw).hexdigest(),
 reduced_groups_checked=3,convergents_per_group=20000,total_convergents=60000,
 group_results=rows,actual_reduced_units_found=0,original_units_recovered=0,
 integer_norm_minus_two_roots_found=0,remaining_unresolved_selected_families=53,
 excluded_selected_families=82,root19='OPEN',original_22d_wall='NOT REPLAYED',
 note='The convergent prefix was exhausted, not the entire Pell problem. Every nontrivial norm-one unit has y greater than the last tested convergent denominator within its reduced group.')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
assert hashlib.sha256(out.read_bytes()).hexdigest()=='0c5cc30a499222457339908b0ff6556f898bd83ce0a7b0e17df2549b70286ed2'
print('PASS RQT-632: 60000 convergents, zero units; Root 19 OPEN')
