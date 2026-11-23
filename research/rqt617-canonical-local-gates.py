#!/usr/bin/env python3
"""RQT-617 exact local-gradient and bounded Pell sieve.
Inputs: RQT-616-results.json RQT-591-results.json RQT-583-results.json.
No floating-point arithmetic; Python 3 standard library only.
"""
import sys,json,hashlib,math
from pathlib import Path
P=list(map(Path,sys.argv[1:4]));J,G,E=[json.loads(p.read_text()) for p in P]
F=[[int(x) for x in row] for row in G['reduced_gram']]
byid={e['index']:e for e in E['equations']}
assert J['job_count']==27
assert J['last_job_hash']=='6b365ada55f5e44881707b73b764814afbf6dc00e1d05affda4103ea2b229cd7'
assert hashlib.sha256(P[2].read_bytes()).hexdigest()=='5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92'
primes=[2,3,5,7,11,13,17,19,23,29,31]
R=100000;results=[]
for job in J['jobs']:
 e=byid[job['canonical_id']];r,o=e['ray'],e['offset']
 dot=lambda v,w:sum(v[i]*F[i+1][j+1]*w[j] for i in range(3) for j in range(3))
 a=F[0][0];b=2*sum(F[0][i+1]*r[i] for i in range(3));c=dot(r,r)
 d=2*sum(F[0][i+1]*o[i] for i in range(3));f=2*dot(r,o);g=dot(o,o)+2
 q=lambda u,t:a*u*u+b*u*t+c*t*t+d*u+f*t+g
 A,B,C=[int(e[k]) for k in 'ABC']
 for t in (-7,-1,0,1,7):
  z=[r[i]*t+o[i] for i in range(3)]
  h=sum(F[0][i+1]*z[i] for i in range(3))
  assert h*h-a*(dot(z,z)+2)==A*t*t+B*t+C
 local=[]
 for p in primes:
  regular=singular=0;witness=None
  for u in range(p):
   for t in range(p):
    if q(u,t)%p==0:
     gu=(2*a*u+b*t+d)%p;gt=(b*u+2*c*t+f)%p
     if gu or gt:
      regular+=1
      if witness is None:witness=[u,t]
     else:singular+=1
  assert regular+singular>0
  if witness:
   u,t=witness;m=p
   for _ in range(2,6):
    h=(q(u,t)//m)%p;gu=(2*a*u+b*t+d)%p;gt=(b*u+2*c*t+f)%p
    if gu:u+=(-h*pow(gu,-1,p)%p)*m
    else:t+=(-h*pow(gt,-1,p)%p)*m
    m*=p
    assert q(u,t)%m==0
  local.append(dict(prime=p,regular_mod_p=regular,singular_mod_p=singular,regular_witness=witness,regular_lifts_to_p5=bool(witness)))
 hits=[]
 for t in range(-R,R+1):
  z=A*t*t+B*t+C
  if z>=0 and math.isqrt(z)**2==z:hits.append(t)
 assert not hits
 results.append(dict(canonical_id=job['canonical_id'],member_ids=job['family_ids'],local=local,finite_square_hits=hits))
assert len(results)==27
assert [r['canonical_id'] for r in results if next(x['regular_mod_p'] for x in r['local'] if x['prime']==7)==0]==[2]
assert [r['canonical_id'] for r in results if next(x['regular_mod_p'] for x in r['local'] if x['prime']==31)==0]==[28]
assert all(next(x['regular_mod_p'] for x in r['local'] if x['prime']==2)==0 for r in results)
out=dict(rqt=617,canonical_jobs=27,original_ids=53,finite_tests=27*(2*R+1),prime_moduli=primes,results=results,new_global_exclusions=0,selected_excluded=82,selected_unresolved=53,root19='OPEN')
Path(sys.argv[4] if len(sys.argv)>4 else 'RQT-617-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-617: 27 canonical jobs; no finite square hits; root19 OPEN')
