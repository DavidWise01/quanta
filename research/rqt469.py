import json,hashlib,math,sys,itertools
from fractions import Fraction as F
from pathlib import Path

def run(path):
 S=json.load(open(path));Q=[[int(v) for v in r] for r in S['restricted_Gram']];B=[[int(v) for v in r] for r in S['reduced_kernel_basis']];F4=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F4[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[v//2 for v in Q[0]];g,e=[v//2 for v in Q[1][1:]];f=Q[2][2]//2;z=3;D=b*b-a*g;h=a*e-b*c
 def q(x,y):return a*x*x+2*b*x*y+g*y*y+2*c*x*z+2*e*y*z+f*z*z+1
 def local(p,t,k):
  if D%p==0 and a%p:
   y=(-(t*t+(a*f-c*c)*z*z+a)*pow(2*h*z,-1,p))%p;x=((t-b*y-c*z)*pow(a,-1,p))%p
  else:
   assert a%p==0 and b%p;y=(1-c*z)*pow(b,-1,p)%p;x=(-(g*y*y+2*e*y*z+f*z*z+1)*pow(2,-1,p))%p
  m=p;assert q(x,y)%m==0
  for _ in range(1,k):
   dx=2*(a*x+b*y+c*z);dy=2*(b*x+g*y+e*z);v=q(x,y)//m
   if dx%p:x+=m*(-v*pow(dx,-1,p)%p)
   else:y+=m*(-v*pow(dy,-1,p)%p)
   m*=p;assert q(x,y)%m==0
  return x,y,m
 u=(-16,-9);v=(-9,-5);assert u[0]*v[1]-u[1]*v[0]==-1
 def coords(x,y):return -x*v[1]+y*v[0],-u[0]*y+u[1]*x
 cx=F(z*(b*e-g*c),-D);cy=F(z*(b*c-a*e),-D);assert a*cx+b*cy==-c*z and b*cx+g*cy==-e*z
 ch,ck=coords(cx,cy)
 def nearest(x):return (2*x.numerator+x.denominator)//(2*x.denominator)
 def bil(u,v):return a*u[0]*v[0]+b*(u[0]*v[1]+u[1]*v[0])+g*u[1]*v[1]
 aa,bb,gg=bil(u,u),bil(u,v),bil(v,v);assert bb*bb-aa*gg==D
 primes=(19,9781,290533,11,180497);rows=[];hits=[]
 for k in (1,2,4,8):
  M=math.prod(p**k for p in primes);base=None;best=None;seen=set();tested=0;real=0;squares=0;integral=0;controls=0
  for i,j in itertools.product(range(9),repeat=2):
   x=y=0;m=1
   for p,t in zip(primes,(i,j,(i+j)%9,0,0)):
    X,Y,n=local(p,t,k);inv=pow(m,-1,n);x+=m*((X-x)*inv%n);y+=m*((Y-y)*inv%n);m*=n;assert q(x,y)%m==0
   assert m==M;x-=M*(2*x>M);y-=M*(2*y>M);base0=abs(q(x,y));base=base0 if base is None else min(base,base0)
   h0,k0=coords(x,y);h0+=M*nearest((ch-h0)/M);k0+=M*nearest((ck-k0)/M)
   x0,y0=h0*u[0]+k0*v[0],h0*u[1]+k0*v[1];assert (x0-x)%M==(y0-y)%M==q(x0,y0)%M==0
   assert (h0%M,k0%M) not in seen;seen.add((h0%M,k0%M))
   l=bil(u,(x0,y0))+z*(c*u[0]+e*u[1]);n=bil(v,(x0,y0))+z*(c*v[0]+e*v[1]);C=q(x0,y0)
   for row in range(-40,41):
    j0=M*row;L=bb*j0+l;C0=gg*j0*j0+2*n*j0+C;E=L*L-aa*C0;tested+=1
    if E<0:continue
    real+=1;t=math.isqrt(E);squares+=t*t==E
    # Closest lattice points on either side of each real root, exact floor via isqrt.
    for sign in (-1,1):
     num=sign*t-L;den=aa*M
     if den<0:num=-num;den=-den;sg=-sign
     else:sg=sign
     floor=num//den
     if t*t!=E and sg<0 and num%den==0:floor-=1
     for col in (floor,floor+1):
      i0=M*col;X=x0+i0*u[0]+j0*v[0];Y=y0+i0*u[1]+j0*v[1];res=aa*i0*i0+2*L*i0+C0
      assert res==q(X,Y) and res%M==0 and (X-x)%M==(Y-y)%M==0;controls+=1
      if best is None or abs(res)<best:best=abs(res)
      if res==0:
       integral+=1;w=(X,Y,z);R=[sum(B[k][i]*w[i] for i in range(3)) for k in range(4)];assert sum(R[i]*F4[i][j]*R[j] for i in range(4) for j in range(4))==-2;hits.append(list(map(str,w)))
  rows.append(dict(k=k,modulus_bits=M.bit_length(),cosets=len(seen),complete_rows=tested,real_rows=real,exact_squares=squares,coordinate_controls=controls,integral_hits=integral,baseline_bits=base.bit_length(),optimized_bits=best.bit_length(),baseline_scaled_bits=(base//M).bit_length(),optimized_scaled_bits=(best//M).bit_length()))
 return dict(RQT=469,sha256=sha,z=z,d=1,rows=rows,hits=hits,root19='OPEN' if not hits else 'CONDITIONAL',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
