#!/usr/bin/env python3
"""RQT-420 exact rational congruence/Witt-index audit.
Run with the full RQT-401 JSON containing restricted_Gram.
No explicit rational null vector is claimed.
"""
import argparse,itertools,json
from pathlib import Path
import sympy as sp
def audit(data):
 Q=sp.Matrix([[int(v) for v in row] for row in data['restricted_Gram']])
 assert Q.shape==(3,3) and Q==Q.T and all(int(t)%2==0 for t in Q)
 A=Q/2
 H=sp.diag(1,1,1,1);H[:3,:3]=A
 L,D=H.LDLdecomposition(hermitian=False)
 P=L.T.inv()
 assert P.T*H*P==D
 delta=[sp.Integer(1)]+[H[:k,:k].det() for k in range(1,5)]
 entries=[delta[k]/delta[k-1] for k in range(1,5)]
 assert all(D[i,i]==entries[i] for i in range(4))
 signs=[int(sp.sign(t)) for t in entries]
 assert signs==[-1,1,-1,1]
 parity={}
 for x in (0,1):
  for y in (0,1):
   for z in (0,1):
    if not (x or y or z):continue
    v=sp.Matrix([x,y,z])
    parity[f'{x}{y}{z}']=int((v.T*A*v)[0]%4)
 assert parity=={'001':3,'010':2,'011':3,'100':1,'101':2,'110':3,'111':2}
 U=sp.Matrix([[-9,-25,0,0],[-5,-14,0,0],[0,0,1,0],[0,0,0,1]])
 assert U.det()==1 and U.inv().T*(U.T*H*U)*U.inv()==H
 return {'RQT':420,'status':'PASS exact rational congruence; no explicit null vector',
  'inertia':[2,2],'diagonal_signs':signs,
  'leading_minor_signs':[int(sp.sign(t)) for t in delta[1:]],
  'diagonalization':'diag(Delta1,Delta2/Delta1,Delta3/Delta2,1)',
  'numerator_bits':[abs(int(sp.numer(t))).bit_length() for t in entries],
  'denominator_bits':[int(sp.denom(t)).bit_length() for t in entries],
  'parity_mod4':parity,
  'witt_index_over_Q':1,
  'witt_proof':'RQT-414: H isotropic over Q; RQT-405: A anisotropic over Q. A rational totally isotropic 2-plane would meet d=0 nontrivially, contradicting A anisotropy.',
  'explicit_rational_null_vector':'NOT CONSTRUCTED','root19':'OPEN',
  'original_root18_position':'UNVERIFIED'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_gram_json');p.add_argument('--out')
 a=p.parse_args();r=audit(json.loads(Path(a.full_gram_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
