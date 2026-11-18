import json, hashlib, math, sys, itertools
from pathlib import Path

def run(path):
 S=json.load(open(path)); Q=[[int(v) for v in r] for r in S['restricted_Gram']]; B=[[int(v) for v in r] for r in S['reduced_kernel_basis']]; F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest(); assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[v//2 for v in Q[0]];g,e=[v//2 for v in Q[1][1:]];f=Q[2][2]//2;z=3;D=b*b-a*g;h=a*e-b*c
 def q(x,y):return a*x*x+2*b*x*y+g*y*y+2*c*x*z+2*e*y*z+f*z*z+1
 primes=(19,9781,290533,11,180497)
 def local(p,t,k):
  if D%p==0 and a%p:
   y=(-(t*t+(a*f-c*c)*z*z+a)*pow(2*h*z,-1,p))%p;x=((t-b*y-c*z)*pow(a,-1,p))%p
  else:
   assert a%p==0 and b%p
   y=(1-c*z)*pow(b,-1,p)%p;x=(-(g*y*y+2*e*y*z+f*z*z+1)*pow(2,-1,p))%p
  assert q(x,y)%p==0
  m=p
  for _ in range(1,k):
   dx=2*(a*x+b*y+c*z);dy=2*(b*x+g*y+e*z);v=q(x,y)//m
   if dx%p:x+=m*(-v*pow(dx,-1,p)%p)
   else:y+=m*(-v*pow(dy,-1,p)%p)
   m*=p;assert q(x,y)%m==0
  return x,y,m
 def combine(r,s,M,m):return r+M*((s-r)*pow(M,-1,m)%m)
 rows=[];hits=[]
 for k in (1,2,4,8):
  M=math.prod(p**k for p in primes);seen=set();best=None;controls=0
  for i,j in itertools.product(range(9),repeat=2):
   x=y=0;m=1
   for p,t in zip(primes,(i,j,(i+j)%9,0,0)):
    X,Y,n=local(p,t,k);x=combine(x,X,m,n);y=combine(y,Y,m,n);m*=n
    assert q(x,y)%m==0;controls+=1
   assert m==M
   x-=M*(2*x>M);y-=M*(2*y>M);assert q(x,y)%M==0
   seen.add((x,y));v=q(x,y);r=abs(v)//M
   if best is None or r<best:best=r
   if not v:
    w=(x,y,z);R=[sum(B[l][i]*w[i] for i in range(3)) for l in range(4)];assert sum(R[i]*F[i][j]*R[j] for i in range(4) for j in range(4))==-2;hits.append(list(map(str,w)))
  rows.append(dict(k=k,modulus_bits=M.bit_length(),unique=len(seen),crt_controls=controls,min_scaled_residual_bits=best.bit_length()))
 return dict(RQT=468,sha256=sha,z=z,d=1,primes=primes,rows=rows,hits=hits,root19='OPEN' if not hits else 'CONDITIONAL',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(out)
