#!/usr/bin/env python3
"""RQT-661: exact n+1 certified factors and fixed-budget direct R rho search.
Usage: python rqt661.py RQT-660-results.json [output.json].
Python standard library only.
"""
import json,hashlib,sys,math
from pathlib import Path
FACTORS={23:[(2,1),(7,1),(11,1),(13,1),(3709,1),(7723,1)],28:[(2,2),(3,1),(672757,1)]}
def isprime(p):
 if p<2:return False
 if p%2==0:return p==2
 return all(p%d for d in range(3,math.isqrt(p)+1,2))
def rho(n,c,steps=12000):
 x=y=2
 for i in range(1,steps+1):
  x=(x*x+c)%n
  y=(y*y+c)%n;y=(y*y+c)%n
  g=math.gcd(abs(x-y),n)
  if 1<g<n:return g,i
  if g==n:return None,i
 return None,steps
def main():
 p=Path(sys.argv[1]);raw=p.read_bytes();src=json.loads(raw)
 assert src['rqt']==660 and [r['index'] for r in src['records']]==[23,28]
 rows=[]
 for r in src['records']:
  idx=r['index'];n=int(r['target_n']);R=int(r['R']);oldF=int(r['previous_F'])
  assert oldF*R==n-1
  factors=FACTORS[idx];assert all(isprime(q) for q,e in factors)
  F=math.prod(q**e for q,e in factors);assert (n+1)%F==0
  U=(n+1)//F;assert U*F==n+1
  attempts=[];found=None
  for c in (1,3,5,7,11):
   g,i=rho(R,c)
   attempts.append({'c':c,'iterations':i,'factor':str(g) if g else None})
   if g is not None:
    assert 1<g<R and R%g==0
    found=g;break
  rows.append({'index':idx,'target_n':str(n),'target_bits':n.bit_length(),
   'R':str(R),'n_plus_one':str(n+1),'n_plus_one_certified_prime_powers':[[str(q),e] for q,e in factors],
   'n_plus_one_certified_part':str(F),'n_plus_one_unresolved_part':str(U),
   'certified_part_square_exceeds_n':F*F>n,'certified_part_fraction_approx':format(F/(n+1),'.12g'),
   'certified_part_bits':F.bit_length(),'unresolved_cofactor_bits':U.bit_length(),
   'rho_attempts':attempts,'direct_R_factor':str(found) if found else None,
   'target_prime_certified':False})
 assert not any(r['direct_R_factor'] for r in rows)
 out={'rqt':661,'source_rqt660_sha256':hashlib.sha256(raw).hexdigest(),
  'method':'Exact certified small n+1 factors and deterministic bounded direct rho scan of R',
  'results':rows,'new_R_factors':0,'new_target_prime_certificates':0,
  'remaining_open_indexes':[23,28],
  'status_warning':'n+1 partial factorization alone does not prove target primality. Both square thresholds fail.',
  'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN','original_22d_wall':'NOT REPLAYED'}
 dest=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-661-results.json')
 dest.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS RQT-661: two targets, no new R factor, no new prime proof')
 print('SHA256',hashlib.sha256(dest.read_bytes()).hexdigest())
if __name__=='__main__':main()
