#!/usr/bin/env python3
"""RQT-417: denominator-unit symmetry on the exact RQT-401 candidate successor.
Input must be the full RQT-401 JSON including restricted_Gram.
"""
import argparse,itertools,json,math
from pathlib import Path

MODULI={4:(1,3,5,7),8:(1,3,5,7),
        9:(1,2,4,5,7,8),11:(1,2,3,5,7)}
EXPECTED={4:24,8:96,9:162,11:110}

def audit(data):
 raw=data.get('restricted_Gram')
 if raw is None:raise ValueError('Need full RQT-401 restricted_Gram')
 Q=[[int(z) for z in row] for row in raw]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(v%2==0 for row in Q for v in row)
 A=[[v//2 for v in row] for row in Q]
 def q(v,m):
  return sum((A[i][j]%m)*v[i]*v[j] for i in range(3) for j in range(3))%m
 rows=[]
 for m,ds in MODULI.items():
  base={v for v in itertools.product(range(m),repeat=3) if (q(v,m)+1)%m==0}
  assert len(base)==EXPECTED[m]
  counts={}
  for d in ds:
   assert math.gcd(d,m)==1
   inv=pow(d,-1,m)
   transformed={(d*v[0]%m,d*v[1]%m,d*v[2]%m) for v in base}
   direct={v for v in itertools.product(range(m),repeat=3)
           if (q(v,m)+d*d)%m==0}
   assert transformed==direct
   assert all((q(tuple(inv*t%m for t in v),m)+1)%m==0 for v in direct)
   counts[str(d)]=len(direct)
  rows.append({'modulus':m,'unit_denominators':list(ds),'solution_count_by_denominator':counts})
 return {'RQT':417,'status':'PASS exact denominator-unit bijection',
  'theorem':'For gcd(d,m)=1, scaling w by d^-1 modulo m bijects q(w)=-d^2 and q(u)=-1',
  'results':rows,'rational_witness':'NOT CONSTRUCTED',
  'integral_root19':'OPEN','root18_position':'UNVERIFIED',
  'scope':'This theorem concerns congruence classes at moduli coprime to d; it does not rule out finer arithmetic obstructions'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--out')
 a=p.parse_args()
 result=audit(json.loads(Path(a.full_rqt401_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
