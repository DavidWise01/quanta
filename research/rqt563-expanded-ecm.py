#!/usr/bin/env python3
"""RQT-563 bounded exact ECM, requires SymPy; input is RQT-559 results.json."""
import json,sys,hashlib,math,time
from pathlib import Path
from sympy.ntheory.ecm import _ecm_one_factor
p=Path(sys.argv[1]); raw=p.read_bytes();v=json.loads(raw)
assert hashlib.sha256(raw).hexdigest()=='5504e1be18d2b1f55c1db0039f3569330babc93f26bf482fd084c56ee2c3d6b7'
N=int(v['numerator']);T=int(v['T']);beta=int(v['beta'])
assert N.bit_length()==942 and math.gcd(N,T)==math.gcd(N,beta)==1
for B1,B2,curves,seed in [(10000,100000,20,56301),(12000,120000,8,56302)]:
 t=time.monotonic();f=_ecm_one_factor(N,B1,B2,curves,seed)
 if f is not None and 1<int(f)<N and N%int(f)==0:
  print('VERIFIED FACTOR',f,'COFACTOR',N//int(f));break
 print('COMPLETE NO FACTOR',B1,B2,curves,seed,'seconds',round(time.monotonic()-t,3),flush=True)
else:print('RQT-563 bounded nonfinding; composite known; global norm/root19 OPEN')
