#!/usr/bin/env python3
"""Independent RQT-391 original F4 replay of exact cylinder border cases."""
import json,math,random,sys
from pathlib import Path
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H+H.T==-F and H.det()==1
with open(sys.argv[1]) as f:d=json.load(f)
B=s.Matrix([[int(v) for v in row] for row in d['reduced_kernel_basis']])
Q=s.Matrix([[int(v) for v in row] for row in d.get('restricted_F4_Gram',d.get('restricted_Gram'))])
assert Q==B.T*F*B
a,b,c,d,e,f=[int(Q[i,j]) for i,j in ((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))]
moduli=[256,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61]
squares={m:{i*i%m for i in range(m)} for m in moduli}
def delta(x,y):
 return (c*x+e*y)**2-f*(a*x*x+2*b*x*y+d*y*y+2)
def passed(x,y):return all(delta(x,y)%m in squares[m] for m in moduli)
lines=Path(sys.argv[2]).read_text().splitlines();cases=[]
for line in lines:
 if line.startswith('NONNEGATIVE_NONSQUARE'):
  _,X,Y=line.split();x,y=int(X),int(Y);D=delta(x,y)
  assert D>=0 and math.isqrt(D)**2!=D and passed(x,y)
  cases.append([x,y])
assert len(cases)==10 and len({tuple(t) for t in cases})==10
assert all([-x,-y] in cases for x,y in cases)
rng=random.Random(391)
for _ in range(2000):
 x=rng.randint(-10000,10000);y=rng.randint(-10000,10000)
 C=sum(int(Q[i,j])*[x,y][i]*[x,y][j] for i in range(2) for j in range(2))+2
 D=(int(Q[0,2])*x+int(Q[1,2])*y)**2-int(Q[2,2])*C
 assert D==delta(x,y)
 if not passed(x,y):assert D<0 or math.isqrt(D)**2!=D
summary=json.loads(lines[-1])
assert summary=={'radius':10000,'tested_interior_pairs':400000000,'excluded_coordinate_plane_pairs':40001,'modular_rejected':399991618,'passed_modular':8382,'negative_discriminants':8372,'nonnegative_nonsquare':10,'square_discriminants':0,'integer_root_candidates':0}
print(json.dumps({'RQT':391,'status':'PASS independently verified original F4 and ten exact borderline cases','search':summary,'ten_nonsquare_cases':cases,'independent_checks':2000,'root19':'OPEN'},indent=2))
