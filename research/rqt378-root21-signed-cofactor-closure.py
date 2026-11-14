#!/usr/bin/env python3
"""RQT-378 exact root21 cofactor closure. Authentic RQT-242 F4/H4."""
import argparse, itertools, json
from math import gcd
from functools import reduce
import sympy as s

F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172

def signed_cofactors(C):
 assert C.shape==(3,4)
 v=s.Matrix([(-1)**j*C[:,[k for k in range(4) if k!=j]].det() for j in range(4)])
 assert C*v==s.zeros(3,1)
 return v

def complete(first_three,gram=F,wall=H):
 assert len(first_three)==3 and all(len(z)==4 for z in first_three)
 R=s.Matrix.hstack(*(s.Matrix(z) for z in first_three))
 if R.rank()!=3:return {'status':'REJECT','reason':'dependent prefix'}
 norm=[int((R[:,j].T*gram*R[:,j])[0]) for j in range(3)]
 low=[int((R[:,j].T*wall*R[:,i])[0]) for i in range(3) for j in range(i+1,3)]
 if norm!=[-2,-2,-2] or any(low):
  return {'status':'REJECT','reason':'norm or internal Wall pairing failure','norms':norm,'lower_Wall':low}
 C=R.T*wall.T
 v=signed_cofactors(C)
 content=reduce(gcd,(abs(int(z)) for z in v))
 if content!=1:return {'status':'REJECT','reason':'nonprimitive three-root prefix','cofactor_content':content}
 choices=[]
 for sign in (1,-1):
  w=sign*v; n=int((w.T*gram*w)[0]);d=int(s.Matrix.hstack(R,w).det())
  choices.append({'sign':sign,'r21':[int(z) for z in w],'norm':n,'determinant':d,'four_flag_pass':n==-2 and abs(d)==1})
 return {'status':'PASS cofactor closure','cofactor':[int(z) for z in v],
         'two_candidates':choices,'four_root_flag_pass':any(z['four_flag_pass'] for z in choices)}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--three-roots-json');a=parser.parse_args()
 good=complete([[1,0,0,0],[0,1,0,0],[0,0,1,0]],-2*s.eye(4),s.eye(4))
 bad=complete([[2,0,0,0],[0,1,0,0],[0,0,1,0]],-2*s.eye(4),s.eye(4))
 assert good['four_root_flag_pass'] and bad['status']=='REJECT'
 C=s.eye(4)[:3,:]*H.T;v=signed_cofactors(C)
 assert reduce(gcd,(abs(int(z)) for z in v))==1
 data={'rqt':378,'status':'PASS exact original Wall cofactor identities',
       'synthetic_positive':good,'synthetic_negative':bad,
       'original_arbitrary_prefix_kernel_verified':True,
       'roots18_19_20_21':'OPEN','predecessor_17_product':'NOT CHECKED'}
 if a.three_roots_json:
  with open(a.three_roots_json) as f: x=json.load(f)
  data['proposed_original_three_roots']=complete(x)
 print(json.dumps(data,indent=2))
if __name__=='__main__':main()
