#!/usr/bin/env python3
"""RQT-592 exact integer-coordinate modulo-four obstruction verifier.
Usage: python rqt592.py reduced_gram.json rqt583-results.json rqt584-results.json rqt586-results.json
"""
import json,sys,hashlib,math
from pathlib import Path
paths=list(map(Path,sys.argv[1:5]))
F,E,A,B=[json.loads(p.read_text()) for p in paths]
assert len(F)==4 and len(E['equations'])==80
assert hashlib.sha256(paths[1].read_bytes()).hexdigest()=='5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92'
excluded={x['family_index'] for x in A['certificates']} | {x['family_index'] for x in B['certificates']}
assert len(excluded)==26
outstanding=[e for e in E['equations'] if e['index'] not in excluded]
assert len(outstanding)==54
a=F[0][0]
def delta(e,t):
    v=[e['ray'][j]*t+e['offset'][j] for j in range(3)]
    b=sum(F[0][j+1]*v[j] for j in range(3))
    c=sum(F[j+1][k+1]*v[j]*v[k] for j in range(3) for k in range(3))
    return b*b-a*(c+2)
def qplus2(e,u,t):
    v=[u]+[e['ray'][j]*t+e['offset'][j] for j in range(3)]
    return sum(v[i]*F[i][j]*v[j] for i in range(4) for j in range(4))+2
for e in E['equations']:
    A0,B0,C0=[int(e[k]) for k in 'ABC']
    for t in (-31,-2,0,1,23):
        assert delta(e,t)==A0*t*t+B0*t+C0
    assert B0*B0-4*A0*C0==int(e['D'])
moduli=[2,4,8,16,32,64,128,256,3,9,27,81,243,5,25,125,7,49,11,121,13,169,17,19,23,29,31,37,41,43,47,53]
new=[]
for e in outstanding:
    for m in moduli:
        if not any(qplus2(e,u,t)%m==0 for t in range(m) for u in range(m)):
            new.append((e['index'],m))
            break
assert new==[(13,4)]
target=next(e for e in outstanding if e['index']==13)
assert all(qplus2(target,u,t)%4==2 for t in range(4) for u in range(4))
assert not [(e['index'],t) for e in outstanding for t in range(-2000,2001)
            if (z:=delta(e,t))>=0 and math.isqrt(z)**2==z]
print('PASS RQT-592: 80 exact identities; family 13 universally excluded modulo 4; 82/135 excluded; 53 unresolved; Root19 OPEN')
