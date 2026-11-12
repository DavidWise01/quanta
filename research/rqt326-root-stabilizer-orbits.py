#!/usr/bin/env python3
"""RQT-326: exact certified subgroup orbits in the bridge lattice.

Two explicit integral isometries fixing p; NOT the full isometry group.
Frozen eighteenth-root problem remains OPEN.
"""
from collections import Counter
from functools import reduce
from math import gcd
import json
import sympy as s

F=s.Matrix([[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]])
X=s.Matrix([[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]])
I=s.eye(4);p=s.Matrix([1,0,0,1])
C=s.diag(1,1,-1,1)
T=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[2,0,0,-1]])
G=(I,C,T,C*T)
assert C*T==T*C and C*C==I and T*T==I
for M in G:
    assert M.T*F*M==F and M*p==p and abs(M.det())==1

def prim(v):
    g=reduce(gcd,(abs(int(x)) for x in v))
    assert g>0
    v=tuple(int(x)//g for x in v)
    first=next(x for x in v if x)
    return v if first>0 else tuple(-x for x in v)

def raw(m,n):
    return (2*m*n,4*m*n,6*m*m+n*n,6*m*m-n*n+2*m*n)

rays={prim(raw(m,n)) for m in range(-8,9) for n in range(-8,9)
      if (m,n)!=(0,0) and gcd(m,n)==1}
assert len(rays)==88

def apply(M,v):
    return prim(M*s.Matrix(v))

closure=set(rays)
for v in rays:
    closure.update(apply(M,v) for M in G)
assert len(closure)==150
orbits={frozenset(apply(M,v) for M in G) for v in closure}
sizes=Counter(map(len,orbits))
assert len(orbits)==38 and sizes==Counter({4:37,2:1})
assert {x for o in orbits for x in o}==closure
assert all(all(apply(M,v) in closure for M in G) for v in closure)
assert len({apply(M,v) for v in rays for M in G}-rays)==62
mod2=lambda M:M.applyfunc(lambda x:int(x)%2)
assert mod2(X**3)==I and mod2(X)!=I and mod2(X**2)!=I
verified=0
for v in sorted(closure):
    for k in range(-2,3):
        r=p+2*k*s.Matrix(v)
        assert (r.T*F*r)[0]==-2
        assert int(s.gcd_list(list(F*r)))==1
        assert [int(z)%2 for z in r]==[1,0,0,1]
        Y=(I+r*(r.T*F))*X
        assert (Y-I).rank()==3 and mod2(Y**2)==I and mod2(Y)!=I
        verified+=1
assert verified==750

example=(2,4,7,7)
example_orbit=sorted(frozenset(apply(M,example) for M in G))
assert len(example_orbit)==4
print(json.dumps({
  'status':'PASS — explicit isometry subgroup only',
  'base_rays':len(rays),
  'added_by_group_closure':len(closure)-len(rays),
  'closed_rays':len(closure),
  'subgroup_orbits':len(orbits),
  'orbit_sizes':dict(sorted(sizes.items())),
  'root_replay_checks':verified,
  'example_orbit':example_orbit,
  'caveat':'Does NOT classify the full integral isometry group and does NOT solve frozen root 18.'
},indent=2))
