#!/usr/bin/env python3
"""RQT-585 five shared Pell coefficients. Run with archived RQT-583 and RQT-584 result JSON."""
import json,sys,math,collections
j=json.load(open(sys.argv[1])); k=json.load(open(sys.argv[2]))
exclude={int(c['family_index']) for c in k['certificates']}
eq=[e for e in j['equations'] if int(e['index']) not in exclude]
assert len(eq)==68
groups=collections.defaultdict(list)
for e in eq:groups[tuple(e['ray'])].append(e)
factors={(35,-10,14):4,(45,-13,18):5,(80,-23,32):1,(95,-27,38):7,(115,-33,46):1}
assert {r:len(e) for r,e in groups.items()}=={(35,-10,14):9,(45,-13,18):22,(80,-23,32):17,(95,-27,38):12,(115,-33,46):8}
for ray,fams in groups.items():
 s=factors[ray];A=int(fams[0]['A']);assert A%(s*s)==0
 a=A//(s*s)
 for e in fams:
  Ai,B,C=map(int,(e['A'],e['B'],e['C']));D=int(e['D'])
  assert Ai==A and B*B-4*A*C==D
  for t in (-7,-1,0,1,7):
   y2=A*t*t+B*t+C;X=2*A*t+B
   assert X*X-a*(2*s)**2*y2==D
print('PASS: 68 equations, 5 leading coefficients, exact Pell identities; root19 OPEN')
