#!/usr/bin/env python3
"""RQT-359: exact 2-adic smooth/null theorem + 2^64 compatible branch."""
import itertools,json
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
cases=[(194,195,[[1,3,1],[-25,-74,-24],[113,340,113]]),
 (201,202,[[1,2,1],[-26,-51,-25],[117,235,117]])]
results=[]
for m,n,Vlist in cases:
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 V=s.Matrix(Vlist);assert abs(V.det())==1
 A=V.T*T.T*F*T*V
 mat=[[int(A[i,j]) for j in range(3)] for i in range(3)]
 def q(z):return sum(z[i]*mat[i][j]*z[j] for i in range(3) for j in range(3))//2
 def grad(z):return [sum(mat[i][j]*z[j] for j in range(3)) for i in range(3)]
 smooth=[];singular=[]
 for v in itertools.product(range(2),repeat=3):
  if not any(v) or q(v)%2:continue
  (smooth if any(x%2 for x in grad(v)) else singular).append(v)
 assert smooth==[(0,1,0),(0,1,1),(1,1,0),(1,1,1)]
 assert singular==[(1,0,1)]
 assert all(q((1+2*w[0],2*w[1],1+2*w[2]))%4==2
            for w in itertools.product(range(2),repeat=3))
 counts=[]
 for k in range(1,6):
  mod=2**k
  sols=[v for v in itertools.product(range(mod),repeat=3)
        if any(t%2 for t in v) and q(v)%mod==0]
  assert len(sols)==(5 if k==1 else 4**k)
  if k>=2:
   assert all(v[1]%2==1 for v in sols)
   assert all(sum(v[1]==h for v in sols)==2**(k+1) for h in range(1,mod,2))
  counts.append([k,len(sols)])
 v=(0,1,0)
 for k in range(1,64):
  mod=2**k
  assert q(v)%mod==0
  opts=[(v[0]+mod*a,1,v[2]+mod*b) for a,b in itertools.product(range(2),repeat=2)
        if q((v[0]+mod*a,1,v[2]+mod*b))%(2*mod)==0]
  assert len(opts)==2
  v=opts[0]
 assert q(v)%(2**64)==0 and q(v)!=0
 u=T*V*s.Matrix(v)
 assert int((u.T*F*u)[0])//2==q(v)
 results.append({'slope':f'{m}/{n}','mod2_smooth':smooth,'mod2_blocked':singular,
 'primitive_counts_2power_k':counts,'branch_mod_2power64':list(v),
 'original_residues_mod_2power64':[int(t)%(2**64) for t in u],
 'q_mod_2power64':q(v)%(2**64),'integral_exact_null':'OPEN'})
print(json.dumps({'status':'PASS exact finite 2-adic induction',
 'source':'authentic stoicheion RQT242 F4','results':results,
 'root18':'OPEN','roots19_to21':'OPEN'},indent=2))
