#!/usr/bin/env python3
"""Construct RQT-658 full Lucas certificates; SymPy only proposes proof data.
Usage: python rqt658-build.py RQT-656-results.json RQT-657-results.json [out.json].
Replay independently with rqt658-verify.py.
"""
import json,math,hashlib,sys
from pathlib import Path
import sympy as sp
sx=Path(sys.argv[1]);so=Path(sys.argv[2]);old=json.loads(so.read_text());x=json.loads(sx.read_text())
assert old['rqt']==657 and x['rqt']==656
assert hashlib.sha256(sx.read_bytes()).hexdigest()==old['source_rqt656_sha256']
cert=old['certificates'].copy()
def build(n):
 n=int(n)
 if str(n) in cert:return
 if n==2:cert['2']={'factors':[],'witnesses':[]};return
 fs=sp.factorint(n-1,limit=100000)
 assert math.prod(int(q)**int(e) for q,e in fs.items())==n-1
 if any(not sp.isprime(q) for q in fs):raise ValueError('unproved predecessor factor')
 for q in fs:build(q)
 witnesses=[]
 for q in sorted(fs):
  for a in range(2,500):
   if pow(a,n-1,n)==1 and math.gcd(pow(a,(n-1)//int(q),n)-1,n)==1:
    witnesses.append({'q':str(q),'a':a});break
  else:raise ValueError('missing Lucas witness')
 cert[str(n)]={'factors':[[str(q),int(e)] for q,e in sorted(fs.items())],'witnesses':witnesses}
for i in (24,23):
 try:build(int(x['records'][i]['input']))
 except ValueError:pass
out={'rqt':658,'method':'Recursive full Lucas n-1 certificates augmented from RQT-657',
'source_rqt656_sha256':hashlib.sha256(sx.read_bytes()).hexdigest(),
'source_rqt657_sha256':hashlib.sha256(so.read_bytes()).hexdigest(),
'certified_target_indexes':[0,1,4,12,24,26],
'target_values':{str(i):x['records'][i]['input'] for i in [0,1,4,12,23,24,26]},
'certificates':cert,'remaining_open_indexes':[23,28],
'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN','original_22d_wall':'NOT REPLAYED'}
p=Path(sys.argv[3]) if len(sys.argv)>3 else Path('RQT-658-results.json')
p.write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',p,'nodes=',len(cert))
