#!/usr/bin/env python3
"""RQT-381 exact parity bridge from isotropic null vector; no original root claimed."""
import argparse,itertools,json
from functools import reduce
from math import gcd
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
ALLOWED=('0111','1001','1110')
def parity(v):return ''.join(str(int(z)%2) for z in v)
def q(v):
 n=int((v.T*F*v)[0]);assert n%2==0;return n//2
def pair(u,v):return int((u.T*F*v)[0])
def bezout(v):
 d=0;coeff=[]
 for a in v:
  x,y,g=map(int,s.gcdex(d,int(a)))
  coeff=[x*c for c in coeff]+[y];d=g
 assert d>=0 and sum(int(a)*b for a,b in zip(v,coeff))==d
 return d,s.Matrix(coeff)
def options(u):
 out={}
 for ds in itertools.product(range(4),repeat=4):
  v=s.Matrix(ds)
  if pair(u,v)%4!=1:continue
  p=parity((1+q(v))*u-v)
  if p in ALLOWED and p not in out:out[p]=list(ds)
 return out
def construct(u):
 assert u.shape==(4,1) and q(u)==0
 assert reduce(gcd,(abs(int(x)) for x in u),0)==1
 d,z=bezout(F*u)
 assert d==1,'pairing divisibility must be one'
 choices=options(u)
 assert choices,'no accepted parity residue for this isotropic u'
 selected=next(p for p in ALLOWED if p in choices)
 v0=s.Matrix(choices[selected]);n=pair(u,v0)
 assert n%4==1
 v=v0+4*((1-n)//4)*z
 r=(1+q(v))*u-v
 assert pair(u,v)==1 and q(r)==-1 and parity(r)==selected
 assert int((r.T*H*r)[0])==1
 return {'u':list(map(int,u)),'bezout_v':list(map(int,v)),
 'exact_original_root':list(map(int,r)),'norm':int((r.T*F*r)[0]),
 'parity':selected,'predecessor_factorization':'NOT CHECKED'}
def plane(m,n):
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 cs=[];counts={p:0 for p in ALLOWED}
 for ds in itertools.product(range(4),repeat=3):
  u=T*s.Matrix(ds)
  if (2*q(u))%8 or not any(int(x)%2 for x in u):continue
  assert reduce(gcd,(int(x)%2 for x in F*u),0)==1
  opts=options(u)
  assert len(opts)>=2
  for p in opts:counts[p]+=1
  cs.append({'ternary_mod4':list(ds),'u_mod4':[int(x)%4 for x in u],
   'accepted_root_parities':sorted(opts),'v_mod4_witnesses':opts})
 assert len(cs)==16
 return {'plane':str(m)+'/'+str(n),'eligible_classes':16,
  'classes_reaching_at_least_two_accepted_parities':16,
  'per_parity_class_counts':counts,'witnesses':cs}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--u',type=int,nargs=4)
 args=ap.parse_args()
 out={'rqt':381,'status':'PASS exact conditional parity bridge',
 'planes':[plane(194,195),plane(201,202)],
 'root_existence':'CONDITIONAL upon earlier RQT351 rational isotropy and RQT353A divisibility-one theorem',
 'explicit_u_found':False,'actual_root18_to21':'OPEN',
 'frozen_17_root_prefix':'NOT CHECKED'}
 if args.u:out['new_exact_root_candidate']=construct(s.Matrix(args.u))
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
