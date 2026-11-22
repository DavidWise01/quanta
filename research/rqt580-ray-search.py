#!/usr/bin/env python3
"""RQT-580 exact selected-ray neighborhood search. Requires reduced_gram.json from RQT-575."""
import json,math,itertools,sys
F=[[int(x) for x in row] for row in json.load(open(sys.argv[1]))]
a=F[0][0]
rays=[(35,-10,14),(45,-13,18),(80,-23,32),(95,-27,38),(115,-33,46)]
counts=[0,0,0,0]
for r in rays:
 for offset in itertools.product((-1,0,1),repeat=3):
  for t in range(1,20001):
   v,w,z=[t*r[i]+offset[i] for i in range(3)]
   b=F[0][1]*v+F[0][2]*w+F[0][3]*z
   c=F[1][1]*v*v+F[2][2]*w*w+F[3][3]*z*z+2*(F[1][2]*v*w+F[1][3]*v*z+F[2][3]*w*z)
   delta=b*b-a*(c+2);counts[0]+=1
   if delta<0:continue
   counts[1]+=1
   sq=math.isqrt(delta)
   if sq*sq!=delta:continue
   counts[2]+=1
   for sign in (-1,1):
    if (-b+sign*sq)%a==0:counts[3]+=1
assert counts==[2700000,2695792,0,0],counts
print('RQT-580 PASS',counts,'— no exact norm -2 hit in selected finite rays; Root19 OPEN')
