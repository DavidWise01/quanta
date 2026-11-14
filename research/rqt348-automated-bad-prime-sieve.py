#!/usr/bin/env python3
"""RQT-348: bounded bad-prime certificates; original frozen F4, no root asserted."""
import json
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
primes=list(s.primerange(3,20000))
def certify(G,p,det):
 if det%p or det%(p*p)==0:return None
 a,b,c=map(int,(G[0,0],G[0,1],G[1,1]))
 minor=(a*c-b*b)%p
 if not minor or pow(-minor%p,(p-1)//2,p)!=p-1:return None
 e,f=int(G[0,2])%p,int(G[1,2])%p
 inv=pow(minor,-1,p)
 v=s.Matrix([(-(c*e-b*f)*inv)%p,(-(-b*e+a*f)*inv)%p,1])
 assert all(int(z)%p==0 for z in G*v)
 Q=int((v.T*G*v)[0])
 assert Q%p==0 and Q%(p*p)!=0
 return {'prime':p,'radical_mod_p':list(map(int,v)),'norm_over_p_mod_p':Q//p%p}
rows=[]
for d,lo,hi in [(-1,188,205),(1,837,851)]:
 for n in range(lo,hi):
  m=n+d;T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
  G=T.T*F*T;det=int(G.det())
  found=[c for p in primes if (c:=certify(G,p,det)) is not None]
  rows.append({'slope':f'{m}/{n}','certificates':found,'status':'EXCLUDED' if found else 'INCONCLUSIVE'})
assert len(rows)==31 and sum(r['status']=='EXCLUDED' for r in rows)==16
assert sum(r['status']=='INCONCLUSIVE' for r in rows)==15
assert any(r['slope']=='189/190' and any(c['prime']==17 for c in r['certificates']) for r in rows)
assert any(r['slope']=='838/837' and any(c['prime']==83 for c in r['certificates']) for r in rows)
print(json.dumps({'status':'PASS exact bounded obstruction scan','prime_limit_exclusive':20000,
 'tested':31,'excluded':16,'inconclusive':15,'results':rows,
 'source':'authentic RQT-242 Gram','roots18_to21':'OPEN'},indent=2))
