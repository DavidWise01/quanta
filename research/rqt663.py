#!/usr/bin/env python3
"""RQT-663 exhaustive residue-wheel integer seed scan.
python rqt663.py RQT-619-results.json [result.json] [bound=100000]
"""
import json,math,hashlib,sys
from pathlib import Path
SRC="97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021"
MODS=(64,63,65,17,19);WHEEL=4032
def main():
 p=Path(sys.argv[1]);raw=p.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==SRC
 data=json.loads(raw);assert data['rqt']==619 and len(data['families'])==27
 dst=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-663-results.json')
 B=int(sys.argv[3]) if len(sys.argv)>3 else 100000
 assert 1<=B<=1000000
 sq={m:{y*y%m for y in range(m)} for m in MODS}
 rows=[];seeds=[]
 for rec in data['families']:
  idx=rec['canonical_id'];r0,r1,r2,r3,r4,r5=map(int,rec['R_coefficients_as_strings'])
  assert r0!=0
  a=r1*r1-4*r0*r2;h=r1*r3-2*r0*r4;c=r3*r3-4*r0*r5
  residues=[t for t in range(WHEEL) if ((a*t+2*h)*t+c)%64 in sq[64] and ((a*t+2*h)*t+c)%63 in sq[63]]
  wheel=survive=nonneg_wheel=squares=0;hits=[]
  for residue in residues:
   kmin=(-B-residue+WHEEL-1)//WHEEL;kmax=(B-residue)//WHEEL
   for k in range(kmin,kmax+1):
    t=residue+k*WHEEL
    assert -B<=t<=B and t%WHEEL==residue
    wheel+=1
    F=(a*t+2*h)*t+c
    if F<0:continue
    nonneg_wheel+=1
    if any(F%m not in sq[m] for m in (65,17,19)):continue
    survive+=1
    y=math.isqrt(F)
    if y*y!=F:continue
    squares+=1;L=r1*t+r3
    for sign in (-1,1):
     v=-L+sign*y
     if v%(2*r0):continue
     u=v//(2*r0)
     assert r0*u*u+r1*u*t+r2*t*t+r3*u+r4*t+r5==0
     hits.append({'canonical_id':idx,'u':str(u),'t':t,'y':str(y),'sign':sign})
  full_nonneg=sum((a*t+2*h)*t+c>=0 for t in range(-B,B+1))
  rows.append({'canonical_id':idx,'member_ids':rec['member_ids'],
   'parameter_count':2*B+1,'nonnegative_discriminants_all':full_nonneg,
   'wheel_modulus':WHEEL,'wheel_admissible_residue_classes':len(residues),
   'wheel_candidates_within_bound':wheel,'nonnegative_after_wheel':nonneg_wheel,
   'passed_remaining_modular_filters':survive,'exact_square_discriminants':squares,
   'integral_original_solutions':len(hits),'solutions':hits})
  seeds.extend(hits)
 out={'rqt':663,'input_sha256':SRC,'bound_t_inclusive':B,'wheel_modulus':WHEEL,
  'modular_square_moduli':list(MODS),
  'search_semantics':'All integer t in range exhaustively enumerated through wheel residue classes; exact-square and original coordinate gate.',
  'orbits':rows,'total_parameter_orbit_checks':sum(x['parameter_count'] for x in rows),
  'total_nonnegative_discriminants':sum(x['nonnegative_discriminants_all'] for x in rows),
  'wheel_candidates':sum(x['wheel_candidates_within_bound'] for x in rows),
  'modular_survivors':sum(x['passed_remaining_modular_filters'] for x in rows),
  'exact_square_discriminants':sum(x['exact_square_discriminants'] for x in rows),
  'integral_original_seeds':len(seeds),'solutions':seeds,
  'new_all_scale_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
  'root19':'OPEN','original_22d_wall':'NOT REPLAYED',
  'scope':'Finite original t window across 27 canonical quadratic charts; no all-scale negative theorem.'}
 if B==100000:
  assert [out[k] for k in ('total_parameter_orbit_checks','total_nonnegative_discriminants','wheel_candidates','modular_survivors','exact_square_discriminants','integral_original_seeds')]==[5400027,5398223,1732949,310407,0,0]
 dst.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS RQT-663',out['total_parameter_orbit_checks'],'checks,',out['modular_survivors'],'survivors,',len(seeds),'seeds')
 print('SHA256',hashlib.sha256(dst.read_bytes()).hexdigest())
if __name__=='__main__':main()
