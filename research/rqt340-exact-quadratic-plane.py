#!/usr/bin/env python3
"""RQT-340: authentic F4 Lorentzian 2-plane and 2-adic descent obstruction.
The algebraic null vector is over a quadratic extension, NOT over Q.
No integral root18 constructed.
"""
import json
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
N=lambda a,b:(a.T*F*b)[0]
p=s.Matrix([-9979,-1271,10000,5812])
A=N(p,p)
assert A>0
qraw=A*s.eye(4)[:,0]-N(p,s.eye(4)[:,0])*p
q=qraw/s.igcd(*list(qraw))
B=-N(q,q)
assert B>0 and N(p,q)==0
C=s.Integer(528280454887176328887138801371672078777)
assert s.Rational(A,B)==s.Rational(2,C) and C%2==1
# In span_Q(p,q), q_F(a*p+b*q)=A*a²-B*b².
# An isotropic rational vector requires (b/a)²=2/C.
# Since v_2(2/C)=1, this cannot be a rational square.
t=s.sqrt(s.Rational(2,C))
u=p+t*q
assert s.simplify(N(u,u))==0
assert s.simplify(N(p,u))==A
print(json.dumps({'status':'EXACT algebraic plane / rational obstruction',
 'source':'stoicheion original RQT-242 F4',
 'positive_vector':list(map(int,p)),'positive_norm':str(A),
 'negative_vector':list(map(int,q)),'negative_norm':str(-B),
 'pairing':int(N(p,q)),'ratio':'2/'+str(C),
 'rational_null_in_this_plane':'IMPOSSIBLE by odd 2-adic valuation',
 'quadratic_extension_null':'u=p+sqrt(2/C)*q',
 'rational_null_in_full_F4':'OPEN','original_root18':'OPEN','roots19_to21':'OPEN'},indent=2))
