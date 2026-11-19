import json,hashlib,math,sys
from fractions import Fraction as F
from pathlib import Path

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
 mods=(64,63,65,11,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97);sq={p:{i*i%p for i in range(p)} for p in mods}
 rows=[];hits=[];controls=0
 for m,n in [(1,3),(3,1),(3,2),(5,1),(5,2),(5,6),(1,7),(7,5),(7,6)]:
  T=a*(h*m*m-J*n*n)//M;counts=[0]*len(mods);tested=exact=0;maxj=0
  for l in range(1,82):
   # Threshold for nonnegative discriminant; when already positive, use natural balance scale.
   center=math.isqrt(abs(aa*T)*l*l//h);maxj=max(maxj,center)
   for j in range(max(0,center-40),center+41):
    tested+=1
    if (j-center)%20==0:
     i=2;X=back(i,j,l,m,n);assert M*(aa*i*i+2*bb*i*j+gg*j*j-T*l*l)==-h*a*norm(X);controls+=1
    for idx,p in enumerate(mods):
     if (h%p*(j%p)**2+aa%p*(T%p)*(l%p)**2)%p not in sq[p]:break
     counts[idx]+=1
    else:
     E=h*j*j+aa*T*l*l
     if E<0:continue
     exact+=1;t=math.isqrt(E)
     if t*t!=E:continue
     for s in {t,-t}:
      i,rem=divmod(s-bb*j,aa)
      if rem:continue
      X=back(i,j,l,m,n);assert norm(X)==0
      w=[x/X[3] for x in X[:3]];integral=all(x.denominator==1 for x in w)
      if integral:
       R=[sum(B[k][i]*w[i] for i in range(3)) for k in range(4)];assert sum(R[i]*O[i][j]*R[j] for i in range(4) for j in range(4))==-2
      hits.append(dict(X=list(map(str,X)),integer=integral))
  rows.append(dict(slope=[m,n],rows=tested,survivors=counts,square_tests=exact,center_bits=maxj.bit_length()))
 return dict(RQT=484,sha256=sha,mods=mods,rows=rows,controls=controls,total_rows=sum(r['rows'] for r in rows),totals=[sum(r['survivors'][i] for r in rows) for i in range(len(mods))],square_tests=sum(r['square_tests'] for r in rows),hits=hits,root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='rows'});print([(r['slope'],r['center_bits'],r['square_tests']) for r in out['rows']])
