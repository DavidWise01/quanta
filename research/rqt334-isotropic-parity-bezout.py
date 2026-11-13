#!/usr/bin/env python3
"""RQT-334: exact admissible parity for primitive isotropic splits of authentic F4.
Conditional theorem; does NOT construct an actual integral isotropic vector or root18.
"""
import itertools,json
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert F==F.T and F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
assert H.det()==1 and H+H.T==-F
D=s.eye(4)+H.inv()*F
assert D.det()==1 and D.T*F*D==F
q=lambda v:int((s.Matrix(v).T*F*s.Matrix(v))[0]//2)
bil=lambda u,v:int((s.Matrix(u).T*F*s.Matrix(v))[0])
bit=lambda u:''.join(map(str,u))
classes=[u for u in itertools.product((0,1),repeat=4) if q(u)%2==0 and any(int(t)%2 for t in F*s.Matrix(u))]
assert len(classes)==6
wanted={'0111','1001','1110'}
seeds={}
for u in classes:
 choices=[]
 for vv in itertools.product((0,1),repeat=4):
  if bil(u,vv)%2!=1:continue
  rr=tuple((int(vv[i])+(1+q(vv))*int(u[i]))%2 for i in range(4))
  if bit(rr) in wanted:choices.append({'partner_parity':bit(vv),'root_parity':bit(rr)})
 assert len(choices)==4 and len({z['root_parity'] for z in choices})==2
 seeds[bit(u)]=choices
assert sum(len(z) for z in seeds.values())==24
assert {z['root_parity'] for x in seeds.values() for z in x}==wanted
# Symbolic hyperbolic-plane witness (formal pairing u²=0,u·v=1,v²=2t)
t=s.symbols('t',integer=True)
U=s.Matrix([1,0]); V=s.Matrix([0,1]); G=s.Matrix([[0,1],[1,2*t]])
W=V-t*U;R=U-W
assert (U.T*G*U)[0]==0 and (U.T*G*W)[0]==1
assert s.expand((W.T*G*W)[0])==0 and s.expand((R.T*G*R)[0])==-2
assert s.expand((U.T*G*R)[0])==-1
print(json.dumps({'status':'PASS exact conditional parity/Bezout gate',
 'source':'DavidWise01/stoicheion RQT-242 authentic F4/H4',
 'isotropic_mod2_classes':len(classes),'class_to_partners':seeds,
 'compatible_pairs':24,'targets_each_u':2,
 'construction':'For actual u norm0 div1, choose candidate vbar with <u,vbar> odd; lift v=vbar+2z with <u,v>=1. Then w=v-(v²/2)u and r=u-w are integral, w²=0, r²=-2, gcd(Fr)=1.',
 'actual_u':'OPEN','actual_root18':'OPEN','roots19_to21':'OPEN'},indent=2))
