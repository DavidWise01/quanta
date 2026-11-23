#!/usr/bin/env python3
"""RQT-623 exact parameter residue projection. Python 3 standard library.
Usage: python rqt623-coordinate-projection.py RQT-619.json RQT-591.json RQT-583.json OUT.json
"""
import sys,json,hashlib
from pathlib import Path
from collections import Counter
a,b,c,out=map(Path,sys.argv[1:5])
j,g,e=[json.loads(p.read_text()) for p in (a,b,c)]
assert j['rqt']==619 and g['rqt']==591 and e['rqt']==583
assert hashlib.sha256(a.read_bytes()).hexdigest()=='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
assert hashlib.sha256(c.read_bytes()).hexdigest()=='5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92'
F=[[int(z) for z in row] for row in g['reduced_gram']]
byid={v['index']:v for v in e['equations']}
records=[]
for rec in j['families']:
 idx=rec['canonical_id'];eq=byid[idx];r,o=eq['ray'],eq['offset']
 dot=lambda v,w:sum(v[i]*F[i+1][k+1]*w[k] for i in range(3) for k in range(3))
 A=F[0][0];B=2*sum(F[0][i+1]*r[i] for i in range(3));C=dot(r,r)
 D=2*sum(F[0][i+1]*o[i] for i in range(3));E=2*dot(r,o);G=dot(o,o)+2
 assert all(v%2==0 for v in (A,B,C,D,E,G))
 half=tuple(v//2 for v in (A,B,C,D,E,G))
 assert half==tuple(map(int,rec['R_coefficients_as_strings']))
 def norm(coeff,u,t):
  a,b,c,d,e,f=coeff
  return a*u*u+b*u*t+c*t*t+d*u+e*t+f
 allowed=[];number=0;sample=[]
 for t in range(256):
  roots=[u for u in range(256) if norm((A,B,C,D,E,G),u,t)%256==0]
  if roots:
   allowed.append(t);number+=len(roots)
   if len(sample)<4:sample.append({'t':t,'u':roots[0],'u_choices':len(roots)})
 independent=[t for t in range(256) if any(norm(half,u,t)%128==0 for u in range(128))]
 assert allowed==independent
 members=rec['member_ids']
 if len(members)==2:
  partner=byid[members[1]]
  assert partner['ray']==r and partner['offset']==[-z for z in o]
 records.append({'canonical_id':idx,'member_ids':members,'modulus':256,
 'allowed_t_residues':allowed,'allowed_t_count':len(allowed),
 'exact_coordinate_pairs':number,'sample_witnesses':sample,'mirror_t_map':'t -> (-t) modulo 256'})
assert len(records)==27 and sum(len(x['member_ids']) for x in records)==53
dist=Counter(x['allowed_t_count'] for x in records)
assert dist=={128:10,196:1,200:6,224:4,228:1,240:1,256:4}
result={'rqt':623,'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (a,b,c)},
'projection_modulus':256,'canonical_jobs':27,'original_family_ids':53,
'distribution_allowed_t_residues':{str(k):v for k,v in sorted(dist.items())},
'families':records,'new_full_family_exclusions':0,'selected_excluded':82,
'selected_unresolved':53,'original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
out.write_text(json.dumps(result,indent=2)+'\n')
print('PASS RQT-623, 27 canonical orbits, exact modulo256 parameter gates')
