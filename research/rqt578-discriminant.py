#!/usr/bin/env python3
"""RQT-578 exact narrow-cone discriminant search.
Usage: python rqt578.py reduced_gram.json [bound=120]
Only three coordinates are bounded; the fourth is solved over all integers.
"""
import json,math,sys,itertools
F=[[int(y) for y in row] for row in json.load(open(sys.argv[1]))]
B=int(sys.argv[2]) if len(sys.argv)>2 else 120
a=F[0][0];n=nonneg=squares=hits=0
for v,w,z in itertools.product(range(-B,B+1),repeat=3):
 b=F[0][1]*v+F[0][2]*w+F[0][3]*z
 c=F[1][1]*v*v+F[2][2]*w*w+F[3][3]*z*z+2*(F[1][2]*v*w+F[1][3]*v*z+F[2][3]*w*z)
 delta=b*b-a*(c+2);n+=1
 if delta<0:continue
 nonneg+=1;r=math.isqrt(delta)
 if r*r!=delta:continue
 squares+=1
 for k in set((r,-r)):
  t=-b+k
  if t%a==0:
   u=t//a
   x=(u,v,w,z)
   assert sum(x[i]*F[i][j]*x[j] for i in range(4) for j in range(4))==-2
   hits+=1
assert (B,n,nonneg,squares,hits)==(120,13997521,17,0,0)
print('RQT-578 PASS: 13997521 triples, 17 real-coordinate possibilities, 0 squares, 0 integer roots. Root19 OPEN.')
