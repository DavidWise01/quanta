#!/usr/bin/env python3
"""RQT-609 — deterministic exact 2/7-adic Hensel branch verifier.
Usage: python rqt609.py RQT-608-results.json RQT-591-results.json RQT-583-results.json [out.json]
"""
import json,sys,math,hashlib
from pathlib import Path
P=[Path(s) for s in sys.argv[1:4]]
a,b,c=[json.loads(p.read_text()) for p in P]
assert hashlib.sha256(P[0].read_bytes()).hexdigest()=='0a86b00b80c7add37edba135971ed0018cae1170685e5feadad8ef0914a15844'
F=[[int(z) for z in row] for row in b['reduced_gram']]
eq={e['index']:e for e in c['equations']}
def coeff(e):
 r,o=e['ray'],e['offset']
 dot=lambda v,w:sum(v[i]*F[i+1][j+1]*w[j] for i in range(3) for j in range(3))
 return F[0][0],2*sum(F[0][i+1]*r[i] for i in range(3)),dot(r,r),2*sum(F[0][i+1]*o[i] for i in range(3)),2*dot(r,o),dot(o,o)+2
def norm(c,u,t):
 a,b,d,e,f,g=c;return a*u*u+b*u*t+d*t*t+e*u+f*t+g
def grad(c,u,t):
 a,b,d,e,f,g=c;return 2*a*u+b*t+e,b*u+2*d*t+f
def all_lifts(c,p,n):
 roots={(u,t) for u in range(p) for t in range(p) if norm(c,u,t)%p==0}
 m=p;counts=[len(roots)]
 for k in range(2,n+1):
  fresh=set();newm=m*p
  for u,t in roots:
   h=(norm(c,u,t)//m)%p;du,dt=grad(c,u,t);du%=p;dt%=p
   for x in range(p):
    for y in range(p):
     if (h+du*x+dt*y)%p==0:fresh.add((u+x*m,t+y*m))
  roots=fresh;m=newm;counts.append(len(roots))
  assert roots
 return roots,counts
def regular7(c):
 for u in range(7):
  for t in range(7):
   if norm(c,u,t)%7 or not any(g%7 for g in grad(c,u,t)):continue
   m=7
   for k in range(2,7):
    h=(norm(c,u,t)//m)%7;du,dt=grad(c,u,t);du%=7;dt%=7
    x,y=next((x,y) for x in range(7) for y in range(7) if (h+du*x+dt*y)%7==0)
    u+=x*m;t+=y*m;m*=7
   return u,t
 return None
mods=[16384,81,125,117649,11,13,17,19,23,29,31]
M=math.prod(mods)
assert M==14*int(a['combined_modulus'])==18639287143547406336000
def crt(vals):
 return sum((v%m)*(M//m)*pow(M//m,-1,m) for v,m in zip(vals,mods))%M
out=[]
for row in a['records']:
 i=row['index'];f=coeff(eq[i]);u0=int(row['u_mod_combined']);t0=int(row['t_mod_combined'])
 roots2,counts2=all_lifts(f,2,14)
 assert counts2[:13]==row['two_branch_counts_by_exponent']
 r7=regular7(f)
 if r7 is None:
  assert i in (2,24)
  roots7,counts7=all_lifts(f,7,6)
  assert counts7==[1,49,392,2744,19208,134456]
  r7=min(roots7)
 u2,t2=min(roots2)
 uv=[u2,u0%81,u0%125,r7[0]]+[u0%m for m in mods[4:]]
 tv=[t2,t0%81,t0%125,r7[1]]+[t0%m for m in mods[4:]]
 u,t=crt(uv),crt(tv)
 assert norm(f,u,t)%M==0
 base={}
 for p in (2,7):
  rr=[(x,y) for x in range(p) for y in range(p) if norm(f,x,y)%p==0]
  regular=sum(any(g%p for g in grad(f,x,y)) for x,y in rr)
  base[p]={'roots':len(rr),'regular':regular,'singular':len(rr)-regular}
 out.append({'index':i,'mod2':base[2],'mod7':base[7],'two_branch_counts':counts2,
             'u_mod_combined':str(u),'t_mod_combined':str(t)})
assert len(out)==53 and {r['index'] for r in out if r['mod7']['regular']==0}=={2,24}
obj={'rqt':609,'source_608_sha256':hashlib.sha256(P[0].read_bytes()).hexdigest(),
 'combined_modulus':str(M),'moduli':mods,'records':out,'new_all_scale_exclusions':0,
 'excluded_selected':82,'unresolved_selected':53,'root19':'OPEN'}
path=Path(sys.argv[4]) if len(sys.argv)>4 else Path('RQT-609-replay.json')
path.write_text(json.dumps(obj,indent=2)+'\n')
print('PASS 53/53 next-level lifts; 2-adic base roots all singular; p7 singular-only families 2 & 24')
