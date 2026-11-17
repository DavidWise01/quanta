import math,json,hashlib,sys
from pathlib import Path

def run(path,lo_y=10101,hi_y=11000):
 S=json.load(open(path));Q=[[int(v) for v in r] for r in S['restricted_Gram']];B=[[int(v) for v in r] for r in S['reduced_kernel_basis']];F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[v//2 for v in Q[0]];g,e=[v//2 for v in Q[1][1:]];f=Q[2][2]//2;al=c*c-f*a;K=c*e-f*b;ga=e*e-f*g;de=-f;assert al<0 and de>0
 def E(x,y):return al*x*x+2*K*x*y+ga*y*y+de
 lanes={k:[[0]*9 for _ in range(9)] for k in 'JANE'};hits=[];diamonds=0
 for y in range(lo_y,hi_y+1):
  R=(K*K-al*ga)*y*y-al*de
  if R<0:continue
  h=math.isqrt(R);lo=-((h-K*y)//(-al));hi=(K*y+h)//(-al)
  for x in range(lo,hi+1):
   i,j=y%9,x%9;lanes['J'][i][j]+=1
   v=E(x,y);dx=18*al*x+81*al+18*K*y;dy=18*ga*y+81*ga+18*K*x;cross=162*K
   assert v+dx+dy+cross==E(x+9,y+9) and v+dx==E(x+9,y) and v+dy==E(x,y+9)
   diamonds+=1;lanes['A'][i][j]+=1
   L=c*x+e*y;C=a*x*x+2*b*x*y+g*y*y+1;assert v==L*L-f*C and 0<=v<f*f
   z0=(-L)//f
   for z in (z0,z0+1):
    lanes['N'][i][j]+=1
    if f*z*z+2*L*z+C:continue
    r=[sum(B[k][j]*w for j,w in enumerate((x,y,z))) for k in range(4)];assert sum(F[k][j]*r[k]*r[j] for k in range(4) for j in range(4))==-2
    hits.append([str(w) for w in (x,y,z)]);lanes['E'][i][j]+=1
 return dict(RQT=449,sha256=sha,y=[lo_y,hi_y],d=1,diamonds=diamonds,totals={k:sum(map(sum,v)) for k,v in lanes.items()},lanes=lanes,hits=hits,root19='OPEN' if not hits else 'CONDITIONAL',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='lanes'})
