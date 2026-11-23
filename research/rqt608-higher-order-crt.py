#!/usr/bin/env python3
"""RQT-608: reproduce compatible higher 2/7-adic lifts.
python rqt608.py RQT-607-results.json RQT-591-reduced_gram.json RQT-583-results.json
"""
import json,hashlib,math,sys
from pathlib import Path
P=list(map(Path,sys.argv[1:4]))
sha=[hashlib.sha256(p.read_bytes()).hexdigest() for p in P]
assert sha==['f92b68e0bb3a6ae71a44f380ff1c8d40b7fae383d7c234a8050c0e35103464cf','f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228','5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92']
s,g,e=[json.loads(p.read_text()) for p in P]
equations={v['index']:v for v in e['equations']}
factors=[8192,81,125,16807,11,13,17,19,23,29,31]
M=math.prod(factors)
assert M==784*int(s['lifted_modulus'])==1331377653110529024000
def coeff(v):
 r,o=v['ray'],v['offset']
 dot=lambda a,b:sum(a[i]*g[i+1][j+1]*b[j] for i in range(3) for j in range(3))
 return (g[0][0],2*sum(g[0][i+1]*r[i] for i in range(3)),dot(r,r),2*sum(g[0][i+1]*o[i] for i in range(3)),2*dot(r,o),dot(o,o)+2)
def norm(c,u,t):
 a,b,d,e,f,h=c
 return a*u*u+b*u*t+d*t*t+e*u+f*t+h
def lift(c,u,t,p,k,n):
 m=p**k;branches={(u%m,t%m)}
 assert norm(c,u,t)%m==0
 for _ in range(k+1,n+1):
  mm=m*p
  branches={(x+i*m,y+j*m) for x,y in branches for i in range(p) for j in range(p) if norm(c,x+i*m,y+j*m)%mm==0}
  if not branches:return None
  m=mm
 return min(branches)
def all_branches(c,p,n):
 branches={(u,t) for u in range(p) for t in range(p) if norm(c,u,t)%p==0}
 counts=[len(branches)];m=p
 for _ in range(2,n+1):
  mm=m*p
  branches={(u+i*m,t+j*m) for u,t in branches for i in range(p) for j in range(p) if norm(c,u+i*m,t+j*m)%mm==0}
  assert branches
  counts.append(len(branches));m=mm
 return min(branches),counts
def regular7(c):
 a,b,d,e,f,h=c
 for t in range(7):
  for u in range(7):
   if norm(c,u,t)%7==0 and ((2*a*u+b*t+e)%7 or (b*u+2*d*t+f)%7):
    return lift(c,u,t,7,1,5)
 return None
def crt(xs):
 return sum((v%m)*(M//m)*pow(M//m,-1,m) for v,m in zip(xs,factors))%M
res=[];fail2=[];fail7=[];singular=[]
for row in s['families']:
 i=row['family_index'];c=coeff(equations[i]);u0=int(row['u_mod_14M']);t0=int(row['t_mod_14M'])
 assert norm(c,u0,t0)%int(s['lifted_modulus'])==0
 old2=lift(c,u0,t0,2,9,13);old7=lift(c,u0,t0,7,3,5)
 if old2 is None:fail2.append(i)
 if old7 is None:fail7.append(i)
 new2,counts2=all_branches(c,2,13)
 new7=regular7(c)
 if new7 is None:
  singular.append(i)
  new7,counts7=all_branches(c,7,5)
 else:counts7=None
 a2=old2 or new2;a7=old7 or new7
 U=crt([a2[0],u0%81,u0%125,a7[0]]+[u0%m for m in factors[4:]])
 T=crt([a2[1],t0%81,t0%125,a7[1]]+[t0%m for m in factors[4:]])
 assert norm(c,U,T)%M==0
 res.append(dict(index=i,u=str(U),t=str(T),two_branches=counts2,seven_singular_counts=counts7))
assert len(res)==53 and len(fail2)==29 and fail7==singular==[2,24]
print('PASS: 53/53 modulo',M,'old 2-adic dead ends',len(fail2),'old 7-adic dead ends',len(fail7))
print('82/135 all-scale excluded; 53 unresolved; original 22D Wall not replayed; root 19 OPEN.')
