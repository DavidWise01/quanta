#!/usr/bin/env python3
"""RQT-358: exact conductor-six normalization of RQT-357 norm equation."""
import json
from math import gcd
from functools import reduce
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
F=s.Matrix([
[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
cases=[(194,195,[[1,3,1],[-25,-74,-24],[113,340,113]]),
       (201,202,[[1,2,1],[-26,-51,-25],[117,235,117]])]
rows=[]
for m,n,Vdata in cases:
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 V=s.Matrix(Vdata);assert abs(V.det())==1
 A=V.T*T.T*F*T*V
 p,q,r=-int(A[0,0]),-int(A[0,2]),-int(A[2,2])
 g0,g1=int(A[0,1]),int(A[2,1])
 D=p*r-q*q;gamma=p*g1-q*g0;N=int(A.det())
 assert p>0 and D>0 and N>0
 S=s.Matrix([[p,-g0,q],[0,-gamma,D],[0,1,0]])
 assert abs(int(S.det()))==p*D
 assert S.applyfunc(lambda v:int(v)%6)==s.Matrix([[0,1,0],[0,0,0],[0,1,0]])
 snf=smith_normal_form(S,domain=ZZ)
 assert [abs(int(snf[i,i])) for i in range(3)]==[1,6,p*D//6]
 assert reduce(gcd,[p,q,D,gamma,g0+1])==6
 R=s.diag(s.Rational(1,6),s.Rational(1,6),1)*s.Matrix([[1,0,-1],[0,1,0],[0,0,1]])*S
 assert all(t.q==1 for t in R)
 assert abs(int(R.det()))==p*D//36
 assert D%3==0 and (p*N-D)%36==0
 K=(p*N-D)//36
 X,Y,h=s.symbols('X Y h',integer=True)
 normalized=D*X**2+(D//3)*X*h+Y**2-K*h**2
 assert s.expand(36*normalized-(D*(h+6*X)**2+36*Y**2-p*N*h**2))==0
 x,hh,y=s.symbols('x hh y',integer=True);z=s.Matrix([x,hh,y]);t=R*z
 assert s.expand(36*normalized.subs({X:t[0],Y:t[1],h:t[2]})+p*D*(z.T*A*z)[0])==0
 rows.append({'slope':f'{m}/{n}','S_smith':[str(1),str(6),str(p*D//6)],
 'six_congruences':['M=0 (mod 6)','L=h (mod 6)'],
 'D':str(D),'D_over_3':str(D//3),'K':str(K),
 'normalized_equation':'D*X^2+(D/3)*X*h+Y^2=K*h^2',
 'integral_map_R':[[int(v) for v in row] for row in R.tolist()],
 'image_index':str(p*D//36),
 'membership':'(X,Y,h) must lie in R Z^3 to reconstruct integers'})
print(json.dumps({'status':'PASS exact norm conductor and image lattice',
'original_source':'stoicheion RQT242 F4','planes':rows,
'exact_isotropic_u':'OPEN','roots18_to21':'OPEN'},indent=2))
