#!/usr/bin/env python3
"""RQT-423: exact rational-line search in RQT-419 unimodular coordinates.
Requires full RQT-401 JSON. A bounded numerator exclusion is not a global proof.
"""
import argparse,itertools,json,math
from pathlib import Path

def dot(M,u,v):
 return sum(M[i][j]*u[i]*v[j] for i in range(3) for j in range(3))

def audit(src,bound=6):
 Q=[[int(z) for z in row] for row in src['restricted_Gram']]
 B=[[int(z) for z in row] for row in src['reduced_kernel_basis']]
 F=[[int(z) for z in row] for row in src['original_F4']]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(z%2==0 for row in Q for z in row)
 assert all(sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4))==Q[i][j] for i in range(3) for j in range(3))
 A=[[z//2 for z in row] for row in Q]
 T=[[-9,-25,0],[-5,-14,0],[0,0,1]]
 assert T[0][0]*T[1][1]-T[0][1]*T[1][0]==1
 C=[[sum(T[k][i]*A[k][l]*T[l][j] for k in range(3) for l in range(3)) for j in range(3)] for i in range(3)]
 vs=list(itertools.product(range(-bound,bound+1),repeat=3))
 directions=[v for v in vs if any(v)]
 indexed=[(v,dot(C,v,v),[sum(C[i][j]*v[j] for j in range(3)) for i in range(3)]) for v in directions]
 checked=positive=squares=0;found=None
 for a in vs:
  gamma=dot(C,a,a)+1
  for b,alpha,Cb in indexed:
   assert alpha!=0 # RQT-405 rational anisotropy
   beta=sum(a[i]*Cb[i] for i in range(3))
   D=beta*beta-alpha*gamma
   checked+=1
   if D<0:continue
   positive+=1
   r=math.isqrt(D)
   if r*r!=D:continue
   squares+=1
   for sign in (-1,1):
    vec=[alpha*a[i]+(-beta+sign*r)*b[i] for i in range(3)]+[alpha]
    g=math.gcd(*vec)
    vec=[v//g for v in vec]
    if vec[3]<0:vec=[-v for v in vec]
    w=[sum(T[i][j]*vec[j] for j in range(3)) for i in range(3)]
    d=vec[3]
    assert d>0 and d%2==1 and dot(A,w,w)+d*d==0
    rw=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)]
    assert sum(F[i][j]*rw[i]*rw[j] for i in range(4) for j in range(4))==-2*d*d
    found={'transformed_primitive':list(map(str,vec)),'original_numerator':list(map(str,w)),'denominator':str(d)}
    break
   if found:break
  if found:break
 return {'RQT':423,'status':'WITNESS FOUND' if found else 'NO WITNESS IN FINITE TRANSFORMED FAMILY',
  'bound':bound,'T':T,'det_T':1,'anchors':len(vs),'directions':len(directions),
  'lines_checked':checked,'nonnegative_D':positive,'perfect_square_D':squares,
  'witness':found,'bounded_conclusion':'No primitive transformed spatial numerator in [-bound,bound]^3 (any denominator): the anchor a=0 and direction b=numerator would produce D=d^2.',
  'root19':'OPEN' if not found else 'Requires frozen prefix check',
  'root18_position':'UNVERIFIED','scope':'Finite numerator-height only'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json')
 p.add_argument('--bound',type=int,default=6);p.add_argument('--out')
 args=p.parse_args();assert 1<=args.bound<=10
 result=audit(json.loads(Path(args.full_rqt401_json).read_text()),args.bound)
 if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
