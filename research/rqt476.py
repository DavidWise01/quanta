import json,hashlib,itertools,math,sys
from pathlib import Path
import sympy as s
from rqt458 import reduce_rows

def run(path):
 S=json.load(open(path));Q=s.Matrix(S['restricted_Gram']);B=s.Matrix(S['reduced_kernel_basis']);F=s.Matrix(S['original_F4']);sha=hashlib.sha256(json.dumps([[str(x) for x in r] for r in Q.tolist()],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809' and B.T*F*B==Q and all(x%2==0 for x in Q)
 H=s.diag(Q/2,1);p=19;assert H.det()%p==6 and pow(6,9,p)==1
 L0=s.eye(4);D=[]
 for i in range(4):
  d=H[i,i]-sum(L0[i,k]**2*D[k] for k in range(i));D.append(d)
  for j in range(i+1,4):L0[j,i]=(H[j,i]-sum(L0[j,k]*L0[i,k]*D[k] for k in range(i)))/d
 G=L0*s.diag(*map(abs,D))*L0.T;assert L0*s.diag(*D)*L0.T==H and all(G[:i,:i].det()>0 for i in range(1,5))
 h=[[int(t)%p for t in row] for row in H.tolist()]
 def dot(a,b):return sum(a[i]*h[i][j]*b[j] for i in range(4) for j in range(4))%p
 e=s.eye(4)[2:4,:]; planes=[]
 for a,b in itertools.product(range(p),repeat=2):
  u=(1,0,a,b)
  if dot(u,u):continue
  for c,d in itertools.product(range(p),repeat=2):
   v=(0,1,c,d)
   if dot(v,v) or dot(u,v):continue
   V=s.Matrix([u,v]);C=V*H*e.T
   assert C.det()%p;planes.append(V)
 rows=[];hits=[]
 for idx,V0 in enumerate(planes[:4]):
  V=V0.copy();M=p
  for k in range(2,9):
   C=V*H*e.T;err=V*H*V.T;assert all(t%M==0 for t in err)
   ci=(C.T.adjugate()*pow(int(C.det()),-1,p)).applyfunc(lambda t:t%p)
   delta=(-pow(2,-1,p)*(err/M)*ci).applyfunc(lambda t:t%p)
   V+=M*delta*e;M*=p;assert all(t%M==0 for t in V*H*V.T)
   if k not in (2,4,8):continue
   L=V.col_join(M*e);assert abs(L.det())==M*M
   K=L*H*L.T/M;assert all(t.q==1 for t in K) and K.det()==H.det()
   R,T=reduce_rows(L,G);assert R==T*L
   best=None;bestvec=None;tests=0
   for c in itertools.product((-1,0,1),repeat=4):
    if not any(c) or next(t for t in c if t)<0:continue
    w=R.T*s.Matrix(c);n=int((w.T*H*w)[0]);assert n%M==0;tests+=1
    if not any(w[:3]) or not w[3]:continue
    g=math.gcd(*map(int,w));prim=w/g;val=abs(n)//g**2
    if best is None or val<best:best=val;bestvec=list(map(str,prim))
    if not n:
     assert (prim.T*H*prim)[0]==0;hits.append(list(map(str,prim)))
   rows.append(dict(plane=idx,k=k,modulus_bits=M.bit_length(),tests=tests,primitive_residual_bits=best.bit_length() if best is not None else None,best_vector=bestvec));print(rows[-1]['plane'],k,rows[-1]['primitive_residual_bits'],flush=True)
 return dict(RQT=476,sha256=sha,prime=p,graph_planes=len(planes),planes=[v.tolist() for v in planes],rows=rows,hits=hits,root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2,default=str)+'\n')
