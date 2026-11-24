#!/usr/bin/env python3
"""RQT-660: exact bounded predecessor neighbor-factor audit.
python rqt660.py RQT-659-results.json [output.json]
Python standard library only; does NOT prove either large target prime.
"""
import json,math,hashlib,sys
from pathlib import Path
SIDE={23:{'minus':[(2,2)],'plus':[(2,1),(3,5),(7264393,1)]},
      28:{'minus':[(2,4),(1451,1)],'plus':[(2,1),(3,1),(3182573,1),(402939577,1)]}}
def certified_prime(n):
 if n<2:return False
 if n%2==0:return n==2
 for k in range(3,math.isqrt(n)+1,2):
  if n%k==0:return False
 return True
def trial(n,bound=100000):
 if n%2==0:return 2
 for k in range(3,bound+1,2):
  if n%k==0:return k
 return None
def main():
 p=Path(sys.argv[1]);raw=p.read_bytes();d=json.loads(raw)
 assert d['rqt']==659 and [v['index'] for v in d['candidates']]==[23,28]
 results=[]
 for c in d['candidates']:
  idx=c['index'];n=int(c['n']);R=int(c['unresolved_part_R']);F=int(c['certified_part_F'])
  assert F*R==n-1 and F*F<n
  neighbors=[]
  for direction in ('minus','plus'):
   number=R-1 if direction=='minus' else R+1
   fs=SIDE[idx][direction]
   for q,e in fs:assert certified_prime(q) and e>=1
   known=math.prod(q**e for q,e in fs)
   assert number%known==0
   unknown=number//known;assert known*unknown==number
   neighbors.append({'side':direction,'value':str(number),
     'certified_prime_powers':[[str(q),e] for q,e in fs],
     'certified_product':str(known),'unresolved_cofactor':str(unknown),
     'cofactor_prime_status':'UNPROVED' if unknown>1 else 'complete'})
  assert trial(R) is None
  results.append({'index':idx,'target_n':str(n),'R':str(R),'previous_F':str(F),
    'R_prime_status':'UNPROVED' if idx==23 else 'COMPOSITE_PROVED_FERMAT',
    'R_base2_fermat_residue':str(pow(2,R-1,R)),
    'R_trial_divisor_at_most_100000':None,'side_factor_audits':neighbors,
    'target_pocklington_threshold_met':F*F>n})
 assert results[0]['R_base2_fermat_residue']=='1'
 assert results[1]['R_base2_fermat_residue']!='1'
 out={'rqt':660,'source_rqt659_sha256':hashlib.sha256(raw).hexdigest(),
    'exact_factors_verified':sum(len(z['certified_prime_powers']) for r in results for z in r['side_factor_audits']),
    'blocking_cofactor_factors_recovered':0,'new_target_primes_proved':0,
    'certified_prime_nodes_inherited':130,'remaining_open_indexes':[23,28],
    'records':results,'new_full_family_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
    'root19':'OPEN','original_22d_wall':'NOT REPLAYED',
    'scope':'Exact partial factorization of R-1 and R+1, not R; neither target n proved prime.'}
 dest=Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-660-results.json')
 dest.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS RQT-660:',out['exact_factors_verified'],'prime-power records, two targets open')
 print('SHA256',hashlib.sha256(dest.read_bytes()).hexdigest())
if __name__=='__main__':main()
