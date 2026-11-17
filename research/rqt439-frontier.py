#!/usr/bin/env python3
"""RQT-439: disjoint frontier expansion. Usage: python research/rqt439-frontier.py RQT401_FULL.json [output.json]"""
import json,math,hashlib,sys
from pathlib import Path
s=json.load(open(sys.argv[1])); Q=[[int(t) for t in r] for r in s['restricted_Gram']];B=[[int(t) for t in r] for r in s['reduced_kernel_basis']];F=[[int(t) for t in r] for r in s['original_F4']]
sha=hashlib.sha256(json.dumps([[str(t) for t in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
assert all(Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) and Q[i][j]%2==0 for i in range(3) for j in range(3))
A=[[t//2 for t in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2];al=c*c-f*a;K=c*e-f*b;ga=e*e-f*g;de=-f;assert al<0 and de>0
for p,n in [(13,11),(23,7)]:assert f%p==(c+5*e)%p==0 and (-a-10*b-25*g)%p==n and n not in {i*i%p for i in range(p)}
mods=(256,63,65,11,17,19,23,31);sq={m:{i*i%m for i in range(m)} for m in mods}
res=[]
for name,yl,yh,dl,dh in [('denominator',1,256,257,511),('numerator',257,512,1,511)]:
 cnt=dict.fromkeys(['pairs','empty','x','prime_rejected','modular_survivors','squares','witnesses'],0);hits=[]
 for y in range(yl,yh+1):
  for d in range(dl,dh+1,2):
   cnt['pairs']+=1;R=(K*K-al*ga)*y*y-al*de*d*d
   if R<0:cnt['empty']+=1;continue
   h=math.isqrt(R);lo=-((h-K*y)//(-al));hi=(K*y+h)//(-al)
   if lo>hi:cnt['empty']+=1;continue
   for x in range(lo,hi+1):
    cnt['x']+=1;E=al*x*x+2*K*x*y+ga*y*y+de*d*d;assert E>=0
    if (x%13 and (y-5*x)%13==0) or (x%23 and (y-5*x)%23==0):cnt['prime_rejected']+=1;continue
    if any(E%m not in sq[m] for m in mods):continue
    cnt['modular_survivors']+=1;t=math.isqrt(E)
    if t*t!=E:continue
    cnt['squares']+=1
    for ss in {t,-t}:
     L=c*x+e*y
     if (ss-L)%f:continue
     z=(ss-L)//f;w=(x,y,z);assert sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))==-d*d
     r=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)];assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2*d*d
     if math.gcd(x,y,z,d)==1:cnt['witnesses']+=1;hits.append([str(t) for t in (*w,d)])
 res.append(dict(tile=name,y=[yl,yh],d=[dl,dh],counts=cnt,hits=hits))
 print(name,cnt,flush=True)
out={'RQT':439,'sha256':sha,'tiles':res,'root19':'OPEN' if not any(t['hits'] for t in res) else 'REVIEW WITNESSES','root18_position':'UNVERIFIED'}
Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-439-results.json').write_text(json.dumps(out,indent=2))
