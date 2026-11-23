#!/usr/bin/env python3
"""RQT-605 exact combined CRT verification. Usage: python rqt605.py CERT_DIR GRAM OUT_JSON"""
import json,hashlib,math,sys
from pathlib import Path
D,G,O=map(Path,sys.argv[1:4]); F=json.loads(G.read_text())
ledger=json.loads((D/'RQT-604-results.json').read_text())
assert hashlib.sha256(G.read_bytes()).hexdigest()=='f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228'
assert ledger['ledger_tip_sha256']=='e2bd1c5818a294ecd578af40791c81b3b96c432ee9276f0f404b7e4b054994a2'
mods=[256,81,125,49,11,13,17,19,23,29,31]; M=math.prod(mods)
assert M==121298984430624000
assert all(math.gcd(a,b)==1 for i,a in enumerate(mods) for b in mods[i+1:])
def crt(vals):
 return sum((v%m)*(M//m)*pow(M//m,-1,m) for v,m in zip(vals,mods))%M
def q(e,u,t):
 v=[u]+[e['ray'][i]*t+e['offset'][i] for i in range(3)]
 return sum(v[i]*F[i][j]*v[j] for i in range(4) for j in range(4))+2
prev='0'*64;results=[]
for entry in ledger['records']:
 e=json.loads((D/entry['path']).read_text());h=e.pop('sha256')
 assert h==entry['sha256']==hashlib.sha256(json.dumps(e,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 assert e['previous_hash']==prev;prev=h
cases={c['modulus']:c for c in e['direct_norm_modular_pairs']}
 assert all(cases[m]['number_of_pairs']>0 for m in mods)
 u=crt([cases[m]['example'][0] for m in mods])
 t=crt([cases[m]['example'][1] for m in mods])
 assert all(u%m==cases[m]['example'][0]%m and t%m==cases[m]['example'][1]%m for m in mods)
 assert q(e,u,t)%M==0
 count=math.prod(cases[m]['number_of_pairs'] for m in mods)
 results.append({'family_index':e['family_index'],'u_mod_M':str(u),'t_mod_M':str(t),'joint_solution_count':str(count),'norm_residue':0,'previous_record_sha256':h})
assert prev==ledger['ledger_tip_sha256'] and len(results)==53
O.write_text(json.dumps({'rqt':605,'combined_modulus':str(M),'moduli':mods,'families':results,'new_all_scale_exclusions':0,'excluded':82,'unresolved':53,'wall22d':'NOT REPLAYED','root19':'OPEN'},indent=2)+'\n')
print('PASS: 53 combined CRT coordinate witnesses modulo',M,'; Root19 OPEN')
