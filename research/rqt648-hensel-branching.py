#!/usr/bin/env python3
"""RQT-648: exact 27-orbit Hensel roots and 0-or-4 pair lifting.
python rqt648-hensel-branching.py RQT-619-results.json [output.json]
"""
import json,math,hashlib,sys
from pathlib import Path
from collections import Counter
src=Path(sys.argv[1]);R=json.loads(src.read_text())
assert R['rqt']==619
assert hashlib.sha256(src.read_bytes()).hexdigest()=='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
rows=[];tot=Counter()
for r in R['families']:
 idx=r['canonical_id'];r0,r1,r2,r3,r4,r5=map(int,r['R_coefficients_as_strings'])
 D=abs(2*r0);assert D%8==0 and D%16!=0
 def G(u,t):return r0*u*u+r1*u*t+r2*t*t+r3*u+r4*t+r5
 def der(u,t):return 2*r0*u+r1*t+r3
 seeds=[(u,t) for t in range(2) for u in range(2) if not G(u,t)%2 and der(u,t)%2]
 assert seeds
 u,t=seeds[0];lifts=[]
 for n in range(1,25):
  assert G(u,t)%(1<<n)==0
  if n in (1,2,3,4,8,16,24):lifts.append({'n':n,'u':u,'t':t})
  if n<24:u+=((G(u,t)//(1<<n))%2)*(1<<n)
 a=r1*r1-4*r0*r2;h=r1*r3-2*r0*r4;c=r3*r3-4*r0*r5
 def valid(T,Y,m):
  g=math.gcd(m,D);L=r1*T+r3
  return (Y*Y-a*T*T-2*h*T-c)%m==0 and ((Y-L)%g==0 or (Y+L)%g==0)
 m=16;deg=Counter();num=0
 for T in range(m):
  for Y in range(m):
   if not valid(T,Y,m):continue
   num+=1
   children=sum(valid(T+i*m,Y+j*m,m*2) for i in range(2) for j in range(2))
   assert children in (0,4)
   deg[children]+=1
 tot.update({'parent_pairs':num,'dead':deg[0],'four':deg[4]})
 rows.append({'canonical_id':idx,'member_ids':r['member_ids'],
  'mod2_seeds':[{'u':u,'t':t} for u,t in seeds],
  'selected_seed':{'u':seeds[0][0],'t':t},'hensel_lifts':lifts,
  'parents_mod16':num,'degree_zero':deg[0],'degree_four':deg[4]})
assert len(rows)==27 and sum(len(x['member_ids']) for x in rows)==53
assert (tot['parent_pairs'],tot['dead'],tot['four'])==(1544,736,808)
out={'rqt':648,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'theorem_zero_or_four':'For k>=4, all four pair children obey the same mod 2^(k+1) predicate; hence degree 0 or 4.',
 'theorem_hensel':'Every orbit has G mod 2 = 0 with odd dG/du, thus a unique fixed-t lift to Z_2.',
 'families':rows,'aggregate':dict(tot),'new_full_family_exclusions':0,
 'selected_excluded':82,'selected_unresolved':53,'root19':'OPEN',
 'original_22d_wall':'NOT REPLAYED','integer_root':'NOT CONSTRUCTED'}
dst=Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-648-results.json')
dst.write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-648: 27 all-depth 2-adic roots; 1544 parents, 736 dead, 808 four-child')
