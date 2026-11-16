#!/usr/bin/env python3
"""RQT-418 exact Smith invariants for homogenized candidate successor form.
Input: full RQT-401 JSON with restricted_Gram. Smith equivalence is
NOT an integer congruence diagonalization of a quadratic form.
"""
import argparse,itertools,json
from pathlib import Path
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

def audit(data):
 Q=s.Matrix([[int(x) for x in row] for row in data['restricted_Gram']])
 assert Q.shape==(3,3) and Q==Q.T and all(int(x)%2==0 for x in Q)
 A=Q/2
 H=s.diag(1,1,1,1);H[:3,:3]=A
 S=smith_normal_form(H,domain=ZZ)
 inv=[abs(int(S[i,i])) for i in range(4)]
 determinant=abs(int(H.det()))
 assert inv[:3]==[1,1,9] and 9*inv[3]==determinant
 assert all(inv[i+1]%inv[i]==0 for i in range(3))
 assert determinant.bit_length()==3512
 arr=[[int(A[i,j]) for j in range(3)] for i in range(3)]
 counts={}
 for d in range(9):
  count=primitive=0
  for v in itertools.product(range(9),repeat=3):
   q=sum(arr[i][j]*v[i]*v[j] for i in range(3) for j in range(3))
   if (q+d*d)%9==0:
    count+=1
    if not all(t%3==0 for t in (*v,d)):primitive+=1
  counts[str(d)]={'all':count,'primitive_mod3':primitive}
 assert [counts[str(d)]['all'] for d in range(9)]==[243,162,162,243,162,162,243,162,162]
 assert [counts[str(d)]['primitive_mod3'] for d in range(9)]==[216,162,162,216,162,162,216,162,162]
 return {'RQT':418,'status':'PASS exact homogenized Smith invariants',
  'homogeneous_form':'H=diag(A,1), A=Q/2; (w,d)^T H(w,d)=0',
  'invariant_factor_magnitudes_first_three':inv[:3],
  'last_invariant':'abs(det(A))/9','det_bits':determinant.bit_length(),
  'mod9_denominator_residue_counts':counts,
  'scope':'Integer presentation invariants, NOT congruence diagonalization or isotropic witness',
  'rational_witness':'NOT CONSTRUCTED','root19':'OPEN','position18':'UNVERIFIED'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--out')
 a=p.parse_args();r=audit(json.loads(Path(a.full_rqt401_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
