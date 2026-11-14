#!/usr/bin/env python3
"""RQT-357: symbolic reversible norm equation on authentic RQT-242 F4.
This is a reduction, not an explicit rational isotropic witness.
"""
import json
from math import gcd
import sympy as s
F=s.Matrix([
[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
CASES=[(194,195,[[1,3,1],[-25,-74,-24],[113,340,113]]),
       (201,202,[[1,2,1],[-26,-51,-25],[117,235,117]])]
rows=[]
for m,n,Vlist in CASES:
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 V=s.Matrix(Vlist);assert abs(V.det())==1
 A=V.T*T.T*F*T*V
 p,q,r=-int(A[0,0]),-int(A[0,2]),-int(A[2,2])
 g0,g1=int(A[0,1]),int(A[2,1])
 D=p*r-q*q; gamma=p*g1-q*g0; N=int(A.det())
 assert p>0 and D>0 and N>0
 x,h,y=s.symbols('x h y',integer=True)
 L=p*x+q*y-g0*h; M=D*y-gamma*h
 z=s.Matrix([x,h,y]);Q=(z.T*A*z)[0]
 # For ANY integers x,h,y (not just isotropic coordinates).
 assert s.expand(D*L**2+M**2-p*N*h**2+p*D*Q)==0
 for xx,hh,yy in [(0,0,0),(1,1,2),(-3,7,9),(129,251,-47)]:
  lv=int(L.subs({x:xx,h:hh,y:yy}))
  mv=int(M.subs({x:xx,h:hh,y:yy}))
  assert (mv+gamma*hh)%D==0
  yy2=(mv+gamma*hh)//D
  assert (lv+g0*hh-q*yy2)%p==0
  xx2=(lv+g0*hh-q*yy2)//p
  assert (xx2,yy2)==(xx,yy)
  assert D*lv**2+mv**2-p*N*hh**2==-p*D*int(Q.subs({x:xx,h:hh,y:yy}))
 rows.append({'plane':f'{m}/{n}', 'p':str(p),'q':str(q),'r':str(r),
  'D':str(D),'g0':str(g0),'gamma':str(gamma),'N_detA':str(N),
  'gcd_D_gamma':gcd(D,gamma),'gcd_D_pN':gcd(D,p*N),
  'equation':'D*L^2+M^2=p*N*h^2',
  'reconstruction':'y=(M+gamma*h)/D; x=(L+g0*h-q*y)/p',
  'integrality_gates':['D divides M+gamma*h','p divides L+g0*h-q*y'],
  'integer_null_witness':'OPEN'})
print(json.dumps({'status':'PASS exact symbolic identity plus integral inverse',
 'source':'authentic stoicheion RQT-242 F4',
 'result':'Reduced the conic to quadratic norm with integrality gates',
 'planes':rows,'exact_root18':'OPEN','roots19_to21':'OPEN'},indent=2))
