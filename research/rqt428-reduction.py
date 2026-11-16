#!/usr/bin/env python3
"""RQT-428 exact unimodular shear audit; requires full RQT-401 JSON."""
import argparse,hashlib,json,math
from pathlib import Path
from sympy import Matrix,eye

def bit_score(M):
 return sum(abs(int(M[i,j])).bit_length() for i in range(M.rows) for j in range(i,M.cols))
def total_abs(M): return sum(abs(int(x)) for x in M)
def audit(src):
 Q=Matrix([[int(v) for v in row] for row in src['restricted_Gram']])
 assert Q.shape==(3,3) and Q==Q.T and all(int(x)%2==0 for x in Q)
 sha=hashlib.sha256(json.dumps([[str(x) for x in row] for row in Q.tolist()],separators=(',',':')).encode()).hexdigest()
 assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 A=Q/2;T=Matrix([[-9,-25,0],[-5,-14,0],[0,0,1]]);C=T.T*A*T
 assert T.det()==1 and bit_score(A)==7053 and bit_score(C)==7015
 checked=better=0
 for i in range(3):
  for j in range(3):
   if i==j:continue
   for k in (-4,-3,-2,-1,1,2,3,4):
    E=eye(3);E[i,j]=k
    better+=bit_score(E.T*C*E)<bit_score(C);checked+=1
 assert checked==48 and better==0
 V=eye(3);V[1,2]=-8;D=V.T*C*V
 assert (T*V).det()==1 and D==(T*V).T*A*(T*V)
 assert total_abs(D)<total_abs(C) and bit_score(D)==bit_score(C)
 rows=[]
 for label,M in [('original',A),('RQT419',C),('RQT428',D)]:
  S=total_abs(M)+1
  B=math.isqrt((3*S)**3)
  rows.append({'basis':label,'bit_score_3D':bit_score(M),'S':str(S),'bound':str(B),
               'bound_digits':len(str(B)),'bound_bits':B.bit_length()})
 assert rows[0]['bound_digits']==rows[1]['bound_digits']==rows[2]['bound_digits']==611
 assert int(rows[2]['S'])<int(rows[1]['S'])<int(rows[0]['S'])
 return {'RQT':428,'status':'PASS','Gram_SHA256':sha,
  'T':[[-9,-25,0],[-5,-14,0],[0,0,1]],'V':[[1,0,0],[0,1,-8],[0,0,1]],'det_TV':1,
  'small_shears_tested':checked,'small_shears_better_bit_score':better,'metrics':rows,
  'root19':'OPEN','position18':'UNVERIFIED','rational_witness':'NOT CONSTRUCTED',
  'scope':'Exact unimodular equivalence; local finite shear audit; not global optimality'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--out')
 a=p.parse_args();r=audit(json.loads(Path(a.full_rqt401_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
