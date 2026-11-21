#!/usr/bin/env python3
"""RQT-539: exact rank-one ambiguity; NOT authentic lattice transport."""
from math import gcd
a=(-183,-198,174,572,-368,-188)
b=(-232,-246,223,729,-473,-242)
lam=(-198,183,0,0,0,0)
w=(1,-1)+ (0,)*20
dot=lambda u,v:sum(x*y for x,y in zip(u,v))
assert gcd(*a)==1
assert dot(lam,a)==0
assert dot(lam,b)==918
assert sum(w[:4])==0
# For any T, T'=T+w*lam^T maps a identically but maps b differently.
assert tuple(dot(lam,a)*v for v in w)==(0,)*22
assert tuple(dot(lam,b)*v for v in w)==(918,-918)+(0,)*20
print('PASS non-uniqueness from one known image; authentic transport remains unverified')
