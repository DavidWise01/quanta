#!/usr/bin/env python3
"""RQT-436: exact giant-denominator cone and bounded first-seed search.
Requires the full RQT-401 JSON (restricted_Gram, reduced_kernel_basis, original_F4).
"""
import argparse, hashlib, json, math
from pathlib import Path

LOW,UP,DEN=177065,178600,100000
RATIO=1<<531
SHA='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
def audit(src,maxd=1001):
 Q=[[int(t) for t in row] for row in src['restricted_Gram']]
 B=[[int(t) for t in row] for row in src['reduced_kernel_basis']]
 F=[[int(t) for t in row] for row in src['original_F4']]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(v%2==0 for row in Q for v in row)
 assert all(sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4))==Q[i][j] for i in range(3) for j in range(3))
 sha=hashlib.sha256(json.dumps([[str(t) for t in row] for row in Q],separators=(',',':')).encode()).hexdigest()
 assert sha==SHA
 A=[[t//2 for t in row] for row in Q]
 a,b,c=A[0];g,e=A[1][1:];f=A[2][2]
 alpha=c*c-f*a;K=c*e-f*b;gamma=e*e-f*g;delta=-f
 assert alpha<0 and delta>0 and LOW*(-alpha)<K*DEN<UP*(-alpha)
 margins={}
 for label,n in [('lower',LOW),('upper',UP)]:
  val=alpha*n*n+2*K*n*DEN+gamma*DEN*DEN+delta*DEN*DEN*RATIO*RATIO
  assert val<0
  margins[label]=(-val).bit_length()
 assert margins=={'lower':2449,'upper':2448}
 mods=(256,63,65,11,17,19,23,31)
 squares={m:{i*i%m for i in range(m)} for m in mods}
 keys=('triples','excluded_prime','prime_survivors','modular_square','nonnegative','perfect_square','integral_z','primitive_witness')
 cnt={k:0 for k in keys};witnesses=[]
 for d in range(3,maxd+1,2):
  for y in range(1,d):
   for x in range(LOW*y//DEN+1,(UP*y-1)//DEN+1):
    cnt['triples']+=1
    if (x%13 and (y-5*x)%13==0) or (x%23 and (y-5*x)%23==0):
     cnt['excluded_prime']+=1;continue
    cnt['prime_survivors']+=1
    L=c*x+e*y;M=a*x*x+2*b*x*y+g*y*y
    E=L*L-f*(M+d*d)
    if any(E%m not in squares[m] for m in mods):continue
    cnt['modular_square']+=1
    if E<0:continue
    cnt['nonnegative']+=1
    s=math.isqrt(E)
    if s*s!=E:continue
    cnt['perfect_square']+=1
    for ss in (s,-s):
     if (ss-L)%f:continue
     z=(ss-L)//f;cnt['integral_z']+=1
     w=(x,y,z)
     assert sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))==-d*d
     r=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)]
     assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2*d*d
     if math.gcd(x,y,z,d)!=1:continue
     cnt['primitive_witness']+=1
     witnesses.append({'w':list(map(str,w)),'d':str(d),'r':list(map(str,r))})
 if maxd==1001:
  assert cnt=={'triples':1284928,'excluded_prime':142743,'prime_survivors':1142185,'modular_square':4469,'nonnegative':4467,'perfect_square':0,'integral_z':0,'primitive_witness':0}
 assert math.isqrt(delta)**2!=delta
 return {'RQT':436,'status':'PASS exact cone extension and bounded negative search','sha256':sha,
  'ratio_limit':'2^531','boundary_negative_margin_bits':margins,'counts':cnt,
  'witnesses':witnesses,'bounds':'odd d=3..maxd, 0<|y|<d; x inside exact cone',
  'y_zero':'Only x=y=0 is excluded; y=0,x nonzero remains open',
  'root19':'OPEN','root18_position':'UNVERIFIED'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json')
 p.add_argument('--maxd',type=int,default=1001);p.add_argument('--out')
 x=p.parse_args();r=audit(json.loads(Path(x.full_rqt401_json).read_text()),x.maxd)
 if x.out:Path(x.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
