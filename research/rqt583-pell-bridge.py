#!/usr/bin/env python3
"""RQT-583 exact algebraic Pell reduction from RQT-582 coefficients.
Usage: python rqt583-pell-bridge.py RQT-582-results.json
"""
import json,math,sys
d=json.load(open(sys.argv[1]))
excluded={int(z['family_index']) for tag in ('prior_certificates','certificates') for z in d[tag]}
assert len(excluded)==55 and len(d['all_families'])==135
remaining=0
for i,f in enumerate(d['all_families']):
 if i in excluded: continue
 A,B,C=map(int,(f['A'],f['B'],f['C']))
 D=B*B-4*A*C
 assert A>0 and math.isqrt(A)**2!=A and D!=0
 for t in (-5,-1,0,1,5):
  delta=A*t*t+B*t+C
  X=2*A*t+B
  assert X*X-4*A*delta==D
 remaining+=1
assert remaining==80
print('RQT-583 PASS: 80 exact generalized Pell identities and nonsquare coefficients.')
print('No global integral norm-2 vector certified; Root19 OPEN.')
