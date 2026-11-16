#!/usr/bin/env python3
"""RQT-435 denominator-aware cone and bounded exact rational seed sieve.
Run: python research/rqt435-denominator-aware.py FULL_RQT401.json
"""
import argparse,json,math,hashlib
from pathlib import Path
SHA='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
def audit(src,N=3000,Dmax=25):
 Q=[[int(t) for t in row] for row in src['restricted_Gram']]
 A=[[z//2 for z in row] for row in Q]
 F=[[int(t) for t in row] for row in src['original_F4']]
 B=[[int(t) for t in row] for row in src['reduced_kernel_basis']]
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(z%2==0 for row in Q for z in row)
 assert all(sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4))==Q[i][j] for i in range(3) for j in range(3))
 sha=hashlib.sha256(json.dumps([[str(z) for z in row] for row in Q],separators=(',',':')).encode()).hexdigest()
 assert sha==SHA
 a,b,c=A[0];g,e=A[1][1:];f=A[2][2];assert f<0
 aq=c*c-f*a;K=c*e-f*b;cq=e*e-f*g;delta=-f
 assert aq<0 and K>0 and cq<0
 assert 177065*(-aq)<100000*K<178600*(-aq)
 for n in (177065,178600):
  assert aq*n*n+2*K*n*100000+cq*100000**2+delta*100000**2<0
 moduli=(256,63,65,11,17,19,23,31)
 squares={m:{(t*t)%m for t in range(m)} for m in moduli}
 keys=['cone_pairs','pair_denominator_cases','prime_exclusions','prime_survivors','square_modular_survivors','nonnegative','exact_squares','integral_z','primitive_witnesses']
 count=dict.fromkeys(keys,0);found=[]
 for y in range(1,N+1):
  for x in range(177065*y//100000+1,(178600*y-1)//100000+1):
   count['cone_pairs']+=1
   bad=(x%13 and (y-5*x)%13==0) or (x%23 and (y-5*x)%23==0)
   L=c*x+e*y;M=a*x*x+2*b*x*y+g*y*y
   for d in range(1,min(Dmax,y)+1,2):
    count['pair_denominator_cases']+=1
    if bad:count['prime_exclusions']+=1;continue
    count['prime_survivors']+=1
    E=L*L-f*(M+d*d)
    if any(E%m not in squares[m] for m in moduli):continue
    count['square_modular_survivors']+=1
    if E<0:continue
    count['nonnegative']+=1
    s=math.isqrt(E)
    if s*s!=E:continue
    count['exact_squares']+=1
    for t in (s,-s):
     if (t-L)%f:continue
     z=(t-L)//f;count['integral_z']+=1
     w=(x,y,z)
     assert sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))==-d*d
     r=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)]
     assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2*d*d
     if math.gcd(x,y,z,d)!=1:continue
     count['primitive_witnesses']+=1;found.append({'w':w,'d':d,'r':r})
 if (N,Dmax)==(3000,25):
  assert count==dict(cone_pairs=69094,pair_denominator_cases=898201,prime_exclusions=98474,prime_survivors=799727,square_modular_survivors=3239,nonnegative=3238,exact_squares=0,integral_z=0,primitive_witnesses=0)
 return {'RQT':435,'status':'PASS exact denominator-aware cone and bounded search','source_sha256':sha,'positive_y_max':N,'odd_d_max':Dmax,'counts':count,'witnesses':found,'root19':'OPEN','rational_witness':'OPEN','candidate_position18':'UNVERIFIED','scope':'d<=y cone corridor; d>y not excluded'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--ymax',type=int,default=3000);p.add_argument('--dmax',type=int,default=25);p.add_argument('--out')
 z=p.parse_args();r=audit(json.loads(Path(z.full_rqt401_json).read_text()),z.ymax,z.dmax)
 if z.out:Path(z.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
