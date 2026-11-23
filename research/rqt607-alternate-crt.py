#!/usr/bin/env python3
"""RQT-607: repair nonliftable stored CRT classes; reproduce 53 modular witnesses.
Usage: python rqt607-alternates.py RQT604_DIR RQT605.json RQT606.json GRAM.json OUT.json
"""
import json,hashlib,math,sys
from pathlib import Path
D,P,Q,G,O=map(Path,sys.argv[1:6])
rd=lambda p:json.loads(p.read_text())
L=rd(D/'RQT-604-results.json');A=rd(P);B=rd(Q);F=rd(G)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(P)==B['source_605_sha256']
assert sha(G)==A['source_gram_sha256']==B['source_gram_sha256']
assert L['ledger_tip_sha256']==A['source_ledger_tip']==B['ledger_tip']
M=int(A['combined_modulus']);mm=[512,81,125,343,11,13,17,19,23,29,31]
N=math.prod(mm);assert N==14*M==1698185782028736000
def crt(vals):
 return sum((v%m)*(N//m)*pow(N//m,-1,m) for v,m in zip(vals,mm))%N
def coeff(e):
 r,o=e['ray'],e['offset'];dot=lambda v,w:sum(v[i]*F[i+1][j+1]*w[j] for i in range(3) for j in range(3))
 return F[0][0],2*sum(F[0][i+1]*r[i] for i in range(3)),dot(r,r),2*sum(F[0][i+1]*o[i] for i in range(3)),2*dot(r,o),dot(o,o)+2
def norm(c,u,t):
 a,b,d,e,f,g=c
 return a*u*u+b*u*t+d*t*t+e*u+f*t+g
def alternate(c,p,m):
 for t in range(m):
  for u in range(m):
   if norm(c,u,t)%m:continue
   for j in range(p):
    for i in range(p):
     U=u+i*m;T=t+j*m
     if norm(c,U,T)%(p*m)==0:return [U,T],[u,t]
 raise AssertionError('no liftable class')
aa={x['index']:x for x in A['families']};bb={x['index']:x for x in B['family_results']}
prev='0'*64;out=[];repaired={2:0,7:0}
for ref in L['records']:
 e=rd(D/ref['path']);canon=dict(e);canon.pop('sha256')
 h=hashlib.sha256(json.dumps(canon,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 assert e['sha256']==ref['sha256']==h and e['previous_hash']==prev
 prev=h;idx=e['family_index'];c=coeff(e)
 x=aa[idx];y=bb[idx];u0,t0=int(x['u_mod_M']),int(x['t_mod_M'])
 assert norm(c,u0,t0)%M==0
 locals={z['modulus']:z['example'] for z in e['direct_norm_modular_pairs']}
 selected={}
 for p,m in ((2,256),(7,49)):
  old=[u0%m,t0%m];ext=None
  for j in range(p):
   for i in range(p):
    z=[old[0]+i*m,old[1]+j*m]
    if norm(c,*z)%(p*m)==0:ext=z;break
   if ext is not None:break
  failed=not bool(ext)
  assert failed==(y['one_step_local_lifts'][str(p)]['count']==0)
  if failed:
   ext,base=alternate(c,p,m)
   assert base!=old
   repaired[p]+=1
  selected[p]=[ext,failed]
 uu=[selected[2][0][0],locals[81][0],locals[125][0],selected[7][0][0]]
 tt=[selected[2][0][1],locals[81][1],locals[125][1],selected[7][0][1]]
 for m in mm[4:]:uu.append(locals[m][0]);tt.append(locals[m][1])
 u,t=crt(uu),crt(tt)
 assert all(u%m==z%m and t%m==w%m for z,w,m in zip(uu,tt,mm))
 assert norm(c,u,t)%N==0
 out.append({'index':idx,'source_hash':h,'old_failed_p2':selected[2][1],'old_failed_p7':selected[7][1],
             'u_mod_14M':str(u),'t_mod_14M':str(t),'selected_2adic':selected[2][0],
             'selected_7adic':selected[7][0]})
assert prev==L['ledger_tip_sha256'] and len(out)==53 and repaired=={2:26,7:2}
O.write_text(json.dumps({'rqt':607,'M_prime':str(N),'repaired':repaired,'families':out,
'excluded_selected':82,'unresolved_selected':53,'original_22D_wall':'NOT REPLAYED','root19':'OPEN'},indent=2)+'\n')
print('PASS RQT-607: 53/53 combined solutions modulo',N,'repaired 26 p2 and 2 p7 classes')
