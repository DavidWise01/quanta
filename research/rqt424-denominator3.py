#!/usr/bin/env python3
"""RQT-424: exact singular denominator-3 lifting on the RQT-401 Gram."""
import argparse, itertools, json
from pathlib import Path
def audit(src):
 Q=[[int(a) for a in row] for row in src['restricted_Gram']]
 assert all(a%2==0 for row in Q for a in row)
 A=[[a//2 for a in row] for row in Q]
 assert [[a%27 for a in row] for row in A]==[[8,3,14],[3,0,21],[14,21,2]]
 def q(x,y,z,m):
  return (A[0][0]*x*x+2*A[0][1]*x*y+2*A[0][2]*x*z+
          A[1][1]*y*y+2*A[1][2]*y*z+A[2][2]*z*z)%m
 def primitive(x,y,z):return not (x%3==y%3==z%3==0)
 parents=[]
 for x,y,z in itertools.product(range(9),repeat=3):
  if (x+z)%3 or not primitive(x,y,z):continue
  assert q(x,y,z,9)==0
  t=(x+z)//3
  residue=(z*z+z*t+2*t*t+y*z+2*t*y)%3
  assert q(x,y,z,27)==9*residue
  parents.append((x,y,z,residue))
 assert len(parents)==216
 group={r:sum(v[3]==r for v in parents) for r in (0,1,2)}
 assert group=={0:72,1:108,2:36}
 for x,y,z,_ in parents:
  assert all(q(x+9*i,y+9*j,z+9*k,27)==q(x,y,z,27)
    for i,j,k in itertools.product(range(3),repeat=3))
 direct={3:0,9:0}
 for x,y,z in itertools.product(range(27),repeat=3):
  if not primitive(x,y,z):continue
  for d in direct:
   if (q(x,y,z,27)+d*d)%27==0:direct[d]+=1
 assert direct=={3:972,9:1944}
 return {'RQT':424,'status':'PASS exact mod9-to-mod27 singular branches',
   'A_mod27':[[a%27 for a in row] for row in A],
   'primitive_parent_classes_mod9':216,
   'parent_survivors_v3_d_eq1':36,'parent_survivors_v3_d_ge2':72,
   'parents_dead_both':108,
   'primitive_triples_mod27_for_d3':972,
   'primitive_triples_mod27_for_d9':1944,
   'identity':'x+z=3t => q(x,y,z)/9 = z²+zt+2t²+yz+2ty (mod3)',
   'rational_coordinates':'NOT CONSTRUCTED','root19':'OPEN',
   'candidate_root18_ordering':'UNVERIFIED'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_json');p.add_argument('--out')
 a=p.parse_args();r=audit(json.loads(Path(a.full_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
