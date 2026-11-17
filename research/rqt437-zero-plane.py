#!/usr/bin/env python3
"""RQT-437: unbounded y=0 exclusion, exact variable-width cone.
Usage: python research/rqt437-zero-plane.py RQT401_FULL.json
"""
import argparse,hashlib,json,math
from pathlib import Path
def audit(src):
 Q=[[int(v) for v in r] for r in src['restricted_Gram']]
 B=[[int(v) for v in r] for r in src['reduced_kernel_basis']]
 F=[[int(v) for v in r] for r in src['original_F4']]
 assert len(Q)==3 and all(len(r)==3 for r in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(v%2==0 for r in Q for v in r)
 assert all(sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4))==Q[i][j] for i in range(3) for j in range(3))
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest()
 assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 A=[[v//2 for v in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2]
 assert (a%11,c%11,f%11,a%121)==(0,0,3,88)
 assert 8 not in {t*t%11 for t in range(11)}
 assert all((3*z*z+d*d)%11 for z in range(11) for d in range(11) if z or d)
 assert all((88*x*x)%121 for x in range(1,11))
 alpha=c*c-f*a;K=c*e-f*b;gamma=e*e-f*g;delta=-f
 assert alpha<0 and delta>0
 checks=[]
 for x,y,d in [(0,1,1),(16,9,1),(41,23,3),(0,1,1<<600),(125,70,27)]:
  L=c*x+e*y;M=a*x*x+2*b*x*y+g*y*y
  E=L*L-f*(M+d*d)
  lhs=(alpha*x+K*y)**2
  rhs=(K*K-alpha*gamma)*y*y-alpha*delta*d*d
  assert alpha*E==lhs-rhs and (E>=0)==(lhs<=rhs)
  checks.append({'x':str(x),'y':str(y),'d_bits':abs(d).bit_length(),
   'real_feasible':E>=0,'exact_square':E>=0 and math.isqrt(E)**2==E})
 assert checks[3]['real_feasible'] and not checks[3]['exact_square']
 return {'RQT':437,'status':'PASS exact zero-plane proof and expanding cone',
  'sha256':sha,'zero_plane':'Every y=0 integer null vector has 11|x,z,d, so cannot be primitive',
  'mod11_coefficients':[a%11,c%11,f%11],'a_mod121':a%121,
  'conic_inequality':'(alpha*x+K*y)^2 <= (K^2-alpha*gamma)*y^2-alpha*delta*d^2',
  'samples':checks,'rational_witness':'OPEN','root19':'OPEN','root18_prefix':'UNVERIFIED'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json');p.add_argument('--out')
 args=p.parse_args();r=audit(json.loads(Path(args.full_rqt401_json).read_text()))
 if args.out:Path(args.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
