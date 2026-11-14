#!/usr/bin/env python3
"""RQT-360 exact squarefree quadratic norm fields. No original root asserted."""
import json
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
cases=[(194,195,[[1,3,1],[-25,-74,-24],[113,340,113]]),(201,202,[[1,2,1],[-26,-51,-25],[117,235,117]])]
rows=[]
for m,n,Vdata in cases:
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 V=s.Matrix(Vdata);assert abs(V.det())==1
 A=V.T*T.T*F*T*V
 p,q,r=-int(A[0,0]),-int(A[0,2]),-int(A[2,2])
 g0,g1=int(A[0,1]),int(A[2,1])
 D=p*r-q*q;gamma=p*g1-q*g0;N=int(A.det())
 assert p>0 and D>0 and N>0
 factors=s.factorint(D)
 assert all(s.isprime(k) for k in factors)
 c=int(s.prod(k**(e//2) for k,e in factors.items()))
 delta=int(s.prod(k**(e%2) for k,e in factors.items()))
 assert D==c*c*delta
 neg=-delta;disc=neg if neg%4==1 else 4*neg
 for x,h,y in [(0,1,0),(3,7,-2),(-11,17,19)]:
  L=p*x+q*y-g0*h;M=D*y-gamma*h;B=c*L
  z=s.Matrix([x,h,y])
  assert M*M+delta*B*B-p*N*h*h==-p*D*int((z.T*A*z)[0])
  assert B%c==0 and (M+gamma*h)%D==0
  yr=(M+gamma*h)//D
  assert yr==y and (L+g0*h-q*yr)%p==0
  assert (L+g0*h-q*yr)//p==x
  assert M%6==0 and (L-h)%6==0
 rows.append({'slope':f'{m}/{n}','D':str(D),'factorization':{str(k):e for k,e in sorted(factors.items())},
 'square_multiplier':c,'squarefree_delta':str(delta),
 'field_discriminant':str(disc),
 'ramified_primes':[str(k) for k in sorted(s.factorint(abs(disc)))],
 'norm_equation':'M^2+delta*B^2=p*N*h^2',
 'membership_gates':['B mod c = 0','(M+gamma*h) mod D = 0',
 '(B/c+g0*h-q*(M+gamma*h)/D) mod p = 0'],
 'exact_integral_witness':'OPEN'})
assert [r['square_multiplier'] for r in rows]==[2,18]
print(json.dumps({'status':'PASS exact squarefree norm descent',
 'source':'authentic stoicheion RQT-242 F4','planes':rows,
 'roots18_to21':'OPEN'},indent=2))
