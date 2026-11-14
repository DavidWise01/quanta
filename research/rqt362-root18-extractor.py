#!/usr/bin/env python3
"""RQT-362 exact, conditional root-18 extractor; NOT a recovered original root.
Usage: python research/rqt362-root18-extractor.py --u X0 X1 X2 X3
Optionally: --prior-roots-json prior17.json (17 ordered integer 4-vectors).
"""
import argparse,itertools,json
from math import gcd
from functools import reduce
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
assert H.det()==1 and H+H.T==-F
ALLOWED={'0111','1001','1110'}
def eg(a,b):
 aa,bb=abs(a),abs(b);x0,y0,x1,y1=1,0,0,1
 while bb:
  k=aa//bb;aa,bb=bb,aa-k*bb;x0,x1=x1,x0-k*x1;y0,y1=y1,y0-k*y1
 return aa,x0*(1 if a>=0 else -1),y0*(1 if b>=0 else -1)
def bezout(p):
 d=0;coeff=[]
 for v in p:
  g,x,y=eg(d,int(v));coeff=[x*z for z in coeff]+[y];d=g
 assert sum(int(a)*b for a,b in zip(p,coeff))==d
 return d,s.Matrix(coeff)
def q(M,v):
 n=int((v.T*M*v)[0]);assert n%2==0;return n//2
def parity(v):return ''.join(str(int(a)%2) for a in v)
def extract(M,u):
 assert u.rows==M.rows and M==M.T
 assert reduce(gcd,(abs(int(a)) for a in u))==1,'nonprimitive u'
 assert q(M,u)==0,'nonisotropic u'
 p=M*u;d,z=bezout(p)
 assert d==1,'pairing divisibility is not one'
 for bits in itertools.product((0,1),repeat=M.rows):
  v0=s.Matrix(bits);pair=int((u.T*M*v0)[0])
  if pair%2==0:continue
  v=v0+2*((1-pair)//2)*z
  assert int((u.T*M*v)[0])==1
  r=(1+q(M,v))*u-v
  assert q(M,r)==-1
  if parity(r) in ALLOWED:return v,r
 return None
def selftest():
 U=s.Matrix([[0,1],[1,0]]);M=s.diag(U,U)
 v,r=extract(M,s.Matrix([1,0,0,0]))
 assert q(M,r)==-1 and parity(r) in ALLOWED
 print('PASS synthetic U+U extraction',list(map(int,r)))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--u',nargs=4,type=int)
 ap.add_argument('--prior-roots-json')
 a=ap.parse_args();selftest()
 if a.u is None:
  print(json.dumps({'root18':'OPEN','cause':'no authentic primitive F4-null vector supplied or found','synthetic_test':'PASS'},indent=2));return
 u=s.Matrix(a.u);found=extract(F,u)
 if found is None:
  print(json.dumps({'root18':'OPEN','reason':'no permitted parity in enumerated pairings'}));return
 v,r=found
 result={'u':list(map(int,u)),'v':list(map(int,v)),'root':list(map(int,r)),
 'norm':int((r.T*F*r)[0]),'parity':parity(r),'H_self':int((r.T*H*r)[0])}
 assert result['norm']==-2 and result['H_self']==1
 if a.prior_roots_json:
  with open(a.prior_roots_json) as f:prior=json.load(f)
  assert len(prior)==17 and all(len(z)==4 for z in prior)
  w=[int((r.T*H*s.Matrix(z))[0]) for z in prior]
  result['Wall_prefix_18_versus_1_to_17']=w
  result['status']='VALID PREFIX EXTENSION' if all(z==0 for z in w) else 'NOT PREFIX COMPATIBLE'
 else:result['status']='NORM ROOT ONLY; ORIGINAL 17-PREFIX NOT CHECKED'
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
