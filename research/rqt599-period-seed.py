#!/usr/bin/env python3
"""RQT-599 exact sqrt(d) period and bounded generalized Pell seed test.
Usage: python rqt599.py RQT-597-results.json RQT-595-results.json [out.json]
"""
import json,hashlib,math,sys
from pathlib import Path
p597,p595=map(Path,sys.argv[1:3]);r=json.loads(p597.read_text());s=json.loads(p595.read_text())
d=int(r['squarefree_D']);A=int(s['A']);B=int(s['B']);C=int(s['C']);N=int(s['N']);K=int(s['D'])
assert d==3580734425344222227352852171253793 and N==100*d==4*A and B*B-4*A*C==K
a0=math.isqrt(d);m=0;q=1;a=a0;checkpoints={}
for n in range(1,2000001):
    m=q*a-m
    num=d-m*m
    assert num>0 and num%q==0
    q=num//q
    a=(a0+m)//q
    assert q>0 and a>=1 and a!=2*a0,'Period closed: revise bound'
    if n in (10000,100000,1000000,2000000):
        checkpoints[str(n)]={'m':str(m),'q':str(q),'a':str(a)}
T=50000;hits=[]
for t in range(-T,T+1):
    delta=A*t*t+B*t+C
    if delta>=0:
        y=math.isqrt(delta)
        if y*y==delta:
            X=2*A*t+B;Z=10*y
            assert X*X-d*Z*Z==K and X%(2*A)==B%(2*A) and Z%10==0
            hits.append({'t':t,'X':str(X),'Y':str(y)})
assert hits==[]
result={'rqt':599,'family_index':28,'squarefree_d':str(d),'steps':2000000,'period_closed':False,'checkpoints':checkpoints,'finite_t_range':[-T,T],'finite_square_hits':hits,'rqt597_sha256':hashlib.sha256(p597.read_bytes()).hexdigest(),'rqt595_sha256':hashlib.sha256(p595.read_bytes()).hexdigest(),'excluded_selected':82,'unresolved_selected':53,'root19':'OPEN','original_22d_wall':'NOT REPLAYED'}
Path(sys.argv[3] if len(sys.argv)>3 else 'RQT-599-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS RQT-599: period >2,000,000; zero finite seeds; root19 OPEN')
