#!/usr/bin/env python3
"""RQT-647 exact coherent (t,y) 2-adic lifting through 1024.
python rqt647.py RQT-619-results.json RQT-626-results.json [OUTPUT.json]
"""
import sys,json,math,hashlib,collections
from pathlib import Path
rp,pp=map(Path,sys.argv[1:3]);out=Path(sys.argv[3] if len(sys.argv)>3 else 'RQT-647-results.json')
R=json.loads(rp.read_text());P=json.loads(pp.read_text())
assert R['rqt']==619 and P['rqt']==626
byid={v['canonical_id']:v for v in P['records']}
SHARP=(28,31,34,37,55,61,64,67,109,112)
levels=(16,32,64,128,256,512,1024)
records=[]
for rec in R['families']:
 idx=rec['canonical_id']
 if idx not in SHARP:continue
 r0,r1,r2,r3,r4,r5=map(int,rec['R_coefficients_as_strings'])
 q=byid[idx];a=int(q['pell_a']);h=int(q['pell_h']);c=int(q['primitive_discriminant_coefficients'][2]);N=int(q['pell_N']);D=abs(2*r0)
 assert (a,h,c,N)==(r1*r1-4*r0*r2,r1*r3-2*r0*r4,r3*r3-4*r0*r5,h*h-a*c)
 def valid(t,y,m):
  g=math.gcd(m,D);L=r1*t+r3
  return (y*y-a*t*t-2*h*t-c)%m==0 and ((y-L)%g==0 or (y+L)%g==0)
 def pairs_at(m):
  buckets=collections.defaultdict(list)
  for y in range(m):buckets[y*y%m].append(y)
  g=math.gcd(m,D);found=set()
  for t in range(m):
   L=r1*t+r3;target=(a*t*t+2*h*t+c)%m
   for y in buckets[target]:
    if (y-L)%g==0 or (y+L)%g==0:found.add((t,y))
  return found
 prev=pairs_at(16)
 info=[{'modulus':16,'pairs':len(prev),'projected_t':len({t for t,y in prev})}]
 for m in levels[1:]:
  parent=m//2;nxt=set();branch_counts=collections.Counter()
  for t,y in prev:
   kids=[(t+dt,y+dy) for dt in (0,parent) for dy in (0,parent) if valid(t+dt,y+dy,m)]
   branch_counts[len(kids)]+=1;nxt.update(kids)
  assert len(nxt)==sum(k*v for k,v in branch_counts.items())
  if m<=256:assert nxt==pairs_at(m)
  info.append({'modulus':m,'pairs':len(nxt),'projected_t':len({t for t,y in nxt}),
   'parent_pair_count':len(prev),'parent_child_degree':{str(k):branch_counts[k] for k in range(5)},
   'terminated_parent_pairs':branch_counts[0],
   'parents_with_at_least_one_lift':len(prev)-branch_counts[0]})
  prev=nxt
 records.append({'canonical_id':idx,'members':rec['member_ids'],'levels':info})
assert len(records)==10
agg=[]
for j,m in enumerate(levels):
 v={'modulus':m,'pairs':sum(r['levels'][j]['pairs'] for r in records),
    'projected_t':sum(r['levels'][j]['projected_t'] for r in records)}
 if j:
  v['terminated_parent_pairs']=sum(r['levels'][j]['terminated_parent_pairs'] for r in records)
  v['parents_with_lifts']=sum(r['levels'][j]['parents_with_at_least_one_lift'] for r in records)
  v['branch_degrees']={str(k):sum(r['levels'][j]['parent_child_degree'][str(k)] for r in records) for k in range(5)}
 agg.append(v)
result={'rqt':647,'scope':'10 sharpened canonical orbits; paired finite coherent lifts through modulus 1024; no infinity claimed',
 'inputs_sha256':{'rqt619':hashlib.sha256(rp.read_bytes()).hexdigest(),'rqt626':hashlib.sha256(pp.read_bytes()).hexdigest()},
 'levels':list(levels),'families':records,'aggregate':agg,'selected_excluded':82,
 'selected_unresolved':53,'new_full_family_exclusions':0,'root19':'OPEN','original_22d_wall':'NOT REPLAYED'}
out.write_text(json.dumps(result,indent=2)+'\n')
print('PASS RQT-647: 10 orbit trees; final',agg[-1]['pairs'],'coherent pairs')
