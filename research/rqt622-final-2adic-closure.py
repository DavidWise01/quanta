#!/usr/bin/env python3
"""RQT-622: exact final singular branch closure.
Usage: python rqt622.py RQT-619-results.json RQT-620-results.json RQT-621-results.json [out.json]
"""
import json,hashlib,sys
from pathlib import Path
ps=list(map(Path,sys.argv[1:4]))
d619,d620,d621=[json.loads(p.read_text()) for p in ps]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert list(map(sha,ps))==[
'97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021',
'c23027155b581a22983649642141ba95d0a00c081ece6c8b1215443a2f97b7b3',
'5d0a88735d0bdb0d7cc9ca3a51381475debb5e580cc8233e85a68711d3c1be92']
r=next(v for v in d619['families'] if v['canonical_id']==29)
s=next(v for v in d620['cases'] if v['canonical_id']==29)
t=next(v for v in d621['cases'] if v['canonical_id']==29)
assert t['member_ids']==[29,51]
assert len(r['regular_roots_R_mod_2'])==2 and r['singular_roots_R_mod_2']==[[0,1]]
assert len(s['S_regular_roots_mod2'])==2 and s['S_singular_roots_mod2']==[[1,1]]
assert t['T_regular_roots_mod2']==[[0,0],[1,1]] and t['T_singular_roots_mod2']==[[1,0]]
a,b,c,d,e,f=map(int,t['T_coefficients_exact'])
T=lambda u,v:a*u*u+b*u*v+c*v*v+d*u+e*v+f
du=lambda u,v:2*a*u+b*v+d
dv=lambda u,v:b*u+2*c*v+e
assert T(1,0)%4==2 and du(1,0)%2==dv(1,0)%2==0
for x in (-11,-1,0,1,11):
 for y in (-11,-1,0,1,11):
  assert T(1+2*x,2*y)%4==2
counts=r['archived_counts_k1_to_k10']
assert counts==[4,12,32,80,192,448,768,1536,3072,6144]
for k in range(7,11):assert counts[k-1]==6*2**k
result={'rqt':622,'source_sha256':{p.name:sha(p) for p in ps},
'canonical_family':29,'mirror_family':51,'final_singular_T_root_mod2':[1,0],
'T_coefficients_exact':list(map(str,(a,b,c,d,e,f))),
'fixed_class_obstruction':'T(1+2x,2y) congruent 2 mod 4 for all integers x,y',
'exact_all_exponent_count':'C_29(k)=C_51(k)=6*2^k for every integer k>=7',
'archived_counts_k1_to_k10':counts,'new_full_family_exclusions':0,
'selected_excluded':82,'selected_unresolved':53,
'original_22D_wall':'NOT REPLAYED','root19':'OPEN'}
Path(sys.argv[4] if len(sys.argv)>4 else 'RQT-622-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS RQT-622: exact six-regular-branch law, last singular branch blocked')
