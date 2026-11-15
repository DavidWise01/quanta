#!/usr/bin/env python3
"""RQT-406: all three primitive parity classes admit 2-adic norm -2 solutions.
Input: complete RQT-401 JSON with restricted_Gram. Python integers only.
"""
import argparse,itertools,json
from pathlib import Path

def audit(data,max_power=64):
 Q=[[int(v) for v in row] for row in data['restricted_Gram']]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(v%2==0 for row in Q for v in row)
 A=[[v//2 for v in row] for row in Q]
 assert [[v%4 for v in row] for row in A]==[[1,0,1],[0,2,3],[1,3,3]]
 classes={}
 for v in itertools.product(range(2),repeat=3):
  if not any(v):continue
  classes[''.join(map(str,v))]=sum(A[i][j]*v[i]*v[j] for i in range(3) for j in range(3))%4
 allowed=[k for k,t in classes.items() if t==3]
 assert allowed==['001','011','110']
 seeds={'001':(0,1),'011':(1,1),'110':(1,2)}
 rows={}
 for tag,(y,z) in seeds.items():
  a=A[0][0];b=A[0][1]*y+A[0][2]*z
  c=A[1][1]*y*y+2*A[1][2]*y*z+A[2][2]*z*z+1
  D=b*b-a*c
  assert a%2==1 and D%8==1
  roots=[r for r in range(8) if (r*r-D)%8==0]
  modulus=8; witnesses={}
  for k in range(3,max_power+1):
   if k>3:
    new=2*modulus
    roots=[r+t*modulus for r in roots for t in (0,1) if ((r+t*modulus)**2-D)%new==0]
    modulus=new
   assert roots
   if k in (8,16,32,64):
    xs=[((-b+r)*pow(a,-1,modulus))%modulus for r in roots]
    xs=[x for x in xs if (x%2,y%2,z%2)==tuple(map(int,tag))]
    assert xs
    x=xs[0]
    assert (a*x*x+2*b*x+c)%modulus==0
    assert (1+sum(A[i][j]*(x,y,z)[i]*(x,y,z)[j] for i in range(3) for j in range(3)))%modulus==0
    witnesses[str(k)]=str(x)
  rows[tag]={'y':y,'z':z,'D_mod8':D%8,'D_mod256':D%256,'x_mod_2k':witnesses}
 return {'RQT':406,'status':'PASS: all allowed primitive classes are 2-adically represented',
  'primitive_half_norm_mod4':classes,'allowed_parity':allowed,'families':rows,
  'infinite_proof':'D==1 mod8 has square root in Z2 and a is odd, so x=(-b+sqrt(D))/a in Z2',
  'ordinary_integral_root19':'OPEN',
  'position18_frozen_predecessor':'UNVERIFIED'}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('full_kernel_json');p.add_argument('--out')
 args=p.parse_args();result=audit(json.loads(Path(args.full_kernel_json).read_text()))
 if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
