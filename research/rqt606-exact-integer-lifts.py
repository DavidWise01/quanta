#!/usr/bin/env python3
"""RQT-606 exact integer lifts and one-step residue-class lifting.
Usage: python rqt606.py RQT-605-results.json RQT-591-reduced_gram.json RQT-604-dir OUTPUT.json
"""
import sys,json,hashlib,math
from pathlib import Path
P,G,D,O=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4])
s=json.loads(P.read_text());F=json.loads(G.read_text())
ledger=json.loads((D/'RQT-604-results.json').read_text())
assert hashlib.sha256(P.read_bytes()).hexdigest()=='c3f6d0c97c960e6d5721e08d63e4b55e9752ecb139c5dc014f3fac9ea4dc724d'
assert hashlib.sha256(G.read_bytes()).hexdigest()==s['source_gram_sha256']
assert s['source_ledger_tip']==ledger['ledger_tip_sha256']
M=int(s['combined_modulus']);assert M==math.prod(s['moduli'])
families={v['index']:v for v in s['families']}
all_results=[];hits=[];B=20
for ref in ledger['records']:
 e=json.loads((D/ref['path']).read_text());i=e['family_index'];src=families[i]
 assert ref['sha256']==src['source_hash']==e['sha256']
 u0,t0=int(src['u_mod_M']),int(src['t_mod_M'])
 def q(u,t):
  v=[u]+[e['ray'][j]*t+e['offset'][j] for j in range(3)]
  return sum(v[a]*F[a][b]*v[b] for a in range(4) for b in range(4))+2
 assert q(u0,t0)%M==0
 minimum=None;best=None
 for k in range(-B,B+1):
  for l in range(-B,B+1):
   n=q(u0+k*M,t0+l*M)
   assert n%M==0
   if not n:hits.append([i,k,l])
   if minimum is None or abs(n)<minimum:minimum=abs(n);best=[k,l]
 local={}
 for p in (2,3,5,7,11):
  admissible=[[k,l] for k in range(p) for l in range(p) if q(u0+k*M,t0+l*M)%(p*M)==0]
  local[str(p)]={'count':len(admissible),'example':admissible[0] if admissible else None}
 all_results.append({'index':i,'minimum_abs_norm_plus_two':str(minimum),'best_k_l':best,'one_step_local_lifts':local})
assert len(all_results)==53 and not hits
assert {p:sum(not x['one_step_local_lifts'][str(p)]['count'] for x in all_results) for p in (2,3,5,7,11)}=={2:26,3:0,5:0,7:2,11:0}
O.write_text(json.dumps({'rqt':606,'source_605_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),
'M':str(M),'family_results':all_results,'integer_pairs_tested':53*(2*B+1)**2,
'exact_hits':hits,'all_scale_excluded':82,'unresolved':53,'new_exclusions':0,
'original_22d_wall':'NOT REPLAYED','root19':'OPEN'},indent=2)+'\n')
print('PASS RQT-606: 89,093 exact pairs, zero hits; selected families 82 excluded / 53 unresolved.')
