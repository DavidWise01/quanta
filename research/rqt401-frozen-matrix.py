#!/usr/bin/env python3
"""RQT-401: reconstruct ORIGINAL target lattice and audit two-adic counts.

Requires sympy and the existing canonical source files RQT-386, RQT-377,
RQT-388 in the same research/ directory. Exact integer only.
Run: python research/rqt401-frozen-matrix.py --out research/RQT-401-full-local.json
"""
import argparse,hashlib,importlib.util,itertools,json,subprocess,sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent

def load_module(filename,name):
 spec=importlib.util.spec_from_file_location(name,str(HERE/filename))
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 return mod

def canonical_sha(obj):
 return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()

def audit():
 r386=json.loads(subprocess.run(
  [sys.executable,str(HERE/'rqt386-exact-null-and-root-candidate.py')],
  capture_output=True,text=True,check=True).stdout)
 ladder=load_module('rqt377-exact-wall-kernel-ladder.py','ladder401')
 reduce=load_module('rqt388-exact-second-key.py','reduce401')
 r=s.Matrix([int(t) for t in r386['root_candidate_r']])
 F,H=ladder.F,ladder.H
 assert (r.T*F*r)[0]==-2 and (r.T*H*r)[0]==1
 B,Q0,_=ladder.kernel_ladder([list(map(int,r))])
 L,U,loops=reduce.exact_lll(B.T.tolist())
 assert abs(U.det())==1 and L==U*B.T
 R=L.T;Q=R.T*F*R
 assert Q==Q.T and Q==U*Q0*U.T
 assert r.T*H.T*R==s.zeros(1,3)
 q=[[int(x) for x in row] for row in Q.tolist()]
 counts={}
 for m in (2,4,8,16,32,64,5,7,9):
  qm=[[v%m for v in row] for row in q]
  count=0
  for v in itertools.product(range(m),repeat=3):
   n=(sum(qm[i][j]*v[i]*v[j] for i in range(3) for j in range(3))+2)%m
   count+=n==0
  counts[str(m)]=count
 assert [counts[str(m)] for m in (5,7,8,9)]==[20,42,192,162]
 assert [counts[str(m)] for m in (2,4,8,16,32,64)]==[8,32,192,768,3072,12288]
 result={'RQT':401,'status':'PASS exact frozen candidate successor lattice local audit',
  'original_root_candidate_norm':-2,'original_root_candidate_H_self':1,
  'frozen_17_predecessor_compatibility':'NOT VERIFIED',
  'LLL_loops':loops,
  'reduced_basis_max_bits':max(abs(int(x)).bit_length() for x in R),
  'Q_max_bits':max(abs(int(x)).bit_length() for x in Q),
  'modular_survivor_triples':counts,
  'sha256_reduced_Gram':canonical_sha([[str(x) for x in row] for row in Q.tolist()]),
  'sha256_reduced_basis':canonical_sha([[str(x) for x in row] for row in R.tolist()]),
  'sha256_root_candidate':canonical_sha([str(x) for x in r]),
  'root19':'OPEN','root20':'OPEN','root21':'conditional',
  'scope':'Finite local necessity checks; not proof of norm -2 integral successor'}
 full={'certificate':result,'reduced_kernel_basis':[[str(x) for x in row] for row in R.tolist()],
       'restricted_Gram':[[str(x) for x in row] for row in Q.tolist()],
       'root_candidate_r':[str(x) for x in r]}
 return result,full

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out');a=p.parse_args()
 result,full=audit()
 if a.out:Path(a.out).write_text(json.dumps(full,indent=2)+'\n')
 print(json.dumps(result,indent=2))
