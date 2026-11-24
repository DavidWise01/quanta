#!/usr/bin/env python3
"""RQT-650 — exact singular-prime resolution. Python 3 standard library.
Usage: python rqt650-singular-primes.py RQT-619-results.json [output.json]
"""
import json,hashlib,sys
from pathlib import Path
source=Path(sys.argv[1]);raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
data=json.loads(raw);records=[]
for idx,p in ((2,7),(28,31)):
 r=next(z for z in data['families'] if z['canonical_id']==idx)
 a,b,c,d,e,f=map(int,r['R_coefficients_as_strings'])
 def G(u,t):return a*u*u+b*u*t+c*t*t+d*u+e*t+f
 def Gu(u,t):return 2*a*u+b*t+d
 def Gt(u,t):return b*u+2*c*t+e
 roots=[(u,t) for u in range(p) for t in range(p) if G(u,t)%p==0]
 assert len(roots)==1
 u0,t0=roots[0];assert Gu(u0,t0)%p==Gt(u0,t0)%p==0
 assert G(u0,t0)%(p*p)==0
 A,B,C,D,E,F=a,b,c,Gu(u0,t0)//p,Gt(u0,t0)//p,G(u0,t0)//(p*p)
 def H(U,T):return A*U*U+B*U*T+C*T*T+D*U+E*T+F
 def Hu(U,T):return 2*A*U+B*T+D
 def Ht(U,T):return B*U+2*C*T+E
 for U,T in ((0,0),(1,3),(-2,5),(p+1,-7)):
  assert G(u0+p*U,t0+p*T)==p*p*H(U,T)
 regular=[(U,T) for U in range(p) for T in range(p) if H(U,T)%p==0 and (Hu(U,T)%p or Ht(U,T)%p)]
 assert len(regular)==(8 if p==7 else 32)
 U,T=regular[0];var='U' if Hu(U,T)%p else 'T';lifts=[]
 for n in range(1,13):
  assert H(U,T)%(p**n)==0
  assert G(u0+p*U,t0+p*T)%(p**(n+2))==0
  if n in (1,2,3,6,9,12):lifts.append({'G_exponent':n+2,'u':str(u0+p*U),'t':str(t0+p*T)})
  if n==12:break
  grad=(Hu(U,T) if var=='U' else Ht(U,T))%p
  digit=(-(H(U,T)//p**n)*pow(grad,-1,p))%p
  if var=='U':U+=digit*p**n
  else:T+=digit*p**n
 assert all(G(u0+p*i,t0+p*j)%(p*p)==0 for i in range(p) for j in range(p))
 records.append({'orbit':idx,'prime':p,'singular_mod_p_root':[u0,t0],
   'H_coefficients':[str(z) for z in (A,B,C,D,E,F)],
   'H_coefficients_mod_p':[z%p for z in (A,B,C,D,E,F)],
   'H_nonsingular_roots_mod_p':len(regular),'lifted_variable':var,'witnesses':lifts,
   'original_roots_mod_p2':p*p,'original_roots_mod_p3':len(regular)*p*p,
   'Z_p_solvability':'PROVED','ordinary_integer_root':'NOT ESTABLISHED'})
assert [(r['orbit'],r['prime'],r['H_nonsingular_roots_mod_p']) for r in records]==[(2,7,8),(28,31,32)]
out={'rqt':650,'source_sha256':hashlib.sha256(raw).hexdigest(),
 'singular_exceptions_resolved':2,'exceptions':records,
 'all_351_tested_odd_prime_orbit_cases_Z_p_solvable':True,
 'no_all_primes_claim':True,'new_family_exclusions':0,'excluded':82,'unresolved':53,
 'root19':'OPEN','original_22d_wall':'NOT REPLAYED'}
path=Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-650-results.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print('PASS: both singular primes resolved p-adically; integer root remains open.')
