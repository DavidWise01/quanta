import json, math, hashlib, sys
from pathlib import Path

def root_candidates(f,L,C):
 E=L*L-f*C
 if E<0:return ()
 j=math.isqrt(E//(f*f)); z0=(-L)//f
 return tuple(sorted({z0-j,z0-j-1,z0+j,z0+j+1} if j else {z0,z0+1}))

def engine(A,yl,yh,d=1):
 a,b,c=A[0];g,e=A[1][1:];f=A[2][2]
 al=c*c-f*a; K=c*e-f*b; ga=e*e-f*g; de=-f
 assert al<0 and de>0
 lanes={k:[[0]*9 for _ in range(9)] for k in 'JANE'}; hits=[]; checks=0; total=0; fallback=0
 for y in range(yl,yh+1):
  R=(K*K-al*ga)*y*y-al*de*d*d
  if R<0:continue
  h=math.isqrt(R); lo=-((h-K*y)//(-al));hi=(K*y+h)//(-al)
  row=y%9
  for col in range(9):
   x=lo+(col-lo)%9
   if x>hi:continue
   L=c*x+e*y; C=a*x*x+2*b*x*y+g*y*y+d*d
   step=18*a*x+81*a+18*b*y
   E=L*L-f*C; de1=18*al*x+81*al+18*K*y
   while x<=hi:
    lanes['J'][row][col]+=1; total+=1
    assert x%9==col and E>=0
    assert L==c*x+e*y and C==a*x*x+2*b*x*y+g*y*y+d*d and E==L*L-f*C
    lanes['A'][row][col]+=1
    zs=root_candidates(f,L,C);fallback+=E>=f*f
    for z in zs:
     lanes['N'][row][col]+=1; checks+=1
     if f*z*z+2*L*z+C==0:
      assert sum(A[i][j]*v*w for i,v in enumerate((x,y,z)) for j,w in enumerate((x,y,z)))==-d*d
      lanes['E'][row][col]+=1; hits.append((x,y,z,d))
    x+=9;L+=9*c;C+=step;step+=162*a;E+=de1;de1+=162*al
 return dict(lanes=lanes,feasible_x=total,coordinate_tests=checks,fallback=fallback,hits=hits)

def run(path,yl=10001,yh=10100):
 s=json.load(open(path));Q=[[int(v) for v in r] for r in s['restricted_Gram']]; B=[[int(v) for v in r] for r in s['reduced_kernel_basis']];F=[[int(v) for v in r] for r in s['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 A=[[v//2 for v in r] for r in Q]
 A0=[[-1,0,0],[0,1,0],[0,0,-1]]
 test=engine(A0,1,12); brute={(x,y,z,1) for y in range(1,13) for x in range(-13,14) for z in range(-13,14) if -x*x+y*y-z*z==-1}
 assert set(test['hits'])==brute and brute
 out=engine(A,yl,yh)
 for x,y,z,d in out['hits']:
  v=[sum(B[i][j]*w for j,w in enumerate((x,y,z))) for i in range(4)]
  assert sum(F[i][j]*v[i]*v[j] for i in range(4) for j in range(4))==-2*d*d
 assert sum(map(sum,out['lanes']['J']))==sum(map(sum,out['lanes']['A']))==out['feasible_x']
 return dict(RQT=448,sha256=sha,y=[yl,yh],d=1,positive_control_hits=len(brute),**out,root19='OPEN' if not out['hits'] else 'CONDITIONAL CANDIDATE',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='lanes'})
