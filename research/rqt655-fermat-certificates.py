#!/usr/bin/env python3
"""Exact Fermat compositeness certificates from RQT-654-results.json."""
import hashlib,json,math,sys
from pathlib import Path
src=Path(sys.argv[1]);raw=src.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='f96f757aeb861f7a0c117639c91c6653fb00b745227cf80eb36b6bb2cbe4eae8'
x=json.loads(raw);assert x['rqt']==654 and len(x['records'])==31
rows=[]
for rec in x['records']:
 i=int(rec['cofactor_index']);n=int(rec['unresolved_remainder'])
 assert n>2 and n%2
 assert math.prod(int(f['prime'])**int(f['exponent']) for f in rec['certified_factors'])*n==int(rec['original'])
 residue=pow(2,n-1,n)
 rows.append({'index':i,'n':str(n),'fermat_residue':str(residue),'classification':'COMPOSITE_PROVED' if residue!=1 else 'PRIMALITY_UNRESOLVED'})
assert [r['index'] for r in rows]==list(range(31))
assert sum(r['classification']=='COMPOSITE_PROVED' for r in rows)==23
assert sum(r['classification']=='PRIMALITY_UNRESOLVED' for r in rows)==8
out={'rqt':655,'source_sha256':hashlib.sha256(raw).hexdigest(),'records':rows,'proven_composite':23,'primality_unresolved':8,'new_prime_certificates':0,'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN','wall22d':'NOT REPLAYED'}
p=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-655-results.json')
p.write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 23 composite and 8 primality unresolved')
