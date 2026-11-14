#!/usr/bin/env python3
"""RQT-379: valid three-root Wall prefix forces +/- root21, no norm scan."""
import argparse,itertools,json,random
from functools import reduce
from math import gcd
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
def cofactors(C):
 assert C.shape==(3,4)
 v=s.Matrix([(-1)**j*C[:,[k for k in range(4) if k!=j]].det() for j in range(4)])
 assert C*v==s.zeros(3,1)
 return v
def verify(R,gram,wall):
 if R.shape!=(4,3) or R.rank()!=3:return {'accepted':False,'reason':'rank3 required'}
 W=R.T*wall*R
 norms=[int((R[:,i].T*gram*R[:,i])[0]) for i in range(3)]
 # Explicit lower triangle: the row index MUST be greater than the column.
 lower=[int(W[i,j]) for j in range(3) for i in range(j+1,3)]
 if norms!=[-2]*3 or any(lower):
  return {'accepted':False,'norms':norms,'lower_Wall':lower}
 assert W.det()==1
 minors=[int(R[list(rows),:].det()) for rows in itertools.combinations(range(4),3)]
 assert reduce(gcd,(abs(n) for n in minors),0)==1
 v=cofactors(R.T*wall.T)
 assert reduce(gcd,(abs(int(n)) for n in v),0)==1
 det=int(s.Matrix.hstack(R,v).det())
 norm=int((v.T*gram*v)[0])
 assert abs(det)==1 and norm==-2
 return {'accepted':True,'cofactor':[int(n) for n in v],
  'two_root21_signs':[[int(sign*n) for n in v] for sign in (1,-1)],
  'root21_norm_for_both_signs':norm,'unimodular_completion_determinant':det,
  'primitive_prefix_automatic':True}
def synthetic(seed):
 rng=random.Random(seed);P=s.eye(4)
 for _ in range(15):
  i,j=rng.sample(range(4),2)
  P[i,:]=P[i,:]+rng.choice((-3,-2,-1,1,2,3))*P[j,:]
 assert abs(P.det())==1
 T=s.eye(4)
 for i in range(4):
  for j in range(i+1,4):T[i,j]=rng.randint(-13,13)
 Q=P.inv()
 return verify(P[:,:3],-Q.T*(T+T.T)*Q,Q.T*T*Q)
def main():
 p=argparse.ArgumentParser();p.add_argument('--three-roots-json');args=p.parse_args()
 tests=[synthetic(i) for i in range(100)]
 assert all(t['accepted'] for t in tests)
 ordinary=s.eye(4)[:,:3];v=cofactors(ordinary.T*H.T)
 assert ordinary.T*H.T*v==s.zeros(3,1)
 out={'rqt':379,'status':'PASS exact conditional four-root closure theorem',
 'original_F4_H4':'PASS authentic Gram determinant, Wall unimodularity and symmetry',
 'synthetic_controls':len(tests),'forced_root21_norm':-2,
 'three_valid_roots_suffice_for_fourth':True,
 'actual_roots18_to21':'OPEN','frozen17_prefix_order':'NOT CHECKED'}
 if args.three_roots_json:
  with open(args.three_roots_json) as f: roots=json.load(f)
  assert len(roots)==3 and all(len(r)==4 for r in roots)
  result=verify(s.Matrix.hstack(*(s.Matrix(r) for r in roots)),F,H)
  out['candidate']=result
  out['root18_parity_checked']=(''.join(str(int(x)%2) for x in roots[0]) in
     ('0111','1001','1110'))
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
