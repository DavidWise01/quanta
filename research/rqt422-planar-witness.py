#!/usr/bin/env python3
"""RQT-422: exact rational-line witness construction attempt using full RQT-401 JSON.
Any witness must satisfy the original F4 backmap exactly. A negative finite
search is NOT a nonexistence proof; RQT-414 proves rational existence.
"""
import argparse,itertools,json,math
from pathlib import Path
def dot(Q,u,v):
 return sum(Q[i][j]*u[i]*v[j] for i in range(4) for j in range(4))
def audit(src,bound=4):
 Q=[[int(z) for z in row] for row in src['restricted_Gram']]
 B=[[int(z) for z in row] for row in src['reduced_kernel_basis']]
 F=[[int(z) for z in row] for row in src['original_F4']]
 assert all(z%2==0 for row in Q for z in row)
 assert all(sum(B[i][k]*F[i][j]*B[j][l] for i in range(4) for j in range(4))==Q[k][l] for k in range(3) for l in range(3))
 A=[[z//2 for z in row] for row in Q]
 H=[r+[0] for r in A]+[[0,0,0,1]]
 vectors=[v for v in itertools.product(range(-bound,bound+1),repeat=3) if any(v)]
 checked=nonnegative=squares=0
 for av in itertools.product(range(-bound,bound+1),repeat=3):
  u=(*av,1);gamma=dot(H,u,u)
  for bv in vectors:
   v=(*bv,0)
   alpha=dot(H,v,v)
   assert alpha!=0 # RQT-405: A anisotropic over rational numbers
   beta=dot(H,u,v)
   delta=beta*beta-alpha*gamma
   checked+=1
   if delta<0:continue
   nonnegative+=1
   s=math.isqrt(delta)
   if s*s!=delta:continue
   squares+=1
   for sign in (-1,1):
    v4=[alpha*u[i]+(-beta+sign*s)*v[i] for i in range(4)]
    if all(z==0 for z in v4):continue
    g=math.gcd(*v4)
    v4=[z//g for z in v4]
    if v4[3]<0:v4=[-z for z in v4]
    assert v4[3]!=0 and v4[3]%2==1
    assert dot(H,v4,v4)==0
    r=[sum(B[i][j]*v4[j] for j in range(3)) for i in range(4)]
    assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2*v4[3]**2
    return {'RQT':422,'status':'EXPLICIT RATIONAL WITNESS CONSTRUCTED','planes_checked':checked,'nonnegative_discriminants':nonnegative,'square_discriminants':squares,'primitive_w_d':list(map(str,v4)),'original_F4_numerator':list(map(str,r)),'integral_denominator_one':v4[3]==1}
 return {'RQT':422,'status':'NO WITNESS IN BOUNDED RATIONAL-LINE FAMILY','bound':bound,'planes_checked':checked,'nonnegative_discriminants':nonnegative,'square_discriminants':squares,'witnesses':[],'rational_existence':'PROVEN ABSTRACTLY, RQT-414','root19':'OPEN','position18':'UNVERIFIED','scope':'Finite family only'}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('full_lattice_json');p.add_argument('--bound',type=int,default=4);p.add_argument('--out')
 a=p.parse_args();assert 1<=a.bound<=20
 r=audit(json.loads(Path(a.full_lattice_json).read_text()),a.bound)
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
