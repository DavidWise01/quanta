import json,hashlib,math,sys,itertools
from fractions import Fraction as F
from pathlib import Path
import sympy as sp
from rqt458 import reduce_rows

def run(path):
 S=json.load(open(path));Q=[[int(x) for x in r] for r in S['restricted_Gram']];B=[[int(x) for x in r] for r in S['reduced_kernel_basis']];O=[[int(x) for x in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(x) for x in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*O[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[x//2 for x in Q[0]];g,e=[x//2 for x in Q[1][1:]];f=Q[2][2]//2;D=b*b-a*g;delta=a*(g*f-e*e)-b*(b*f-c*e)+c*(b*e-c*g)
 h=D//9;J=delta//9;M=abs(a);r=b//3;assert D%9==delta%9==b%3==0 and (r*r-h)%M==0
 C=[[M,r],[r,(r*r-h)//M]];u=(3,-5);v=(16,-27)
 def dot(u,v):return sum(u[i]*C[i][j]*v[j] for i in range(2) for j in range(2))
 aa,bb,gg=dot(u,u),dot(u,v),dot(v,v);assert bb*bb-aa*gg==h and aa
 def back(i,j,l,m,n):
  k,U=3*i+16*j,-5*i-27*j;P=M*k+r*U;z=n*l;d=m*l;y=F(3*P-(b*c-a*e)*z,D);x=F(U-b*y-c*z,a);return x,y,F(z),F(d)
 def norm(X):
  x,y,z,d=X;return a*x*x+2*b*x*y+g*y*y+2*c*x*z+2*e*y*z+f*z*z+d*d
 rows=[];hits=[]
 for m,n in [(1,3),(1,7),(3,1)]:
  T=a*(h*m*m-J*n*n)//M;A=aa*T;assert A>0
  p=next(p for p in (5,7,11,13,17,19,23,29,31) if h*A%p)
  seeds=[(t,j) for j in range(p) for t in range(p) if (t*t-h*j*j-A)%p==0 and (t or j)]
  assert seeds
  G=sp.diag(1,h,A);H=sp.diag(1,-h,-A)
  for er,es in [(0,0),(-2100,-4500),(-1000,-2200),(0,-4500),(-2100,0)]:
   G=sp.diag(1,h*sp.Rational(2)**er,A*sp.Rational(2)**es)
   k=12
   mod=p**k;best=None;tests=0;nontrivial=0;best_vector=None;unit_scaling=0
   for t,j in seeds[:1]:
    q=p
    for _ in range(1,2*k):
     err=(t*t-h*j*j-A)//q
     if t%p:t+=q*(-err*pow(2*t,-1,p)%p)
     else:j+=q*(-err*pow(-2*h*j,-1,p)%p)
     q*=p;assert (t*t-h*j*j-A)%q==0
    assert q==mod**2
    if t%p:
     L=sp.Matrix([[mod**2,0,0],[mod*(h*j*pow(t,-1,mod)%mod),mod,0],[t,j,1]])
    else:
     L=sp.Matrix([[mod,mod*(t*pow(h*j,-1,mod)%mod),0],[0,mod**2,0],[t,j,1]])
    assert L.det()==mod**3 and all(v%mod**2==0 for v in L*H*L.T)
    R,U=reduce_rows(L,G);assert R==U*L
    for c0 in itertools.product(range(-2,3),repeat=3):
     if not any(c0) or next(v for v in c0 if v)<0:continue
     x,y,l=map(int,R.T*sp.Matrix(c0));res=x*x-h*y*y-A*l*l;assert res%mod**2==0;tests+=1
     if not l:continue
     nontrivial+=1;g0=math.gcd(x,y,l);val=abs(res)//g0**2;unit_scaling+=abs(l)==g0
     if best is None or val<best:best=val;best_vector=[str(v//g0) for v in (x,y,l)]
     if res==0:
      i=F(x-bb*y,aa);X=back(i,y,l,m,n);assert norm(X)==0;hits.append([str(v) for v in X])
   rows.append(dict(slope=[m,n],weights=[er,es],p=p,k=k,seeds=min(1,len(seeds)),tests=tests,nontrivial=nontrivial,best_bits=None if best is None else best.bit_length(),best_residual=str(best),best_vector=best_vector,unit_scaling=unit_scaling))
 return dict(RQT=488,sha256=sha,rows=rows,hits=hits,root19='CONDITIONAL' if hits else 'OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(out)
