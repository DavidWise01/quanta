#!/usr/bin/env python3
"""RQT-349: exact replay and extended discriminant-prime audit, authentic RQT-242 F4.
Requires rqt348-results.json in the same directory (full frozen input ledger).
No rational/isotropic or integral-root witness is claimed.
"""
import json
import sympy as s
F=s.Matrix([
[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172

def gram(n,d):
 T=s.Matrix([[-(n+d),0,0],[0,1,0],[n,0,0],[0,0,1]])
 return T.T*F*T
def cert(G,p):
 assert s.isprime(p)
 det=int(G.det())
 if det%p or det%(p*p)==0:return None
 a,b,c=map(int,(G[0,0],G[0,1],G[1,1]))
 h=(a*c-b*b)%p
 if not h or pow(-h%p,(p-1)//2,p)!=p-1:return None
 e,f=int(G[0,2])%p,int(G[1,2])%p
 inv=pow(h,-1,p)
 v=s.Matrix([(-(c*e-b*f)*inv)%p,(-(-b*e+a*f)*inv)%p,1])
 assert all(int(z)%p==0 for z in G*v)
 Q=int((v.T*G*v)[0])
 assert Q%p==0 and Q%(p*p)!=0
 return {'p':int(p),'radical':list(map(int,v)),'norm_over_p_mod_p':Q//p%p}
ledger=[]
oldprimes=list(s.primerange(3,20000))
for d,lo,hi in [(-1,188,205),(1,837,851)]:
 for n in range(lo,hi):
  G=gram(n,d)
  hits=[c for p in oldprimes if (c:=cert(G,p)) is not None]
  ledger.append({'slope':f'{n+d}/{n}','n':n,'d':d,'certificates':hits})
prior={'187/188':887773937,'839/838':159171641,'840/839':2316121}
primes=list(s.primerange(20000,100000))
results=[]
for row in ledger:
 G=gram(row['n'],row['d'])
 old=[]
 for c in row['certificates']:
  z=cert(G,c['p'])
  assert z==c,(row['slope'],z,c)
  old.append(z)
 source=[]
 if row['slope'] in prior:
  z=cert(G,prior[row['slope']]);assert z
  source.append(z)
 extended=[]
 if not old and not source:
  for p in primes:
   if (z:=cert(G,p)) is not None:
    extended.append(z)
    break
 status='EXCLUDED' if old or source or extended else 'OPEN_AFTER_BOUNDED_SIEVE'
 results.append({'slope':row['slope'],'status':status,
  'RQT348_certificates':old,'RQT347_recovered':source,'RQT349_new':extended})
assert len(results)==31
assert sum(bool(x['RQT348_certificates']) for x in results)==16
assert sum(bool(x['RQT347_recovered']) for x in results)==3
assert [(x['slope'],x['RQT349_new'][0]['p']) for x in results if x['RQT349_new']]==[
 ('845/844',35327),('849/848',38299)]
assert sum(x['status']=='EXCLUDED' for x in results)==21
out={'source':'authentic stoicheion RQT-242 F4','status':'PASS exact replay + extended scan',
 'primes':'20000<=p<100000 tested for previously inconclusive slopes',
 'excluded':21,'inconclusive':10,'results':results,
 'root18':'OPEN','roots19_to21':'OPEN'}
print(json.dumps(out,indent=2))
