#!/usr/bin/env python3
"""RQT-586 exact Pell-family odd-prime obstruction verifier.
Usage: python rqt586-gates.py RQT-583-results.json RQT-584-results.json RQT-575-reduced_gram.json
"""
import sys,json
from sympy import primerange,isprime
d=json.load(open(sys.argv[1])); old=json.load(open(sys.argv[2]));F=json.load(open(sys.argv[3]))
prior={x['family_index'] for x in old['certificates']}
expected={32:59659,39:18371,41:18371,48:59659,66:3793,68:3793,83:11027,90:75029,91:15173,97:15173,98:75029,105:11027,115:4973,127:4973}
found={}
for e in d['equations']:
 i=e['index']
 if i in prior:continue
 A,B,C=[int(e[k]) for k in 'ABC'];D=B*B-4*A*C
 r=e['ray'];o=e['offset']
 for t in (-17,-2,0,1,19):
  v=[r[j]*t+o[j] for j in range(3)]
  b=sum(F[0][j+1]*v[j] for j in range(3))
  c=sum(F[j+1][k+1]*v[j]*v[k] for j in range(3) for k in range(3))
  assert A*t*t+B*t+C==b*b-F[0][0]*(c+2)
 for p in primerange(2001,200001):
  p=int(p)
  if D%p or A%p==0 or pow(A%p,(p-1)//2,p)!=p-1:continue
  assert isprime(p)
  assert (D//p)%p!=0
  t0=(-B*pow(2*A,-1,p))%p
  z=(A*t0*t0+B*t0+C)%(p*p)
  assert z%p==0 and z!=0
  for k in (-2,-1,0,1,2):
   assert (A*(t0+k*p)**2+B*(t0+k*p)+C)%(p*p)==z
  found[i]=p;break
assert found==expected
print('PASS 14 new all-scale exclusions; 81/135 excluded, 54 open; Root19 OPEN')
