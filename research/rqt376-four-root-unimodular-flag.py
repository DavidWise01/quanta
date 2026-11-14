#!/usr/bin/env python3
"""RQT-376: exact unimodularity theorem / prefix-minor certificate for roots 18..21."""
import argparse,itertools,json
import sympy as s
from math import gcd
from functools import reduce
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
def minor_gcd(R):
 k=R.cols
 return reduce(gcd,(abs(int(R[list(rows),:].det())) for rows in itertools.combinations(range(4),k)),0)
def check(roots,gram=F,wall=H):
 assert 1<=len(roots)<=4 and all(len(r)==4 for r in roots)
 R=s.Matrix.hstack(*(s.Matrix(r) for r in roots))
 norms=[int((R[:,i].T*gram*R[:,i])[0]) for i in range(R.cols)]
 W=R.T*wall*R
 lower=[int(W[j,i]) for j in range(R.cols) for i in range(j)]
 minors=[minor_gcd(R[:,:k]) for k in range(1,R.cols+1)]
 result={'norms':norms,'lower_Wall_pairings':lower,'prefix_maximal_minor_gcd':minors,
         'norm_gate':all(n==-2 for n in norms),'Wall_gate':all(n==0 for n in lower),
         'primitive_prefixes':all(n==1 for n in minors),
         'first_parity':''.join(str(int(n)%2) for n in roots[0])}
 if R.cols==4:
  det=int(R.det())
  result['determinant']=det
  result['determinant_identity']=int(W.det())==det*det*int(wall.det())
  if result['norm_gate'] and result['Wall_gate']:
   assert W.det()==1 and abs(det)==1 and result['primitive_prefixes']
 return result
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--candidate-json',help='list of 1..4 original integral four-vectors')
 args=parser.parse_args()
 identity=[[int(i==j) for i in range(4)] for j in range(4)]
 success=check(identity,-2*s.eye(4),s.eye(4))
 rejection=check([[2,0,0,0]],-2*s.eye(4),s.eye(4))
 assert success['determinant']==1 and success['Wall_gate'] and success['norm_gate']
 assert not rejection['primitive_prefixes'] and not rejection['norm_gate']
 out={'rqt':376,'status':'PASS exact theorem + synthetic control cases',
 'original_lattice_source':'stoicheion RQT-242 frozen F4 and H4',
 'theorem':'For a 4-root norm-minus-two Wall flag, W=R.T H4 R is upper triangular with diagonal 1. Thus 1=det(W)=det(R)^2*det(H4)=det(R)^2: det(R)=+/-1.',
 'necessary_prefix_gate':'For any k<=4, gcd of all k by k minors of first k root columns must equal 1.',
 'synthetic_positive':success,'synthetic_negative':rejection,
 'original_roots18_to21':'OPEN'}
 if args.candidate_json:
  with open(args.candidate_json) as f: roots=json.load(f)
  out['authentic_candidate']=check(roots)
  out['frozen_prefix_product']='NOT CHECKED, original 17-reflection source required'
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
