#!/usr/bin/env python3
"""Verify complete recursive Lucas n−1 primality certificates, Python standard library.
Usage: python rqt657.py RQT-657-results.json [RQT-656-results.json]
"""
import sys,json,math,hashlib
from pathlib import Path
p=Path(sys.argv[1]);d=json.loads(p.read_text());assert d['rqt']==657
C=d['certificates'];verified=set()
def verify(n):
 n=int(n)
 if n in verified:return
 rec=C[str(n)]
 if n==2:
  assert rec['factors']==[] and rec['witnesses']==[]
  verified.add(n);return
 assert n>2 and n%2
 factors=[(int(q),int(e)) for q,e in rec['factors']]
 assert factors and len({q for q,e in factors})==len(factors)
 assert all(e>=1 for q,e in factors)
 assert math.prod(q**e for q,e in factors)==n-1
 for q,e in factors:verify(q)
 witnesses={int(x['q']):int(x['a']) for x in rec['witnesses']}
 assert len(witnesses)==len(factors)
 for q,e in factors:
  a=witnesses[q]
  assert 1<a<n and pow(a,n-1,n)==1
  assert math.gcd(pow(a,(n-1)//q,n)-1,n)==1
 verified.add(n)
for index in d['certified_target_indexes']:verify(int(d['target_values'][str(index)]))
assert set(d['certified_target_indexes'])=={0,1,4,12,26}
assert d['other_indexes_still_open']==[23,24,28]
if len(sys.argv)>2:
 source=Path(sys.argv[2])
 assert hashlib.sha256(source.read_bytes()).hexdigest()==d['source_rqt656_sha256']
 x=json.loads(source.read_text())
 for i in d['certified_target_indexes']:
  assert int(x['records'][i]['input'])==int(d['target_values'][str(i)])
print(f"PASS: {len(d['certified_target_indexes'])} targets; {len(verified)} prime nodes; 3 open")
