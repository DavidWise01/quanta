#!/usr/bin/env python3
"""RQT-616: exact 27-job canonical planner; Python 3 standard library.
Usage: python rqt616.py RQT-615-results.json RQT-583-results.json [OUT.json]
"""
import hashlib,json,sys
from pathlib import Path
p,q=map(Path,sys.argv[1:3]);a=json.loads(p.read_text());b=json.loads(q.read_text())
assert a['rqt']==615 and b['rqt']==583
expected='5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92'
assert hashlib.sha256(q.read_bytes()).hexdigest()==expected
assert a['source_sha256'][q.name]==expected
byid={int(e['index']):e for e in b['equations']}
unresolved=[o for o in a['orbits'] if o['status']=='unresolved']
assert len(unresolved)==27 and sum(len(o['member_ids']) for o in unresolved)==53
jobs=[];prev='0'*64
for n,o in enumerate(sorted(unresolved,key=lambda x:x['canonical_id']),1):
 i=o['canonical_id'];e=byid[i];members=o['member_ids']
 assert members[0]==i and e['ray']==o['ray'] and e['offset']==o['canonical_offset']
 maps=[]
 for j in members:
  other=byid[j];s=1 if j==i else -1
  assert other['ray']==e['ray'] and other['offset']==[s*v for v in e['offset']]
  assert int(other['A'])==int(e['A']) and int(other['B'])==s*int(e['B'])
  assert int(other['C'])==int(e['C']) and int(other['D'])==int(e['D'])
  for t in (-17,-1,0,1,19):
   delta=lambda v,k:int(v['A'])*k*k+int(v['B'])*k+int(v['C'])
   assert delta(other,s*t)==delta(e,t)
  maps.append({'family_index':j,'sign_from_canonical':s,'forward':f'(u,t) -> ({s}*u,{s}*t)','inverse':f'(u,t) -> ({s}*u,{s}*t)'})
 gates={}
 for prime in (7,11,13):
  sq={v*v%prime for v in range(prime)}
  gates[str(prime)]=[t for t in range(prime) if (int(e['A'])*t*t+int(e['B'])*t+int(e['C']))%prime in sq]
 r={'ordinal':n,'canonical_id':i,'family_ids':members,'ray':e['ray'],'canonical_offset':e['offset'],'symmetry_mappings':maps,'discriminant_coefficients':{k:e[k] for k in 'ABCD'},'preflight_prime_residues':gates,'assigned_task':'exact integrality and generalized Pell seed constraints','evidence_ancestry':'RQT-583/RQT-584/RQT-586/RQT-592 -> RQT-614 -> RQT-615','prior_hash':prev,'status':'UNRESOLVED'}
 h=hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 r['sha256']=h;prev=h;jobs.append(r)
assert len(jobs)==27 and len({j for r in jobs for j in r['family_ids']})==53
assert prev=='6b365ada55f5e44881707b73b764814afbf6dc00e1d05affda4103ea2b229cd7'
out={'rqt':616,'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest(),q.name:expected},'jobs':jobs,'job_count':27,'unresolved_family_ids':53,'mirror_pair_jobs':26,'singleton_jobs':1,'last_job_hash':prev,'new_all_scale_exclusions':0,'selected_excluded':82,'selected_unresolved':53,'unclassified_prior_55_symmetry':'NOT VERIFIED','original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
Path(sys.argv[3] if len(sys.argv)>3 else 'RQT-616-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 27 jobs, 53 IDs, zero duplicates; Root19 OPEN')
