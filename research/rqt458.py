import json,math,hashlib,itertools,sys
from pathlib import Path
import sympy as s

def reduce_rows(L,G):
 from fractions import Fraction as F
 b=[list(map(int,r)) for r in L.tolist()]; n=len(b)
 g=[[F(x) for x in row] for row in G.tolist()]
 def dot(x,y):return sum(x[i]*g[i][j]*y[j] for i in range(n) for j in range(n))
 def gs():
  o=[]; ns=[]; mu=[]
  for v in b:
   w=list(map(F,v)); row=[]
   for t,d in zip(o,ns):
    c=dot(v,t)/d; row.append(c); w=[x-c*y for x,y in zip(w,t)]
   o.append(w); ns.append(dot(w,w)); mu.append(row)
  return mu,ns
 k=1
 while k<n:
  mu,ns=gs()
  for j in range(k-1,-1,-1):
   q=mu[k][j]; t=(2*q.numerator+q.denominator)//(2*q.denominator)
   if t:b[k]=[x-t*y for x,y in zip(b[k],b[j])]; mu,ns=gs()
  if ns[k]>=(F(3,4)-mu[k][k-1]**2)*ns[k-1]:k+=1
  else:b[k],b[k-1]=b[k-1],b[k];k=max(1,k-1)
 R=s.Matrix(b);T=R*L.inv();assert all(x.q==1 for x in T) and abs(T.det())==1
 return R,T

def run(path):
 S=json.load(open(path)); Q=s.Matrix([[int(x) for x in r] for r in S['restricted_Gram']]); B=s.Matrix([[int(x) for x in r] for r in S['reduced_kernel_basis']]); F=s.Matrix([[int(x) for x in r] for r in S['original_F4']]);sha=hashlib.sha256(json.dumps([[str(x) for x in r] for r in Q.tolist()],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809' and B.T*F*B==Q and all(x%2==0 for x in Q)
 A=Q/2; H=s.diag(A,s.Integer(1)); p=5
 L0=s.eye(4); D=[]
 for i in range(4):
  d=H[i,i]-sum(L0[i,k]**2*D[k] for k in range(i));assert d;D.append(d)
  for j in range(i+1,4):L0[j,i]=(H[j,i]-sum(L0[j,k]*L0[i,k]*D[k] for k in range(i)))/d
 assert L0*s.diag(*D)*L0.T==H and sum(1 for d in D if d>0)==2
 G=L0*s.diag(*map(abs,D))*L0.T
 assert all(G[:i,:i].det()>0 for i in range(1,5))
 def norm(v):return int((v.T*H*v)[0])
 seeds=[]
 for xyz in itertools.product(range(p),repeat=3):
  v=s.Matrix([*xyz,1]); av=A*v[:3,0];
  if norm(v)%p==0 and any(int(x)%p for x in av):seeds.append((xyz,next(i for i in range(3) if int(av[i])%p)))
 rows=[];hits=[]
 for k in (8,32):
  M=p**k; tests=0; best=None; nontrivial=None; primitive_best=None; pure=0
  for xyz,j in seeds[:4]:
   v=s.Matrix([*xyz,1]);mod=p
   for _ in range(1,2*k):
    n=norm(v);assert n%mod==0
    der=2*int((H*v)[j]);v[j]+=mod*((-n//mod)*pow(der,-1,p)%p);mod*=p
   assert mod==M*M and norm(v)%mod==0
   av=H*v; inv=pow(int(av[j]),-1,M)
   vectors=[v]
   for i in range(3):
    u=s.zeros(4,1);u[i]=M
    if i==j:u[j]=M*M
    else:u[j]=M*(-int(av[i])*inv%M)
    vectors.append(u)
   L=s.Matrix.hstack(*vectors).T; assert abs(L.det())==M**4
   gram=L*H*L.T;assert all(int(t)%(M*M)==0 for t in gram)
   R,T=reduce_rows(L,G);assert R==T*L and abs(T.det())==1
   for c in itertools.product((-1,0,1),repeat=4):
    if c==(0,0,0,0) or next(x for x in c if x)!=1:continue
    w=R.T*s.Matrix(c); n=norm(w);assert n%(M*M)==0;tests+=1
    assert abs(n)<= (w.T*G*w)[0]
    val=abs(n)//(M*M)
    if any(w[i] for i in range(3)):
     nontrivial=val if nontrivial is None else min(nontrivial,val)
     prim=abs(n)//math.gcd(*map(int,w))**2;primitive_best=prim if primitive_best is None else min(primitive_best,prim)
    else:pure+=1
    if best is None or val<best:best=val
    if n==0:
     gg=math.gcd(*map(int,w));w=w/gg;assert norm(w)==0 and w[3]!=0
     hits.append([str(x) for x in w])
  rows.append(dict(k=k,modulus_bits=(M*M).bit_length(),seeds=min(4,len(seeds)),tests=tests,min_scaled_abs_norm_bits=best.bit_length(),nontrivial_bits=nontrivial.bit_length(),primitive_nontrivial_bits=primitive_best.bit_length(),pure_d=pure))
  print(rows[-1],flush=True)
 return dict(RQT=458,sha256=sha,prime=p,regular_seeds=len(seeds),rows=rows,hits=hits,root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(out)
