import json,math,hashlib,sys,itertools
from pathlib import Path

def run(path):
 S=json.load(open(path));Q=[[int(v) for v in r] for r in S['restricted_Gram']];B=[[int(v) for v in r] for r in S['reduced_kernel_basis']];F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 A=[[v//2 for v in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2];p=f*a-c*c;m=-f;K=c*e-f*b;ga=e*e-f*g;H=K*K+p*ga
 assert p>0 and m>0 and H>0
 def norm(w):return sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))
 assert [w for w in itertools.product(range(2),repeat=3) if norm(w)%4==0]==[(0,0,0)]
 assert (a%8,2*b%8,g%8)==(1,0,2)
 residues=sorted({(x*x+2*y*y)%8 for x,y in itertools.product(range(8),repeat=2)});assert 7 not in residues
 def bound(Y,D):
  R=H*Y*Y+p*m*D*D
  L=(abs(c*K+e*p)*Y+abs(c)*math.isqrt(R))//p
  t=math.isqrt(R//p)
  return L+t
 Y=D=2**138;U=bound(Y,D);assert U<m and 1000*U<682*m
 lo=Y;hi=2*Y
 assert bound(hi,hi)>=m
 while hi-lo>1:
  mid=(lo+hi)//2
  if bound(mid,mid)<m:lo=mid
  else:hi=mid
 assert bound(lo,lo)<m<=bound(lo+1,lo+1)
 return dict(RQT=451,sha256=sha,primitive_even_d_impossible=True,z0_mod8_residues=residues,certified_equal_height=str(Y),z_abs_upper_bound=str((1000000*U+m-1)//m)+'/1000000 (rounded up)',exact_ratio=[str(U),str(m)],max_equal_height_this_bound=str(lo),root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='exact_ratio'})
