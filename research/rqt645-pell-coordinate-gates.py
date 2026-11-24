#!/usr/bin/env python3
"""RQT-645 exact Pell-target to original integer-coordinate recovery.
Usage: python rqt645-pell-coordinate-gates.py RQT-619-results.json RQT-626-results.json [out.json]
"""
import sys,json,math,hashlib
from pathlib import Path
p,q=map(Path,sys.argv[1:3])
R=json.loads(p.read_text());P=json.loads(q.read_text())
assert R['rqt']==619 and P['rqt']==626
assert hashlib.sha256(p.read_bytes()).hexdigest()=='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
assert hashlib.sha256(q.read_bytes()).hexdigest()=='1d901288a9a6007f79496615ef421bd0c6aa147aab1ecc33355e5ef71d4c1052'
assert len(R['families'])==len(P['records'])==27
byid={x['canonical_id']:x for x in P['records']}
moduli=(8,16,32,121,169);rows=[]
for rec in R['families']:
 idx=rec['canonical_id'];p=byid[idx]
 r0,r1,r2,r3,r4,r5=map(int,rec['R_coefficients_as_strings'])
 a=int(p['pell_a']);h=int(p['pell_h'])
 c=int(p['primitive_discriminant_coefficients'][2]);N=int(p['pell_N'])
 assert (a,h,c)==(r1*r1-4*r0*r2,r1*r3-2*r0*r4,r3*r3-4*r0*r5)
 assert N==h*h-a*c
 denominator=abs(2*r0)
 def F(t):return a*t*t+2*h*t+c
 def L(t):return r1*t+r3
 for t in (-123456789,-1,0,1,123456789):
  assert F(t)-L(t)**2==-4*r0*(r2*t*t+r4*t+r5)
 modular=[]
 for m in moduli:
  roots={}
  for y in range(m):roots.setdefault(y*y%m,[]).append(y)
  pair_count=accepted=pt=at=0;rejected_t=[]
  g=math.gcd(denominator,m)
  for t in range(m):
   yy=roots.get(F(t)%m,[])
   if yy:pt+=1
   chosen=[y for y in yy if (y-L(t))%g==0 or (y+L(t))%g==0]
   if chosen:at+=1
   if yy and not chosen:rejected_t.append(t)
   pair_count+=len(yy);accepted+=len(chosen)
  modular.append({'modulus':m,'pell_pairs':pair_count,'recovery_pairs':accepted,'pell_t':pt,'recovery_t':at,'rejected_t':rejected_t})
 rows.append({'canonical_id':idx,'member_ids':rec['member_ids'],'coordinate_denominator':str(denominator),
              'pell_a':str(a),'pell_h':str(h),'pell_N':str(N),'modular':modular})
assert len(rows)==27 and len({v['coordinate_denominator'] for v in rows})==1
assert [sum(v['modular'][i]['recovery_t'] for v in rows) for i in range(len(moduli))]==[216,432,704,2992,4329]
assert [v['canonical_id'] for v in rows if v['modular'][2]['rejected_t']]==[28,31,34,37,55,61,64,67,109,112]
out={'rqt':645,'source_sha256':{'RQT-619':hashlib.sha256(p.read_bytes()).hexdigest(),'RQT-626':hashlib.sha256(q.read_bytes()).hexdigest()},
'canonical_orbits':27,'coordinate_identity':'u=(-r1*t-r3 ± y)/(2*r0), y^2=a*t^2+2*h*t+c','families':rows,
'selected_excluded':82,'selected_unresolved':53,'new_full_family_exclusions':0,'root19':'OPEN','original_22D_wall':'NOT REPLAYED'}
dest=Path(sys.argv[3] if len(sys.argv)>3 else 'RQT-645-results.json')
dest.write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-645: 27 target identities, mod32 t residues 784 -> 704')
