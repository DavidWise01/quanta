#!/usr/bin/env python3
"""RQT-363: original rank-four direct norm -2 cylinder, exact integer arithmetic.
RQT-362 correction: RQT-257 six Wall constraints are internal to proposed
four-root block; orthogonality to all previous 17 is NOT a proven gate.
"""
from math import isqrt
import json
import sympy as sp
F=sp.Matrix([
[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=sp.Matrix([
[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],
[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],
[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],
[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
U=sp.Matrix([
[224,29,-224,-130],
[-193,-25,193,112],
[40,5,-40,-23],
[-336,-43,335,195]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
assert H.det()==1 and H+H.T==-F and abs(U.det())==1
G=U*F*U.T
mat=[[int(G[i,j]) for j in range(4)] for i in range(4)]
A=mat[3][3]
R=60
count=nonnegative=square=integer=0
found=[]
for a in range(-R,R+1):
 for b in range(-R,R+1):
  for c in range(-R,R+1):
   count+=1
   B=2*(mat[0][3]*a+mat[1][3]*b+mat[2][3]*c)
   C=(mat[0][0]*a*a+mat[1][1]*b*b+mat[2][2]*c*c
      +2*(mat[0][1]*a*b+mat[0][2]*a*c+mat[1][2]*b*c)+2)
   disc=B*B-4*A*C
   if disc<0:continue
   nonnegative+=1
   t=isqrt(disc)
   if t*t!=disc:continue
   square+=1
   for top in {-B+t,-B-t}:
    if top%(2*A):continue
    z=sp.Matrix([a,b,c,top//(2*A)])
    r=U.T*z
    assert int((r.T*F*r)[0])==-2
    integer+=1
    found.append([int(v) for v in r])
assert (count,nonnegative,square,integer)==(1771561,81167,0,0)
print(json.dumps({
 'status':'PASS exact four-dimensional cylinder exclusion',
 'source':'stoicheion frozen authentic F4/H4',
 'unimodular_U':[[int(v) for v in row] for row in U.tolist()],
 'tested_triples':count,'nonnegative_discriminants':nonnegative,
 'perfect_square_discriminants':square,
 'integer_norm_minus_two_candidates':integer,'exact_candidates':found,
 'bounded':{'t0':[-60,60],'t1':[-60,60],'t2':[-60,60]},
 'unbounded':'t3 determined by exact discriminant',
 'root18':'OPEN',
 'prefix_correction':'RQT-257 six Wall pairings involve candidate four-root block, NOT an automatic orthogonality condition against all preceding 17 roots'
},indent=2))
