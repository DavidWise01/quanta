#!/usr/bin/env python3
"""RQT-419: exact integral congruence on the full RQT-401 candidate-successor Gram.
Usage: python research/rqt419-congruence.py FULL_RQT401.json
"""
import argparse,json
from pathlib import Path
import sympy as s
def score(M):
 return sum(abs(int(M[i,j])).bit_length() for i in range(M.rows) for j in range(i,M.cols))
def audit(source):
 Q=s.Matrix([[int(v) for v in row] for row in source['restricted_Gram']])
 assert Q.shape==(3,3) and Q==Q.T and all(int(v)%2==0 for v in Q)
 H=s.diag(1,1,1,1);H[:3,:3]=Q/2
 U=s.Matrix([[-9,-25,0,0],[-5,-14,0,0],[0,0,1,0],[0,0,0,1]])
 assert U.det()==1
 Hnew=U.T*H*U
 assert Hnew==Hnew.T and Hnew!=H
 assert score(H)==7054 and score(Hnew)==7016
 def inertia(M):
  signs=[s.sign(M[:k,:k].det()) for k in range(1,5)]
  assert all(signs)
  piv=[signs[0]]+[signs[k]*signs[k-1] for k in range(1,4)]
  return [sum(a==1 for a in piv),sum(a==-1 for a in piv)]
 assert inertia(H)==inertia(Hnew)==[2,2]
 positive_vector=[int(x) for x in U[:,1]]
 positive_norm=int((s.Matrix(positive_vector).T*H*s.Matrix(positive_vector))[0])
 assert positive_norm>0
 for v in [[1,0,0,0],[0,1,0,0],[1,1,1,1],[3,-2,7,1]]:
  t=s.Matrix(v)
  assert (t.T*Hnew*t)[0]==((U*t).T*H*(U*t))[0]
 return {'RQT':419,'status':'PASS exact integral congruence',
         'U':U.tolist(),'det_U':1,'score_definition':'sum bit_lengths of 10 upper-triangular entries',
         'score_before':7054,'score_after':7016,'inertia_positive_negative':[2,2],
         'positive_vector_in_original_coordinates':positive_vector,
         'positive_vector_norm':str(positive_norm),
         'identity':'t.T Hnew t = (U t).T H (U t) for every integer t',
         'explicit_rational_witness':'NOT FOUND','root19':'OPEN',
         'root18_position':'UNVERIFIED',
         'visual_correction':'JPG incorrectly shows signature (1,3); exact signature is (2,2)'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--out')
 a=p.parse_args();r=audit(json.loads(Path(a.full_rqt401_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
