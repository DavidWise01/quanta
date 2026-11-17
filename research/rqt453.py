import json,math,hashlib,sys
from pathlib import Path

def run(path):
 S=json.load(open(path)); Q=[[int(v) for v in r] for r in S['restricted_Gram']];B=[[int(v) for v in r] for r in S['reduced_kernel_basis']];F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[v//2 for v in Q[0]];g,e=[v//2 for v in Q[1][1:]];f=Q[2][2]//2;D=b*b-a*g;T=D*(a*f-c*c)+(b*c-a*e)**2
 assert D>0 and math.isqrt(D)**2!=D
 local={}
 for p in (2,3,5,7,11,13,17,19,23,29,31,37,41,43):
  z=2;m=p*p;aa,bb,cc,gg,ee,ff=[v%m for v in (a,2*b,2*c,g,2*e,f)]
  def q(x,y):return aa*x*x+bb*x*y+cc*x*z+gg*y*y+ee*y*z+ff*z*z+1
  base=[(x,y) for x in range(p) for y in range(p) if q(x,y)%p==0];count=0
  for x,y in base:
   # exact linear lift: q(x+pi,y+pj)/p mod p
   t=q(x,y)//p;u=2*aa*x+bb*y+cc*z;v=bb*x+2*gg*y+ee*z
   count+=p if u%p or v%p else (p*p if t%p==0 else 0)
  local[str(p)]=[len(base),count]
  if p<=17:assert count==sum(q(x,y)%m==0 for x in range(m) for y in range(m))
 # CF recurrence, no enormous convergent squares: exact norm via complete quotient recurrence; check directly for each step here
 s=math.isqrt(D);M=0;den=1;k=s;P0,P1=0,1;Q0,Q1=1,0;unit=None;best=None;target=4*T+D*a;match=[]
 for i in range(512):
  P=k*P1+P0;R=k*Q1+Q0;norm=P*P-D*R*R
  if best is None or abs(norm)<abs(best):best=norm
  if norm==target:match.append(i)
  if norm==1:unit=i;break
  P0,P1=P1,P;Q0,Q1=Q1,R;M=den*k-M;den=(D-M*M)//den;assert den>0;k=(s+M)//den
 return dict(RQT=453,sha256=sha,local_z2=local,D_bits=D.bit_length(),target_bits=abs(target).bit_length(),convergents=i+1,unit_index=unit,target_matches=match,last_convergent_bits=P.bit_length(),best_abs_norm_bits=abs(best).bit_length(),root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(out)
