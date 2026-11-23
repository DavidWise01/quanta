#!/usr/bin/env python3
"""RQT-604 exact replay and hash-chain certificate writer.
Usage: python research/rqt604-append-only.py RQT-603-results.json RQT-591-reduced_gram.json OUTDIR
"""
import json,hashlib,sys
from pathlib import Path
R,G,O=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]);O.mkdir(parents=True,exist_ok=True)
x=json.loads(R.read_text());F=json.loads(G.read_text()); assert x['rqt']==603 and len(x['family_results'])==53
assert hashlib.sha256(G.read_bytes()).hexdigest()=='f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228'
lo,hi=x['tested_t_range'];assert [lo,hi]==[-100000,100000]
mods=[2,4,8,16,32,64,128,256,3,9,27,81,5,25,125,7,49,11,13,17,19,23,29,31]
prev='0'*64;count=0;records=[]
for e in sorted(x['family_results'],key=lambda v:v['index']):
 r,o=e['ray'],e['offset'];idx=e['index']
 dot=lambda v,w:sum(v[i]*F[i+1][j+1]*w[j] for i in range(3) for j in range(3))
 a=F[0][0];br=sum(F[0][i+1]*r[i] for i in range(3));bo=sum(F[0][i+1]*o[i] for i in range(3))
 c=(a,2*br,dot(r,r),2*bo,2*dot(r,o),dot(o,o)+2)
 def norm(u,t,m):
  a,b,d,e,f,g=c
  return (a*u*u+b*u*t+d*t*t+e*u+f*t+g)%m
 def delta(t):
  v=[r[i]*t+o[i] for i in range(3)];b=sum(F[0][i+1]*v[i] for i in range(3))
  return b*b-a*(dot(v,v)+2)
 C=delta(0);A=(delta(1)+delta(-1)-2*C)//2;B=delta(1)-A-C
 assert all(delta(t)==A*t*t+B*t+C for t in (-23,-1,0,1,29))
 bits=bytearray(b'\x01')*(hi-lo+1);gates=[]
 for z in e['prime_gates']:
  p=z['prime'];squares={n*n%p for n in range(p)}
  good={t for t in range(p) if (A*t*t+B*t+C)%p in squares}
  assert len(good)==z['admissible_residues']
  for bad in range(p):
   if bad in good:continue
   i=(bad-lo)%p
   if i<len(bits):bits[i::p]=b'\x00'*((len(bits)-1-i)//p+1)
  left=bits.count(1)
  assert left==z['survivors']
  gates.append({'p':p,'allowed':len(good),'survived':left});count+=1
 assert bits.count(1)==0
 direct=[]
 for m in mods:
  n=0;first=None
  for t in range(m):
   for u in range(m):
    if norm(u,t,m)==0:
     n+=1
     if first is None:first=[u,t]
  assert n>0
  direct.append({'modulus':m,'number_of_pairs':n,'example':first})
 record={'rqt':604,'family_index':idx,'ray':r,'offset':o,'gram_discriminant_coefficients':[str(A),str(B),str(C)],'interval':[lo,hi],'source_gate_replay':gates,'direct_norm_modular_pairs':direct,'finite_survivors':0,'new_all_scale_exclusion':False,'previous_hash':prev}
 h=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 record['sha256']=h;name=f'family-{idx:03d}.json'
 (O/name).write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
 records.append({'index':idx,'sha256':h,'path':name});prev=h
assert count==989 and prev=='e2bd1c5818a294ecd578af40791c81b3b96c432ee9276f0f404b7e4b054994a2'
(O/'manifest.json').write_text(json.dumps({'rqt':604,'genesis':'0'*64,'tip':prev,'records':records,'all_scale_excluded':82,'unresolved':53,'root19':'OPEN'},indent=2)+'\n')
print('PASS RQT-604: 53 family certificates; 989 prime gates; tip',prev)
