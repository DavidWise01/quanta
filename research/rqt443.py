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

def coupled(f,L,C,p):
 # f has valuation exactly one at p; solve f*z*z+2*L*z+C=0 in Z_p.
 assert f%p==0 and f%(p*p)!=0
 if L%p:return True
 if C%p:return False
 return square((L//p)**2-(f//p)*(C//p),p)

def run(path):
 S=json.load(open(path));Q=[[int(v) for v in r] for r in S['restricted_Gram']];B=[[int(v) for v in r] for r in S['reduced_kernel_basis']];F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 A=[[v//2 for v in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2];al=c*c-f*a;K=c*e-f*b;ga=e*e-f*g;de=-f;assert al<0 and de>0
 tests=0
 for p,kmax in [(2,12),(3,5),(5,5)]:
  for k in range(1,kmax+1):
   m=p**k; sq={i*i%m for i in range(m)}
   for n in range(m):assert square(n,p,k)==(n in sq);tests+=1
 for p,n in [(13,11),(23,7)]:assert f%p==(c+5*e)%p==0 and (-a-10*b-25*g)%p==n and n not in {i*i%p for i in range(p)}
 mods=(256,63,65,11,17,19,23,31,25);sq={m:{i*i%m for i in range(m)} for m in mods};coef={m:[v%m for v in (al,2*K,ga,de)] for m in mods};rows=[]
 for name,yl,yh in [('regression',1,640),('new_numerator',641,704)]:
  cnt=dict.fromkeys(['pairs','feasible_x','prime_rejected','base','finite','local2','local3','local5','coupled13','coupled23','exact_squares','witnesses'],0);hits=[]
  for y in range(yl,yh+1):
   for d in range(1,768,2):
    cnt['pairs']+=1;R=(K*K-al*ga)*y*y-al*de*d*d
    if R<0:continue
    h=math.isqrt(R);lo=-((h-K*y)//(-al));hi=(K*y+h)//(-al)
    for x in range(lo,hi+1):
     cnt['feasible_x']+=1
     if (x%13 and (y-5*x)%13==0) or (x%23 and (y-5*x)%23==0):cnt['prime_rejected']+=1;continue
     if any((u*x*x+v*x*y+w*y*y+t*d*d)%m not in sq[m] for m,(u,v,w,t) in coef.items()):continue
     E=al*x*x+2*K*x*y+ga*y*y+de*d*d;assert E>=0;cnt['base']+=1
     if not all(square(E,p,k) for p,k in [(2,12),(3,5),(5,5)]):continue
     cnt['finite']+=1
     for p in (2,3,5):
      if not square(E,p):break
      cnt['local'+str(p)]+=1
     else:
      L=c*x+e*y;C=a*x*x+2*b*x*y+g*y*y+d*d
      if not coupled(f,L,C,13):continue
      cnt['coupled13']+=1
      if not coupled(f,L,C,23):continue
      cnt['coupled23']+=1
      t=math.isqrt(E)
      if t*t!=E:continue
      cnt['exact_squares']+=1
      for ss in {t,-t}:
       if (ss-c*x-e*y)%f:continue
       z=(ss-c*x-e*y)//f;w=(x,y,z);assert sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))==-d*d
       r=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)];assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2*d*d
       if math.gcd(x,y,z,d)==1:cnt['witnesses']+=1;hits.append(list(map(str,(*w,d))))
  rows.append(dict(tile=name,y=[yl,yh],odd_d=[1,767],counts=cnt,hits=hits));print(name,cnt,flush=True)
 return dict(RQT=443,sha256=sha,finite_residue_tests=tests,tiles=rows,root19='OPEN' if not any(r['hits'] for r in rows) else 'REVIEW',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n')
