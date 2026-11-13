#!/usr/bin/env python3
"""RQT-330: AUTHENTIC frozen F4/H4 recovered from stoicheion RQT-242.
Source repository: DavidWise01/stoicheion
Source path: research/rqt/rqt242_mod4_audit.py
Source blob SHA: 11d4d1102ec450fd9bfba869ee9be261dc0490a4
Root 18 through 21 remain OPEN; do not substitute bridge matrices.
"""
import sympy as s
import json
from itertools import product
from math import gcd

F=s.Matrix([["-4523390658618420908","2239380521691398176","-2422224054680331217","-3109472006028867029"],["2239380521691398176","-6703602364620082676","-1185189370853509030","4418426561730616356"],["-2422224054680331217","-1185189370853509030","-5270086080008383040","4649693842155823637"],["-3109472006028867029","4418426561730616356","4649693842155823637","-12373412455412906476"]])
H=s.Matrix([["2261695329309210454","-1051245631696015003","1175645097188971547","1627042015946053765"],["-1188134889995383173","3351801182310041338","491285385866907237","-2161158408172372287"],["1246578957491359670","693903984986601793","2635043040004191520","-2244501232348113591"],["1482429990082813264","-2257268153558244069","-2405192609807710046","6186706227706453238"]])
I=s.eye(4)
assert F==F.T and H.det()==1 and H+H.T==-F
D=I+H.inv()*F
assert D.det()==1 and D.T*F*D==F and (D-I).rank()==4
L,W=F.LDLdecomposition(hermitian=False)
inertia=[int(s.sign(v)) for v in W.diagonal()]
assert inertia==[-1,-1,-1,1]
positive=L.T.inv()*s.Matrix([0,0,0,1])
den=s.ilcm(*(z.q for z in positive))
e=positive*den
q=lambda z:(z.T*F*z)[0]
pair=(e.T*F*D*e)[0]
assert q(e)>0 and pair>0
m2=lambda M:M.applyfunc(lambda a:int(a)%2)
assert m2(D**3)==I and m2(D)!=I and m2(D**2)!=I
assert m2(D)==s.Matrix([[0,0,0,1],[1,1,1,0],[1,0,0,0],[0,0,1,0]])
# Since (D-I)=H^-1 F and det H=1, det(D-I)=det F.
# Symmetrized rank-drop form collapses to -(det F)/2 F, 
# so any norm-2 root triggers rational rank drop.
E=D-I
assert E.det()==F.det()
B=(F*E.adjugate()+E.adjugate().T*F)/2
assert B==-(F.det()/2)*F
parities={"0111","1001","1110"}
candidates=0;roots=[]
for r in product(range(-3,4),repeat=4):
    if ''.join(str(x%2) for x in r) not in parities:continue
    candidates+=1
    v=s.Matrix(r)
    if q(v)!=-2:continue
    if gcd(*(int(z) for z in F*v))!=1:continue
    assert ((I+v*(v.T*F))*D-I).rank()==3
    roots.append(list(r))
print(json.dumps({
"status":"AUTHENTIC_FROZEN_SOURCE_VERIFIED",
"source_repo":"DavidWise01/stoicheion",
"source_path":"research/rqt/rqt242_mod4_audit.py",
"source_blob_sha":"11d4d1102ec450fd9bfba869ee9be261dc0490a4",
"gram_determinant":str(F.det()),
"wall_determinant":int(H.det()),
"residual_determinant":int(D.det()),
"signature":{"positive":1,"negative":3},
"moving_rank":int((D-I).rank()),
"binary_order":3,
"positive_cone":"PRESERVED; time-orientation obstruction ABSENT",
"orientation_pairing_sign":int(s.sign(pair)),
"rank_drop_quadratic":"B=-(det F)/2 * F (automatic for norm -2)",
"bounded_height":3,"parity_candidates_tested":candidates,
"integral_roots_found_in_bounded_box":roots,
"unbounded_root18":"OPEN",
"roots19_20_21":"OPEN",
"note":"No bounded negative result excludes larger integer roots."
},indent=2))
