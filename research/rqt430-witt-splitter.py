#!/usr/bin/env python3
"""RQT-430 exact Witt splitting GIVEN an isotropic seed. Does not find first seed."""
import argparse,json,math,hashlib
from pathlib import Path
from sympy import Matrix, eye

def norm(H,v):
 v=Matrix(v);return (v.T*H*v)[0]
def pair(H,v,w):return (Matrix(v).T*H*Matrix(w))[0]
def split(H,p):
 p=Matrix(p)
 assert p!=Matrix.zeros(4,1) and norm(H,p)==0
 j=next(j for j in range(4) if pair(H,p,eye(4)[:,j]))
 v=eye(4)[:,j];beta=pair(H,p,v)
 h=v-norm(H,v)/(2*beta)*p
 assert norm(H,h)==0 and pair(H,p,h)==beta
 rows=Matrix.vstack(p.T*H,h.T*H);N=rows.nullspace()
 assert len(N)==2
 U=Matrix.hstack(p,h,*N);G=U.T*H*U
 assert U.det()!=0 and G[:2,:2]==Matrix([[0,beta],[beta,0]])
 assert G[:2,2:]==Matrix.zeros(2,2) and G[2:,:2]==Matrix.zeros(2,2)
 return {'pairing':str(beta),'hyperbolic':[[str(v) for v in r] for r in G[:2,:2].tolist()],'binary':[[str(v) for v in r] for r in G[2:,2:].tolist()]}
def audit(src,candidate=None):
 Q=Matrix([[int(x) for x in r] for r in src['restricted_Gram']])
 F=Matrix([[int(x) for x in r] for r in src['original_F4']])
 B=Matrix([[int(x) for x in r] for r in src['reduced_kernel_basis']])
 assert Q==Q.T and B.T*F*B==Q and all(int(x)%2==0 for x in Q)
 digest=hashlib.sha256(json.dumps([[str(t) for t in r] for r in Q.tolist()],separators=(',',':')).encode()).hexdigest()
 assert digest=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 H=Matrix.diag(1,1,1,1);H[:3,:3]=Q/2
 positive=split(Matrix.diag(-1,1,1,1),[1,1,0,0])
 assert positive['hyperbolic']==[['0','-1'],['-1','0']] and positive['binary']==[['1','0'],['0','1']]
 try:split(Matrix.diag(-1,1,1,1),[1,0,0,0]);raise RuntimeError('invalid accepted')
 except AssertionError:pass
 result={'RQT':430,'source_sha256':digest,'F4_backmap':'PASS','synthetic_positive':'PASS','synthetic_negative':'PASS','synthetic_split':positive,
 'original_rational_witness':'NOT FOUND','root19':'OPEN','frozen_root18_position':'UNVERIFIED',
 'limitation':'A first isotropic seed must be supplied; exact splitting alone does not construct it.'}
 if candidate is not None:
  assert len(candidate)==4
  v=Matrix([int(t) for t in candidate])
  if v[3]==0 or math.gcd(*(int(t) for t in v))!=1 or norm(H,v)!=0:
   result['candidate_accepted']=False;result['candidate_norm']=str(norm(H,v))
  else:
   assert norm(F,B*v[:3,:])==-2*v[3]**2
   result['candidate_accepted']=True;result['original_seed_split']=split(H,v)
   result['root19']='PREFIX CHECK REQUIRED' if abs(v[3])==1 else 'OPEN: nonunit denominator'
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_json');p.add_argument('--candidate');p.add_argument('--out')
 a=p.parse_args();r=audit(json.loads(Path(a.full_json).read_text()),json.loads(a.candidate) if a.candidate else None)
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
