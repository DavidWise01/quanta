#!/usr/bin/env python3
"""RQT-628: exact continued-fraction Pell-unit bounds + bounded generalized seed diagnostic.
Usage: python rqt628-unit-search.py RQT-627-results.json RQT-626-results.json OUTPUT.json
"""
import json,hashlib,math,sys
from pathlib import Path
assert len(sys.argv)>=4
p,r626,output=map(Path,sys.argv[1:4])
raw=p.read_bytes();data=json.loads(raw)
assert data['rqt']==627
assert hashlib.sha256(raw).hexdigest()=='cd65fb37c79d8c4f7ef25763b4fa3e78e216498c816e621a56e67b8a17a06ae8'
r626j=json.loads(r626.read_text())
assert r626j['rqt']==626
coeffs=sorted({int(r['pell_a']) for r in data['records']})
limit=10000;res=[]
for D in coeffs:
 A=math.isqrt(D);assert A*A!=D
 m=0;den=1;aa=A;p_old,p_prev=0,1;q_old,q_prev=1,0;first=[];last=None
 for j in range(limit):
  numer=aa*p_prev+p_old;denom=aa*q_prev+q_old
  delta=numer*numer-D*denom*denom
  assert delta not in (-1,1),('unit found',D,j)
  if j<4:first.append({'index':j,'quotient':str(aa),'norm':str(delta),'numerator':str(numer),'denominator':str(denom)})
  last=(numer,denom,delta)
  p_old,p_prev=p_prev,numer;q_old,q_prev=q_prev,denom
  m=den*aa-m;den=(D-m*m)//den;assert den>0
  aa=(A+m)//den
 def fingerprint(n):
  return hashlib.sha256(n.to_bytes((n.bit_length()+7)//8 or 1,'big')).hexdigest()
 numer,denom,delta=last
 res.append({'a':str(D),'convergents_checked':limit,'positive_norm_one_hits':0,'negative_norm_one_hits':0,
  'last_convergent_index':limit-1,'last_denominator_bit_length':denom.bit_length(),
  'last_denominator_SHA256_big_endian':fingerprint(denom),
  'last_numerator_bit_length':numer.bit_length(),'last_numerator_SHA256_big_endian':fingerprint(numer),
  'last_norm':str(delta),'first_four_convergents':first,
  'certified_unit_y_lower_bound':'Any nontrivial norm-one unit has y greater than q_9999',
  'family_ids':[r['canonical_id'] for r in data['records'] if int(r['pell_a'])==D]})
coeff626={v['canonical_id']:v for v in r626j['records']}
seeds={}
for rec in data['records']:
 D=int(rec['pell_a']);h=int(rec['pell_h']);target=int(rec['pell_N'])
 c=int(coeff626[rec['canonical_id']]['primitive_discriminant_coefficients'][2])
 hits=[]
 for t in range(-1000,1001):
  z=D*t+h;y2=D*t*t+2*h*t+c
  if y2>=0:
   y=math.isqrt(y2)
   if y*y==y2:
    assert z*z-D*y*y==target and z%D==h%D
    hits.append({'t':t,'z':str(z),'y':str(y)})
 seeds[str(rec['canonical_id'])]=hits
assert all(not hits for hits in seeds.values())
out={'rqt':628,'source_rqt627_sha256':hashlib.sha256(raw).hexdigest(),
 'method':'simple continued fractions of sqrt(a), exact integer convergence and norm checks',
 'convergents_checked_per_a':limit,'five_a_units':res,'fundamental_units_found':0,
 'generalized_pell_seed_check':{'parameter_window':[-1000,1000],'seeds':seeds,'exact_square_hits':0},
 'unit_absence_scope':'first 10000 convergents per a only; no all-scale unit nonexistence claim',
 'new_all_scale_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
 'integer_norm_minus_two_root':'NOT FOUND','original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 50000 convergents checked; five lower bounds; Root19 OPEN')
