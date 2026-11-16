#!/usr/bin/env python3
"""RQT-414: exact rational-local-global hypotheses on full RQT-401 Gram.
Requires sympy. Does not construct rational coordinates or integer root19.
"""
import argparse,itertools,json,math
from pathlib import Path
import sympy as s

def audit(source):
 Q=[[int(t) for t in row] for row in source["restricted_Gram"]]
 assert len(Q)==3 and all(len(r)==3 for r in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(t%2==0 for row in Q for t in row)
 A=[[t//2 for t in row] for row in Q]
 q=lambda v:sum(A[i][j]*v[i]*v[j] for i in range(3) for j in range(3))
 assert int(s.Matrix(A).det())!=0 and A[0][0]<0
 parity={''.join(map(str,v)):q(v)%4
         for v in itertools.product((0,1),repeat=3) if any(v)}
 assert parity=={'001':3,'010':2,'011':3,'100':1,
                 '101':2,'110':3,'111':2}
 minor=[]
 for rs in itertools.combinations(range(3),2):
  for cs in itertools.combinations(range(3),2):
   i,j=rs;k,l=cs
   minor.append(A[i][k]*A[j][l]-A[i][l]*A[j][k])
 assert math.gcd(*minor)==9
 seed=(0,0,1)
 grad=[2*sum(A[i][j]*seed[j] for j in range(3))%3 for i in range(3)]
 assert (q(seed)+1)%3==0 and grad==[1,0,1]
 a,b,c=A[0][0],A[0][2],A[2][2]+1
 assert a%2 and (b*b-a*c)%8==1
 return {'RQT':414,
  'status':'PASS exact Hasse-Minkowski hypotheses',
  'real_negative_direction':True,'matrix_nonsingular':True,
  'odd_prime_minor_gcd':9,'p3_seed':[0,0,1],
  'two_adic_discriminant_mod8':1,
  'rational_anisotropy_primitive_parities':parity,
  'global_theorem':'Hasse-Minkowski applied to q(v)+t^2 has a rational isotropic vector; anisotropic q forces t != 0, hence q(v/t)=-1 over Q',
  'rational_coordinates':'NOT CONSTRUCTED','integer_root19':'OPEN',
  'root18_position':'UNVERIFIED','root20':'OPEN','root21':'conditional'}
if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument('full_rqt401_json');p.add_argument('--out')
 args=p.parse_args();r=audit(json.loads(Path(args.full_rqt401_json).read_text()))
 if args.out:Path(args.out).write_text(json.dumps(r,indent=2)+"\n")
 print(json.dumps(r,indent=2))
