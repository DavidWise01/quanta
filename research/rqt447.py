import math,json,hashlib,sys
from pathlib import Path

def direct(f,L,C):
 E=L*L-f*C
 if E<0:return set()
 m=abs(f); j=math.isqrt(E//(m*m))
 a=(-L)//f
 return {z for z in (a-j,a-j-1,a+j,a+j+1) if f*z*z+2*L*z+C==0}

def run(path):
 n=0
 for f in range(-12,13):
  if not f:continue
  for L in range(-15,16):
   for C in range(-30,31):
    E=L*L-f*C; expected=set()
    if E>=0:
     t=math.isqrt(E)
     if t*t==E:expected={(s-L)//f for s in (t,-t) if (s-L)%f==0}
    assert direct(f,L,C)==expected;n+=1
 S=json.load(open(path));Q=[[int(v) for v in r] for r in S['restricted_Gram']]; B=[[int(v) for v in r] for r in S['reduced_kernel_basis']]; F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[v//2 for v in Q[0]];g,e=[v//2 for v in Q[1][1:]];f=Q[2][2]//2;al=c*c-f*a;K=c*e-f*b;ga=e*e-f*g;de=-f;assert al<0 and de>0
 cnt=dict(pairs=0,feasible_x=0,zero_quotient=0,coordinate_tests=0,witnesses=0);hits=[]
 for y in range(3001,10001):
  cnt['pairs']+=1;R=(K*K-al*ga)*y*y-al*de
  if R<0:continue
  h=math.isqrt(R);lo=-((h-K*y)//(-al));hi=(K*y+h)//(-al)
  for x in range(lo,hi+1):
   cnt['feasible_x']+=1;L=c*x+e*y;C=a*x*x+2*b*x*y+g*y*y+1;E=L*L-f*C;assert E>=0
   assert E<f*f;cnt['zero_quotient']+=1
   z0=(-L)//f
   for z in (z0,z0+1):
    cnt['coordinate_tests']+=1
    if f*z*z+2*L*z+C:continue
    r=[sum(B[i][j]*v for j,v in enumerate((x,y,z))) for i in range(4)];assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2
    hits.append([str(v) for v in (x,y,z)]);cnt['witnesses']+=1
 return dict(RQT=447,sha256=sha,controls=n,y=[3001,10000],d=1,counts=cnt,hits=hits,root19='OPEN' if not hits else 'REVIEW',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(out)
