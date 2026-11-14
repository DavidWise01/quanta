#!/usr/bin/env python3
"""RQT-344 exact original-lattice real cone and integer-slope exclusion."""
import json
from itertools import product
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],
[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],
[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],
[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
assert H.det()==1 and H+H.T==-F
A=F.extract([0,2],[0,2])
B=F.extract([0,2],[1,3])
C=F.extract([1,3],[1,3])
K=A-B*C.inv()*B.T
assert C[0,0]<0 and C.det()>0 and K.det()<0
assert all(K[i,j]<0 for i,j in ((0,0),(0,1),(1,1)))
k=s.symbols('k',real=True)
P=s.expand((s.Matrix([-k,1]).T*K*s.Matrix([-k,1]))[0])
assert s.diff(P,k,2)<0
assert P.subs(k,0)<0 and s.diff(P,k).subs(k,0)>0
assert P.subs(k,2)<0 and s.diff(P,k).subs(k,2)<0
assert P.subs(k,1)>0
T=s.Matrix([[-1,0,0],[0,1,0],[1,0,0],[0,0,1]])
G=T.T*F*T
a,b,c,d,e,f=[int(G[i,j])%25 for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))]
primitive=0
for x,y,z in product(range(25),repeat=3):
 if x%5==y%5==z%5==0:continue
 if (a*x*x+b*y*y+c*z*z+2*(d*x*y+e*x*z+f*y*z))%25==0:primitive+=1
assert primitive==0
L=s.Rational(19893,20000);R=s.Rational(2503,2500)
assert P.subs(k,L)<-s.Rational(2,5011**2)
assert P.subs(k,R)<-s.Rational(2,5011**2)
assert s.diff(P,k).subs(k,L)>0 and s.diff(P,k).subs(k,R)<0
print(json.dumps({'status':'PASS exact real cone and all-integer-k exclusion',
'source':'original stoicheion RQT-242 F4/H4',
'negative_transverse':'x1,x3',
'integer_k_other_than_1':'negative definite',
'k1_mod25_primitive_solutions':primitive,
'rational_null_in_any_integer_k_plane':False,
'necessary_rational_slope':'19893/20000 < -x0/x2 < 2503/2500',
'nonzero_isotropic_x0_plus_x2':True,
'norm_minus2_slope_conditional':'same window, if |x2|>=5011 (prior result)',
'root18':'OPEN','roots19_to21':'OPEN'},indent=2))
