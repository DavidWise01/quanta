import json,math,hashlib,sys
from pathlib import Path
from sympy import primerange,sqrt_mod

def run(path):
 S=json.load(open(path));Q=[[int(x) for x in r] for r in S['restricted_Gram']];B=[[int(x) for x in r] for r in S['reduced_kernel_basis']];F=[[int(x) for x in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(x) for x in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 A=[[x//2 for x in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2];D=b*b-a*g;delta=a*(g*f-e*e)-b*(b*f-c*e)+c*(b*e-c*g);assert D>0
 K=2*(b*c-a*e);T=c*c-a*f
 assert K*K-4*D*T==-4*a*delta
 controls=0
 for z in range(-4,5):
  for y in range(-4,5):
   E=D*y*y+K*z*y+T*z*z-a
   assert E==(b*y+c*z)**2-a*(g*y*y+2*e*y*z+f*z*z+1)
   assert (2*D*y+K*z)**2-4*D*E==4*a*(D-delta*z*z);controls+=1
 limit=6561;blocked={};primes=inert=eligible=progressions=valuation_checks=0
 for p in primerange(3,1000001):
  primes+=1
  if not a%p or pow(D%p,(p-1)//2,p)!=p-1:continue
  inert+=1
  if delta%p==0:continue
  r=D*pow(delta,-1,p)%p
  if pow(r,(p-1)//2,p)!=1:continue
  eligible+=1
  roots=sqrt_mod(r,p,all_roots=True);assert len(roots)==2 and all((delta*t*t-D)%p==0 for t in roots)
  for t in roots:
   progressions+=1
   for z in range(t or p,limit+1,p):
    N=D-delta*z*z;assert N%p==0;v=0
    while N and N%p==0:N//=p;v+=1
    valuation_checks+=1
    if v%2 and z not in blocked:blocked[z]=[p,v]
 for z,p in ((1,17),(2,199)):
  assert z in blocked
  aa,bb,cc,gg,ee,ff=[v%(p*p) for v in (a,2*b,2*c,g,2*e,f)]
  def q(x,y):return aa*x*x+bb*x*y+cc*x*z+gg*y*y+ee*y*z+ff*z*z+1
  base=[(x,y) for x in range(p) for y in range(p) if q(x,y)%p==0]
  assert not any(q(x+p*i,y+p*j)%(p*p)==0 for x,y in base for i in range(p) for j in range(p))
 residues=[z for z in range(8) if any((a*x*x+2*b*x*y+2*c*x*z+g*y*y+2*e*y*z+f*z*z+1)%8==0 for x in range(8) for y in range(8))]
 combined=[z for z in range(1,limit+1) if z not in blocked and z%8 in residues]
 return dict(RQT=465,sha256=sha,controls=controls,z_limit=limit,primes=primes,inert=inert,eligible=eligible,progressions=progressions,valuation_checks=valuation_checks,blocked_count=len(blocked),blocked=blocked,mod8_allowed=residues,combined_survivors=len(combined),first_survivors=combined[:30],previous_branches={str(z):blocked.get(z) for z in (3,5,7,9,10,13,14,17,19)},root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='blocked'})
