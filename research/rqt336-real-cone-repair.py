#!/usr/bin/env python3
"""RQT-336 exact real obstruction and repaired local CRT in original RQT-242 F4."""
import itertools,json
from math import gcd
import sympy as s
from sympy.ntheory.modular import crt
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
D=s.eye(4)+H.inv()*F
assert D.det()==1 and D.T*F*D==F
q=lambda u:int((u.T*F*u)[0]//2)
bil=lambda u,v:int((u.T*F*v)[0])
N=F.extract([0,1,3],[0,1,3])
minors=[int(N[:k,:k].det()) for k in (1,2,3)]
assert [int(s.sign(z)) for z in minors]==[-1,1,-1]
# Hence q(a,b,0,d)<0 for all nonzero real (a,b,d).
e=s.eye(4)[:,0]
def lift(seed,p,n):
 u=s.Matrix(seed)
 assert u[2]!=0 and q(u)%p==0 and bil(u,e)%p!=0
 for k in range(1,n):
  power=p**k
  digit=(-q(u)//power*pow(bil(u,e),-1,p))%p
  u[0]+=digit*power
  assert q(u)%(p*power)==0
 return u
m2=2**256;m3=3**128;M=m2*m3
u2=lift([0,0,1,0],2,256)
u3=lift([0,1,1,1],3,128)
u=s.Matrix([int(crt([m2,m3],[int(u2[i])%m2,int(u3[i])%m3])[0]) for i in range(4)])
assert u[2]!=0 and q(u)%M==0 and gcd(bil(u,e),M)==1
wanted={(0,1,1,1),(1,0,0,1),(1,1,1,0)}
choices=[]
for bits in itertools.product((0,1),repeat=4):
 v=s.Matrix(bits)
 if bil(u,v)%2!=1:continue
 par=tuple(int(z)%2 for z in ((1+q(v))*u-v))
 if par in wanted:choices.append((bits,par))
assert choices
bits,par=choices[0]
v=s.Matrix(bits)
delta=(((1-bil(u,v))//2)*pow(bil(u,e),-1,M//2))%(M//2)
v[0]+=2*delta
assert bil(u,v)%M==1
w=v-q(v)*u;r=u-w
assert q(w)%M==0 and (bil(u,w)-1)%M==0
assert (bil(r,r)+2)%M==0 and tuple(int(z)%2 for z in r)==par
Z=((s.eye(4)+r*(r.T*F))*D).applyfunc(lambda a:int(a)%2)
assert Z**2==s.eye(4) and Z!=s.eye(4) and (Z-s.eye(4)).rank()==1
assert q(u)!=0 and bil(r,r)!=-2
print(json.dumps({'scope':'AUTHENTIC RQT-242 F4/H4','negative_hyperplane':'x2=0',
 'leading_minors':[str(z) for z in minors],
 'RQT335_limitation':'fixed x2=0 gives impossible exact real isotropy',
 'new_local_seeds':[[0,0,1,0],[0,1,1,1]],
 'modulus':'2^256*3^128','u_x2':str(u[2]),
 'u_parity':''.join(str(int(z)%2) for z in u),
 'r_parity':''.join(map(str,par)),
 'local_q_u_modM':q(u)%M,'local_root_norm_plus2_modM':(bil(r,r)+2)%M,
 'exact_isotropic':False,'exact_root18':False,'roots19_to21':'OPEN'},indent=2))
