#!/usr/bin/env python3
"""RQT-415: exact denominator parity proof, full RQT-401 JSON required."""
import argparse,itertools,json
from pathlib import Path
def audit(source):
 Q=[[int(t) for t in row] for row in source['restricted_Gram']]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(t%2==0 for row in Q for t in row)
 A=[[t//2 for t in row] for row in Q]
 assert [[t%4 for t in row] for row in A]==[[1,0,1],[0,2,3],[1,3,3]]
 def q(v):return sum(A[i][j]*v[i]*v[j] for i in range(3) for j in range(3))
 parity={''.join(map(str,v)):q(v)%4 for v in itertools.product((0,1),repeat=3)}
 assert parity=={'000':0,'001':3,'010':2,'011':3,'100':1,'101':2,'110':3,'111':2}
 accepted8=[v for v in itertools.product(range(8),repeat=3) if q(v)%8==7]
 assert len(accepted8)==96
 assert {''.join(str(x%2) for x in v) for v in accepted8}=={'001','011','110'}
 assert sum(q(v)%4==3 for v in itertools.product(range(4),repeat=3))==24
 return {'RQT':415,'status':'PASS global odd denominator necessity theorem',
  'A_mod4':[[t%4 for t in row] for row in A],
  'primitive_parity_q_mod4':{k:v for k,v in parity.items() if k!='000'},
  'denominator_necessary':'ODD',
  'numerator_parity_necessary':['001','011','110'],
  'numerator_mod8_classes':96,'mod4_norm_minus1_triples':24,
  'proof':'If d even, q(w)=-d²=0 mod4 forces all w coordinates even, contradicting gcd(w0,w1,w2,d)=1',
  'explicit_rational_coordinates':'NOT CONSTRUCTED','ordinary_integer_root19':'OPEN',
  'candidate_position18':'UNVERIFIED'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--out')
 a=p.parse_args();r=audit(json.loads(Path(a.full_rqt401_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
