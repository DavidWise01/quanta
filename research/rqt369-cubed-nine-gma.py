#!/usr/bin/env python3
"""RQT-369: true cubed-nine GMA, 729 cells/generation around ||||.
Original F4 exact discriminant; root18 remains open.
"""
from collections import Counter
import math,json
F=[[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]]
U=[[224,29,-224,-130],[-193,-25,193,112],[40,5,-40,-23],[-336,-43,335,195]]
G=[[sum(U[i][k]*F[k][l]*U[j][l] for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
H=[[G[i][3]*G[j][3]-G[3][3]*G[i][j] for j in range(3)] for i in range(3)]
assert G[3][3]==-5868287405277328266
N=729**9
def unpack(n):
 assert 0<=n<729
 return (n%9-4,n//9%9-4,n//81-4)
def pack(v):
 assert len(v)==3 and all(-4<=x<=4 for x in v)
 return (v[0]+4)+9*(v[1]+4)+81*(v[2]+4)
def decode(i):
 assert 0<=i<N
 address=[];t=[0,0,0];weight=1
 for _ in range(9):
  i,d=divmod(i,729);v=unpack(d);address.append(v)
  for j in range(3):t[j]+=weight*v[j]
  weight*=9
 assert i==0
 return address,tuple(t)
def delta(t):
 return sum(t[i]*H[i][j]*t[j] for i in range(3) for j in range(3))-2*G[3][3]
def test(t):
 D=delta(t)
 if D<0:return 'negative',[]
 root=math.isqrt(D)
 if root*root!=D:return 'nonsquare',[]
 B=sum(t[i]*G[i][3] for i in range(3))
 hits=[]
 for sign in (-1,1):
  num=-B+sign*root
  if num%G[3][3]:continue
  z=(*t,num//G[3][3])
  r=tuple(sum(U[j][i]*z[j] for j in range(4)) for i in range(4))
  assert sum(r[i]*F[i][j]*r[j] for i in range(4) for j in range(4))==-2
  if ''.join(str(v%2) for v in r) in {'0111','1001','1110'}:hits.append({'t':z,'r':r})
 return 'square',hits
def main():
 assert N==9**27
 for i in range(729):assert pack(unpack(i))==i
 squares81={i*i%81 for i in range(81)}
 pruned=survived=0
 for x in range(-40,41):
  for y in range(-40,41):
   for z in range(-40,41):
    if delta((x,y,z))%81 in squares81:survived+=1
    else:pruned+=1
 assert (pruned,survived)==(124659,406782)
 moduli=(256,3,5,7,11,13,17,19,23,29,31,37)
 sq={m:{j*j%m for j in range(m)} for m in moduli}
 step=6364136223846793007%N
 assert math.gcd(step,N)==1
 count=Counter();first=set();roots=[]
 for k in range(10000):
  addr,t=decode((k*step)%N);first.add(addr[0])
  if any(delta(t)%m not in sq[m] for m in moduli):
   count['modular']+=1;continue
  status,found=test(t);count[status]+=1;roots+=found
 assert len(first)==729 and not roots
 print(json.dumps({'status':'PASS original F4 exact cubic search',
 'geometry':'9x9x9 per generation, center (0,0,0) ||||',
 'generations':9,'cells_per_generation':729,'total_addresses':N,
 'two_generation_nodes':729**2,'pruned':pruned,'survivors':survived,
 'full_depth_sample':10000,'first_generation_coverage':len(first),
 'sample_counts':dict(count),'candidates':roots,'root18':'OPEN'},indent=2))
if __name__=='__main__':main()
