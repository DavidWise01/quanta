#!/usr/bin/env python3
"""RQT-662: bounded exact original integer-seed search.
Usage: python rqt662.py RQT-619-results.json [results.json] [bound=20000]
No floating point and no all-scale exclusion claim.
"""
import hashlib,json,math,sys
from pathlib import Path
SOURCE_SHA='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
def main():
 p=Path(sys.argv[1]);raw=p.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA
 src=json.loads(raw);assert src['rqt']==619 and len(src['families'])==27
 dest=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-662-results.json')
 B=int(sys.argv[3]) if len(sys.argv)>3 else 20000
 assert 1<=B<=100000
 mods=(64,63,65,17,19)
 squares={m:{x*x%m for x in range(m)} for m in mods}
 records=[];found=[]
 for entry in src['families']:
  idx=entry['canonical_id'];r0,r1,r2,r3,r4,r5=map(int,entry['R_coefficients_as_strings'])
  assert r0!=0
  a=r1*r1-4*r0*r2;h=r1*r3-2*r0*r4;c=r3*r3-4*r0*r5
  passes=square_discriminants=positive=integral=0;hits=[]
  for t in range(-B,B+1):
   F=(a*t+2*h)*t+c
   if F<0:continue
   positive+=1
   if any(F%m not in squares[m] for m in mods):continue
   passes+=1
   y=math.isqrt(F)
   if y*y!=F:continue
   square_discriminants+=1;L=r1*t+r3
   for sign in (-1,1):
    numerator=-L+sign*y
    if numerator%(2*r0):continue
    u=numerator//(2*r0)
    assert r0*u*u+r1*u*t+r2*t*t+r3*u+r4*t+r5==0
    integral+=1
    hit={'canonical_id':idx,'member_ids':entry['member_ids'],'u':str(u),'t':t,'y':str(y),'sign':sign,'G_original':0}
    hits.append(hit);found.append(hit)
  records.append({'canonical_id':idx,'member_ids':entry['member_ids'],
   'parameters_tested':2*B+1,'nonnegative_discriminants':positive,
   'passed_modular_square_filters':passes,'exact_square_discriminants':square_discriminants,
   'integral_recovered_solutions_count':integral,'solutions':hits,
   'quadratic_discriminant_coefficient_a':str(a),'integer_coordinate_denominator':str(2*r0)})
 output={'rqt':662,'source_sha256':SOURCE_SHA,'search_bound_t_inclusive':B,
  'canonical_orbits':27,'original_family_count':53,
  'total_parameter_orbit_checks':sum(z['parameters_tested'] for z in records),
  'total_nonnegative_discriminants':sum(z['nonnegative_discriminants'] for z in records),
  'total_passed_modular_square_filters':sum(z['passed_modular_square_filters'] for z in records),
  'total_exact_square_discriminants':sum(z['exact_square_discriminants'] for z in records),
  'total_integral_coordinate_solutions':sum(z['integral_recovered_solutions_count'] for z in records),
  'solutions':found,'records':records,'new_all_scale_exclusions':0,
  'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN','original_22d_wall':'NOT REPLAYED',
  'scope':'FINITE |t|<=B IN THESE 27 CHARTS ONLY; no all-scale conclusion.'}
 dest.write_text(json.dumps(output,indent=2)+'\n')
 print('PASS RQT-662',output['total_parameter_orbit_checks'],'checks',
  output['total_exact_square_discriminants'],'squares',
  output['total_integral_coordinate_solutions'],'integer-coordinate solutions')
 print('SHA256',hashlib.sha256(dest.read_bytes()).hexdigest())
if __name__=='__main__':main()
