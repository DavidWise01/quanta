#!/usr/bin/env python3
"""RQT-562 bounded deterministic ECM; run with RQT-559 results.json as argument."""
import json,sys,math,time
from pathlib import Path
from sympy.ntheory.ecm import _ecm_one_factor
v=json.loads(Path(sys.argv[1]).read_text()); N=int(v['numerator']);T=int(v['T']);beta=int(v['beta'])
assert N.bit_length()==942 and math.gcd(N,T)==math.gcd(N,beta)==1
configs=[(1000,10000,8,562),(2000,20000,8,1562),(5000,50000,6,2562)]
for B1,B2,curves,seed in configs:
 t=time.monotonic();f=_ecm_one_factor(N,B1,B2,curves,seed)
 if f is not None and 1<int(f)<N and N%int(f)==0:
  print('FACTOR',f,'cofactor',N//int(f));break
 print('NO FACTOR',B1,B2,curves,seed,'seconds',round(time.monotonic()-t,3))
else: print('RQT-562 bounded nonfinding only; composite known, global norm/root19 OPEN')
