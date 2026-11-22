#!/usr/bin/env python3
"""RQT-595 exact family-28 generalized Pell gate. Python 3 standard library."""
import sys,json,math,hashlib
from pathlib import Path
p=Path(sys.argv[1]);g=Path(sys.argv[2]);src=p.read_bytes()
assert hashlib.sha256(src).hexdigest()=="5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92"
eq=json.loads(src)["equations"];f=next(e for e in eq if e["index"]==28)
F=json.loads(g.read_text())
A,B,C,D=map(int,(f["A"],f["B"],f["C"],f["D"]))
N=4*A;assert B*B-4*A*C==D and math.isqrt(N)**2!=N
for t in (-97,-1,0,1,97):
 v=[f["ray"][j]*t+f["offset"][j] for j in range(3)]
 b=sum(F[0][j+1]*v[j] for j in range(3))
 c=sum(F[j+1][k+1]*v[j]*v[k] for j in range(3) for k in range(3))
 assert b*b-F[0][0]*(c+2)==A*t*t+B*t+C
 assert (2*A*t+B)**2-N*(A*t*t+B*t+C)==D
a0=math.isqrt(N);m,d,a=0,1,a0
h2,h1,k2,k1=0,1,1,0
for i in range(10000):
 h=a*h1+h2;k=a*k1+k2
 assert h*h-N*k*k!=1
 h2,h1,k2,k1=h1,h,k1,k
 m=d*a-m;d=(N-m*m)//d;a=(a0+m)//d
U=a0*a0+N;V=2*a0;W=a0*a0-N
assert W!=0 and U*U-N*V*V==W*W
hits=[]
for t in range(-12000,12001):
 z=A*t*t+B*t+C
 if z>=0 and math.isqrt(z)**2==z:hits.append(t)
assert hits==[]
print("PASS: family 28 Pell identities; 10000 convergents without norm-one unit; no finite square hits; rational norm-one action only; Root19 OPEN")
