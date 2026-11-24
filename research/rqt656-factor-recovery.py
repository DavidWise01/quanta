#!/usr/bin/env python3
"""RQT-656 exact bounded factor recovery.
Usage: python rqt656-factor-recovery.py RQT-655-results.json [OUTPUT.json]
Requires Python 3 and SymPy for uncertified probable-prime screening only.
"""
import json,hashlib,math,sys
from pathlib import Path
from sympy import isprime
SOURCE_HASH='f8b712bfd62052d9f01590b8061de0bdcb613b769b24ff1c614e3a453f2f9198'
def sieve(n):
 s=bytearray(b'\x01')*(n+1);s[:2]=b'\x00\x00'
 for i in range(2,math.isqrt(n)+1):
  if s[i]:s[i*i:n+1:i]=b'\x00'*len(range(i*i,n+1,i))
 return [i for i in range(2,n+1) if s[i]]
P=sieve(5000)
def rho(n):
 for c in (1,3,5,7):
  x=y=2
  for step in range(1,8001):
   x=(x*x+c)%n;y=(y*y+c)%n;y=(y*y+c)%n
   g=math.gcd(abs(x-y),n)
   if 1<g<n:return g,{'method':'rho','c':c,'steps':step}
   if g==n:break
 return None,None
def pminusone(n):
 a=2
 for p in P:
  if p>3000:break
  power=p
  while power*p<=3000:power*=p
  a=pow(a,power,n);g=math.gcd(a-1,n)
  if 1<g<n:return g,{'method':'pminusone','prime_at_discovery':p}
 return None,None
def certprime(n):
 return n>1 and all(n%p for p in range(2,math.isqrt(n)+1))
def main():
 f=Path(sys.argv[1]);raw=f.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==SOURCE_HASH
 inp=json.loads(raw);assert inp['rqt']==655 and len(inp['records'])==31
 rows=[]
 for r in inp['records']:
  n=int(r['unresolved_remainder']);index=int(r['index']);old=r['classification']
  factor=method=None;classification='UNRESOLVED'
  if old=='COMPOSITE_PROVED_BY_FERMAT':
   factor,method=rho(n)
   if factor is None:factor,method=pminusone(n)
   if factor is not None:
    assert 1<factor<n and n%factor==0
    classification='FACTOR_FOUND_PRIME_CERTIFIED' if factor<10**10 and certprime(factor) else 'FACTOR_FOUND_UNCERTIFIED'
   q=n//factor if factor else n
  else:
   classification='PROBABLE_PRIME_UNCERTIFIED' if isprime(n) else 'COMPOSITE_UNDER_SCREEN'
   q=n
  assert factor is None or factor*q==n
  rows.append({'index':index,'input':str(n),'prior':old,'status':classification,
   'factor':str(factor) if factor else None,
   'certified_factor':str(factor) if classification=='FACTOR_FOUND_PRIME_CERTIFIED' else None,
   'quotient':str(q),'factor_method':method,
   'exact_recomposition':factor is None or factor*q==n})
 assert [r['index'] for r in rows]==list(range(31))
 out={'rqt':656,'source_rqt655_sha256':hashlib.sha256(raw).hexdigest(),'records':rows,
  'explicit_factors_found':sum(r['factor'] is not None for r in rows),
  'prime_certified_factors':sum(r['certified_factor'] is not None for r in rows),
  'unfactored_prior_composites':sum(r['factor'] is None and r['prior']=='COMPOSITE_PROVED_BY_FERMAT' for r in rows),
  'uncertified_probable_primes':sum(r['status']=='PROBABLE_PRIME_UNCERTIFIED' for r in rows),
  'primality_certificates_for_open_remainders':0,'new_family_exclusions':0,
  'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN','original_22d_wall':'NOT REPLAYED'}
 assert (out['explicit_factors_found'],out['prime_certified_factors'],out['unfactored_prior_composites'],out['uncertified_probable_primes'])==(11,11,12,8)
 dst=Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-656-results.json')
 dst.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS RQT-656: 11 certified factors, 12 composites unfactored, 8 primality open')
if __name__=='__main__':main()
