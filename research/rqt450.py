import json, math, hashlib, sys
from pathlib import Path

def run(path,yl=11001,yh=12000):
 S=json.load(open(path)); Q=[[int(v) for v in r] for r in S['restricted_Gram']]; B=[[int(v) for v in r] for r in S['reduced_kernel_basis']]; F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[v//2 for v in Q[0]];g,e=[v//2 for v in Q[1][1:]];f=Q[2][2]//2;al=c*c-f*a;K=c*e-f*b;ga=e*e-f*g;de=-f;assert al<0 and de>0
 mods=(9,8,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)
 coeff=[(m,tuple(t%m for t in (a,2*b,2*c,g,2*e,f))) for m in mods]
 counts=[0]*len(mods); lanes={k:[[0]*9 for _ in range(9)] for k in 'JANE'}; hits=[]; controls=0; exact=0
 for y in range(yl,yh+1):
  R=(K*K-al*ga)*y*y-al*de
  if R<0:continue
  h=math.isqrt(R);lo=-((h-K*y)//(-al));hi=(K*y+h)//(-al)
  for col in range(9):
   x=lo+(col-lo)%9;L=c*x+e*y;E=al*x*x+2*K*x*y+ga*y*y+de;D=18*al*x+81*al+18*K*y
   while x<=hi:
    i=y%9;lanes['J'][i][col]+=1;assert 0<=E<f*f
    z0=(-L)//f; lanes['A'][i][col]+=2
    for z in (z0,z0+1):
     for k,(m,(aa,bb,cc,gg,ee,ff)) in enumerate(coeff):
      if (aa*x*x+bb*x*y+cc*x*z+gg*y*y+ee*y*z+ff*z*z+1)%m:break
      counts[k]+=1
     else:
      exact+=1;lanes['N'][i][col]+=1
      if a*x*x+2*b*x*y+2*c*x*z+g*y*y+2*e*y*z+f*z*z+1==0:
       r=[sum(B[k][j]*v for j,v in enumerate((x,y,z))) for k in range(4)];assert sum(F[k][j]*r[k]*r[j] for k in range(4) for j in range(4))==-2
       hits.append([str(t) for t in (x,y,z)]);lanes['E'][i][col]+=1
     if y<=yl+2:
      n=a*x*x+2*b*x*y+2*c*x*z+g*y*y+2*e*y*z+f*z*z+1
      assert all((aa*x*x+bb*x*y+cc*x*z+gg*y*y+ee*y*z+ff*z*z+1)%m==n%m for m,(aa,bb,cc,gg,ee,ff) in coeff);controls+=1
    x+=9;L+=9*c;E+=D;D+=162*al
 return dict(RQT=450,sha256=sha,y=[yl,yh],d=1,mods=mods,survivors=counts,controls=controls,totals={k:sum(map(sum,v)) for k,v in lanes.items()},lanes=lanes,hits=hits,root19='OPEN' if not hits else 'CONDITIONAL',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='lanes'})
