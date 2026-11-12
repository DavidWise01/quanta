#!/usr/bin/env python3
"""RQT-325: primitive integral rays of bridge-lattice tangent cone.
No claim to classify lattice-isometry orbits or solve frozen root 18.
"""
from collections import Counter
from functools import reduce
from math import gcd
import json
import sympy as s

F=s.Matrix([[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]])
X=s.Matrix([[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]])
I=s.eye(4);p=s.Matrix([1,0,0,1])
D=X-I; B=(F*D.adjugate()+D.adjugate().T*F)/2
assert B==-6*F and D.det()==12 and X.T*F*X==F
q=lambda M,v:s.expand((v.T*M*v)[0])
mod2=lambda M:M.applyfunc(lambda z:int(z)%2)
assert mod2(X**3)==I and mod2(X)!=I and mod2(X**2)!=I

def raw(m,n):
    return (2*m*n,4*m*n,6*m*m+n*n,6*m*m-n*n+2*m*n)

def primitive(v):
    g=reduce(gcd,map(abs,v))
    assert g>0
    u=tuple(x//g for x in v)
    # orientation is irrelevant for affine lines p+2k*u
    for x in u:
        if x:
            return (tuple(-z for z in u) if x<0 else u),g
    raise ValueError('zero direction')

def verify_ray(u):
    vec=s.Matrix([2*z for z in u])
    assert (p.T*F*vec)[0]==0 and q(F,vec)==0
    assert (p.T*B*vec)[0]==0 and q(B,vec)==0
    for k in (-3,-2,-1,0,1,2,3):
        r=p+k*vec
        assert q(F,r)==-2 and q(B,r)==D.det()
        assert int(s.gcd_list(list(F*r)))==1
        assert [int(z)%2 for z in r]==[1,0,0,1]
        Y=(I+r*(r.T*F))*X
        assert (Y-I).rank()==3 and mod2(Y**2)==I and mod2(Y)!=I

pairs=[]
by_ray={}
gcds=Counter()
for m in range(-8,9):
    for n in range(-8,9):
        if (m,n)==(0,0) or gcd(m,n)!=1:continue
        ray,g=primitive(raw(m,n))
        gcds[g]+=1
        by_ray.setdefault(ray,[]).append((m,n))
        pairs.append((m,n))
assert len(pairs)==176 and len(by_ray)==88
assert all(len(pre)==2 and pre[1]==(-pre[0][0],-pre[0][1]) for pre in by_ray.values())
assert sum(u[0]!=0 for u in by_ray)==86
for u in by_ray:verify_ray(u)
print(json.dumps({'status':'PASS','primitive_coprime_parameter_pairs':len(pairs),
 'unoriented_primitive_rays':len(by_ray),'non_old_slice_rays':86,
 'raw_content_distribution':dict(sorted(gcds.items())),
 'replayed_root_tests':len(by_ray)*7,
 'sample_primitive_even_directions':[list(map(lambda x:2*x,u)) for u in list(by_ray)[:5]],
 'guarantee':'Every rational isotropic ray has a primitive integer representative; its parity-compatible vectors are exactly the even multiples of this representative.',
 'limits':'Isometry-orbit classification not established; original frozen root-18 remains open.'},indent=2))
