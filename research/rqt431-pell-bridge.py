#!/usr/bin/env python3
"""RQT-431 exact generalized Pell bridge for full RQT-401 candidate lattice.
Verifies a necessary-and-sufficient completed-square equivalence.
Not a Pell solver and not an integral root19 witness.
"""
import argparse,hashlib,json,math
from pathlib import Path
SHA='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
def norm(A,w):
 return sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))
def pell(A,x,y):
 a,b,c=A[0];aa,e=A[1][1:];f=A[2][2]
 L=c*x+e*y;M=a*x*x+2*b*x*y+aa*y*y
 return f,L,L*L-f*M
def accept(A,x,y,s,d):
 f,L,E0=pell(A,x,y)
 if not d or (s-L)%f or s*s+f*d*d!=E0:return None
 z=(s-L)//f
 assert norm(A,(x,y,z))==-d*d
 return [x,y,z,d]
def audit(src):
 Q=[[int(t) for t in r] for r in src['restricted_Gram']]
 B=[[int(t) for t in r] for r in src['reduced_kernel_basis']]
 F=[[int(t) for t in r] for r in src['original_F4']]
 assert len(Q)==3 and all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(t%2==0 for row in Q for t in row)
 assert all(sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4))==Q[i][j] for i in range(3) for j in range(3))
 sha=hashlib.sha256(json.dumps([[str(t) for t in r] for r in Q],separators=(',',':')).encode()).hexdigest()
 assert sha==SHA
 A=[[t//2 for t in row] for row in Q];f=A[2][2];D=-f
 assert f<0 and f%2 and D.bit_length()==1352 and math.isqrt(D)**2!=D
 trials=[]
 for x,y,z,d in ((16,9,1,3),(23,13,6,5),(31,17,9,7),(1,0,0,1),(0,0,1,1)):
  f,L,E0=pell(A,x,y);s=f*z+L
  residual=s*s+f*d*d-E0
  assert residual==f*(norm(A,(x,y,z))+d*d)
  assert (s-L)%f==0
  trials.append({'w':[x,y,z],'denominator':d,'norm_zero':residual==0})
 assert not any(t['norm_zero'] for t in trials)
 A0=[[1,0,0],[0,1,0],[0,0,-2]];f0,L0,E00=pell(A0,1,0)
 s0=f0+L0
 assert s0*s0+f0==E00 and accept(A0,1,0,s0,1)==[1,0,1,1]
 assert accept(A0,1,0,s0+1,1) is None
 return {'RQT':431,'status':'PASS exact Pell norm equivalence and controls',
  'source_sha256':sha,'D_bits':D.bit_length(),'D_is_square':False,
  'identity':'s²+f*d²=E0(x,y); f=A22<0, s=f*z+L, E0=L²-f*M',
  'integrality':'s congruent L modulo abs(f)',
  'positive_control':'PASS diag(1,1,-2), w=(1,0,1), d=1',
  'negative_control':'PASS wrong s rejected',
  'original_trial_vectors':trials,'explicit_rational_witness':'NOT CONSTRUCTED',
  'root19':'OPEN','root18_frozen_ordering':'UNVERIFIED',
  'limitation':'Exact change of variables, not a complete generalized Pell solver'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--out')
 a=p.parse_args();r=audit(json.loads(Path(a.full_rqt401_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
