#!/usr/bin/env python3
"""RQT-384: exact conic decoder and global coordinate-zero obstruction.
No original null-vector seed is claimed to have been recovered.
"""
import argparse,itertools,json,random
from math import isqrt,gcd
from functools import reduce
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
PLANES=[(194,195,s.Matrix([[1,3,1],[-25,-74,-24],[113,340,113]])),
(201,202,s.Matrix([[1,2,1],[-26,-51,-25],[117,235,117]]))]
def norm(A,z):return int((z.T*A*z)[0])
def primitive(z):
 d=reduce(gcd,(abs(int(x)) for x in z),0)
 return s.Matrix([int(x)//d for x in z]) if d else None
def decoder(A,u,w):
 assert norm(A,u)==0
 p=int((u.T*A*w)[0]); q=norm(A,w)
 z=primitive(q*u-2*p*w)
 if z is not None:assert norm(A,z)==0
 return z
def audit(m,n,V):
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 assert abs(V.det())==1
 A=V.T*T.T*F*T*V
 results=[]
 for omission in range(3):
  ids=[i for i in range(3) if i!=omission]
  B=A.extract(ids,ids)
  delta=int(B[0,1]**2-B[0,0]*B[1,1])
  possible=delta>=0 and isqrt(delta)**2==delta
  assert not possible
  results.append({'zero_coordinate':('h','x','y')[omission],
    'binary_half_discriminant':str(delta),
    'rational_null_possible':False})
 return T,A,results
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--plane',choices=('194/195','201/202'))
 p.add_argument('--seed',nargs=3,type=int)
 a=p.parse_args()
 report={'rqt':384,'result':'PASS exact global coordinate-hyperplane obstruction',
   'original_roots18_to21':'OPEN','original_integer_null_seed':'NOT FOUND'}
 db={}
 for m,n,V in PLANES:
  T,A,res=audit(m,n,V)
  db[f'{m}/{n}']=(T,A)
  report.setdefault('planes',[]).append({'name':f'{m}/{n}',
   'ternary_det':str(A.det()),'coordinate_slices':res})
 A=s.diag(1,1,-1);u=s.Matrix([1,0,1]);rng=random.Random(384);points=set()
 for j in range(150):
  w=s.Matrix([rng.randint(-10,10) for _ in range(3)])
  z=decoder(A,u,w)
  if z is not None:points.add(tuple(map(int,z)))
 assert len(points)>=20
 report['synthetic_parametrization_exact_points']=len(points)
 if a.seed is not None:
  assert a.plane is not None
  T,A=db[a.plane];u=primitive(s.Matrix(a.seed))
  assert u is not None and norm(A,u)==0
  witnesses=[]
  for w in itertools.product(range(-3,4),repeat=3):
   z=decoder(A,u,s.Matrix(w))
   if z is None:continue
   root=T*z;assert norm(F,root)==0
   witnesses.append({'ternary':list(map(int,z)),
    'original_null':list(map(int,root))})
   if len(witnesses)==15:break
  report['verified_original_null_family']=witnesses
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
