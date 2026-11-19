import json,math,hashlib,sys
from sympy import primerange,sqrt_mod
from pathlib import Path

def run(path):
 S=json.load(open(path));Q=[[int(v) for v in r] for r in S['restricted_Gram']];B=[[int(v) for v in r] for r in S['reduced_kernel_basis']];F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[v//2 for v in Q[0]];g,e=[v//2 for v in Q[1][1:]];f=Q[2][2]//2;D=b*b-a*g;delta=a*(g*f-e*e)-b*(b*f-c*e)+c*(b*e-c*g);assert D>0 and math.isqrt(D)**2!=D and D%9==delta%9==0
 H=D//9;J=delta//9;assert H>0
 def vp(n,p):
  assert n;k=0
  while n%p==0:n//=p;k+=1
  return k,n
 def symbol(N,H,p):
  k,u=vp(N,p);l,v=vp(H,p)
  if p==2:return -1 if (((u-1)//2)*((v-1)//2)+k*((v*v-1)//8)+l*((u*u-1)//8))%2 else 1
  return -1 if (((p-1)//2)*k*l+l*(pow(u%p,(p-1)//2,p)!=1)+k*(pow(v%p,(p-1)//2,p)!=1))%2 else 1
 pairs=[(m,n) for m in range(1,82) for n in range(1,82) if math.gcd(m,n)==1];targets={(m,n):a*(H*m*m-J*n*n) for m,n in pairs};assert all(targets.values())
 blocked={};counts={}
 for p in (2,19,9781,290533,11,180497,1129):
  bad=[r for r in pairs if r not in blocked and symbol(targets[r],H,p)==-1];counts[str(p)]=len(bad)
  for r in bad:blocked[r]=p
 primes=0;inert=0;checks=0
 for p in primerange(3,100001):
  primes+=1
  if not a%p or not H%p or not J%p or pow(H%p,(p-1)//2,p)!=p-1:continue
  inert+=1;r=J*pow(H,-1,p)%p
  if pow(r,(p-1)//2,p)!=1:continue
  for root in sqrt_mod(r,p,all_roots=True):
   for n in range(1,82):
    for m in range(root*n%p or p,82,p):
     key=(m,n)
     if key not in targets or key in blocked:continue
     checks+=1;assert targets[key]%p==0
     if vp(targets[key],p)[0]%2:blocked[key]=p
 controls=0
 for m,n in [(1,1),(1,3),(3,1),(8,9),(81,80)]:
  for x in range(-4,5):
   for y in range(-4,5):
    z=n;d=m;U=a*x+b*y+c*z;V=D*y+(b*c-a*e)*z;assert V%3==0;P=V//3
    q=a*x*x+2*b*x*y+g*y*y+2*c*x*z+2*e*y*z+f*z*z+d*d
    assert H*a*q==H*U*U-P*P+targets[m,n];controls+=1
 survivors=[r for r in pairs if r not in blocked];return dict(RQT=481,sha256=sha,pairs=len(pairs),fixed_prime_exclusions=counts,odd_primes=primes,inert=inert,valuation_checks=checks,excluded=len(blocked),remaining=len(survivors),controls=controls,first_survivors=sorted(survivors,key=lambda r:(max(r),sum(r),r))[:30],blocked=[[m,n,p] for (m,n),p in sorted(blocked.items())],survivors=survivors,root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ('blocked','survivors')})
