#!/usr/bin/env python3
"""RQT-429: exact certified numerator-shell search; complete RQT-401 JSON required."""
import argparse,json,math
from pathlib import Path
def run(src,lo=121,hi=124):
 Q=[[int(t) for t in r] for r in src['restricted_Gram']]
 B=[[int(t) for t in r] for r in src['reduced_kernel_basis']]
 F=[[int(t) for t in r] for r in src['original_F4']]
 assert all(sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4))==Q[i][j] for i in range(3) for j in range(3))
 assert all(t%2==0 for r in Q for t in r)
 A=[[t//2 for t in r] for r in Q]
 T=[[-9,-25,0],[-5,-14,0],[0,0,1]]
 V=[[1,0,0],[0,1,-8],[0,0,1]]
 W=[[sum(T[i][k]*V[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
 C=[[sum(W[k][i]*A[k][l]*W[l][j] for k in range(3) for l in range(3)) for j in range(3)] for i in range(3)]
 a,b,c=C[0];d,e=C[1][1:];f=C[2][2]
 mods=(64,63,65,11,17,19,23,31)
 squares={m:{t*t%m for t in range(m)} for m in mods}
 total=nonpositive=positive=passed=exact=0;witness=[]
 for x in range(-hi,hi+1):
  for y in range(-hi,hi+1):
   base=a*x*x+2*b*x*y+d*y*y
   linear=2*(c*x+e*y)
   for z in range(-hi,hi+1):
    if max(abs(x),abs(y),abs(z))<lo or math.gcd(x,y,z)!=1:continue
    total+=1
    N=-(base+linear*z+f*z*z)
    if N<=0:nonpositive+=1;continue
    positive+=1
    if any(N%m not in squares[m] for m in mods):continue
    passed+=1
    D=math.isqrt(N)
    if D*D!=N:continue
    exact+=1
    w=[sum(W[i][j]*t for j,t in enumerate((x,y,z))) for i in range(3)]
    assert sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))==-D*D
    r=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)]
    assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2*D*D
    assert D%2==1
    witness.append({'wprime':[x,y,z],'d':str(D),'w':list(map(str,w)),'r':list(map(str,r))})
 return {'RQT':429,'basis':'T*V (RQT-428)','min_radius':lo,'max_radius':hi,
 'primitive_triples':total,'nonpositive_N':nonpositive,'positive_N':positive,
 'modular_square_survivors':passed,'exact_squares':exact,'witnesses':witness,
 'root19':'OPEN' if not witness else 'PREFIX CHECK REQUIRED',
 'note':'Shell is in T*V basis; earlier 0..120 search used T basis.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json')
 p.add_argument('--min-radius',type=int,default=121);p.add_argument('--max-radius',type=int,default=124);p.add_argument('--out')
 args=p.parse_args();assert 1<=args.min_radius<=args.max_radius
 r=run(json.loads(Path(args.full_rqt401_json).read_text()),args.min_radius,args.max_radius)
 if args.out:Path(args.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
