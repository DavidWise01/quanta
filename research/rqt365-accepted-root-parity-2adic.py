#!/usr/bin/env python3
"""RQT-365: accepted root18 parities have smooth Z_2 lifts.
No exact integral norm-minus-two vector is asserted.
"""
import itertools,json
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
assert H.det()==1 and H+H.T==-F
assert all(int(F[i,i])%2==0 for i in range(4))
def q(v):return int((v.T*F*v)[0])//2
rows=[]
for parity in ('0111','1001','1110'):
 r=s.Matrix([int(c) for c in parity])
 assert (q(r)+1)%2==0
 grad=F*r;odd=[i for i in range(4) if int(grad[i])%2]
 assert odd
 first=[bits for bits in itertools.product((0,1),repeat=4)
        if (q(r+2*s.Matrix(bits))+1)%4==0]
 assert len(first)==8
 # At any precision k>=1, 16 bit updates produce exactly eight lifts
 # because q(r+2^k*d)=q(r)+2^k*(Fr).d+2^(2k)*q(d).
 idx=odd[0]
 for k in range(1,80):
  assert (q(r)+1)%(2**k)==0
  if (q(r)+1)%(2**(k+1)):r[idx]+=2**k
  assert (q(r)+1)%(2**(k+1))==0
 assert q(r)!=-1
 assert (int((r.T*H*r)[0])-1)%(2**80)==0
 rows.append({'parity':parity,'gradient_mod2':[int(t)%2 for t in grad],
  'first_lifts_mod4':len(first),'all_lifts_per_level':8,
  'representative_mod_2power80':list(map(int,r)),
  'q_plus_one_mod_2power80':(q(r)+1)%(2**80),
  'exact_integer_root':False})
print(json.dumps({'status':'PASS exact necessary 2-adic root18 parity gate',
 'original_source':'authentic RQT-242 F4/H4','results':rows,
 'root18':'OPEN','roots19_to21':'OPEN'},indent=2))
