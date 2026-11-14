#!/usr/bin/env python3
"""RQT-347: exact discriminant-prime obstruction on authentic RQT-242 F4."""
import json
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
def certify(n,d,p):
 assert s.isprime(p)
 T=s.Matrix([[-(n+d),0,0],[0,1,0],[n,0,0],[0,0,1]])
 G=T.T*F*T
 det=int(G.det())
 assert det%p==0 and det%(p*p)!=0
 a,b,c=[int(G[i,j])%p for i,j in ((0,0),(0,1),(1,1))]
 minor=(a*c-b*b)%p
 assert minor and pow(-minor%p,(p-1)//2,p)==p-1
 r0,r1=[int(G[i,2])%p for i in (0,1)]
 inv=pow(minor,-1,p)
 v=s.Matrix([(-(c*r0-b*r1)*inv)%p,(-(-b*r0+a*r1)*inv)%p,1])
 assert all(int(q)%p==0 for q in G*v)
 Q=int((v.T*G*v)[0])
 assert Q%p==0 and Q%(p*p)!=0
 return {'slope':f'{n+d}/{n}','prime':p,
 'det_valuation':1,'negative_minor_legendre':-1,
 'radical_mod_p':[int(z) for z in v],
 'radical_Q_over_p_mod_p':Q//p%p,
 'primitive_null_mod_p2':False}
results=[certify(188,-1,887773937),
certify(838,1,159171641),
certify(839,1,2316121)]
assert [r['radical_Q_over_p_mod_p'] for r in results]==[459468411,1677429,1268829]
print(json.dumps({'status':'PASS exact prime-square obstruction',
'result':results,'integer_root18':'OPEN','roots19_to21':'OPEN'},indent=2))
