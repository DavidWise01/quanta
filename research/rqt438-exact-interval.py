#!/usr/bin/env python3
"""RQT-438: complete exact integer-x interval for fixed y,d, original RQT-401 Gram."""
import argparse,hashlib,json,math
from pathlib import Path
SHA="5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809"
def ceildiv(a,b): return -((-a)//b)
def audit(src,ymax=256,dmax=255):
 Q=[[int(v) for v in row] for row in src['restricted_Gram']]
 B=[[int(v) for v in row] for row in src['reduced_kernel_basis']]
 F=[[int(v) for v in row] for row in src['original_F4']]
 assert len(Q)==3 and all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(v%2==0 for row in Q for v in row)
 assert all(sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4))==Q[i][j] for i in range(3) for j in range(3))
 sha=hashlib.sha256(json.dumps([[str(v) for v in row] for row in Q],separators=(',',':')).encode()).hexdigest()
 assert sha==SHA
 A=[[v//2 for v in row] for row in Q]
 a,b,c=A[0];g,e=A[1][1:];f=A[2][2]
 alpha=c*c-f*a;K=c*e-f*b;gamma=e*e-f*g;delta=-f
 assert alpha<0 and delta>0
 A0=-alpha
 mods=(256,63,65,11,17,19,23,31)
 squares={m:{t*t%m for t in range(m)} for m in mods}
 keys=('yd_cases','empty_intervals','admissible_x','excluded_prime','prime_survivors','modular_square','exact_square','integral_z','primitive_witness')
 counts={k:0 for k in keys};witnesses=[]
 for y in range(1,ymax+1):
  for d in range(1,dmax+1,2):
   counts['yd_cases']+=1
   R=(K*K-alpha*gamma)*y*y-alpha*delta*d*d
   if R<0:counts['empty_intervals']+=1;continue
   h=math.isqrt(R)
   lo=ceildiv(K*y-h,A0);hi=(K*y+h)//A0
   if lo>hi:counts['empty_intervals']+=1;continue
   for x in range(lo,hi+1):
    counts['admissible_x']+=1
    L=c*x+e*y;M=a*x*x+2*b*x*y+g*y*y;E=L*L-f*(M+d*d)
    assert E>=0
    if x==lo:
     v=x-1
     assert (c*v+e*y)**2-f*(a*v*v+2*b*v*y+g*y*y+d*d)<0
    if x==hi:
     v=x+1
     assert (c*v+e*y)**2-f*(a*v*v+2*b*v*y+g*y*y+d*d)<0
    if (x%13!=0 and (y-5*x)%13==0) or (x%23!=0 and (y-5*x)%23==0):
     counts['excluded_prime']+=1;continue
    counts['prime_survivors']+=1
    if any(E%m not in squares[m] for m in mods):continue
    counts['modular_square']+=1
    s=math.isqrt(E)
    if s*s!=E:continue
    counts['exact_square']+=1
    for ss in (s,-s):
     if (ss-L)%f:continue
     z=(ss-L)//f;counts['integral_z']+=1
     w=(x,y,z)
     assert sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))==-d*d
     r=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)]
     assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2*d*d
     if math.gcd(x,y,z,d)!=1:continue
     counts['primitive_witness']+=1
     witnesses.append({'w':list(map(str,w)),'d':str(d),'original_F4':list(map(str,r))})
 if (ymax,dmax)==(256,255):
  assert counts=={'yd_cases':32768,'empty_intervals':3968,'admissible_x':64512,'excluded_prime':7552,'prime_survivors':56960,'modular_square':223,'exact_square':0,'integral_z':0,'primitive_witness':0}
 ed=1<<600;R=(K*K-alpha*gamma)-alpha*delta*ed*ed
 h=math.isqrt(R);xl=ceildiv(K-h,A0);xh=(K+h)//A0
 E=e*e-f*(g+ed*ed)
 assert xl<=0<=xh and E>0 and math.isqrt(E)**2!=E
 return {'RQT':438,'status':'PASS exact interval and bounded full-Gram search',
  'source_sha256':sha,'ymax':ymax,'dmax':dmax,'counts':counts,'witnesses':witnesses,
  'theorem':'For alpha<0, R=(K²-alpha*gamma)y²-alpha*delta*d², h=isqrt(R), E>=0 iff R>=0 and ceil((Ky-h)/(-alpha))<=x<=floor((Ky+h)/(-alpha))',
  'extreme_sample':{'x':0,'y':1,'d':'2^600','real_feasible':True,'discriminant_square':False,
     'lower_endpoint_abs_bits':abs(xl).bit_length(),'upper_endpoint_abs_bits':abs(xh).bit_length()},
  'root19':'OPEN','frozen_root18':'UNVERIFIED'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--ymax',type=int,default=256);p.add_argument('--dmax',type=int,default=255);p.add_argument('--out')
 a=p.parse_args();r=audit(json.loads(Path(a.full_rqt401_json).read_text()),a.ymax,a.dmax)
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
