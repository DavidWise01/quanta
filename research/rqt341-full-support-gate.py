#!/usr/bin/env python3
"""RQT-341: exact full-support gate on authentic RQT-242 frozen F4.
Proves all four coordinate hyperplanes negative definite and no norm -2.
No rational isotropic vector / integer root 18 constructed.
"""
import json
import sympy as s
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
out=[]
for omit in range(4):
 ids=[j for j in range(4) if j!=omit]
 P=-F.extract(ids,ids)
 minors=[int(P[:j,:j].det()) for j in (1,2,3)]
 assert all(m>0 for m in minors)
 bounds=[2*P.inv()[j,j] for j in range(3)]
 assert all(0<b<1 for b in bounds)
 out.append({'omitted_index':omit,
   'positive_principal_minors':[str(v) for v in minors],
   'coordinate_square_bounds':[str(v) for v in bounds],
   'nonzero_isotropic':'IMPOSSIBLE','integral_norm_minus2':'IMPOSSIBLE'})
print(json.dumps({'status':'VERIFIED on original frozen F4',
 'source':'DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py',
 'full_support_necessary':True,'planes':out,
 'root18':'OPEN','roots19_to21':'OPEN'},indent=2))
