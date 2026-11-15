#!/usr/bin/env python3
"""RQT-383 exact p-adic lift and LLL search on frozen original ternary planes.
Only an exact integer F4-null vector can be promoted to a root witness.
"""
import itertools,json
from math import gcd
from functools import reduce
import sympy as s

F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172

DATA={
 '194/195': (194,195,s.Matrix([[1,3,1],[-25,-74,-24],[113,340,113]]),
 s.Matrix([[-561555435662335446,907442644571173949,758956630833872688],[907442644571173949,258493091816306268,2583803041170332031],[758956630833872688,2583803041170332031,-4624133667290001854]])),
 '201/202': (201,202,s.Matrix([[1,2,1],[-26,-51,-25],[117,235,117]]),
 s.Matrix([[-932546695834969470,1534419477527031407,793284734389436322],[1534419477527031407,-372297003123752932,2700906535086376671],[793284734389436322,2700906535086376671,-4184486200006240562]]))
}
def norm(A,z):
 return int((z.T*A*z)[0])
def lift(A,p,h,y,k):
 z=s.Matrix([h,1,y]);M=p
 assert norm(A,z)%M==0 and (2*(A*z)[0])%p!=0
 for _ in range(1,k):
  error=norm(A,z)//M%p
  deriv=2*int((A*z)[0])%p
  digit=(-error*pow(deriv,-1,p))%p
  z[0]+=M*digit
  M*=p
  assert norm(A,z)%M==0
 return int(z[0]),M
def run():
 branches=steps=vectors=0;found=[];summary=[]
 for name,(m,n,V,A) in DATA.items():
  T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
  assert abs(V.det())==1 and A==V.T*T.T*F*T*V
  for p in (5,7,11,13,17):
   seeds=[]
   for h in range(p):
    for y in range(p):
     v=s.Matrix([h,1,y])
     if norm(A,v)%p==0 and (2*(A*v)[0])%p!=0:seeds.append((h,y))
   assert seeds
   for h,y in seeds[:8]:
    for k in (5,8,11,14):
     hh,M=lift(A,p,h,y,k);steps+=k-1;branches+=1
     B=s.Matrix([[M,0,0],[hh,1,y],[0,0,M]])
     assert abs(B.det())==M*M
     red=B.lll()
     candidate_rows=[red.row(i) for i in range(3)]
     candidate_rows.extend(sum((coeff[i]*red.row(i) for i in range(3)),s.zeros(1,3))
       for coeff in itertools.product((-2,-1,0,1,2),repeat=3) if any(coeff))
     for row in candidate_rows:
      z=s.Matrix(list(row))
      vectors+=1
      if norm(A,z)!=0 or all(int(v)==0 for v in z):continue
      d=reduce(gcd,(abs(int(t)) for t in z),0)
      z=z/d
      u=T*V*z
      assert norm(F,u)==0
      found.append({'plane':name,'prime':p,'exponent':k,
       'u':[int(t) for t in u],'z':[int(t) for t in z]})
   summary.append({'plane':name,'prime':p,'smooth_mod_prime_seeds':len(seeds),
                   'seeds_tested':min(8,len(seeds))})
 return {'rqt':383,'status':'EXACT GLOBAL NULL FOUND' if found else 'LOCAL LIFTS PASS; GLOBAL NULL NOT FOUND',
 'lifting_branches':branches,'exact_lift_steps':steps,
 'integer_vectors_exactly_tested':vectors,'primes':[5,7,11,13,17],
 'lift_exponents':[5,8,11,14],'per_prime':summary,'global_null_witnesses':found[:5],
 'root18_to21':'OPEN','scope':'sampled local branches, no global nonexistence conclusion'}
if __name__=='__main__':print(json.dumps(run(),indent=2))
