#!/usr/bin/env python3
"""RQT-411: coherent square-root CRT classification in the exact RQT-401 lattice.
Usage: python research/rqt411-coherent-root.py FULL_RQT401.json
"""
import argparse,json,math
from pathlib import Path
def audit(data):
 raw=data.get('restricted_Gram')
 if raw is None:raise ValueError('Full reduced Gram required')
 q=[[int(a) for a in row] for row in raw]
 assert len(q)==3 and all(len(r)==3 for r in q)
 assert all(q[i][j]==q[j][i] for i in range(3) for j in range(3))
 assert all(a%2==0 for row in q for a in row)
 A=[[v//2 for v in row] for row in q]
 a,b,c=A[0];d,e=A[1][1:];f=A[2][2]
 assert f<0 and f%299==0
 x,y=16,9; L=c*x+e*y; M=a*x*x+2*b*x*y+d*y*y+1
 E=L*L-f*M
 assert E>0 and math.isqrt(E)**2!=E
 roots=[s for s in range(299) if (s*s-E)%299==0]
 assert roots==[125,148,151,174] and L%299==148
 coherent=[s for s in roots if (s-L)%299==0 or (s+L)%299==0]
 assert coherent==[148,151]
 counts={'four':0,'two':0,'one':0}
 for xx in range(299):
  for yy in range(299):
   ll=(c*xx+e*yy)%299
   kind='one' if ll%13==ll%23==0 else 'two' if ll%13==0 or ll%23==0 else 'four'
   counts[kind]+=1
 assert counts=={'four':78936,'two':10166,'one':299}
 return {'RQT':411,'status':'PASS exact automatic local square and CRT sign classification',
  'f_bits':abs(f).bit_length(),'known_factor_of_f':299,
  'full_factorization_of_f':'NOT ESTABLISHED',
  'theorem':'E=L²-fM, so E is automatically L² mod every divisor of f',
  'crt_root_class_counts':counts,'specific_xy':[x,y],
  'L_mod299':L%299,'square_roots_mod299':roots,
  'coherent_roots_mod299':coherent,
  'mixed_sign_roots_mod299':[125,174],
  'E_exact_square_for_example':False,'root19':'OPEN',
  'root18_position':'UNVERIFIED','root20':'OPEN','root21':'conditional'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_gram_json');p.add_argument('--out')
 a=p.parse_args();r=audit(json.loads(Path(a.full_gram_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
