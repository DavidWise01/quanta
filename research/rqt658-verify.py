#!/usr/bin/env python3
"""Independent Python-stdlib verifier for RQT-658-results.json."""
import json,hashlib,math,sys
from pathlib import Path
p=Path(sys.argv[1]);d=json.loads(p.read_text());assert d['rqt']==658
nodes=d['certificates'];verified=set();visiting=set()
def verify(n):
 n=int(n);key=str(n)
 if n in verified:return
 assert n not in visiting and key in nodes
 visiting.add(n);rec=nodes[key]
 if n==2:
  assert rec['factors']==[] and rec['witnesses']==[]
 else:
  factors=[(int(q),int(e)) for q,e in rec['factors']]
  assert n>2 and n%2 and len(factors)==len({q for q,e in factors})
  assert all(e>=1 and q>=2 for q,e in factors)
  assert math.prod(q**e for q,e in factors)==n-1
  witnesses={int(w['q']):int(w['a']) for w in rec['witnesses']}
  assert set(witnesses)=={q for q,e in factors}
  for q,e in factors:
   verify(q);a=witnesses[q]
   assert 1<a<n and pow(a,n-1,n)==1
   assert math.gcd(pow(a,(n-1)//q,n)-1,n)==1
 visiting.remove(n);verified.add(n)
for k in nodes:verify(k)
for i in d['certified_target_indexes']:verify(int(d['target_values'][str(i)]))
assert len(verified)==126
assert set(d['certified_target_indexes'])=={0,1,4,12,24,26}
assert d['remaining_open_indexes']==[23,28]
if len(sys.argv)>2:
 raw=Path(sys.argv[2]).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==d['source_rqt656_sha256']
 x=json.loads(raw)
 for i in d['certified_target_indexes']:
  assert str(x['records'][i]['input'])==str(d['target_values'][str(i)])
print('PASS RQT-658: 6 certified large prime targets; 126 proof nodes; 23/28 OPEN')
