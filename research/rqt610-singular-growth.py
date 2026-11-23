#!/usr/bin/env python3
"""RQT-610: exact singular 7-adic growth, families 2 and 24.
Usage: python rqt610.py RQT-583-results.json RQT-591-results.json RQT-609-results.json [out.json]
"""
import json,sys,hashlib
from pathlib import Path
P=list(map(Path,sys.argv[1:4]))
E,F,S=[json.loads(p.read_text()) for p in P]
assert E['rqt']==583 and S['rqt']==609
equations={int(e['index']):e for e in E['equations']}
G=[[int(v) for v in row] for row in F['reduced_gram']]
records={int(e['index']):e for e in S['families']}
def coefficients(e):
 r,o=e['ray'],e['offset']
 dot=lambda x,y:sum(x[i]*G[i+1][j+1]*y[j] for i in range(3) for j in range(3))
 return (G[0][0],2*sum(G[0][i+1]*r[i] for i in range(3)),dot(r,r),
 2*sum(G[0][i+1]*o[i] for i in range(3)),2*dot(r,o),dot(o,o)+2)
def Q(c,u,t):
 a,b,d,e,f,g=c
 return a*u*u+b*u*t+d*t*t+e*u+f*t+g
results=[]
for idx in (2,24):
 c=coefficients(equations[idx]);a,b,d,e,f,g=c
 roots=[(u,t) for u in range(7) for t in range(7) if Q(c,u,t)%7==0]
 assert len(roots)==1
 u0,t0=roots[0];gu=2*a*u0+b*t0+e;gt=b*u0+2*d*t0+f
 assert Q(c,u0,t0)%49==gu%7==gt%7==0
 # Q(u0+7x,t0+7y)=49 P(x,y) with P integer.
 red=(a,b,d,gu//7,gt//7,Q(c,u0,t0)//49)
 A,B,C,D,E0,F0=red
 def p(x,y):return A*x*x+B*x*y+C*y*y+D*x+E0*y+F0
 reduced=[(x,y) for x in range(7) for y in range(7) if p(x,y)%7==0]
 assert len(reduced)==8
 assert all((2*A*x+B*y+D)%7 or (B*x+2*C*y+E0)%7 for x,y in reduced)
 for x,y in [(0,0),(1,1),(7,-3),(-11,16)]:
  assert Q(c,u0+7*x,t0+7*y)==49*p(x,y)
 counts=records[idx]['seven_singular_counts']
 assert counts==[1,49,392,2744,19208,134456]
 assert all(v==(1 if k==1 else 49 if k==2 else 8*7**(k-1)) for k,v in enumerate(counts,1))
 results.append({'index':idx,'singular_mod7_root':[u0,t0],
 'reduced_coefficients_mod7':[v%7 for v in red],
 'eight_regular_roots':reduced,'counts_k1_k6':counts})
out={'rqt':610,'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P},
'families':results,'all_k_law':'1 if k=1, 49 if k=2, 8*7^(k-1) if k>=3',
'all_scale_excluded':82,'unresolved':53,'new_exclusions':0,'wall22d':'NOT REPLAYED','root19':'OPEN'}
Path(sys.argv[4] if len(sys.argv)>4 else 'RQT-610-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS RQT-610: exact all-exponent law for both families, Root19 OPEN')
