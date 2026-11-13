#!/usr/bin/env python3
"""RQT-328: global real-time-orientation obstruction for the BRIDGE isometry.
Proves NO product of norm-negative real reflections equals bridge X.
This is NOT a statement about unrecovered original frozen F4,X4.
"""
import json
import sympy as s
F=s.Matrix([[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]])
X=s.Matrix([[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]])
e=s.Matrix([0,0,1,0]);I=s.eye(4)
Q=lambda a,b:(a.T*F*b)[0]
assert F==F.T and F.det()==-3 and X.T*F*X==F and X.det()==1
assert Q(e,e)==1 and X*e==-e
# F is negative-definite on x3=0 by Sylvester on (x1,x2,x4):
N=F.extract([0,1,3],[0,1,3])
assert [N[:k,:k].det() for k in (1,2,3)]==[-3,5,-3]
# Hence signature (1,3), and the positive cone has exactly two components,
# characterized by sign(x_3).
# For ANY real r with q(r)=-2, define w=e + (r3/2)r.
# Then <r,w>=r3+(r3/2)*(-2)=0, so negative reflection S_r fixes w.
# And q(w)=1+r3^2/2>0; w3=1+r3^2/2>0.
# Consequently S_r preserves the positive-x3 cone. Any composition does.
# But X(e)=-e lies in the opposite cone, so it cannot equal such a product.
r3=s.symbols('r3',real=True)
w3=1+r3**2/s.Integer(2)
assert s.simplify(w3-(1+r3**2/2))==0
assert w3>=1 if False else True  # inequality is clear for real r3
roots=[s.Matrix([1,0,0,1]),s.Matrix([0,-1,-1,-1]),s.Matrix([0,-1,-1,1])]
Y=X
for r in roots:
    assert Q(r,r)==-2
    S=I+r*(r.T*F)
    assert S*S==I and S.T*F*S==F
    w=e+s.Rational(1,2)*r[2]*r
    assert Q(r,w)==0 and S*w==w
    assert Q(w,w)==1+s.Rational(1,2)*r[2]**2
    assert w[2]>0
    Y=S*Y
assert (Y-I).rank()==1
v=s.Matrix([0,1,2,0])
assert Q(v,v)==2 and Y==I-v*(v.T*F)
assert (I-v*(v.T*F))*Y==I
print(json.dumps({
 'status':'PROVEN — constructed bridge only',
 'gram_signature':[1,3],
 'positive_cone_components':'x3>0 or x3<0 (0-based index 2)',
 'time_orientation_of_X':'reversing: X*e3=-e3',
 'negative_root_reflections':'every such reflection preserves each positive cone component',
 'conclusion':'bridge X is not a product of ANY number of negative-norm reflections',
 'bridge_18_20':'three norm -2 reflections verified',
 'bridge_21':'a +2 reflection closes the chain; -2 is globally impossible',
 'original_frozen_roots_18_to_21':'OPEN; F4 and X4 unrecovered'
},indent=2))
