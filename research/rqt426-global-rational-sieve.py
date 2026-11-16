#!/usr/bin/env python3
"""RQT-426 exact denominator-free rational witness sieve on full RQT-401 Gram."""
import argparse,json,math
from pathlib import Path
def audit(src,R):
 Q=[[int(v) for v in row] for row in src['restricted_Gram']]
 B=[[int(v) for v in row] for row in src['reduced_kernel_basis']]
 F=[[int(v) for v in row] for row in src['original_F4']]
 assert len(Q)==3 and all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(z%2==0 for row in Q for z in row)
 assert all(sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4))==Q[i][j] for i in range(3) for j in range(3))
 A=[[v//2 for v in row] for row in Q]
 T=[[-9,-25,0],[-5,-14,0],[0,0,1]]
 assert T[0][0]*T[1][1]-T[0][1]*T[1][0]==1
 C=[[sum(T[k][i]*A[k][l]*T[l][j] for k in range(3) for l in range(3)) for j in range(3)] for i in range(3)]
 a,b,c=C[0];d,e=C[1][1:];f=C[2][2]
 mods=(64,63,65,11,17,19)
 square={m:{t*t%m for t in range(m)} for m in mods}
 tested=positive=passed=exact=0;witnesses=[]
 for x in range(-R,R+1):
  for y in range(-R,R+1):
   base=a*x*x+2*b*x*y+d*y*y
   linear=2*(c*x+e*y)
   for z in range(-R,R+1):
    if math.gcd(x,y,z)!=1:continue
    tested+=1
    n=-(base+linear*z+f*z*z)
    if n<=0:continue
    positive+=1
    if any(n%m not in square[m] for m in mods):continue
    passed+=1
    D=math.isqrt(n)
    if D*D!=n:continue
    exact+=1
    assert D%2==1
    w=[sum(T[i][j]*v for j,v in enumerate((x,y,z))) for i in range(3)]
    r=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)]
    assert sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))==-D*D
    assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2*D*D
    witnesses.append({'numerator_transformed':[x,y,z],'denominator':str(D),'numerator_original':list(map(str,w)),'F4_original':list(map(str,r))})
 return {'RQT':426,'radius':R,'primitive_spatial_numerators':tested,'positive_negative_norm':positive,'modular_square_survivors':passed,'exact_square_discriminants':exact,'witnesses':witnesses,'root19':'OPEN' if not any(q['denominator']=='1' for q in witnesses) else 'CONDITIONAL','predecessor18':'UNVERIFIED',
 'primitive_numerator_lemma':'If gcd(w)=g then g² divides d² so g divides d, violating primitive (w,d) unless g=1.',
 'constructive_completeness':'Increasing radius eventually enumerates a rational witness by RQT-414, but with no effective stopping bound.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--radius',type=int,default=120);p.add_argument('--out')
 z=p.parse_args();assert z.radius>=1
 result=audit(json.loads(Path(z.full_rqt401_json).read_text()),z.radius)
 if z.out:Path(z.out).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
