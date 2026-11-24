#!/usr/bin/env python3
"""Independent standard-library Lucas/Pocklington audit for RQT-659.
python rqt659-verify.py RQT-659-results.json [RQT-658-results.json RQT-656-results.json]
"""
import sys,json,hashlib,math
from pathlib import Path
p=Path(sys.argv[1]);d=json.loads(p.read_text())
assert d['rqt']==659
nodes=d['prime_nodes'];verified=set();active=set()
def prime(n):
 n=int(n)
 if n in verified:return
 assert n not in active and str(n) in nodes
 active.add(n);rec=nodes[str(n)]
 if n==2:assert rec['factors']==[] and rec['witnesses']==[]
 else:
  fs=[(int(q),int(e)) for q,e in rec['factors']]
  assert n>2 and n%2 and fs and len(fs)==len({q for q,e in fs})
  assert all(q>=2 and e>=1 for q,e in fs)
  assert math.prod(q**e for q,e in fs)==n-1
  w={int(v['q']):int(v['a']) for v in rec['witnesses']}
  assert set(w)=={q for q,e in fs}
  for q,e in fs:
   prime(q);a=w[q]
   assert 1<a<n and pow(a,n-1,n)==1
   assert math.gcd(pow(a,(n-1)//q,n)-1,n)==1
 active.remove(n);verified.add(n)
for k in nodes:prime(k)
assert len(verified)==130 and 487 in verified and 2273059 in verified
assert [v['index'] for v in d['candidates']]==[23,28]
for row in d['candidates']:
 n=int(row['n']);F=int(row['certified_part_F']);R=int(row['unresolved_part_R'])
 factors=[(int(q),int(e)) for q,e in row['known_prime_power_factors']]
 assert math.prod(q**e for q,e in factors)==F
 assert F*R==n-1 and F*F<=n and row['F_exceeds_sqrt_n'] is False
 ws={int(v['q']):int(v['a']) for v in row['partial_lucas_witnesses']}
 assert set(ws)=={q for q,e in factors}
 for q,e in factors:
  a=ws[q];prime(q)
  assert pow(a,n-1,n)==1 and math.gcd(pow(a,(n-1)//q,n)-1,n)==1
 residual=pow(2,R-1,R)
 assert residual==int(row['unresolved_part_fermat_base2'])
 assert (residual!=1)==row['unresolved_part_composite_proved']
assert d['remaining_open_indexes']==[23,28] and d['new_prime_targets_certified']==0
if len(sys.argv)>2:
 a=Path(sys.argv[2]);b=Path(sys.argv[3])
 assert hashlib.sha256(a.read_bytes()).hexdigest()==d['source_rqt658_sha256']
 assert hashlib.sha256(b.read_bytes()).hexdigest()==d['source_rqt656_sha256']
 x=json.loads(b.read_text())
 assert all(str(x['records'][v['index']]['input'])==v['n'] for v in d['candidates'])
print('PASS RQT-659:',len(verified),'prime nodes; both target indexes OPEN')
