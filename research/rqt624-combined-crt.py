#!/usr/bin/env python3
"""RQT-624 exact combined CRT verifier. Python 3 stdlib only.
python rqt624.py RQT-623-results.json RQT-591-results.json RQT-583-results.json [OUT.json]
"""
import json,hashlib,math,sys
from pathlib import Path
paths=list(map(Path,sys.argv[1:4]))
S,G,E=[json.loads(p.read_text()) for p in paths]
assert S['rqt']==623 and G['rqt']==591 and E['rqt']==583
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(paths[0])=='640343c28a6d18aedc0c7dc503d15c3fcdcafd334aa672d034165db23d52efd5'
assert sha(paths[2])=='5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92'
F=[[int(v) for v in row] for row in G['reduced_gram']]
eq={x['index']:x for x in E['equations']}
def coefficients(e):
 r,o=e['ray'],e['offset']
 dot=lambda x,y:sum(x[i]*F[i+1][j+1]*y[j] for i in range(3) for j in range(3))
 return (F[0][0],2*sum(F[0][i+1]*r[i] for i in range(3)),dot(r,r),
 2*sum(F[0][i+1]*o[i] for i in range(3)),2*dot(r,o),dot(o,o)+2)
def q(c,u,t):
 a,b,d,e,f,g=c
 return a*u*u+b*u*t+d*t*t+e*u+f*t+g
def grad(c,u,t):
 a,b,d,e,f,g=c
 return 2*a*u+b*t+e,b*u+2*d*t+f
def crt(pairs):
 m=math.prod(p for p,u,t in pairs)
 assert all(math.gcd(p,s)==1 for j,(p,_,_) in enumerate(pairs) for s,_,_ in pairs[j+1:])
 u=sum((a%p)*(m//p)*pow(m//p,-1,p) for p,a,b in pairs)%m
 t=sum((b%p)*(m//p)*pow(m//p,-1,p) for p,a,b in pairs)%m
 return m,u,t
results=[]
for x in S['families']:
 idx=x['canonical_id'];c=coefficients(eq[idx])
 first={}
 for t in range(256):
  for u in range(256):
   if q(c,u,t)%256==0:
    first[t]=u;break
 assert sorted(first)==x['allowed_t_residues']
 pairs=[(256,first[min(first)],min(first))]
 proj={'256':sorted(first)}
 for p in (7,31):
  roots=[(u,t) for t in range(p) for u in range(p) if q(c,u,t)%p==0]
  assert roots
  proj[str(p)]=sorted({t for u,t in roots})
  if (idx,p) in ((2,7),(28,31)):
   assert len(roots)==1
   u0,t0=roots[0];du,dt=grad(c,u0,t0)
   assert du%p==dt%p==q(c,u0,t0)%(p*p)==0
   red=(c[0],c[1],c[2],du//p,dt//p,q(c,u0,t0)//(p*p))
   rr=[(a,b) for b in range(p) for a in range(p) if q(red,a,b)%p==0]
   assert all(any(z%p for z in grad(red,a,b)) for a,b in rr)
   proj[str(p*p)]=sorted({(t0+p*b)%(p*p) for a,b in rr})
   if idx==2:assert proj['49']==[13,20,27,34] and len(rr)==8
   if idx==28:assert len(proj['961'])==16 and len(rr)==32
   a,b=rr[0];uu,tt=u0+p*a,t0+p*b
   assert q(c,uu,tt)%(p**3)==0
   pairs.append((p**3,uu,tt))
  else:pairs.append((p,*roots[0]))
 m,u,t=crt(pairs)
 assert q(c,u,t)%m==0
 mods=[256,49 if idx==2 else 7,961 if idx==28 else 31]
 count=math.prod(len(proj[str(p)]) for p in mods)
 results.append({'canonical_id':idx,'member_ids':x['member_ids'],
  'projected_t_residues':proj,'t_wheel_moduli':mods,
  't_wheel_modulus':math.prod(mods),'t_wheel_allowed_classes':count,
  'coordinate_CRT_moduli':[p for p,_,_ in pairs],
  'coordinate_CRT_modulus':m,'coordinate_u':str(u),'coordinate_t':str(t),
  'norm_residue_mod_CRT':0})
assert len(results)==27 and sum(len(r['member_ids']) for r in results)==53
out={'rqt':624,'sources_sha256':{p.name:sha(p) for p in paths},'families':results,
 'new_all_scale_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
 'integer_seed':'NOT FOUND','original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
Path(sys.argv[4] if len(sys.argv)>4 else 'RQT-624-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 27 CRT coordinate witnesses; root19 OPEN')
