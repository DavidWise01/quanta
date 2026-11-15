#!/usr/bin/env python3
"""RQT-392: exact CRT corridor for frozen root19 rank-three Wall kernel.

Reproduce:
 python research/rqt388-exact-second-key.py --bound 30 --out /tmp/rqt388.json
 python research/rqt392-crt-corridor.py /tmp/rqt388.json
"""
import itertools,json,math,sys
from collections import Counter
from sympy import Matrix
from sympy.ntheory.modular import crt
F=Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],
[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],
[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],
[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H+H.T==-F and H.det()==1

def audit(d):
 B=Matrix([[int(v) for v in row] for row in d['reduced_kernel_basis']])
 Q=Matrix([[int(v) for v in row] for row in d.get('restricted_F4_Gram',d.get('restricted_Gram'))])
 assert B.shape==(4,3) and Q==B.T*F*B
 assert [[int(Q[i,j])%16 for j in range(3)] for i in range(3)]==[[2,8,2],[8,4,6],[2,6,14]]
 assert [[int(Q[i,j])%3 for j in range(3)] for i in range(3)]==[[1,0,1],[0,0,0],[1,0,1]]
 q=lambda x:sum(int(Q[i,j])*x[i]*x[j] for i in range(3) for j in range(3))
 sols={};parities=Counter()
 for modulus in (16,3,5):
  sols[modulus]=[v for v in itertools.product(range(modulus),repeat=3) if (q(v)+2)%modulus==0]
  if modulus==16:
   for v in sols[16]:parities[''.join(str(x%2) for x in v)]+=1
  if modulus==3:
   assert all(((v[0]+v[2])%3!=0)==((q(v)+2)%3==0) for v in itertools.product(range(3),repeat=3))
 assert [len(sols[m]) for m in (16,3,5)]==[768,18,20]
 assert dict(parities)=={'001':256,'011':256,'110':256}
 # The mod16 condition depends only on coefficient residues mod8,
 # since every Q diagonal is even and Q is integral symmetric.
 for v in itertools.product(range(8),repeat=3):
  for i in range(3):
   w=list(v);w[i]+=8
   assert (q(v)-q(w))%16==0
 assert sum((q(v)+2)%16==0 for v in itertools.product(range(8),repeat=3))==96
 good=len(sols[16])*len(sols[3])*len(sols[5])
 allstates=(16*3*5)**3
 assert good==276480 and allstates==13824000 and good*50==allstates
 candidate=None
 for a in sols[16]:
  if 0 in a:continue
  for b in sols[3]:
   if 0 in b:continue
   for c in sols[5]:
    if 0 in c:continue
    x=[int(crt([16,3,5],[a[i],b[i],c[i]])[0]) for i in range(3)]
    if all(x):candidate=x;break
   if candidate:break
  if candidate:break
 assert candidate==[1,49,34]
 original=B*Matrix(candidate)
 assert int((original.T*F*original)[0])==q(candidate)
 assert (q(candidate)+2)%240==0 and q(candidate)!=-2
 return {'RQT':392,'status':'PASS exact original F4 local CRT corridor',
  'mod16_solutions':768,'mod3_solutions':18,'mod5_solutions':20,
  'mod3_exact_rule':'x+z != 0 mod3',
  'mod16_parity_classes':dict(sorted(parities.items())),
  'CRT_modulus':240,'CRT_surviving_triples':good,
  'CRT_all_triples':allstates,'surviving_fraction':'1/50',
  'exact_modular_rejection_fraction':'49/50',
  'sample_CRT_coefficients':candidate,
  'sample_original_F4_norm_mod240':q(candidate)%240,
  'sample_is_exact_norm_minus_two':False,
  'root19':'OPEN','scope':'Local necessary congruences, not a global integer root'}

if __name__=='__main__':
 with open(sys.argv[1]) as f:j=json.load(f)
 print(json.dumps(audit(j),indent=2))
