import json,math,hashlib,sys
from pathlib import Path
from sympy import primerange

def run(path):
 S=json.load(open(path)); Q=[[int(v) for v in r] for r in S['restricted_Gram']]; B=[[int(v) for v in r] for r in S['reduced_kernel_basis']]; F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 A=[[v//2 for v in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2];D=b*b-a*g;delta=a*(g*f-e*e)-b*(b*f-c*e)+c*(b*e-c*g)
 assert D%9==delta%9==b%3==e%3==0 and a%3 and math.gcd(a,D)==1
 H=D//9;r=b//3;m=abs(a);assert (r*r-H)%m==0
 assert (H-r*r)%m==0
 N=a*(H-9*(delta//9));factors={};primes=list(primerange(2,1000001))
 for name,n in [('a',a),('H',H),('N_over_a',N//a)]:
  n=abs(n); small=[]
  for p in primes:
   if n%p:continue
   v=0
   while n%p==0:n//=p;v+=1
   small.append([p,v])
  factors[name]={'factors':small,'cofactor_bits':n.bit_length()}
 checks=0
 for x in range(-4,5):
  for y in range(-4,5):
   for z in range(-4,5):
    U=a*x+b*y+c*z; V=D*y+(b*c-a*e)*z;assert V%3==0;P=V//3
    assert (P-r*U)%m==0; k=(P-r*U)//m
    assert P*P-H*U*U==m*m*k*k+2*m*r*k*U+(r*r-H)*U*U
    q=a*x*x+2*b*x*y+2*c*x*z+g*y*y+2*e*y*z+f*z*z+1
    assert H*a*q==H*U*U-P*P+a*(H-(delta//9)*z*z)
    checks+=1
 blockers=[];inert=0
 for p in primes[1:]:
  if pow(H%p,(p-1)//2,p)!=p-1:continue
  inert+=1;n=N;v=0
  while n%p==0:n//=p;v+=1
  if v%2:blockers.append([p,v])
 return dict(RQT=461,sha256=sha,identity_controls=checks,old_D_bits=D.bit_length(),reduced_D_bits=H.bit_length(),target_bits=abs(N).bit_length(),ideal_index_bits=m.bit_length(),ideal_index=str(m),ideal_root=str(r%m),factors=factors,primes_screened=len(primes),inert_primes=inert,blockers_z3=blockers,root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ('ideal_index','ideal_root')})
