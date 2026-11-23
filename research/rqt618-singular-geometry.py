#!/usr/bin/env python3
"""RQT-618: exact singular p=31 and complete p=2 branch checks.
Usage: python rqt618.py RQT-617-results.json RQT-591-results.json RQT-583-results.json
"""
import json,sys,math,hashlib
from pathlib import Path
P=list(map(Path,sys.argv[1:4]));J,G,E=[json.loads(p.read_text()) for p in P]
assert hashlib.sha256(P[2].read_bytes()).hexdigest()==J['source_sha256'][P[2].name]
F=[[int(x) for x in row] for row in G['reduced_gram']]
byid={e['index']:e for e in E['equations']}
def coeff(e):
 r,o=e['ray'],e['offset']
 dot=lambda v,w:sum(v[i]*F[i+1][j+1]*w[j] for i in range(3) for j in range(3))
 return (F[0][0],2*sum(F[0][i+1]*r[i] for i in range(3)),dot(r,r),2*sum(F[0][i+1]*o[i] for i in range(3)),2*dot(r,o),dot(o,o)+2)
def q(c,u,t):
 a,b,d,e,f,g=c
 return a*u*u+b*u*t+d*t*t+e*u+f*t+g
def grad(c,u,t):
 a,b,d,e,f,g=c
 return 2*a*u+b*t+e,b*u+2*d*t+f
p=31;c=coeff(byid[28]);roots=[(u,t) for u in range(p) for t in range(p) if q(c,u,t)%p==0]
assert roots==[(6,12)]
u0,t0=roots;u0,t0=u0[0],u0[1]
gu,gt=grad(c,u0,t0)
assert gu%p==gt%p==0 and q(c,u0,t0)%(p*p)==0
red=[c[0],c[1],c[2],gu//p,gt//p,q(c,u0,t0)//(p*p)]
assert [v%31 for v in red]==[3,10,24,13,15,9]
roots=[(x,y) for x in range(31) for y in range(31) if q(red,x,y)%31==0]
assert len(roots)==32 and all(any(z%31 for z in grad(red,x,y)) for x,y in roots)
for x,y in ((0,0),(3,6),(-11,19)):
 assert q(c,u0+31*x,t0+31*y)==31*31*q(red,x,y)
jets=[]
for x0,y0 in roots:
 x,y=x0,y0;m=31
 for _ in range(2,9):
  h=(q(red,x,y)//m)%31;du,dt=grad(red,x,y)
  if du%31:x+=(-h*pow(du%31,-1,31)%31)*m
  else:y+=(-h*pow(dt%31,-1,31)%31)*m
  m*=31
  assert q(red,x,y)%m==0
 assert q(c,u0+31*x,t0+31*y)%31**10==0
 jets.append({'reduced_root':[x0,y0],'u':str(u0+31*x),'t':str(t0+31*y)})
twos=[]
for job in J['canonical_results']:
 i=job['canonical_id'];cc=coeff(byid[i])
 branches={(u,t) for u in range(2) for t in range(2) if q(cc,u,t)%2==0}
 assert branches and all(not any(z%2 for z in grad(cc,u,t)) for u,t in branches)
 counts=[len(branches)];m=2
 for _ in range(2,11):
  mm=2*m
  branches={(u+a*m,t+b*m) for u,t in branches for a in (0,1) for b in (0,1) if q(cc,u+a*m,t+b*m)%mm==0}
  counts.append(len(branches));m=mm
  assert branches
 twos.append({'index':i,'counts_mod_2_through_1024':counts,'witness_mod_1024':min(branches)})
assert len(twos)==27
out={'rqt':618,'family28':{'root_mod31':[u0,t0],'reduced_coefficients_mod31':[v%31 for v in red],
'regular_roots':roots,'all_exponent_count':'1 if k=1; 961 if k=2; 32*31^(k-1) for k>=3','jets_through_31_power10':jets},
'two_adic_canonical_jobs':twos,'excluded':82,'unresolved':53,'new_exclusions':0,'root19':'OPEN'}
Path('RQT-618-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-618: 32 p31 branches and 27 canonical p2 cases; root19 OPEN')
