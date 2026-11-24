#!/usr/bin/env python3
"""RQT-651: exact discriminant/determinant prime screen (p<2000).
Usage: python rqt651-discriminant-primes.py RQT-619-results.json [OUTPUT.json]
"""
import sys,json,math,hashlib
from pathlib import Path
def primes(n):
 s=bytearray([1])*n;s[:2]=b'\0\0'
 for p in range(2,math.isqrt(n-1)+1):
  if s[p]:s[p*p:n:p]=bytes(len(range(p*p,n,p)))
 return [p for p in range(3,n,2) if s[p]]
def matrix_det(a,b,c,d,e,f):
 return 2*a*(4*c*f-e*e)-b*(2*b*f-d*e)+d*(b*e-2*c*d)
def roots(C,p):
 a,b,c,d,e,f=C
 sq=[[] for _ in range(p)]
 for y in range(p):sq[y*y%p].append(y)
 inv=pow(2*a%p,-1,p) if 2*a%p else None
 count=regular=0;first=None
 for t in range(p):
  B=(b*t+d)%p;K=(c*t*t+e*t+f)%p
  if inv is not None:uv={(-B+s)*inv%p for s in sq[(B*B-4*a*K)%p]}
  elif B:uv={-K*pow(B,-1,p)%p}
  elif K==0:uv=range(p)
  else:uv=[]
  for u in uv:
   assert (a*u*u+b*u*t+c*t*t+d*u+e*t+f)%p==0
   count+=1
   du=(2*a*u+b*t+d)%p;dt=(b*u+2*c*t+e)%p
   if du or dt:
    regular+=1
    if first is None:first={'u':u,'t':t,'derivative_u':du,'derivative_t':dt}
 return count,regular,first
def main():
 src=Path(sys.argv[1]);raw=src.read_bytes()
 assert hashlib.sha256(raw).hexdigest()=='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
 R=json.loads(raw);assert R['rqt']==619 and len(R['families'])==27
 audited={3,5,7,11,13,17,19,23,29,31,37,41,43}
 old=new=0;records=[];extra=[]
 for family in R['families']:
  coeff=list(map(int,family['R_coefficients_as_strings']))
  a,b,c,d,e,f=coeff;Delta=b*b-4*a*c;Det=matrix_det(*coeff);risks=[]
  for p in primes(2000):
   x=Delta%p==0;y=Det%p==0
   if not (x or y):continue
   row={'p':p,'divides_delta':x,'divides_determinant':y,'previously_audited':p in audited}
   if p in audited:old+=1
   else:
    new+=1;count,regular,witness=roots(coeff,p)
    assert witness is not None
    row.update({'roots':count,'nonsingular_roots':regular,'witness':witness})
    extra.append({'orbit':family['canonical_id'],**row})
   risks.append(row)
  records.append({'canonical_id':family['canonical_id'],'member_ids':family['member_ids'],
    'discriminant':str(Delta),'homogenized_determinant':str(Det),'risks':risks})
 assert old==55 and new==29
 assert sorted({r['p'] for r in extra})==[53,59,71,113,131,271,293,449,491,769,929,1693]
 out={'rqt':651,'original_source_sha256':hashlib.sha256(raw).hexdigest(),
  'prime_bound_exclusive':2000,'old_risk_pairs':old,'new_risk_pairs':new,
  'additional_distinct_primes':sorted({r['p'] for r in extra}),
  'new_nonsingular_cases':new,'new_cases':extra,'orbits':records,
  'all_primes_tested':False,'full_factorization':False,'new_family_exclusions':0,
  'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN','wall22d':'NOT REPLAYED'}
 path=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-651-results.json')
 path.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS RQT-651: 84 risk pairs (<2000); 55 previous; 29 new nonsingular')
if __name__=='__main__':main()
