import json,math,hashlib,sys
from pathlib import Path

def square(n,p,k=None):
 if k is not None:n%=p**k
 if not n:return True
 v=0
 while n%p==0:n//=p;v+=1
 if v%2:return False
 if p==2:return n%(8 if k is None else 2**min(3,k-v))==1
 return pow(n%p,(p-1)//2,p)==1

def val(n,p):
 k=0
 while n and n%p==0:n//=p;k+=1
 return k,n

def coupled(f,L,C,p):
 assert f and p>=2
 h,_=val(f,p);E=L*L-f*C
 if not E:return L%p**h==0
 v,U=val(E,p)
 if v%2:return False
 if p==2:
  if U%8!=1:return False
 elif pow(U%p,(p-1)//2,p)!=1:return False
 k=v//2
 if k>=h:return L%p**h==0
 if L%p**k:return False
 l=L//p**k;r=h-k
 if l%p==0:return False
 return (l*l-U)%p**(r+(p==2))==0

def signmask(t,L,m):
 return {sign for sign in (-1,1) if (sign*t-L)%m==0}

def controls():
 count=conflicts=0
 for f in range(1,101):
  m=f; factors=[];p=2
  while p*p<=m:
   a=1
   while m%p==0:m//=p;a*=p
   if a>1:factors.append(a)
   p+=1
  if m>1:factors.append(m)
  for t in range(21):
   for L in range(f):
    masks=[signmask(t,L,q) for q in factors]
    both=set.intersection({-1,1},*masks)
    assert both==signmask(t,L,f)
    conflicts+=all(masks) and not both
    count+=1
 assert not signmask(1,4,15) and signmask(1,4,3)=={1} and signmask(1,4,5)=={-1}
 return dict(tests=count,mixed_sign_conflicts=conflicts)

def run(path):
 S=json.load(open(path));Q=[[int(v) for v in r] for r in S['restricted_Gram']];B=[[int(v) for v in r] for r in S['reduced_kernel_basis']];F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 A=[[v//2 for v in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2];al=c*c-f*a;K=c*e-f*b;ga=e*e-f*g;de=-f;assert al<0 and de>0
 mods=(256,63,65,11,17,19,23,31,25);sq={m:{i*i%m for i in range(m)} for m in mods};coef={m:[v%m for v in (al,2*K,ga,de)] for m in mods}
 for p,n in [(13,11),(23,7)]:assert f%p==(c+5*e)%p==0 and (-a-10*b-25*g)%p==n and n not in {i*i%p for i in range(p)}
 cnt=dict.fromkeys(['pairs','feasible_x','prime_rejected','base','coupled','exact_squares','global_sign_survivors','witnesses'],0);hits=[]
 for y in range(737,769):
  for d in range(1,768,2):
   cnt['pairs']+=1;R=(K*K-al*ga)*y*y-al*de*d*d
   if R<0:continue
   h=math.isqrt(R);lo=-((h-K*y)//(-al));hi=(K*y+h)//(-al)
   for x in range(lo,hi+1):
    cnt['feasible_x']+=1
    if (x%13 and (y-5*x)%13==0) or (x%23 and (y-5*x)%23==0):cnt['prime_rejected']+=1;continue
    if any((u*x*x+v*x*y+w*y*y+t*d*d)%m not in sq[m] for m,(u,v,w,t) in coef.items()):continue
    cnt['base']+=1;L=c*x+e*y;C=a*x*x+2*b*x*y+g*y*y+d*d;E=L*L-f*C;assert E>=0
    if not all(coupled(f,L,C,p) for p in (2,3,5,13,23)):continue
    cnt['coupled']+=1;t=math.isqrt(E)
    if t*t!=E:continue
    cnt['exact_squares']+=1
    signs=signmask(t,L,abs(f))
    assert signs==signmask(t,L,13)&signmask(t,L,23)&signmask(t,L,abs(f)//299)
    cnt['global_sign_survivors']+=bool(signs)
    for ss in {sign*t for sign in signs}:
     z=(ss-L)//f;w=(x,y,z);assert sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))==-d*d
     r=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)];assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2*d*d
     if math.gcd(x,y,z,d)==1:cnt['witnesses']+=1;hits.append(list(map(str,(*w,d))))
 return dict(RQT=445,sha256=sha,controls=controls(),tile=dict(y=[737,768],odd_d=[1,767],counts=cnt,hits=hits),root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(out)
