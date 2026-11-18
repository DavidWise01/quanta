import json,hashlib,sys
from pathlib import Path
from sympy import isprime
def run(path):
 S=json.load(open(path));Q=[[int(v) for v in r] for r in S['restricted_Gram']];B=[[int(v) for v in r] for r in S['reduced_kernel_basis']];F=[[int(v) for v in r] for r in S['original_F4']]
 sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
 assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
 a,b,c=[v//2 for v in Q[0]];g,e=[v//2 for v in Q[1][1:]];f=Q[2][2]//2;D=b*b-a*g;delta=a*(g*f-e*e)-b*(b*f-c*e)+c*(b*e-c*g)
 rows=[];controls=0
 for p in (19,9781,290533):
  assert isprime(p) and D%p==0 and a%p and delta%p
  h=(a*e-b*c)%p;assert h and a*delta%p==(-h*h)%p
  ok=pow(-a%p,(p-1)//2,p)==1
  aa,bb,cc,gg,ee,ff=[t%p for t in (a,b,c,g,e,f)]
  for z in (1,2,3,p-1):
   for t in (0,1,2,p-1):
    y=(-(t*t+(aa*ff-cc*cc)*z*z+aa)*pow(2*h*z,-1,p))%p
    x=((t-bb*y-cc*z)*pow(aa,-1,p))%p
    assert (aa*x*x+2*bb*x*y+2*cc*x*z+gg*y*y+2*ee*y*z+ff*z*z+1)%p==0
    assert (2*aa*x+2*bb*y+2*cc*z)%p or (2*bb*x+2*gg*y+2*ee*z)%p
    controls+=1
  rows.append(dict(p=p,zero_class_allowed=ok,nonzero_classes_regular=p-1,excluded_multiples_up_to_6561=0 if ok else 6561//p,excluded_multiples_up_to_59049=0 if ok else 59049//p))
 for p in (11,180497):
  assert isprime(p) and a%p==0 and b%p
  aa,bb,cc,gg,ee,ff=[t%p for t in (a,b,c,g,e,f)]
  for z in (0,1,2,3,p-1):
   y=(1-cc*z)*pow(bb,-1,p)%p
   x=(-(gg*y*y+2*ee*y*z+ff*z*z+1)*pow(2,-1,p))%p
   assert (aa*x*x+2*bb*x*y+2*cc*x*z+gg*y*y+2*ee*y*z+ff*z*z+1)%p==0 and (2*bb*y+2*cc*z)%p==2
   controls+=1
  rows.append(dict(p=p,all_classes_regular=True))
 return dict(RQT=467,sha256=sha,controls=controls,prime_gates=rows,root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(out)
