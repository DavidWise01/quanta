#!/usr/bin/env python3
"""RQT-338: exact combined height-cone gate for authentic RQT-242 frozen F4.
Previous height exclusions are source inputs, NOT rerun here.
Original roots 18–21 remain OPEN.
"""
import json
import sympy as s
F=s.Matrix([
[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([
[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],
[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],
[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],
[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
assert H.det()==1 and H+H.T==-F
D=s.eye(4)+H.inv()*F
assert D.det()==1 and D.T*F*D==F
# New integral coordinate basis z=(x2,y0,x0,-13*x1-10*x3)
U=s.Matrix([[0,0,1,0],[-24,-22,-17,-17],[1,0,0,0],[0,-13,0,-10]])
assert U.det()==1
J=U.inv().T*F*U.inv()
N=J[2:4,2:4]
assert N[0,0]<0 and N.det()>0
K=s.simplify(J[:2,:2]-J[:2,2:4]*N.inv()*J[2:4,:2])
assert K==(U[:2,:]*F.inv()*U[:2,:].T).inv()
assert all(K[i,j]<0 for i in (0,1) for j in (0,1))
assert K.det()<0
# Schur completion yields exact q(x) <= (x2,y0)^T K (x2,y0).
# For target q=0 or -2 and preexisting |x2|>=5001, the ratio
# t=y0/x2 must lie strictly in (-63/250, -2/125).
t=s.symbols('t', real=True)
P=s.expand(K[0,0]+2*K[0,1]*t+K[1,1]*t*t)
lo=-s.Rational(63,250)
hi=-s.Rational(2,125)
assert lo<hi and K[1,1]<0
assert P.subs(t,lo)<-s.Rational(2,5001**2)
assert P.subs(t,hi)<-s.Rational(2,5001**2)
assert s.diff(P,t).subs(t,lo)>0
assert s.diff(P,t).subs(t,hi)<0
assert (K[0,0]*5001**2+2*K[0,1]*5001*1021+K[1,1]*1021**2)<-2
print(json.dumps({
 'status':'PASS exact RQT-338 original-lattice combined gate',
 'source':'DavidWise01/stoicheion research/rqt/rqt242_mod4_audit.py',
 'U':[[int(z) for z in row] for row in U.tolist()],
 'det_U':int(U.det()),
 'transverse_negative_definite':True,
 'projection_K':[[str(z) for z in row] for row in K.tolist()],
 'necessary_for_norm_0_and_minus2':['abs(x2)>=5001','x2*y0<0',
   '-63/250<y0/x2<-2/125'],
 'additional_prior_root_bound':'abs(y0)>=1021 for norm -2',
 'roots_18_19_20_21':'OPEN',
 'note':'Previously published height exclusions were not replayed here.'
},indent=2))
