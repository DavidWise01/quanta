#!/usr/bin/env python3
"""RQT-390: exact mod8 global z=0 exclusion in the frozen root19 lattice.
Generate input with:
 python research/rqt388-exact-second-key.py --bound 30 --out /tmp/rqt388.json
Then run:
 python research/rqt390-remaining-corridor.py /tmp/rqt388.json
"""
import itertools,json,sys
from collections import Counter
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
def audit(payload):
 Q=s.Matrix([[int(v) for v in row] for row in payload.get('restricted_F4_Gram',payload.get('restricted_Gram'))])
 B=s.Matrix([[int(v) for v in row] for row in payload['reduced_kernel_basis']])
 assert B.shape==(4,3) and Q==B.T*F*B and Q==Q.T
 assert all(int(Q[i,i])%2==0 for i in range(3))
 a=int(Q[0,0]//2);b=int(Q[0,1]);c=int(Q[1,1]//2)
 assert (a%8,b%8,c%8)==(1,0,2)
 residues=sorted({(a*x*x+b*x*y+c*y*y)%8 for x,y in itertools.product(range(8),repeat=2)})
 assert residues==[0,1,2,3,4,6] and 7 not in residues
 for x,y in itertools.product(range(8),repeat=2):
  v=B*s.Matrix([x,y,0]);n=int((v.T*F*v)[0])
  assert n%16==2*(a*x*x+b*x*y+c*y*y)%16
  assert n%16!=14
 parity=Counter()
 for x,y,z in itertools.product(range(8),repeat=3):
  v=s.Matrix([x,y,z])
  if int((v.T*Q*v)[0])%16==14:parity[''.join(map(str,(x%2,y%2,z%2)))]+=1
 assert dict(parity)=={'001':32,'011':32,'110':32}
 return {'RQT':390,'status':'PASS exact original F4 certificate',
  'restricted_Gram_mod16':[[int(Q[i,j])%16 for j in range(3)] for i in range(3)],
  'slice_z0_half_coeff_mod8':[a%8,b%8,c%8],
  'z0_attainable_half_norm_mod8':residues,'needed_half_norm_mod8':7,
  'z0_exclusion':'GLOBAL, all integer x/y, not bounded',
  'mod8_compatible_triplets':sum(parity.values()),
  'mod8_parity_classes':dict(sorted(parity.items())),
  'combined_with_RQT389':'any root19 requires x,y,z ALL nonzero',
  'root19':'OPEN','root20':'OPEN','root21':'CONDITIONAL'}
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python rqt390-remaining-corridor.py RQT-388-kernel.json')
 with open(sys.argv[1]) as f:data=json.load(f)
 print(json.dumps(audit(data),indent=2))
