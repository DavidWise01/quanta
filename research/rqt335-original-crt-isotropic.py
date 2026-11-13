#!/usr/bin/env python3
"""RQT-335: authentic F4, constructive local isotropic/root certificate.
Checks modulus 2**256 * 3**128. NOT an exact integer root18.
Requires SymPy.
"""
import json
import sympy as s
from sympy.ntheory.modular import crt
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
q=lambda a:int((a.T*F*a)[0]//2)
pair=lambda a,b:int((a.T*F*b)[0])
e0=s.eye(4)[:,0]
def lift(seed,prime,exponent):
    u=s.Matrix(seed)
    assert q(u)%prime==0 and pair(u,e0)%prime!=0
    for k in range(1,exponent):
        pk=prime**k
        digit=((-q(u)//pk)*pow(pair(u,e0),-1,prime))%prime
        u[0]+=digit*pk
        assert q(u)%(prime*pk)==0
    return u
m2=2**256;m3=3**128;M=m2*m3
u2=lift([0,0,0,1],2,256)
u3=lift([0,1,0,1],3,128)
u=s.Matrix([int(crt([m2,m3],[int(u2[i])%m2,int(u3[i])%m3])[0]) for i in range(4)])
assert q(u)%M==0 and pair(u,e0)%6 in (1,5)
assert [int(z)%2 for z in u]==[0,0,0,1]
assert [int(z)%3 for z in u]==[0,1,0,1]
v=s.Matrix([0,1,1,0]);assert pair(u,v)%2==1
# keep v parity, enforce <u,v> = 1 modulo M
t=(((1-pair(u,v))//2)*pow(pair(u,e0),-1,M//2))%(M//2)
v[0]+=2*t
assert pair(u,v)%M==1
w=v-q(v)*u
r=u-w
assert q(w)%M==0 and (pair(u,w)-1)%M==0
assert (pair(r,r)+2)%M==0 and [int(z)%2 for z in r]==[0,1,1,1]
S=s.eye(4)+r*(r.T*F)
Z=(S*D).applyfunc(lambda x:int(x)%2)
assert (Z-s.eye(4)).rank()==1 and Z**2==s.eye(4) and Z!=s.eye(4)
assert q(u)!=0 and pair(r,r)!=-2
print(json.dumps({
 'status':'LOCAL CRT CERTIFICATE; NOT AN INTEGRAL ROOT',
 'modulus':'2^256 * 3^128','source':'stoicheion RQT-242 F4/H4',
 'u_modM':[str(int(z)%M) for z in u],
 'root_r18_modM':[str(int(z)%M) for z in r],
 'q_u_modM':q(u)%M,'root_norm_plus2_modM':(pair(r,r)+2)%M,
 'root_parity':'0111','mod2_successor_order':2,'mod2_successor_rank':1,
 'exact_u_isotropic':False,'exact_r18_norm_minus2':False,
 'original_roots18_to21':'OPEN'},indent=2))
