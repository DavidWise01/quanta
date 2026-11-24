#!/usr/bin/env python3
"""RQT-653 exact coprimality audit. python rqt653.py RQT-652-results.json [out.json]"""
import sys,json,hashlib,math,itertools
from pathlib import Path
def sha(x):return hashlib.sha256(x).hexdigest()
def primes(n):
 s=bytearray(b'\1')*(n+1);s[:2]=b'\0\0'
 for p in range(2,math.isqrt(n)+1):
  if s[p]:s[p*p:n+1:p]=b'\0'*len(range(p*p,n+1,p))
 return [p for p in range(3,n+1,2) if s[p]]
def main():
 path=Path(sys.argv[1]);raw=path.read_bytes()
 assert sha(raw)=='2cd1ccf0119ea4f09617657cbb0e58351cb7812e8661e1109bd03b822da4e72a'
 x=json.loads(raw);assert x['rqt']==652 and len(x['orbits'])==27
 odd={};entries=valuation_sum=even_entries=0;records=[];P=primes(100000)
 for r in x['orbits']:
  items=[]
  for z in r['factors']:
   residual=int(z['remaining_cofactor'])
   if residual==1:continue
   entries+=1;v=(residual&-residual).bit_length()-1;q=residual>>v
   assert q>1 and q%2==1
   assert math.prod(int(f['prime'])**int(f['exponent']) for f in z['small_prime_factors'])*residual==int(z['value'])
   assert all(q%p for p in P)
   valuation_sum+=v;even_entries+=bool(v)
   odd.setdefault(q,[]).append((r['canonical_id'],z['name']))
   items.append({'name':z['name'],'v2':v,'odd_cofactor':str(q)})
  records.append({'orbit':r['canonical_id'],'records':items})
 u=sorted(odd);gcd_tests=0
 for a,b in itertools.combinations(u,2):
  assert math.gcd(a,b)==1;gcd_tests+=1
 assert (entries,len(u),valuation_sum,gcd_tests)==(54,31,82,465)
 result={'rqt':653,'source_sha256':sha(raw),'residual_entries':entries,'unique_odd_cofactors':31,
 'total_v2_exponent_counting_repetitions':82,'even_residual_entries':even_entries,
 'distinct_odd_cofactor_gcd_tests':gcd_tests,'all_pairwise_gcd_one':True,
 'odd_cofactors':[{'value':str(q),'source_count':len(odd[q]),'sources':odd[q]} for q in u],
 'per_orbit':records,'no_odd_prime_factor_at_most_100000':True,
 'primality_status':'UNRESOLVED','new_family_exclusions':0,'selected_excluded':82,
 'selected_unresolved':53,'root19':'OPEN','original_22d_wall':'NOT REPLAYED'}
 dest=Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-653-results.json')
 dest.write_text(json.dumps(result,indent=2)+'\n')
 print('PASS RQT-653: 54 entries / 31 odd cofactors / 465 coprime pairs')
if __name__=='__main__':main()
