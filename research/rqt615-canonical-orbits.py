#!/usr/bin/env python3
"""RQT-615: canonical sign-orbit ledger from RQT-583/584/586/614 exact JSON."""
import sys,json,hashlib
from pathlib import Path
P=list(map(Path,sys.argv[1:5]));E,A,B,R=[json.loads(p.read_text()) for p in P]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert [sha(p) for p in P[:3]]==['5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92','29f0eb2b4ef29d3194185ee45d72c58a793b41bd44993b0b6ad33bf3435cbe5f','45d129e80c7d6b19af2ba7a7e8e541f865e37646a2709efebbba87bb584a4859']
byid={int(e['index']):e for e in E['equations']}
bykey={(tuple(e['ray']),tuple(e['offset'])):e for e in E['equations']}
excluded={int(c['family_index']) for d in (A,B) for c in d['certificates']}|{13}
assert len(byid)==80 and len(bykey)==80 and len(excluded)==27
orbits=[];seen=set()
for i in sorted(byid):
 if i in seen:continue
 e=byid[i];other=bykey[(tuple(e['ray']),tuple(-v for v in e['offset']))]
 j=int(other['index']);ids=sorted({i,j});seen.update(ids)
 assert all((z in excluded)==(i in excluded) for z in ids)
 assert int(e['A'])==int(other['A']) and int(e['B'])==-int(other['B'])
 assert int(e['C'])==int(other['C']) and int(e['D'])==int(other['D'])
 for t in (-101,-1,0,1,101):
  q=lambda x,z:int(x['A'])*z*z+int(x['B'])*z+int(x['C'])
  assert q(e,t)==q(other,-t)
 orbits.append({'canonical_id':ids[0],'member_ids':ids,'status':'excluded' if i in excluded else 'unresolved','ray':e['ray'],'canonical_offset':byid[ids[0]]['offset']})
assert len(orbits)==41 and len(seen)==80
assert sum(len(o['member_ids'])==2 for o in orbits)==39
assert [o['canonical_id'] for o in orbits if len(o['member_ids'])==1]==[13,67]
assert sum(o['status']=='unresolved' for o in orbits)==27
assert sum(len(o['member_ids']) for o in orbits if o['status']=='unresolved')==53
assert sorted(o['member_ids'] for o in orbits if len(o['member_ids'])==2)==R['pairs']
out={'rqt':615,'source_sha256':{p.name:sha(p) for p in P},'archived_equations':80,'canonical_orbits':41,'excluded_orbits':14,'unresolved_orbits':27,'status_conflicts':0,'orbits':orbits,'selected_excluded':82,'selected_unresolved':53,'new_exclusions':0,'root19':'OPEN'}
Path(sys.argv[5] if len(sys.argv)>5 else 'RQT-615-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-615: 41 orbits, 27 unresolved, 0 conflicts, root19 OPEN')
