#!/usr/bin/env python3
"""RQT-354: two explicit 3-adic isotropic branches on authentic 199/200 plane.
These are modulo 3^31 witnesses, NOT integer norm-zero vectors or root18.
No general ternary solver success is claimed.
"""
import itertools, json
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
T=s.Matrix([[-199,0,0],[0,1,0],[200,0,0],[0,0,1]])
G=T.T*F*T;M=F*T
g=[[int(G[i,j]) for j in range(3)] for i in range(3)]
f=[[int(M[i,j]) for j in range(3)] for i in range(4)]
def norm(v):return sum(v[i]*g[i][j]*v[j] for i in range(3) for j in range(3))
def div3(v):return all(sum(f[i][j]*v[j] for j in range(3))%3==0 for i in range(4))
def lifts(v,k):
 p=3**k; mod=3*p
 out=[]
 for digits in itertools.product(range(3),repeat=3):
  w=tuple(v[i]+p*digits[i] for i in range(3))
  if norm(w)%mod==0:out.append(w)
 return out
def branch(seed,depth=31,lookahead=False):
 v=tuple(seed);assert any(z%3 for z in v) and norm(v)%3==0
 counts=[]
 for k in range(1,depth):
  options=lifts(v,k)
  if lookahead:
   productive=[w for w in options if lifts(w,k+1)]
   assert productive
   v=productive[0]
   counts.append({'exponent':k+1,'valid_next_digits':len(options),'next_liftable':len(productive)})
  else:
   assert options
   v=options[0]
   counts.append({'exponent':k+1,'valid_next_digits':len(options)})
  assert norm(v)%(3**(k+1))==0
 return v,counts
# Prove the obvious d3 representative mod9 is not itself liftable modulo27,
# while precisely six of its 27 alternative mod9 representatives are.
base=(1,0,0);all9=lifts(base,1)
assert len(all9)==27 and not lifts(base,2)
assert sum(bool(lifts(w,2)) for w in all9)==6
d3,c3=branch(base,31,True)
d1,c1=branch((0,1,1),31,False)
assert div3(d3) and not div3(d1)
assert norm(d3)%(3**31)==0 and norm(d1)%(3**31)==0
assert norm(d3)!=0 and norm(d1)!=0
print(json.dumps({'status':'PASS exact finite 3-adic branch certificates',
 'source':'stoicheion RQT-242 authentic F4','slope':'199/200',
 'modulus':'3^31','initial_d3_mod9_branches':27,
 'mod9_branches_liftable_mod27':6,
 'd3_branch':{'ternary_coordinates':list(d3),'pairing_divisible_by3':True,
              'norm_mod_3power31':norm(d3)%(3**31),'branch_choices':c3},
 'd1_branch':{'ternary_coordinates':list(d1),'pairing_divisible_by3':False,
              'norm_mod_3power31':norm(d1)%(3**31),'branch_choices':c1},
 'exact_integral_isotropic':'OPEN','exact_root18':'OPEN',
 'roots19_to21':'OPEN'},indent=2))
