#!/usr/bin/env python3
"""RQT-654: deterministic certified prime extraction; no large primality claims.
python rqt654-certified-cofactors.py RQT-653-results.json [output.json]
"""
import sys,math,json,hashlib
from pathlib import Path
LIMIT=5_000_000
def sieve(n):
 bits=bytearray(b'\x01')*(n+1);bits[:2]=b'\x00\x00'
 for i in range(2,math.isqrt(n)+1):
  if bits[i]:bits[i*i:n+1:i]=b'\x00'*len(range(i*i,n+1,i))
 return bits,[i for i in range(2,n+1) if bits[i]]
def main():
 src=Path(sys.argv[1]);raw=src.read_bytes();data=json.loads(raw)
 assert data['rqt']==653
 bits,primes=sieve(LIMIT);records=[];hits=[];remainders=[]
 for i,e in enumerate(data['odd_cofactors']):
  original=int(e['value']);n=original;found=[]
  for p in primes:
   if p*p>n:break
   if n%p==0:
    exponent=0
    while n%p==0:n//=p;exponent+=1
    assert bits[p] and original%(p**exponent)==0
    found.append({'prime':p,'exponent':exponent,'certification':'exact sieve primality and divisibility'})
    hits.append({'cofactor_index':i,'prime':p,'exponent':exponent})
  if n>1 and n<=LIMIT**2 and all(n%p for p in primes if p*p<=n):
   found.append({'prime':n,'exponent':1,'certification':'exact complete trial division'})
   hits.append({'cofactor_index':i,'prime':n,'exponent':1})
   n=1
  assert math.prod(z['prime']**z['exponent'] for z in found)*n==original
  if n>1:remainders.append(n)
  records.append({'cofactor_index':i,'original':str(original),'source_count':e.get('source_count'),
                  'certified_factors':found,'unresolved_remainder':str(n),
                  'remainder_primality':'UNDETERMINED' if n>1 else 'fully extracted'})
 out={'rqt':654,'source_sha256':hashlib.sha256(raw).hexdigest(),'prime_sieve_limit':LIMIT,
  'cofactors_examined':len(records),'cofactors_with_certified_factor':sum(bool(v['certified_factors']) for v in records),
  'certified_prime_factor_occurrences':len(hits),'distinct_certified_primes':sorted(set(h['prime'] for h in hits)),
  'unresolved_remainder_count':len(remainders),'records':records,
  'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN','wall22d':'NOT REPLAYED',
  'ordinary_integer_root':'NOT CONSTRUCTED','new_all_scale_family_exclusions':0}
 assert (out['cofactors_examined'],out['cofactors_with_certified_factor'],len(out['distinct_certified_primes']),out['unresolved_remainder_count'])==(31,8,9,31)
 dst=Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-654-results.json')
 dst.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS: 31 components, nine certified prime factors, 31 unresolved remainders')
if __name__=='__main__':main()
