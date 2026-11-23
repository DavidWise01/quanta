#!/usr/bin/env python3
"""RQT-625 exact bounded integer seed search. Python 3 stdlib.
Usage: python rqt625.py RQT-619-results.json RQT-624-results.json OUT.json [BOUND]
"""
import json,hashlib,math,sys
from pathlib import Path
sfile,cfile,ofile=map(Path,sys.argv[1:4])
B=int(sys.argv[4]) if len(sys.argv)>4 else 1000000
S=json.loads(sfile.read_text());C=json.loads(cfile.read_text())
assert S['rqt']==619 and C['rqt']==624
assert hashlib.sha256(sfile.read_bytes()).hexdigest()=='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
assert hashlib.sha256(cfile.read_bytes()).hexdigest()=='3af5fb6ec8a63b67babc42a4692a688c5a302ddf29bfaf15e56dc3a820cf3397'
sc={r['canonical_id']:r for r in S['families']}
primes=[5,11,13,17,19,23,29,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251]
N=2*B+1
results=[]
for row in C['families']:
 idx=row['canonical_id'];s=sc[idx]
 a,b,c,d,e,f=(2*int(v) for v in s['R_coefficients_as_strings'])
 assert a!=0 and row['member_ids']==s['member_ids']
 A=b*b-4*a*c;BB=2*b*d-4*a*e;CC=d*d-4*a*f
 def delta(t):return (A*t+BB)*t+CC
 mask=bytearray(b'\x01')*N;steps=[]
 for m in row['t_wheel_moduli']:
  allowed=set(row['projected_t_residues'][str(m)])
  for bad in range(m):
   if bad not in allowed:
    start=(bad+B)%m
    if start<N:mask[start::m]=b'\x00'*(((N-1-start)//m)+1)
  steps.append({'gate':'coordinate_projection','modulus':m,'remaining':mask.count(1)})
 for p in primes:
  squares={z*z%p for z in range(p)}
  good={t for t in range(p) if (A*t*t+BB*t+CC)%p in squares}
  for bad in range(p):
   if bad not in good:
    start=(bad+B)%p
    if start<N:mask[start::p]=b'\x00'*(((N-1-start)//p)+1)
  remaining=mask.count(1)
  steps.append({'gate':'discriminant_quadratic_residue','modulus':p,'remaining':remaining})
  if not remaining:break
 survivors=[];squares=[];integer_roots=[]
 for i,live in enumerate(mask):
  if not live:continue
  t=i-B;z=delta(t);survivors.append(t)
  if z>=0:
   h=math.isqrt(z)
   if h*h==z:
    squares.append(t)
    for sign in (-1,1):
     numerator=-(b*t+d)+sign*h
     if numerator%(2*a)==0:
      u=numerator//(2*a)
      assert a*u*u+(b*t+d)*u+c*t*t+e*t+f==0
      integer_roots.append({'u':str(u),'t':t})
 results.append({'canonical_id':idx,'member_ids':row['member_ids'],
 'discriminant_coefficients':[str(A),str(BB),str(CC)],'stages':steps,
 'surviving_t_after_gates':survivors,'square_discriminant_t':squares,'exact_integer_roots':integer_roots})
 print('family',idx,'final_prime',steps[-1]['modulus'],'survivors',len(survivors),flush=True)
assert len(results)==27 and sum(len(x['member_ids']) for x in results)==53
out={'rqt':625,'input_sha256':{sfile.name:hashlib.sha256(sfile.read_bytes()).hexdigest(),cfile.name:hashlib.sha256(cfile.read_bytes()).hexdigest()},
'integer_t_window':[-B,B],'canonical_orbits':27,'t_parameters_total':N*27,
'families':results,'global_family_exclusions_added':0,'all_scale_excluded':82,
'unresolved':53,'root19':'OPEN','22d_wall':'NOT REPLAYED'}
ofile.write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-625:',sum(len(r['exact_integer_roots']) for r in results),'integer roots')
