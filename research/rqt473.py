import json,hashlib,math,itertools,sys
from pathlib import Path

def run(path,prior):
 S=json.load(open(path));Q=[[int(t) for t in r] for r in S['restricted_Gram']];B=[[int(t) for t in r] for r in S['reduced_kernel_basis']];F=[[int(t) for t in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(t) for t in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 A=[[t//2 for t in r] for r in Q]
 def dot(u,v):return sum(u[i]*A[i][j]*v[j] for i in range(3) for j in range(3))
 old=json.load(open(prior));assert old['sha256']==sha
 dirs=[]
 for u in itertools.product(range(-9,10),repeat=3):
  if not any(u) or next(x for x in u if x)<0 or math.gcd(*u)!=1:continue
  v=(-16*u[0]-9*u[1],-9*u[0]-5*u[1],u[2]);a=dot(v,v)
  assert a;dirs.append((v,a))
 def gate(z):return abs(z)>2 and abs(z)!=5 and z%8 in (1,2,3,5,6,7) and z%9781 and z%290533
 rows=[];hits=[]
 for row in old['rows']:
  w=tuple(map(int,row['best_vector']));q=dot(w,w)+1;assert abs(q)==int(row['new_abs']);start=abs(q);history=[];lines=checks=0
  for step in range(20):
   best=abs(q);bw=w;chosen=None
   for v,a in dirs:
    b=dot(w,v);E=b*b-a*q;lines+=1
    t=math.isqrt(E) if E>=0 else 0
    for j in {k for s in (-t,t) for k in range((s-b)//a-1,(s-b)//a+3)}:
     z=w[2]+j*v[2];checks+=1
     if not gate(z):continue
     val=abs(a*j*j+2*b*j+q)
     if val<best:
      best=val;bw=tuple(x+j*y for x,y in zip(w,v));chosen=(v,j)
   if best==abs(q):break
   assert abs(dot(bw,bw)+1)==best
   history.append(dict(bits=best.bit_length(),residual=str(best),vector=list(map(str,bw)),direction=list(chosen[0]),step=str(chosen[1])))
   w=bw;q=dot(w,w)+1
   if not q:
    R=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)];assert sum(R[i]*F[i][j]*R[j] for i in range(4) for j in range(4))==-2;hits.append(list(map(str,w)));break
  rows.append(dict(k=row['k'],start_bits=start.bit_length(),end_bits=abs(q).bit_length(),lines=lines,checks=checks,history=history,stagnated=bool(q and chosen is None),best_vector=list(map(str,w)),new_abs=str(abs(q))))
 return dict(RQT=473,sha256=sha,directions=len(dirs),rows=rows,hits=hits,root19='OPEN' if not hits else 'CONDITIONAL',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1],sys.argv[2]);Path(sys.argv[3]).write_text(json.dumps(out,indent=2)+'\n');print(out['directions']);print([(r['k'],r['start_bits'],r['end_bits'],r['lines'],r['checks'],len(r['history']),r['stagnated'],r['best_vector'][2]) for r in out['rows']])
