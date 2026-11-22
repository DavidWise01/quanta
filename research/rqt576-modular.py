#!/usr/bin/env python3
"""RQT-576 finite exact quadratic congruence enumerator.
Usage: python rqt576-modular.py reduced_gram.json
"""
import sys,json,itertools
F=[[int(x) for x in row] for row in json.load(open(sys.argv[1]))]
assert len(F)==4 and all(len(r)==4 for r in F)
expected={2:16,3:36,4:128,5:130,7:336,8:1280,11:1320,13:2210,16:10240}
for m,expected_count in expected.items():
 fm=[[v%m for v in row] for row in F];count=0;first=None
 for z in itertools.product(range(m),repeat=4):
  q=sum(z[i]*fm[i][j]*z[j] for i in range(4) for j in range(4))%m
  if q==(-2)%m:
   count+=1
   if first is None:first=z
 assert count==expected_count
 print('PASS',m,count,first)
print('Finite modular gates only; integral norm -2, original 22D verification, root19 OPEN')
