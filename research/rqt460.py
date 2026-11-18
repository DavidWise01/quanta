import json,hashlib,sys,itertools
from pathlib import Path
from sympy import primerange

def det(A):
 return sum(A[0][i]*(A[1][(i+1)%3]*A[2][(i+2)%3]-A[1][(i+2)%3]*A[2][(i+1)%3]) for i in range(3))
def run(path):
 S=json.load(open(path));Q=[[int(v) for v in r] for r in S['restricted_Gram']];B=[[int(v) for v in r] for r in S['reduced_kernel_basis']];F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 A=[[v//2 for v in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2];D=b*b-a*g;delta=det(A);T=D*(a*f-c*c)+(b*c-a*e)**2;assert T==-a*delta
 def q(x,y,z):return a*x*x+2*b*x*y+2*c*x*z+g*y*y+2*e*y*z+f*z*z+1
 for x,y,z in itertools.product(range(-2,3),repeat=3):
  U=a*x+b*y+c*z;V=D*y+(b*c-a*e)*z
  assert D*a*q(x,y,z)==D*U*U-V*V+a*(D-delta*z*z)
 p=199;m=p*p;assert a%p and pow(D%p,(p-1)//2,p)==p-1 and delta%p
 roots=[z for z in range(p) if (D-delta*z*z)%p==0];lift_roots=[z for z in range(m) if (D-delta*z*z)%m==0]
 excluded=[z for z in range(m) if z%p in roots and z not in lift_roots];assert 2 in excluded and m-2 in excluded
 aa,bb,cc,gg,ee,ff=[v%m for v in (a,2*b,2*c,g,2*e,f)]
 def r(x,y,z):return aa*x*x+bb*x*y+cc*x*z+gg*y*y+ee*y*z+ff*z*z+1
 base=[(x,y) for x in range(p) for y in range(p) if r(x,y,2)%p==0];assert base==[(2,20)]
 lift_count=sum(r(x+i*p,y+j*p,2)%m==0 for x,y in base for i in range(p) for j in range(p));assert lift_count==0
 small={m:[z for z in range(m) if any(q(x,y,z)%m==0 for x in range(m) for y in range(m))] for m in (8,9,16,25)}
 primes=list(primerange(3,100001));inert=[p for p in primes if a%p and pow(D%p,(p-1)//2,p)==p-1]
 results={}
 for z in range(3,82):
  bad=[m for m,allowed in small.items() if z%m not in allowed]
  blockers=[]
  for p in inert:
   n=D-delta*z*z
   if n%p:continue
   v=0
   while n and n%p==0:n//=p;v+=1
   if v%2:blockers.append([p,v])
  results[str(z)]={'small_moduli':bad,'inert_prime_obstructions':blockers}
 survivors=[int(z) for z,r in results.items() if not r['small_moduli'] and not r['inert_prime_obstructions']]
 return dict(RQT=460,sha256=sha,identity_controls=125,prime=199,modulus=m,coefficients_mod_39601=[v%m for v in (a,b,c,g,e,f,D,delta)],base_z2=base,base_tests=199**2,lift_tests=199**2,lift_survivors=lift_count,roots_mod_199=roots,lift_roots_mod_39601=lift_roots,excluded_z_classes=excluded,primes_screened=len(primes),inert_primes=len(inert),small_modulus_z_classes=small,z_screen=results,survivors=survivors,root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ('excluded_z_classes','z_screen')});print('excluded',len(out['excluded_z_classes']));print('blocked',[(z,r) for z,r in out['z_screen'].items() if int(z)<12])
