#!/usr/bin/env python3
"""Build RQT-659 partial Pocklington proof bundle.
python rqt659-build.py RQT-658-results.json RQT-656-results.json [out.json]
SymPy proposes predecessor factors; rqt659-verify.py checks all proofs independently.
"""
import json,sys,math,hashlib
from pathlib import Path
import sympy as sp
cfile,rfile=map(Path,sys.argv[1:3])
old=json.loads(cfile.read_text());base=json.loads(rfile.read_text())
assert old['rqt']==658 and base['rqt']==656
nodes=dict(old['certificates'])
def add_prime(n):
 n=int(n)
 if str(n) in nodes:return
 if n==2:nodes['2']={'factors':[],'witnesses':[]};return
 fs=sp.factorint(n-1)
 assert math.prod(int(q)**int(e) for q,e in fs.items())==n-1
 for q in fs:add_prime(q)
 witnesses=[]
 for q in sorted(fs):
  a=next(a for a in range(2,500) if pow(a,n-1,n)==1 and math.gcd(pow(a,(n-1)//int(q),n)-1,n)==1)
  witnesses.append({'q':str(q),'a':a})
 nodes[str(n)]={'factors':[[str(q),int(e)] for q,e in sorted(fs.items())],'witnesses':witnesses}
for q in (487,2273059):add_prime(q)
candidates=[]
for idx,fs in [(23,[(2,2),(3,1),(257,1)]),(28,[(2,1),(487,1),(2273059,1)])]:
 n=int(base['records'][idx]['input']);F=math.prod(q**e for q,e in fs)
 assert (n-1)%F==0
 R=(n-1)//F;witnesses=[]
 for q,e in fs:
  assert str(q) in nodes
  a=next(a for a in range(2,500) if pow(a,n-1,n)==1 and math.gcd(pow(a,(n-1)//q,n)-1,n)==1)
  witnesses.append({'q':str(q),'a':a,'exponent':e})
 candidates.append({'index':idx,'n':str(n),'certified_part_F':str(F),'unresolved_part_R':str(R),
 'known_prime_power_factors':[[str(q),e] for q,e in fs],
 'partial_lucas_witnesses':witnesses,'F_exceeds_sqrt_n':F*F>n,
 'missing_for_threshold':'F^2 <= n; no Pocklington primality conclusion',
 'unresolved_part_fermat_base2':str(pow(2,R-1,R)),
 'unresolved_part_composite_proved':pow(2,R-1,R)!=1})
assert [c['F_exceeds_sqrt_n'] for c in candidates]==[False,False]
result={'rqt':659,'method':'Exact partial n-1 factor and Lucas/Pocklington witness threshold audit',
 'source_rqt658_sha256':hashlib.sha256(cfile.read_bytes()).hexdigest(),
 'source_rqt656_sha256':hashlib.sha256(rfile.read_bytes()).hexdigest(),
 'prime_nodes':nodes,'candidates':candidates,
 'additional_certified_predecessor_primes':[487,2273059],
 'previously_proved_candidate_indexes':old['certified_target_indexes'],
 'remaining_open_indexes':[23,28],'new_prime_targets_certified':0,
 'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN','original_22d_wall':'NOT REPLAYED'}
out=Path(sys.argv[3] if len(sys.argv)>3 else 'RQT-659-results.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print('Built RQT-659:',len(nodes),'certified nodes; index 23 and 28 OPEN')
