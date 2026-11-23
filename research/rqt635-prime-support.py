#!/usr/bin/env python3
"""RQT-635 — standalone exact prime-support CRT and Pell recovery verifier.
Python 3 standard library. Run:
 python rqt635.py [output.json] [candidate.json]
Candidate: {"group":1, "x":"integer", "Y":"integer"}.
"""
import sys,json,math,hashlib
from pathlib import Path
from itertools import product

GROUPS=[
 (1,5,3,89518360633605555683821304281344825,[3,13,1693],[28,29,30,31,33,34,35,36,37]),
 (2,7,3,149561530769640628300862186866588569,[3],[81,89,92]),
 (3,4,2,158134758925461363207454619257200752,[12097,87083],[0,1,2,7]),
]
def is_prime(n):
 if n<2:return False
 for j in range(2,math.isqrt(n)+1):
  if n%j==0:return False
 return True
def crt(res,primes):
 M=math.prod(primes)
 return sum(v*(M//p)*pow(M//p,-1,p) for v,p in zip(res,primes))%M
def multiply(a,b,d):
 x,y=a;z,w=b
 return x*z+d*y*w,x*w+y*z
def power(u,n,d):
 out=(1,0)
 while n:
  if n&1:out=multiply(out,u,d)
  u=multiply(u,u,d);n//=2
 return out
rows=[]
for index,s,E,D,primes,ids in GROUPS:
 assert D%(s*s)==0
 d=D//(s*s)
 assert math.isqrt(d)**2!=d
 assert len(primes)==len(set(primes))
 assert all(is_prime(p) and d%p==0 for p in primes)
 M=math.prod(primes)
 allowed=sorted({crt(signs,primes) for signs in product(*[(-1,1) for _ in primes])})
 assert len(allowed)==2**len(primes)
 assert all(all((x*x-1)%p==0 for p in primes) for x in allowed)
 rows.append({'group':index,'canonical_ids':ids,'s':s,'recovery_E':E,'reduced_d':str(d),
 'original_D':str(D),'certified_odd_prime_divisors':primes,'divisor_product_M':M,
 'allowed_x_mod_M':allowed,'allowed_x_count':len(allowed),
 'allowed_x_fraction':f'{len(allowed)}/{M}'})
assert [r['allowed_x_count'] for r in rows]==[8,2,4]
out={'rqt':635,'method':'Exact odd-prime divisibility and CRT signs',
 'canonical_orbits_covered':16,'total_unresolved_canonical_orbits':27,
 'groups':rows,'numeric_norm_one_units_found':0,'new_all_scale_family_exclusions':0,
 'selected_excluded':82,'selected_unresolved':53,'original_22D_wall':'NOT REPLAYED',
 'root19':'OPEN'}
if len(sys.argv)>2:
 c=json.loads(Path(sys.argv[2]).read_text());i=int(c['group'])
 r=rows[i-1];x=int(c['x']);Y=int(c['Y']);d=int(r['reduced_d'])
 assert Y and x*x-d*Y*Y==1,'Candidate is NOT a genuine nontrivial norm-one unit'
 assert x%r['divisor_product_M'] in r['allowed_x_mod_M']
 X,YY=power((x,Y),r['recovery_E'],d)
 s=r['s'];assert YY%s==0
 y=YY//s
 assert X*X-int(r['original_D'])*y*y==1
 out['validated_candidate']={'group':i,'X':str(X),'y':str(y),'exact_original_norm':1}
 out['numeric_norm_one_units_found']=1
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('RQT-635-results.json')
p.write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-635 | CRT class counts:',[r['allowed_x_count'] for r in rows],
 '| candidate units:',out['numeric_norm_one_units_found'])
print('SHA256:',hashlib.sha256(p.read_bytes()).hexdigest())
