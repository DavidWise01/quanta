#!/usr/bin/env python3
"""RQT-373. Exact integral fourth-coordinate gate for roots 18..21."""
import itertools,json,random,argparse
from collections import Counter
F=[[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]]
H=[[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]]
U=[[224,29,-224,-130],[-193,-25,193,112],[40,5,-40,-23],[-336,-43,335,195]]
G=[[sum(U[i][k]*F[k][l]*U[j][l] for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
assert G[3][3]==-5868287405277328266
assert all(H[i][j]+H[j][i]==-F[i][j] for i in range(4) for j in range(4))
A=G[3][3]%81;S={d*d%81 for d in range(81)}
ALLOWED={(b,(-A*d*d-2*b*d)%81) for b in range(81) for d in range(81)}
def bc(t):
 b=sum(t[i]*G[i][3] for i in range(3))%81
 c=(2+sum(t[i]*G[i][j]*t[j] for i in range(3) for j in range(3)))%81
 return b,c
def core(t):
 d=[(x+4)%9-4 for x in t]
 def band(x):return 0 if x<=-2 else (1 if x<=1 else 2)
 x,y,z=d
 return 'RCF'[band(z)]+'UCD'[2-band(y)]+'LCR'[band(x)]
def pair(M,u,v):
 return sum(u[i]*M[i][j]*v[j] for i in range(4) for j in range(4))
def verify_four(block):
 if len(block)!=4 or any(len(r)!=4 or any(type(v)!=int for v in r) for r in block):
  return {'valid':False,'reason':'expected 4 integer 4-vectors'}
 norm=[pair(F,r,r) for r in block]
 w=[pair(H,block[j],block[i]) for j in range(4) for i in range(j)]
 parity=[''.join(str(x%2) for x in r) for r in block]
 return {'norms':norm,'six_lower_Wall_pairings':w,'parity':parity,
  'norm_gate':all(x==-2 for x in norm),'internal_Wall_gate':all(x==0 for x in w),
  'root18_first_parity_gate':parity[0] in ('0111','1001','1110'),
  'frozen_17_prefix_factorization':'NOT CHECKED; original prefix is required'}
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--four-roots-json')
 args=parser.parse_args()
 counts=Counter();per_core={name:Counter() for name in
  (z+y+x for z in 'RCF' for y in 'UCD' for x in 'LCR')}
 examples=[]
 for t in itertools.product(range(-40,41),repeat=3):
  b,c=bc(t);disc=(b*b-A*c)%81
  square=disc in S
  fourth=(b,c) in ALLOWED
  assert not fourth or square
  kind='old_square_exclusion' if not square else ('new_fourth_coordinate_exclusion' if not fourth else 'survives')
  counts[kind]+=1;per_core[core(t)][kind]+=1
  if kind=='new_fourth_coordinate_exclusion' and len(examples)<5:
   examples.append({'t':t,'B_mod81':b,'C_mod81':c,'Delta_mod81':disc})
 assert counts=={'old_square_exclusion':124659,'new_fourth_coordinate_exclusion':4374,'survives':402408}
 assert len(per_core)==27 and all(sum(v.values())==19683 for v in per_core.values())
 random.seed(373)
 for _ in range(2000):
  t=tuple(random.randint(-40,40) for _ in range(3))
  descendant=tuple(t[i]+81*random.randint(-20,20) for i in range(3))
  assert bc(t)==bc(descendant)
  b,c=bc(t)
  assert ((b,c) in ALLOWED)==any((A*d*d+2*b*d+c)%81==0 for d in range(81))
 result={'rqt':373,'status':'PASS','source':'authentic RQT-242 F4/H4',
  'architecture':'9^3 cubic GMA / ||||',
  'generation2_ancestors':531441,'old_exclusions':124659,
  'new_exclusions':4374,'total_exclusions':129033,
  'surviving_ancestors':402408,'counterexamples':examples,
  'per_core':{k:dict(v) for k,v in sorted(per_core.items())},
  'descendant_and_direct_d_checks':2000,'root18_to21':'OPEN'}
 if args.four_roots_json:
  with open(args.four_roots_json) as f:result['four_root_block']=verify_four(json.load(f))
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
