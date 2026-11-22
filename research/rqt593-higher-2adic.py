#!/usr/bin/env python3
"""RQT-593: 2-adic coordinate-lift certification; selected ray-offset families.
python rqt593.py GRAM RQT583 RQT584 RQT586 [OUT]
"""
import json,hashlib,sys,math
from pathlib import Path
p=list(map(Path,sys.argv[1:5]));F,E,A,B=[json.loads(x.read_text()) for x in p]
assert hashlib.sha256(p[0].read_bytes()).hexdigest()=="f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228"
assert hashlib.sha256(p[1].read_bytes()).hexdigest()=="5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92"
excluded={int(c['family_index']) for d in (A,B) for c in d['certificates']}|{13}
assert len(excluded)==27 and len(E['equations'])==80
todo=[e for e in E['equations'] if int(e['index']) not in excluded]
assert len(todo)==53
def coefficients(e):
 r=e['ray'];o=e['offset']
 dot=lambda v,w:sum(v[i]*F[i+1][j+1]*w[j] for i in range(3) for j in range(3))
 br=sum(F[0][i+1]*r[i] for i in range(3))
 bo=sum(F[0][i+1]*o[i] for i in range(3))
 return (F[0][0],2*br,dot(r,r),2*bo,2*dot(r,o),dot(o,o)+2)
def q(c,u,t):
 a,b,d,e,f,g=c
 return a*u*u+b*u*t+d*t*t+e*u+f*t+g
records=[]
for e in todo:
 c=coefficients(e)
 for t in (-5,-1,0,1,13):
  v=[e['ray'][j]*t+e['offset'][j] for j in range(3)]
  b=sum(F[0][j+1]*v[j] for j in range(3))
  d=sum(F[j+1][k+1]*v[j]*v[k] for j in range(3) for k in range(3))
  assert b*b-F[0][0]*(d+2)==int(e['A'])*t*t+int(e['B'])*t+int(e['C'])
 residues={(0,0)}; m=1; counts=[]
 for exp in range(1,14):
  newm=2*m
  residues={(u+i*m,t+j*m) for u,t in residues for i in (0,1) for j in (0,1) if q(c,u+i*m,t+j*m)%newm==0}
  counts.append(len(residues))
  m=newm
  if not residues: break
 records.append({'family_index':e['index'],'counts_by_power_of_2':counts})
assert all(len(x['counts_by_power_of_2'])==13 and x['counts_by_power_of_2'][-1]>0 for x in records)
T=12000; squares=[]
for e in todo:
 aa,bb,cc=[int(e[k]) for k in 'ABC']
 for t in range(-T,T+1):
  d=aa*t*t+bb*t+cc
  if d>=0 and math.isqrt(d)**2==d:squares.append([e['index'],t])
assert not squares
result={'rqt':593,'source_gram_sha256':hashlib.sha256(p[0].read_bytes()).hexdigest(),'source_pell_sha256':hashlib.sha256(p[1].read_bytes()).hexdigest(),'tested_families':53,'largest_modulus':8192,'records':records,'finite_t_range':[-T,T],'finite_combinations':53*(2*T+1),'square_candidates':squares,'new_exclusions':0,'total_excluded':82,'unresolved':53,'root19':'OPEN','original_22d_wall':'NOT REPLAYED'}
Path(sys.argv[5] if len(sys.argv)>5 else 'RQT-593-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: 53 survivors through 8192, no new exclusions; 1,272,053 bounded tests, zero square hits; Root19 OPEN')
