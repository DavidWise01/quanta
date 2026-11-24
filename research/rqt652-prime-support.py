#!/usr/bin/env python3
"""RQT-652: Exact prime support for 27 original quadratics.
Usage: python rqt652-prime-support.py RQT-619-results.json [output.json]
Full Python stdlib plus Fermat/Tonelli modular square roots; no complete factorization claim.
"""
import json,hashlib,math,sys
from pathlib import Path
R=Path(sys.argv[1]);raw=R.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
families=json.loads(raw)['families']
def primes(bound):
 s=bytearray(b'\1')*bound;s[:2]=b'\0\0'
 for p in range(2,math.isqrt(bound-1)+1):
  if s[p]:s[p*p:bound:p]=b'\0'*len(range(p*p,bound,p))
 return [p for p in range(3,bound,2) if s[p]]
P=primes(100001)
def determinant(a,b,c,d,e,f):
 return 2*a*(4*c*f-e*e)-b*(2*b*f-d*e)+d*(b*e-2*c*d)
def sqrtmod(w,p):
 w%=p
 if w==0:return [0]
 if pow(w,(p-1)//2,p)!=1:return []
 if p%4==3:
  x=pow(w,(p+1)//4,p);return sorted({x,(-x)%p})
 q=p-1;s=0
 while q%2==0:q//=2;s+=1
 z=2
 while pow(z,(p-1)//2,p)!=p-1:z+=1
 c=pow(z,q,p);x=pow(w,(q+1)//2,p);t=pow(w,q,p);m=s
 while t!=1:
  i=1;v=t*t%p
  while v!=1:v=v*v%p;i+=1
  b=pow(c,1<<(m-i-1),p);x=x*b%p;t=t*b*b%p;c=b*b%p;m=i
 return sorted({x,(-x)%p})
def witness(coeff,p):
 a,b,c,d,e,f=coeff;A=a%p
 for t in range(min(p,256)):
  B=(b*t+d)%p;K=(c*t*t+e*t+f)%p
  if A:
   inv=pow(2*A,-1,p);us=[(-B+v)*inv%p for v in sqrtmod((B*B-4*A*K)%p,p)]
  elif B:us=[-K*pow(B,-1,p)%p]
  elif K==0:us=[0,1]
  else:us=[]
  for u in us:
   du=(2*a*u+b*t+d)%p;dt=(b*u+2*c*t+e)%p
   if (du or dt) and (a*u*u+b*u*t+c*t*t+d*u+e*t+f)%p==0:
    return {'u':int(u),'t':t,'gradient_u':int(du),'gradient_t':int(dt)}
 return None
records=[];new=[]
for f in families:
 co=list(map(int,f['R_coefficients_as_strings']));a,b,c,d,e,z=co
 delta=abs(b*b-4*a*c);det=abs(determinant(*co));parts=[]
 for name,n in [('discriminant',delta),('homogenized_determinant',det)]:
  residue=n;factors=[]
  for p in P:
   if residue%p:continue
   exponent=0
   while residue%p==0:residue//=p;exponent+=1
   factors.append({'prime':p,'exponent':exponent})
  parts.append({'name':name,'value':str(n),'small_prime_factors':factors,
   'remaining_cofactor':str(residue),'cofactor_status':'unfactored-not-proven-prime' if residue>1 else '1'})
 for p in P:
  if p<2000 or (delta%p!=0 and det%p!=0):continue
  w=witness(co,p);assert w is not None
  new.append({'canonical_id':f['canonical_id'],'prime':p,'divides_discriminant':delta%p==0,
    'divides_determinant':det%p==0,'nonsingular_witness':w})
 records.append({'canonical_id':f['canonical_id'],'member_ids':f['member_ids'],'factors':parts})
assert len(records)==27 and len(new)==16
assert sorted({x['prime'] for x in new})==[4679,5303,9521,12097,13457,21499,55049,59029,64283,87083]
assert sum(int(q['remaining_cofactor'])>1 for r in records for q in r['factors'])==54
out={'rqt':652,'source_sha256':hashlib.sha256(raw).hexdigest(),'prime_bound_inclusive':100000,
 'distinct_discriminants':len({r['factors'][0]['value'] for r in records}),
 'distinct_determinants':len({r['factors'][1]['value'] for r in records}),
 'new_risk_pairs_2000_to_100000':len(new),'new_distinct_primes':sorted({x['prime'] for x in new}),
 'new_cases':new,'orbits':records,'unfactored_cofactor_entries':54,
 'new_all_scale_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
 'root19':'OPEN','wall22d':'NOT REPLAYED',
 'scope':'Bounded exact factor sieve, not full factorization or ordinary integer-root proof.'}
dest=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-652-results.json')
dest.write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-652: 16 additional nonsingular risk cases, 54 unfactored entries')
