import json, hashlib, math, sys
from fractions import Fraction as F
from pathlib import Path

def run(path):
 s=json.load(open(path));Q=[[int(t) for t in r] for r in s['restricted_Gram']];B=[[int(t) for t in r] for r in s['reduced_kernel_basis']];F4=[[int(t) for t in r] for r in s['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(t) for t in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F4[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[t//2 for t in Q[0]];g,e=[t//2 for t in Q[1][1:]];f=Q[2][2]//2
 def q(x,y,z):return a*x*x+2*b*x*y+g*y*y+2*c*x*z+2*e*y*z+f*z*z+1
 u=(-16,-9);v=(-9,-5);assert u[0]*v[1]-u[1]*v[0]==-1
 def bil(u,v):return a*u[0]*v[0]+b*(u[0]*v[1]+u[1]*v[0])+g*u[1]*v[1]
 aa,bb,gg=bil(u,u),bil(u,v),bil(v,v);D=b*b-a*g;assert bb*bb-aa*gg==D and aa
 mods=(64,63,65,11,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)
 sq={m:{i*i%m for i in range(m)} for m in mods};rows=[];hits=[]; controls=0
 for z in (3,5,7,9,10,13,14,17,19):
  cx=F(z*(b*e-g*c),-D);cy=F(z*(b*c-a*e),-D)
  assert a*cx+b*cy==-c*z and b*cx+g*cy==-e*z
  def near(t):return (2*t.numerator+t.denominator)//(2*t.denominator)
  h,k=near(-cx*v[1]+cy*v[0]),near(-u[0]*cy+u[1]*cx)
  x0,y0=h*u[0]+k*v[0],h*u[1]+k*v[1]
  l=bil(u,(x0,y0))+z*(c*u[0]+e*u[1]);n=bil(v,(x0,y0))+z*(c*v[0]+e*v[1]);C=q(x0,y0,z)
  E0=l*l-aa*C;E1=2*(bb*l-aa*n)
  coeff=[(m,D%m,E1%m,E0%m) for m in mods];counts=[0]*len(mods);total=neg=exact=checks=0
  intervals=[(-29524,-3281),(3281,29524)] if z==3 else [(-29524,29524)]
  for lo,hi in intervals:
   for j in range(lo,hi+1):
    total+=1
    if (j-lo)%997==0:
     E=D*j*j+E1*j+E0;assert E==(bb*j+l)**2-aa*(gg*j*j+2*n*j+C);assert all((A*j*j+K*j+T)%m==E%m for m,A,K,T in coeff);controls+=1
    for i,(m,A,K,T) in enumerate(coeff):
     if (A*j*j+K*j+T)%m not in sq[m]:break
     counts[i]+=1
    else:
     E=D*j*j+E1*j+E0
     if E<0:neg+=1;continue
     checks+=1;t=math.isqrt(E)
     if t*t!=E:continue
     exact+=1
     for r in {t,-t}:
      i,rem=divmod(r-bb*j-l,aa)
      if rem:continue
      x=x0+i*u[0]+j*v[0];y=y0+i*u[1]+j*v[1];assert q(x,y,z)==0
      w=(x,y,z);X=[sum(B[k][i]*w[i] for i in range(3)) for k in range(4)];assert sum(X[i]*F4[i][j]*X[j] for i in range(4) for j in range(4))==-2;hits.append(list(map(str,w)))
  rows.append(dict(z=z,intervals=intervals,rows=total,survivors=counts,negative=neg,square_tests=checks,exact_squares=exact))
 return dict(RQT=463,sha256=sha,mods=mods,branches=rows,controls=controls,total_rows=sum(r['rows'] for r in rows),totals=[sum(r['survivors'][i] for r in rows) for i in range(len(mods))],square_tests=sum(r['square_tests'] for r in rows),hits=hits,root19='OPEN' if not hits else 'CONDITIONAL',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='branches'})
