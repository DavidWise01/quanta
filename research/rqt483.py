import json, hashlib, math, sys
from fractions import Fraction as F
from pathlib import Path

def run(path):
 S=json.load(open(path)); Q=[[int(x) for x in r] for r in S['restricted_Gram']]; B=[[int(x) for x in r] for r in S['reduced_kernel_basis']]; O=[[int(x) for x in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(x) for x in r] for r in Q],separators=(',',':')).encode()).hexdigest(); assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*O[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[x//2 for x in Q[0]];g,e=[x//2 for x in Q[1][1:]];f=Q[2][2]//2;D=b*b-a*g;delta=a*(g*f-e*e)-b*(b*f-c*e)+c*(b*e-c*g);assert D%9==delta%9==b%3==0
 h=D//9;J=delta//9;M=abs(a);r=b//3;assert (r*r-h)%M==0
 # P=M*k+r*U; divide the entire conic by M.
 C=[[M,r],[r,(r*r-h)//M]];assert C[0][0]*C[1][1]-C[0][1]**2==-h
 G=[[M,r],[r,F(r*r+h,M)]]
 def dot(u,C,v):return sum(u[i]*C[i][j]*v[j] for i in range(2) for j in range(2))
 u,v=[1,0],[0,1];steps=0
 while True:
  if dot(v,G,v)<dot(u,G,u):u,v=v,u
  t=dot(u,G,v)/F(dot(u,G,u));k=(2*t.numerator+t.denominator)//(2*t.denominator);steps+=1
  if not k:break
  v=[v[i]-k*u[i] for i in range(2)]
  assert steps<10000
 assert abs(u[0]*v[1]-u[1]*v[0])==1
 aa,bb,gg=dot(u,C,u),dot(u,C,v),dot(v,C,v);assert bb*bb-aa*gg==h
 rows=[];controls=0;hits=[]
 for m,n in [(1,3),(3,1),(3,2),(5,1),(5,2),(5,6),(1,7),(7,5),(7,6)]:
  N=a*(h*m*m-J*n*n);assert N%M==0;T=N//M
  for i in range(-4,5):
   for j in range(-4,5):
    k,U=[i*u[t]+j*v[t] for t in range(2)];P=M*k+r*U
    assert P*P-h*U*U-N==M*(aa*i*i+2*bb*i*j+gg*j*j-T);controls+=1
  rows.append(dict(slope=[m,n],old_target_bits=abs(N).bit_length(),new_target_bits=abs(T).bit_length(),det_before_bits=abs(h*N).bit_length(),det_after_bits=abs(h*T).bit_length()))
 return dict(RQT=483,sha256=sha,scale=str(M),scale_bits=M.bit_length(),basis=[u,v],steps=steps,binary_before_bits=[abs(h).bit_length(),1],binary_after_bits=[abs(t).bit_length() for t in (aa,bb,gg)],controls=controls,rows=rows,hits=hits,root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='scale'})
