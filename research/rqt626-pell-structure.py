#!/usr/bin/env python3
"""RQT-626: exact generalized Pell structure replay.
python rqt626.py RQT-625-results.json [RQT-626-results.json]
"""
import json,math,hashlib,sys
from pathlib import Path
from collections import defaultdict
p=Path(sys.argv[1]);raw=p.read_bytes();d=json.loads(raw)
assert d['rqt']==625
assert hashlib.sha256(raw).hexdigest()=='201bbc5dfde380016884c775ff1c390a69196303fce3a8199219de739c6ace69'
groups=defaultdict(list);items=[]
for f in d['families']:
 A,B,C=map(int,f['discriminant_coefficients'])
 assert math.gcd(A,math.gcd(B,C))==4
 a,b,c=A//4,B//4,C//4
 assert b%2==0
 h=b//2;N=h*h-a*c
 assert a>0 and math.isqrt(a)**2!=a
 for t in (-100001,-73,-1,0,1,73,100001):
  v=a*t*t+2*h*t+c;z=a*t+h
  assert A*t*t+B*t+C==4*v
  assert z*z-a*v==N
 groups[a].append(f['canonical_id'])
 items.append({'canonical_id':f['canonical_id'],'member_ids':f['member_ids'],
 'primitive_discriminant':[str(a),str(b),str(c)],
 'pell_a':str(a),'pell_h':str(h),'pell_N':str(N),
 'equation':'z^2-a*y^2=N','parameter_gate':'z congruent h mod a; t=(z-h)/a',
 'integer_coordinate_gate':'reconstruct and verify u from original Q(u,t)=0'})
assert len(items)==27 and len(groups)==5 and sorted(map(len,groups.values()))==[3,3,4,8,9]
assert len({(r['pell_a'],r['pell_N']) for r in items})==27
out={'rqt':626,'source_rqt625_sha256':hashlib.sha256(raw).hexdigest(),
 'canonical_orbits':27,'coefficient_groups':[{'a':str(a),'canonical_ids':v} for a,v in sorted(groups.items())],
 'records':items,'new_all_scale_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
 'original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
dst=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-626-results.json')
dst.write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 27 generalized Pell identities, five nonsquare leading coefficients')
