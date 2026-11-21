#!/usr/bin/env python3
"""RQT-542 primitive-pair audit: exact 6D historical coordinates.
Basis-related checks are in the full local conversation artifact rqt542.py.
"""
from math import gcd
a=(-183,-198,174,572,-368,-188)
b=(-232,-246,223,729,-473,-242)
minors=[a[i]*b[j]-a[j]*b[i] for i in range(6) for j in range(i+1,6)]
assert len(minors)==15
assert gcd(*a)==gcd(*b)==gcd(*minors)==1
print('PASS: primitive rank-two historical pair in Z^6')
print('Branch-2 ambient transport still PENDING: do not infer U from this test.')
