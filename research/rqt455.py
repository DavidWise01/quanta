import json,hashlib,math,sys,itertools
from fractions import Fraction as F
from pathlib import Path

def dot(x,G,y): return sum(x[i]*G[i][j]*y[j] for i in range(3) for j in range(3))
def lll(G):
 B=[[int(i==j) for j in range(3)] for i in range(3)]
 def gs():
  O=[];N=[];M=[]
  for b in B:
   w=list(map(F,b));row=[]
   for o,n in zip(O,N):
    u=dot(b,G,o)/n;row.append(u);w=[x-u*y for x,y in zip(w,o)]
   O.append(w);N.append(dot(w,G,w));M.append(row)
  assert min(N)>0
  return M,N
 k=1;steps=0
 while k<3:
  M,N=gs()
  for j in range(k-1,-1,-1):
   u=M[k][j];q=(2*u.numerator+u.denominator)//(2*u.denominator)
   if q:B[k]=[x-q*y for x,y in zip(B[k],B[j])];M,N=gs()
  if N[k]>=(F(3,4)-M[k][k-1]**2)*N[k-1]:k+=1
  else:B[k],B[k-1]=B[k-1],B[k];k=max(1,k-1)
  steps+=1
  assert steps<10000
 return B,steps
