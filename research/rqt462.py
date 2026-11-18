import json,math,hashlib,sys
from fractions import Fraction as F
from pathlib import Path

def dot(u,G,v):return sum(u[i]*G[i][j]*v[j] for i in range(2) for j in range(2))
def near(q):return (2*q.numerator+q.denominator)//(2*q.denominator)
def det(M):return M[0][0]*M[1][1]-M[0][1]*M[1][0]
def run(path):
 S=json.load(open(path));Q=[[int(v) for v in r] for r in S['restricted_Gram']];B=[[int(v) for v in r] for r in S['reduced_kernel_basis']];F4=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F4[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 A=[[v//2 for v in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2];D=b*b-a*g;h=D//9;m=abs(a);r=b//3;z=3
 assert D%9==b%3==g%3==e%3==0 and a!=0 and D>0
 W=[[a,b],[-a*b//(3*m),-a*g//(3*m)]];off=[c*z,-a*e*z//(3*m)]
 assert abs(det(W))==D//3
 def forward(x,y):
  U=a*x+b*y+c*z;P=(D*y+(b*c-a*e)*z)//3;assert (P-r*U)%m==0;return U,(P-r*U)//m
 def inverse(U,k):
  P=r*U+m*k;y,t=divmod(3*P-(b*c-a*e)*z,D)
  if t:return None
  x,t=divmod(U-b*y-c*z,a)
  return None if t else (x,y)
 controls=0
 for x in range(-4,5):
  for y in range(-4,5):
   U,k=forward(x,y);assert (U,k)==tuple(off[i]+W[i][0]*x+W[i][1]*y for i in range(2));assert inverse(U,k)==(x,y);controls+=1
 C=[[a,b],[b,g]];p=F(a);q=F(g)-F(b*b,a);assert p*q<0
 G=[[abs(p),abs(p)*F(b,a)],[abs(p)*F(b,a),abs(p)*F(b,a)**2+abs(q)]]
 u,v=[1,0],[0,1];steps=0
 while True:
  if dot(v,G,v)<dot(u,G,u):u,v=v,u
  t=near(dot(u,G,v)/dot(u,G,u));steps+=1
  if not t:break
  v=[v[i]-t*u[i] for i in range(2)]
  assert steps<10000
 assert abs(det([u,v]))==1
 R=[[dot(i,C,j) for j in (u,v)] for i in (u,v)];assert det(R)==-D
 center=[F(z*(b*e-g*c),-D),F(z*(b*c-a*e),-D)]
 assert all(sum(C[i][j]*center[j] for j in range(2))==-z*[c,e][i] for i in range(2))
 du=det([u,v]);shift=[near((center[0]*v[1]-center[1]*v[0])/du),near((u[0]*center[1]-u[1]*center[0])/du)]
 x0,y0=[shift[0]*u[i]+shift[1]*v[i] for i in range(2)]
 def residual(x,y):return a*x*x+2*b*x*y+g*y*y+2*c*z*x+2*e*z*y+f*z*z+1
 l=[dot(t,C,(x0,y0))+z*(c*t[0]+e*t[1]) for t in (u,v)];const=residual(x0,y0)
 aa,bb=R[0];gg=R[1][1];assert aa!=0
 counts=dict(rows=0,real_rows=0,exact_squares=0,integral_candidates=0);hits=[]
 for j in range(-3280,3281):
  counts['rows']+=1;L=bb*j+l[0];C0=gg*j*j+2*l[1]*j+const;E=L*L-aa*C0
  if E<0:continue
  counts['real_rows']+=1;t=math.isqrt(E)
  if t*t!=E:continue
  counts['exact_squares']+=1
  for s in {t,-t}:
   i,rem=divmod(s-L,aa)
   if rem:continue
   counts['integral_candidates']+=1;x=x0+i*u[0]+j*v[0];y=y0+i*u[1]+j*v[1];assert residual(x,y)==0 and inverse(*forward(x,y))==(x,y)
   w=(x,y,z);X=[sum(B[k][i]*w[i] for i in range(3)) for k in range(4)];assert sum(X[i]*F4[i][j]*X[j] for i in range(4) for j in range(4))==-2;hits.append(list(map(str,w)))
 return dict(RQT=462,sha256=sha,z=z,d=1,controls=controls,ideal_affine_index=str(abs(det(W))),ideal_affine_index_bits=abs(det(W)).bit_length(),basis=[u,v],reduction_steps=steps,before_bits=[abs(t).bit_length() for t in (a,b,g)],after_bits=[abs(t).bit_length() for t in (aa,bb,gg)],center_shift=list(map(str,shift)),original_shift=list(map(str,(x0,y0))),original_shift_bits=[abs(t).bit_length() for t in (x0,y0)],row_range=[-3280,3280],counts=counts,hits=hits,root19='OPEN' if not hits else 'CONDITIONAL',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(out)
