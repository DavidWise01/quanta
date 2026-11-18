import json, math, hashlib, itertools, sys
from pathlib import Path
from rqt455 import dot,lll

def det(U):
 return sum(U[0][i]*(U[1][(i+1)%3]*U[2][(i+2)%3]-U[1][(i+2)%3]*U[2][(i+1)%3]) for i in range(3))
def run(path):
 S=json.load(open(path));Q=[[int(x) for x in r] for r in S['restricted_Gram']];B=[[int(x) for x in r] for r in S['reduced_kernel_basis']];F=[[int(x) for x in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(x) for x in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3)); A=[[x//2 for x in r] for r in Q]
 dirs=[]
 for y in range(1,101):
  for x in range(1,181):
   if math.gcd(x,y)==1 and dot((x,y,0),A,(x,y,0))>0:dirs.append((x,y,0))
 dirs=dirs[:64]; records=[]; seen=set()
 for v in dirs:
  n=dot(v,A,v);av=[sum(A[i][j]*v[j] for j in range(3)) for i in range(3)];G=[[2*av[i]*av[j]-n*A[i][j] for j in range(3)] for i in range(3)]
  U,steps=lll(G);assert abs(det(U))==1
  R=[[dot(u,A,w) for w in U] for u in U];assert det(R)==det(A)
  key=tuple(tuple(r) for r in U)
  if key in seen:continue
  seen.add(key);bits=[[abs(x).bit_length() for x in r] for r in R];score=sum(bits[i][j] for i in range(3) for j in range(i,3))
  records.append(dict(v=v,U=U,steps=steps,bits=bits,score=score,R=R))
 records.sort(key=lambda r:r['score']);mods=(8,9,5,7,11,13,17,19,23,29,31); points=set();counts=[0]*(len(mods)+1);hits=[]
 for rec in records[:9]:
  U=rec['U'];R=rec['R'];coeff=[(m,tuple(t%m for t in (R[0][0],2*R[0][1],2*R[0][2],R[1][1],2*R[1][2],R[2][2]))) for m in mods]
  for w in itertools.product(range(-20,21),repeat=3):
   z=tuple(sum(U[i][j]*w[i] for i in range(3)) for j in range(3))
   if z in points:continue
   points.add(z);counts[0]+=1;x,y,t=w
   for k,(m,(a,b,c,g,e,f)) in enumerate(coeff):
    if (a*x*x+b*x*y+c*x*t+g*y*y+e*y*t+f*t*t+1)%m:break
    counts[k+1]+=1
   else:
    if dot(w,R,w)==-1:
     assert dot(z,A,z)==-1;r=[sum(B[i][j]*z[j] for j in range(3)) for i in range(4)];assert sum(r[i]*F[i][j]*r[j] for i in range(4) for j in range(4))==-2;hits.append(z)
 return dict(RQT=456,sha256=sha,directions=len(dirs),distinct_bases=len(records),searched_bases=min(9,len(records)),best={k:v for k,v in records[0].items() if k!='R'},baseline_score=6750,mods=mods,counts=counts,hits=hits,root19='OPEN' if not hits else 'CONDITIONAL',prefix18='UNVERIFIED',records=[{k:v for k,v in r.items() if k!='R'} for r in records])
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='records'})
