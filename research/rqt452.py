import json,hashlib,math,sys
from pathlib import Path

def run(path):
 S=json.load(open(path)); Q=[[int(v) for v in r] for r in S['restricted_Gram']]; B=[[int(v) for v in r] for r in S['reduced_kernel_basis']]; F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest(); assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[v//2 for v in Q[0]];g,e=[v//2 for v in Q[1][1:]];f=Q[2][2]//2
 p=17;m=p*p;aa,bb,cc,gg,ee,ff=[v%m for v in (a,2*b,2*c,g,2*e,f)]
 def h(x,y,z):return aa*x*x+bb*x*y+cc*x*z+gg*y*y+ee*y*z+ff*z*z+1
 base={z:[(x,y) for x in range(p) for y in range(p) if h(x,y,z)%p==0] for z in range(p)}
 assert base[1]==[(0,9)] and base[16]==[(0,8)]
 allowed=[]; counts={};tested=0
 for z in range(m):
  n=0
  for x,y in base[z%p]:
   for i in range(p):
    for j in range(p):
     n+=h(x+i*p,y+j*p,z)%m==0;tested+=1
  counts[str(z)]=n
  if n:allowed.append(z)
 assert 1 not in allowed and 288 not in allowed
 D=b*b-a*g; T=D*(a*f-c*c)+(b*c-a*e)**2
 assert D>0 and math.isqrt(D)**2!=D
 for x,y,z,d in [(0,0,1,1),(2,-3,5,7),(-1,1,1,1)]:
  U=a*x+b*y+c*z;V=D*y+(b*c-a*e)*z
  q=a*x*x+2*b*x*y+2*c*x*z+g*y*y+2*e*y*z+f*z*z
  assert D*a*(q+d*d)==D*U*U-V*V+T*z*z+D*a*d*d
 return dict(RQT=452,sha256=sha,mod289_coefficients=[aa,bb,cc,gg,ee,ff],base_counts={str(z):len(v) for z,v in base.items()},lift_tests=tested,allowed_z_mod289=allowed,excluded_z_mod289=[z for z in range(m) if z not in allowed],lift_counts=counts,D_bits=D.bit_length(),D=str(D),T=str(T),pell_identity_controls=3,root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ('D','T','lift_counts','allowed_z_mod289')})
