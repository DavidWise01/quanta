#!/usr/bin/env python3
"""RQT-547 standalone exact binary lift enumerator.
Use original historical and new Wall matrices from saved Quanta RQT-516/545:
python rqt547-2adic.py historical_wall.json new_wall.json
Requires sympy.
"""
import sys,json
import sympy as S
Hh=S.Matrix(json.load(open(sys.argv[1])));Hn=S.Matrix(json.load(open(sys.argv[2])))
U0=S.Matrix([[1,1,1,1],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
assert all(int(v)%2==0 for v in U0.T*Hn*U0-Hh)
def solve(rows,rhs):
 rr=[(int(a),int(b)) for a,b in zip(rows,rhs)];pivot=[];rank=0
 for k in range(16):
  sel=next((i for i in range(rank,len(rr)) if rr[i][0]>>k&1),None)
  if sel is None:continue
  rr[rank],rr[sel]=rr[sel],rr[rank]
  for i in range(len(rr)):
   if i!=rank and rr[i][0]>>k&1:rr[i]=(rr[i][0]^rr[rank][0],rr[i][1]^rr[rank][1])
  pivot.append(k);rank+=1
 if any(a==0 and b for a,b in rr):return []
 free=[i for i in range(16) if i not in pivot];sol=[]
 for t in range(1<<len(free)):
  m=sum((t>>j&1)<<f for j,f in enumerate(free))
  for i,k in enumerate(pivot):
   if rr[i][1]^((rr[i][0]&m).bit_count()%2):m|=1<<k
  sol.append(m)
 return sol
def children(U,k):
 mod=2**k;E=U.T*Hn*U-Hh
 assert all(int(x)%mod==0 for x in E)
 J=[]
 for index in range(16):
  X=S.zeros(4);X[index//4,index%4]=1
  J.append((X.T*Hn*U+U.T*Hn*X).applyfunc(lambda x:int(x)&1))
 rows=[];rhs=[]
 for i in range(4):
  for j in range(4):
   rows.append(sum((int(J[t][i,j])&1)<<t for t in range(16)))
   rhs.append((-int(E[i,j])//mod)&1)
 result=[]
 for mask in solve(rows,rhs):
  X=S.Matrix(4,4,[(mask>>i)&1 for i in range(16)])
  V=U+mod*X
  assert V.det()%2 and all(int(z)%(mod*2)==0 for z in V.T*Hn*V-Hh)
  result.append(V)
 return result
nodes=[U0]
for k in range(1,7):
 nodes=[V for U in nodes for V in children(U,k)]
 print('mod',2**(k+1),'valid lifts',len(nodes),flush=True)
 assert nodes
assert len(nodes)==16384
print('RQT-547 PASS; one mod128 witness:',nodes[0].tolist())
